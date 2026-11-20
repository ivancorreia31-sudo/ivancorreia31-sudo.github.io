# Bonnet Up: build and test tools (dev branch)

The live game is on the `main` branch (GitHub Pages). This branch holds what builds and tests it.

- `src/base.html`: the last published build, as one HTML file (the Claude artifact's source). Each new build starts here.
- `patches/pNN*.py`: the changes for the build in progress, applied in order by `tools/build.sh`; `patches/done/` holds published ones.
- `tools/build.sh p48a ... p48_ui` → `out/bonnet-up.html`, syntax check, and the test pages `e2e/flat.html` (2D) and
  `e2e/gl3d.html` (3D).
- `tools/build_app.py out/bonnet-up.html` → `dist/app/` (the files for `main`) and `dist/bonnet-up-itch.zip`.
- `e2e/`: Playwright tests. `python3 e2e/<test>.py PAGE` from inside `e2e/`.
- `NOTES.md`: what each build changed, and how the game is put together.

After publishing build N: copy `out/bonnet-up.html` to `src/base.html`, move the patches to `patches/done/`, commit.
