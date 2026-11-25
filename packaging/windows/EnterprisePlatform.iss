#define AppName "ApexiveAI Enterprise Platform"
#define AppVersion "1.0.0"
#define AppPublisher "ApexiveAI"
#define RepositoryRoot AddBackslash(SourcePath) + "..\.."

[Setup]
AppId={{A1C2F301-5FEA-4E3D-A1E2-9A2F1EE8C047}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={localappdata}\Programs\ApexiveAI\EnterprisePlatform
DefaultGroupName={#AppName}
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir={#RepositoryRoot}\dist
OutputBaseFilename=EnterprisePlatform-Setup
UninstallDisplayIcon={app}\EnterprisePlatform.exe
Compression=lzma2
SolidCompression=yes
WizardStyle=modern

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "{#RepositoryRoot}\build\windows-installer-payload\EnterprisePlatform.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\ApexiveAI Enterprise Platform"; Filename: "{app}\EnterprisePlatform.exe"
Name: "{autodesktop}\ApexiveAI Enterprise Platform"; Filename: "{app}\EnterprisePlatform.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\EnterprisePlatform.exe"; Description: "Launch ApexiveAI Enterprise Platform"; Flags: nowait postinstall skipifsilent
