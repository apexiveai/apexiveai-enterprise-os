# ApexiveAI Enterprise Platform
စစ်ကြည့်ပြီးပါပြီ—လက်ရှိအခြေအနေက **အသုံးပြုလို့ရတဲ့ prototype/MVP အဆင့်** ဖြစ်ပြီး production အပြည့်အစုံတော့ မဟုတ်သေးပါ။

- Desktop launcher နဲ့ Windows/macOS/Linux installer တည်ဆောက်ဖို့ script တွေ ရှိပါတယ်။ Industrial/Robotics အပိုင်းက local simulation ဖြစ်ပြီး hardware နဲ့ မချိတ်ဆက်ထားပါ။
- Workflow API နဲ့ persistence အလုပ်လုပ်နေပြီး backend test **၇ ခုလုံး pass** ပါတယ်။ Frontend build နဲ့ lint လည်း **pass** ဖြစ်ပါတယ်။
- README အရ enterprise suite-ийн бусад screen အများစုက interactive prototype ဖြစ်ပြီး live company systems နဲ့ မချိတ်ဆက်သေးပါ။ အသေးစိတ်ကို `README.md` မှာ ကြည့်နိုင်ပါတယ်။
- အပြောင်းအလဲတွေက Git မှာ **commit မလုပ်ရသေး** ပါ။ `.env` လည်း ပြောင်းထားတာတွေ့ရလို့ commit မလုပ်ခင် အဲဒီဖိုင်ထဲမှာ secret ပါ/မပါ စစ်ပြီး မလိုအပ်ရင် commit ထဲ မထည့်ပါနဲ့။

အကျဉ်းချုပ်—စမ်းသပ်နိုင်တဲ့ core workflow နဲ့ UI/desktop packaging အခြေခံတွေ ရှိနေပြီ။ Live data integration, real hardware integration နဲ့ production deployment validation တွေက မပြီးသေးပါ။



မြန်မြန်ဆန်ဆန်နဲ့ ဆက်လုပ်ရမယ့် အဆင့်စမယ် ..... ပြီးရင် လက်စသတ်ပြီး ထုတ်တော့မယ် ဖြန့်ဝေတော့မယ် အသုံးပြုသူတွေဆီ
## Run on Windows

Build the single-file desktop launcher from the repository root:

```text
build_enterprise_platform.cmd
```

The executable is created at `dist\EnterprisePlatform.exe`. Launch it to start
the local application server and open the platform in your default browser.
Application data is stored under `%LOCALAPPDATA%\ApexiveAI\EnterprisePlatform`.
The desktop build does not require Docker, PostgreSQL, or Redis.

The build requires Python 3.12+ and Node.js/npm. The script installs the Python
build requirements and uses the existing frontend npm dependencies.

## Install on Windows, macOS, and Linux

Native installers are built on their target operating system because PyInstaller
does not cross-compile desktop applications.

- **Windows:** Install Inno Setup 6, then run `build_windows_installer.cmd`.
  The installer is written to `dist\EnterprisePlatform-Setup.exe`.
- **macOS:** Run `bash packaging/macos/build_installer.sh` on a Mac. It creates
  `dist/EnterprisePlatform-macos.dmg`. The app is unsigned; public distribution
  requires Apple Developer signing and notarization.
- **Linux:** Run `bash packaging/linux/build_installer.sh` on Debian or Ubuntu.
  It creates a `.deb` installer and a portable `.tar.gz` in `dist/`. Install the
  `.deb` with `sudo apt install ./dist/apexiveai-enterprise-platform_*.deb`.

The macOS and Linux scripts require Python 3.12+, Node.js/npm, and their native
platform packaging tools. They create a local `.venv-desktop` for Python build
dependencies.

## Run in development

In one PowerShell window, start the API from the repository root:

```powershell
$env:DATABASE_URL = "sqlite:///./enterprise.db"
$env:REDIS_URL = "redis://127.0.0.1:6379/0"
$env:APEXIVE_DATA_DIR = "$PWD\data"
python -m uvicorn app.main:app --app-dir backend --reload
```

In a second window, start the frontend:

```powershell
Push-Location frontend
npm.cmd install
npm.cmd run dev
Pop-Location
```

The API documentation is available at `http://127.0.0.1:8000/docs`. Workflow
definitions, runs, and human tasks use the API and are persisted in the
configured data directory. The other enterprise-suite screens are currently
interactive prototypes; their sample figures and simulated actions are not
connected to live company systems.

## Industrial & Robotics Operations

The Industrial Operations section includes robotics fleet management, OT
connector profiles (OPC UA, Modbus and MQTT), sample IoT telemetry, safety-gated
robot-cell simulations, drone inspection planning, logistics dispatch, asset
maintenance and an operations command center. Its architecture view shows
the flow from AI agents through workflow/policy and edge integration to
physical equipment.

These features are local simulations. They do not connect to or send commands
to PLC/SCADA systems, drones, AMR/AGV fleets or robot arms. Real deployments
require approved vendor integrations, OT network controls, credentials,
hardware-specific safety systems and commissioning.