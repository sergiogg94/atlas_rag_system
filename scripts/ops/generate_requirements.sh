#!/bin/bash

set -e

echo "Generating per-service requirements files from pyproject.toml..."

uv pip compile pyproject.toml --extra backend -o requirements-backend.txt
uv pip compile pyproject.toml --extra frontend -o requirements-frontend.txt
uv pip compile pyproject.toml --extra dashboard -o requirements-dashboard.txt

echo "Done."
