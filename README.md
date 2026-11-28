# ApexiveAI Enterprise Platform

## Linked Product

[ApexiveAI-CAD-BIM-Suite](file:///C:/Users/naing/Desktop/Products/ApexiveAI-CAD-BIM-Suite)
စစ်ကြည့်ပြီးပါပြီ—လက်ရှိအခြေအနေက **အသုံးပြုလို့ရတဲ့ prototype/MVP အဆင့်** ဖြစ်ပြီး production အပြည့်အစုံတော့ မဟုတ်သေးပါ။

- Desktop launcher နဲ့ Windows/macOS/Linux installer တည်ဆောက်ဖို့ script တွေ ရှိပါတယ်။ Industrial/Robotics အပိုင်းက local simulation ဖြစ်ပြီး hardware နဲ့ မချိတ်ဆက်ထားပါ။
- Workflow API နဲ့ persistence အလုပ်လုပ်နေပြီး backend tests pass ဖြစ်ပါတယ်။ Frontend build နဲ့ lint လည်း **pass** ဖြစ်ပါတယ်။
- README အရ enterprise suite-ийн бусад screen အများစုက interactive prototype ဖြစ်ပြီး live company systems နဲ့ မချိတ်ဆက်သေးပါ။ အသေးစိတ်ကို `README.md` မှာ ကြည့်နိုင်ပါတယ်။
- အပြောင်းအလဲတွေက Git မှာ **commit မလုပ်ရသေး** ပါ။ `.env` လည်း ပြောင်းထားတာတွေ့ရလို့ commit မလုပ်ခင် အဲဒီဖိုင်ထဲမှာ secret ပါ/မပါ စစ်ပြီး မလိုအပ်ရင် commit ထဲ မထည့်ပါနဲ့။

အကျဉ်းချုပ်—စမ်းသပ်နိုင်တဲ့ core workflow နဲ့ UI/desktop packaging အခြေခံတွေ ရှိနေပြီ။ Live data integration, real hardware integration နဲ့ production deployment validation တွေက မပြီးသေးပါ။

162.35.43.164

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

## Run the full local stack

The root Docker Compose stack serves both the built frontend and API on
`http://127.0.0.1:8765`. Port 8765 was checked as available on the development
laptop. On Windows, run these scripts from PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-local.ps1
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop-local.ps1
```

The first start creates `.env` from `.env.example` if needed and generates a
local PostgreSQL password without displaying it. Existing `.env` values and
database volumes are preserved. The stack starts with no sample business
records; dashboard counts are read from the selected workspace's saved records.
API docs are at `http://127.0.0.1:8765/docs`.
The execution-policy option applies only to the launched PowerShell process and
does not change the machine or user policy.

This is a local development/prototype deployment, not a production security
boundary: authentication and tenant identity enforcement are not implemented.
The host ports bind to loopback only; do not expose the services publicly.
An AI provider remains unavailable until a valid provider URL and key are
configured in the ignored local `.env`.

The API image runs as a non-root user and checks `/health/ready`. Compose runs
Alembic once in the `migrate` service and starts the API only after migrations
succeed; the API container itself does not mutate the database schema at
startup. Set `APP_ENV=production` to disable the interactive API docs and
OpenAPI schema. This does **not** make the application safe for public access:
authentication, authorization, and trusted tenant identity are still missing.
Before distributing to real users, deploy behind HTTPS and an authenticated
identity-aware gateway, use managed/secured data services and backups, and
complete security and load testing. The included Compose file is for a
loopback-only local stack, not a complete internet-facing production topology.

## Industry Solutions

The sidebar groups these eight products under **Industry Solutions**:
Construction AI Project Management Agent, Manufacturing Factory Automation RPA,
Energy AI Operations & Reporting, Trading AI Sales Agent, Hotels AI Reservation
Chatbot, Agro AI Agriculture Operations, Highway Toll Collection Automation,
and Logistics AI Logistics Agent.

Each workspace supports manual work-item entry, status tracking, tenant-scoped
database persistence, and audit events. New installations start with empty
queues. The API is available under `/api/v1/industry-solutions/{solution}/records`
for `GET`, `POST`, and status `PATCH` operations. These are standalone
operational work queues—not live ERP/PMS/POS/PLC/toll integrations or autonomous
AI agents. AI actions and live integrations are disabled. Configure and validate
vendor systems, credentials, model access, permissions, and approval rules
before enabling those integrations or automated actions.

The build requires Python 3.12+ and Node.js/npm. The script installs the Python
build requirements and uses the existing frontend npm dependencies.
For backend development and tests, install `backend/requirements-dev.txt`;
the production Docker images install only `backend/requirements.txt`.

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
$env:REDIS_URL = ""
$env:APEXIVE_DATA_DIR = "$PWD\data"
python -m uvicorn app.main:app --app-dir backend --reload --port 8765
```

In a second window, start the frontend:

```powershell
Push-Location frontend
npm.cmd install
npm.cmd run dev
Pop-Location
```

The API documentation is available at `http://127.0.0.1:8765/docs`. Workflow
definitions, runs, and human tasks use the API and are persisted in the
configured data directory. Running a workflow creates a persisted approval task
for each User node; both workflow inbox screens load and update those tasks
through the API. Most other enterprise-suite screens remain interactive
prototypes; their simulated actions are not connected to live company systems.
Redis is optional for this local workflow; Docker Compose configures its own
Redis service for the full stack.

## Phase 1: Agent Runtime Foundation

Apply the database migrations from the backend directory, using the same
`DATABASE_URL` that the API will use:

```powershell
Push-Location backend
python -m alembic upgrade head
Pop-Location
```

Agent runs use an OpenAI-compatible chat-completions endpoint. Configure
`MODEL_GATEWAY_URL` (the provider's API base URL),
`MODEL_GATEWAY_API_KEY`, and optionally `MODEL_GATEWAY_DEFAULT_MODEL` and
`MODEL_GATEWAY_TIMEOUT_SECONDS` in the environment. The URL should not include
`/chat/completions`. If the gateway is not configured, agent runs return an
explicit unavailable error rather than simulated output.

The API exposes agent definitions, runs, memory, allowlisted tools, executions,
and audit records under `/api/v1/agents`; see `/docs` for request schemas.
Current tenant and actor identifiers are supplied by API requests and are not
backed by authentication yet. Keep this API on trusted local/development
networks until the identity and tenant-security phase is implemented.

Agent teams can be created and run at `/api/v1/agents/teams`. Members execute
in configured order, each receiving the previous member's output as context;
team runs and per-agent executions are persisted and audited. Desktop/browser
automation and OCR remain Phase 2 work; the existing process-automation
approval queue is available at `/api/v1/process-automation/approvals`.

The **Specialized AI Agents** workspace provides 16 role templates covering
executive, finance, accounting, HR, recruiting, sales, marketing, procurement,
legal, compliance, project, QA, IT, defensive security, and supply-chain work.
Install them for a tenant from the workspace or through
`POST /api/v1/agents/catalog/install`. Agents analyze only submitted prompts
and saved memory; they are not connected to live ERP, HR, CRM, finance, or
security systems and cannot commit business actions. Configure and approve the
model gateway before sending any sensitive information.

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
The device registry persists tenant-scoped device profiles and operator-set
status through `/api/v1/industrial/devices`; it does not establish hardware
connections or receive telemetry.