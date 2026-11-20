#!/bin/bash
# build: start from the last published build (src/base.html) and apply the given patches in order, then syntax-check and
# make the test pages. usage: tools/build.sh p48a_world p48b_catalogue ...
set -e
cd "$(dirname "$0")/.."
cp src/base.html out/bonnet-up.html
cd out && ln -sfn ../tools b24
for p in "$@"; do echo "== $p"; python3 ../patches/$p.py; done
cd .. && python3 tools/check.py out/bonnet-up.html
python3 tools/mk_pages.py out/bonnet-up.html && echo "pages ok"
