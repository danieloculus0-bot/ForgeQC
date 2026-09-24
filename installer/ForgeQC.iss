#define MyAppName "ForgeQC Server"
#define MyAppVersion "0.2.0"
#define MyAppPublisher "EZ Fabricating / WMF"
#define MyAppExeName "ForgeQC_Server.exe"

[Setup]
AppId={{75D37018-A395-4DE5-8482-B493CC667AA0}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\ForgeQC Server
DefaultGroupName=ForgeQC Server
DisableProgramGroupPage=yes
PrivilegesRequired=admin
OutputDir=..\dist-installer
OutputBaseFilename=ForgeQC_Server_Setup_{#MyAppVersion}
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no
UninstallDisplayName=ForgeQC Server
UninstallDisplayIcon={app}\{#MyAppExeName}
SetupLogging=yes

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: unchecked
Name: "autostart"; Description: "Start ForgeQC Server when a user signs in"; GroupDescription: "Server:"; Flags: checkedonce

[Dirs]
Name: "{commonappdata}\ForgeQC"; Permissions: users-modify; Flags: uninsneveruninstall
Name: "{commonappdata}\ForgeQC\audit"; Permissions: users-modify; Flags: uninsneveruninstall
Name: "{commonappdata}\ForgeQC\imports"; Permissions: users-modify; Flags: uninsneveruninstall
Name: "{commonappdata}\ForgeQC\imports\erp_inbox"; Permissions: users-modify; Flags: uninsneveruninstall
Name: "{commonappdata}\ForgeQC\imports\erp_archive"; Permissions: users-modify; Flags: uninsneveruninstall
Name: "{commonappdata}\ForgeQC\uploads"; Permissions: users-modify; Flags: uninsneveruninstall

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; DestName: "{#MyAppExeName}"; Flags: ignoreversion

[Icons]
Name: "{group}\ForgeQC Server"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\ForgeQC Server"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon
Name: "{commonstartup}\ForgeQC Server"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: autostart

[Run]
Filename: "{cmd}"; Parameters: "/C netsh advfirewall firewall delete rule name=""ForgeQC NCR Reporter"" >NUL 2>&1"; Flags: runhidden waituntilterminated
Filename: "{cmd}"; Parameters: "/C netsh advfirewall firewall add rule name=""ForgeQC NCR Reporter"" dir=in action=allow protocol=TCP localport=5080 profile=domain,private"; Flags: runhidden waituntilterminated
Filename: "{app}\{#MyAppExeName}"; Description: "Launch ForgeQC Server"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "{cmd}"; Parameters: "/C netsh advfirewall firewall delete rule name=""ForgeQC NCR Reporter"" >NUL 2>&1"; Flags: runhidden waituntilterminated

; IMPORTANT:
; {commonappdata}\ForgeQC is intentionally marked uninsneveruninstall.
; The database, ERP archives, uploaded evidence, and hash-chained audit journal
; are retained when the application is uninstalled.
