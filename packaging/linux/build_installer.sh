#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv-desktop"
PYTHON="$VENV_DIR/bin/python"
VERSION="${APP_VERSION:-1.0.0}"

python3 -m venv "$VENV_DIR"
"$PYTHON" -m pip install -r "$ROOT_DIR/backend/requirements-desktop.txt"
npm --prefix "$ROOT_DIR/frontend" ci
npm --prefix "$ROOT_DIR/frontend" run build

"$PYTHON" -m PyInstaller --clean --noconfirm --onefile \
  --name EnterprisePlatform \
  --paths "$ROOT_DIR/backend" \
  --add-data "$ROOT_DIR/frontend/dist:frontend/dist" \
  --distpath "$ROOT_DIR/dist" \
  --workpath "$ROOT_DIR/build/pyinstaller-linux" \
  --specpath "$ROOT_DIR/build/spec-linux" \
  "$ROOT_DIR/desktop_launcher.py"

ARCH="$(dpkg --print-architecture)"
STAGE_DIR="$(mktemp -d)"
trap 'rm -rf "$STAGE_DIR"' EXIT

mkdir -p "$STAGE_DIR/DEBIAN" "$STAGE_DIR/usr/bin" "$STAGE_DIR/usr/share/applications"
install -m 0755 "$ROOT_DIR/dist/EnterprisePlatform" "$STAGE_DIR/usr/bin/enterprise-platform"
cat > "$STAGE_DIR/DEBIAN/control" <<EOF
Package: apexiveai-enterprise-platform
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: ApexiveAI Enterprise Team
Description: ApexiveAI Enterprise Platform desktop launcher
 Local enterprise operations platform with a bundled local application server.
EOF
cat > "$STAGE_DIR/usr/share/applications/apexiveai-enterprise-platform.desktop" <<'EOF'
[Desktop Entry]
Type=Application
Name=ApexiveAI Enterprise Platform
Comment=Open the local enterprise operations platform
Exec=/usr/bin/enterprise-platform
Icon=applications-office
Terminal=false
Categories=Office;Utility;
EOF

dpkg-deb --build --root-owner-group "$STAGE_DIR" \
  "$ROOT_DIR/dist/apexiveai-enterprise-platform_${VERSION}_${ARCH}.deb"
tar -C "$ROOT_DIR/dist" -czf "$ROOT_DIR/dist/EnterprisePlatform-linux-${ARCH}.tar.gz" EnterprisePlatform

echo "Built: $ROOT_DIR/dist/apexiveai-enterprise-platform_${VERSION}_${ARCH}.deb"
echo "Built: $ROOT_DIR/dist/EnterprisePlatform-linux-${ARCH}.tar.gz"
