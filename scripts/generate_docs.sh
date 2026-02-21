#!/bin/bash
# Generate API documentation locally

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_ROOT"

echo "Installing documentation dependencies..."
pip install -e ".[docs]" --quiet

echo "Generating API reference with pdoc..."
pdoc --html --output-dir docs/api src/drone_reel --force

# Flatten directory structure
if [ -d "docs/api/drone_reel" ]; then
    mv docs/api/drone_reel/* docs/api/
    rmdir docs/api/drone_reel
fi

echo "Building documentation with MkDocs..."
mkdocs build

echo ""
echo "Documentation generated in site/"
echo "To serve locally: mkdocs serve"
echo "Then open: http://localhost:8000"
