"""Rate limiting for respectful scraping."""

import asyncio
import time
from typing import Optional


class RateLimiter:
    """Async rate limiter for controlling request frequency."""

    def __init__(self, requests_per_second: float = 0.4, min_delay: float = 2.0):
        """
        Initialize rate limiter.

        Args:
            requests_per_second: Maximum requests per second
            min_delay: Minimum delay between requests in seconds
        """
        self.min_interval = max(1.0 / requests_per_second, min_delay)
        self.last_request_time: Optional[float] = None
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """Wait until we can make the next request."""
        async with self._lock:
            if self.last_request_time is not None:
                elapsed = time.monotonic() - self.last_request_time
                if elapsed < self.min_interval:
                    wait_time = self.min_interval - elapsed
                    await asyncio.sleep(wait_time)

            self.last_request_time = time.monotonic()

    async def __aenter__(self):
        """Context manager entry."""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass


class AdaptiveRateLimiter(RateLimiter):
    """Rate limiter that adapts based on server responses."""

    def __init__(
        self,
        initial_delay: float = 2.5,
        min_delay: float = 1.0,
        max_delay: float = 10.0,
        backoff_factor: float = 1.5,
    ):
        super().__init__(min_delay=initial_delay)
        self.current_delay = initial_delay
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.consecutive_successes = 0
        self.consecutive_failures = 0

    def record_success(self) -> None:
        """Record a successful request."""
        self.consecutive_successes += 1
        self.consecutive_failures = 0

        # Gradually decrease delay after multiple successes
        if self.consecutive_successes >= 5:
            self.current_delay = max(
                self.min_delay, self.current_delay / self.backoff_factor
            )
            self.min_interval = self.current_delay
            self.consecutive_successes = 0

    def record_failure(self, is_rate_limit: bool = False) -> None:
        """Record a failed request."""
        self.consecutive_failures += 1
        self.consecutive_successes = 0

        # Increase delay on failures
        if is_rate_limit:
            self.current_delay = min(
                self.max_delay, self.current_delay * self.backoff_factor * 2
            )
        else:
            self.current_delay = min(
                self.max_delay, self.current_delay * self.backoff_factor
            )

        self.min_interval = self.current_delay
