# tic80-stitcher
Script to compile TIC-80 cartridge from multiple files

Currently the cartridge is on binary file. This makes hard to track code changes in source control.
Also there is no easy mechanism how to import binary data into the cartridge.

Usage:
```bash
python3 -m make_cartridge \
  --code=cartridge.lua \
  --map=cartridge.map \
  --sprite=cartridge.spr \
  --background=cartridge.bkg \
  -o cartridge.tic
```
