#!/usr/bin/env bash
set -e
export VERSION=$(poetry run python -c "import chicken_dinner; print(chicken_dinner.__version__)")
poetry build
poetry run twine upload dist/chicken_dinner-${VERSION}*
git tag -a ${VERSION} -m "${VERSION}"
git push --tags