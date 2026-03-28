#!/usr/bin/env bash
# Build the honeybee-ph API documentation.
# Run from the repository root: ./docs/build_docs.sh

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS_DIR="$REPO_ROOT/docs/api_docs"
BUILD_DIR="$DOCS_DIR/_build/docs"

echo "==> Generating .rst files from source packages..."
sphinx-apidoc -f -e -d 4 -o "$DOCS_DIR" "$REPO_ROOT/honeybee_ph"
sphinx-apidoc -f -e -d 4 -o "$DOCS_DIR" "$REPO_ROOT/honeybee_energy_ph"
sphinx-apidoc -f -e -d 4 -o "$DOCS_DIR" "$REPO_ROOT/honeybee_phhvac"
sphinx-apidoc -f -e -d 4 -o "$DOCS_DIR" "$REPO_ROOT/honeybee_ph_utils"
sphinx-apidoc -f -e -d 4 -o "$DOCS_DIR" "$REPO_ROOT/honeybee_ph_standards"

echo "==> Building HTML documentation..."
sphinx-build -b html "$DOCS_DIR" "$BUILD_DIR"

echo ""
echo "==> Done! Open $BUILD_DIR/index.html to view the docs."
