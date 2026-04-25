# Drone-Reel Test Suite

Comprehensive test coverage for the drone-reel automated video stitching project.

## Quick Start

```bash
# Run all tests
pytest tests/

# Run with coverage report
pytest tests/ --cov=src/drone_reel --cov-report=html

# Run specific test file
pytest tests/test_video_processor.py -v

# Run with parallel execution (faster)
pytest tests/ -n auto
```

## Test Structure

### Test Files

| File | Tests | Coverage | Description |
|------|-------|----------|-------------|
| `test_video_processor.py` | 66 | 78% | Video processing, transitions, stitching |
| `test_beat_sync.py` | 32 | 85% | Audio analysis, beat detection, cut points |
| `test_scene_detector.py` | 35+ | 53% | Scene detection, quality scoring |
| `test_reframer.py` | 41 | 81% | Video reframing, aspect ratio conversion |
| `test_color_grader.py` | 58 | 82% | Color grading, presets, adjustments |
| `test_utils.py` | 26 | 75-81% | Utility functions |

**Total: 264 tests, 69% overall coverage**

## Test Categories

### Unit Tests
Test individual functions and methods in isolation using mocks:
- Initialization and configuration
- Data structure properties
- Calculation methods
- Edge case handling

### Integration Tests
Test interactions between components (mostly skipped, require media files):
- Scene detection on real videos
- Audio analysis on real audio files
- End-to-end video processing

### Edge Case Tests
Test boundary conditions and error scenarios:
- Empty inputs
- Extreme parameter values
- All-black/all-white frames
- Very small/large dimensions
- Error conditions

## Test Data

All tests use **synthetic test data** - no real media files required:

### Video Frames
```python
# Simple test frame
frame = np.ones((1080, 1920, 3), dtype=np.uint8) * 128

# Colorful test frame
frame = np.zeros((100, 100, 3), dtype=np.uint8)
frame[:50, :50] = [255, 0, 0]  # Blue quadrant
frame[:50, 50:] = [0, 255, 0]  # Green quadrant
```

### Audio Signals
```python
# Synthetic audio with beats at 120 BPM
t = np.linspace(0, duration, int(sr * duration))
audio = np.sin(2 * np.pi * 440 * t)  # 440Hz tone
# Add beat clicks at tempo intervals
```

### Mock Objects
Extensive use of `unittest.mock` for external dependencies:
- MoviePy VideoFileClip and AudioFileClip
- librosa audio analysis functions
- OpenCV video capture and processing
- File system operations

## Running Specific Tests

### By Module
```bash
# Video processor tests
pytest tests/test_video_processor.py

# Beat sync tests
pytest tests/test_beat_sync.py

# Scene detector tests
pytest tests/test_scene_detector.py

# Reframer tests
pytest tests/test_reframer.py

# Color grader tests
pytest tests/test_color_grader.py
```

### By Test Class
```bash
# Test specific class
pytest tests/test_beat_sync.py::TestBeatInfo

# Test specific method
pytest tests/test_beat_sync.py::TestBeatInfo::test_beat_interval_calculation
```

### By Marker
```bash
# Skip integration tests
pytest tests/ -m "not integration"

# Only run fast tests
pytest tests/ -m "not slow"
```

## Coverage Reports

### Terminal Coverage
```bash
pytest tests/ --cov=src/drone_reel --cov-report=term-missing
```

### HTML Coverage Report
```bash
pytest tests/ --cov=src/drone_reel --cov-report=html
open htmlcov/index.html
```

### Coverage by Module
- `beat_sync.py`: 85%
- `color_grader.py`: 82%
- `reframer.py`: 81%
- `utils/file_utils.py`: 81%
- `video_processor.py`: 78%
- `utils/config.py`: 75%
- `scene_detector.py`: 53% (integration tests skipped)

## Test Fixtures

Common fixtures used across test files:

### Video Processor
- `processor`: VideoProcessor instance
- `sample_scene`: SceneInfo with test data
- `sample_segments`: List of ClipSegment objects

### Beat Sync
- `beat_sync`: BeatSync instance
- `sample_beat_info`: BeatInfo with synthetic data

### Reframer
- `vertical_reframer`: Reframer configured for 9:16 output
- `landscape_frame`: 1920x1080 test frame
- `horizon_frame`: Frame with horizontal line

### Color Grader
- `grader`: ColorGrader instance
- `sample_frame`: Generic test frame
- `colorful_frame`: Frame with multiple colors

## Continuous Integration

Tests are designed to run in CI/CD environments:

```yaml
# Example GitHub Actions configuration
- name: Run tests
  run: |
    pip install -e ".[dev]"
    pytest tests/ --cov=src/drone_reel --cov-report=xml

- name: Upload coverage
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage.xml
```

## Writing New Tests

### Test Template
```python
"""Tests for new_module module."""

import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from drone_reel.core.new_module import NewClass


class TestNewClass:
    """Tests for NewClass."""

    @pytest.fixture
    def instance(self):
        """Create a NewClass instance."""
        return NewClass()

    def test_initialization(self, instance):
        """Test default initialization."""
        assert instance.attribute is not None

    def test_method_basic(self, instance):
        """Test basic method functionality."""
        result = instance.method(input_data)
        assert result == expected_output

    def test_method_edge_case(self, instance):
        """Test edge case handling."""
        with pytest.raises(ValueError):
            instance.method(invalid_input)
```

### Best Practices

1. **Use descriptive test names**: `test_method_name_scenario`
2. **One assertion focus per test**: Test one thing at a time
3. **Use fixtures for setup**: Avoid code duplication
4. **Mock external dependencies**: Keep tests fast and isolated
5. **Test edge cases**: Empty inputs, extreme values, errors
6. **Add docstrings**: Explain what each test verifies

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Install package in development mode
pip install -e .
```

**Missing dependencies:**
```bash
# Install dev dependencies
pip install -e ".[dev]"
```

**Slow tests:**
```bash
# Run in parallel
pip install pytest-xdist
pytest tests/ -n auto
```

**Coverage not collected:**
```bash
# Ensure pytest-cov is installed
pip install pytest-cov
```

## Performance

- **Average test duration**: 8-10 seconds for full suite
- **Parallel execution**: Can reduce to 3-5 seconds with `-n auto`
- **Memory usage**: ~200MB peak
- **No external dependencies**: All tests use synthetic data

## Maintenance

### Updating Tests

When adding new features:
1. Add unit tests for new functions/methods
2. Add integration tests (can be skipped initially)
3. Add edge case tests
4. Update this README with new test information
5. Ensure coverage stays above 65%

### Test Coverage Goals

- **Critical modules** (video_processor, beat_sync, reframer, color_grader): 80%+
- **Utility modules**: 75%+
- **Overall project**: 65%+
- **Integration tests**: Can be skipped in CI (require media files)

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [numpy Testing Best Practices](https://numpy.org/doc/stable/reference/testing.html)
