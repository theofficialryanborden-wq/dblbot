## Cursor Cloud specific instructions

- This repo is a Python/OpenCV automation bot for Dragon Ball Legends. The only product service is the bot in `DBL_Bot/`; there is no build system, package manifest, or formal test runner.
- Live end-to-end runs require an ADB-visible Android device or emulator with Dragon Ball Legends installed and logged in. Without a connected device, `python3 bot.py` starts and reaches ADB, then reports `no devices/emulators found`.
- The scripts hardcode Windows `adb.exe` paths. The Cloud VM setup provides PATH shims for those names that forward to Linux `adb`; if a fresh environment lacks those shims, live-device runs will fail before reaching ADB.
- For non-device validation, use the checked-in `DBL_Bot/test_screen.png` with `DBL_Bot/templates/*.png` to exercise OpenCV template matching and tap-coordinate generation.
