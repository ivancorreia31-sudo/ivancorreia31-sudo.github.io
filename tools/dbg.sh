#!/bin/bash
# debug copy of out/bonnet-up.html with patches/debug/*.py on top → e2e/gl3d_dbg.html (never published)
set -e
cd "$(dirname "$0")/.."
mkdir -p dbg && cp out/bonnet-up.html dbg/bonnet-up.html
cd dbg && ln -sfn ../tools b24 && python3 ../patches/debug/dbg_pick.py && cd ..
python3 tools/mk_pages.py dbg/bonnet-up.html _dbg && rm -f e2e/flat_dbg.html && echo "dbg page ok"
