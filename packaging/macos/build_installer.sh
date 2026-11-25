#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv-desktop"
PYTHON="$VENV_DIR/bin/python"

python3 -m venv "$VENV_DIR"
"$PYTHON" -m pip install -r "$ROOT_DIR/backend/requirements-desktop.txt"
npm --prefix "$ROOT_DIR/frontend" ci
npm --prefix "$ROOT_DIR/frontend" run build

"$PYTHON" -m PyInstaller --clean --noconfirm --windowed \
  --name EnterprisePlatform \
  --paths "$ROOT_DIR/backend" \
  --add-data "$ROOT_DIR/frontend/dist:frontend/dist" \
  --distpath "$ROOT_DIR/dist" \
  --workpath "$ROOT_DIR/build/pyinstaller-macos" \
  --specpath "$ROOT_DIR/build/spec-macos" \
  "$ROOT_DIR/desktop_launcher.py"

DMG_STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "$DMG_STAGE_DIR"' EXIT
cp -R "$ROOT_DIR/dist/EnterprisePlatform.app" "$DMG_STAGE_DIR/"
ln -s /Applications "$DMG_STAGE_DIR/Applications"

hdiutil create \
  -volname "ApexiveAI Enterprise Platform" \
  -srcfolder "$DMG_STAGE_DIR" \
  -ov -format UDZO \
  "$ROOT_DIR/dist/EnterprisePlatform-macos.dmg"

echo "Built: $ROOT_DIR/dist/EnterprisePlatform-macos.dmg"
