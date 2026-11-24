#define MyAppName "NEXORA AI"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "NEXORA Technologies"
#define MyAppExeName "NEXORA_AI.exe"

[Setup]
AppId={{4907E723-0371-48B5-B739-47ECEA54AFA2}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=NEXORA_AI_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Desktop Shortcut"; GroupDescription: "Additional Icons:"

[Files]
Source: "dist\NEXORA_AI\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\NEXORA AI"; Filename: "{app}\NEXORA_AI.exe"
Name: "{autodesktop}\NEXORA AI"; Filename: "{app}\NEXORA_AI.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\NEXORA_AI.exe"; Description: "Launch NEXORA AI"; Flags: nowait postinstall skipifsilent