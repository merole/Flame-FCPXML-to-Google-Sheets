<#
.DESCRIPTION
  Tento program buďto bytvoří novou google sheet tabulku nebo použije uživatelem zadanou tabulky a vloží do ní po sloupcích: název klipu, číslo scény, recordový timekód scény a binární data v base64  prvního snímku scény pro renderování v rabulce. 
  Při prvním a každém dalším spuštění po vypršení relace je potřeba odsouhlasit všechny požadavky od Googlu, které na počítači vyskočí. Tento skript totiž používá Sheets API od Google.
  V běhu programu bude vytvořen soubor s defaultním názvem "first_frames", do kterého pomocí ffmpegu exportuji první snímky klipů.
  Celý běh programu je založen na obsahu .fcpxml souboru. Skript vypisuje pouze tagy "clip" a ignoruje např tagy jako "gap". Skrip počítá s tím, že se v souboru nachází pouze jeden od každého tagu "library", "event", "project", "sequence", "spine". 
  Pokud tomu tak není kontaktujte autora na emailu erik.sab18@gmail.com pro úpravu.
  Skript tvoří jména do tabulky také podle .fcpxml souboru. Pro správné fungování je nutné aby jméno "clipu" bylo ve formátu RB_14_010.. Skript bude fungovat, jenom jména v tabulce nebudou dávat smysl.
  Skript je potřeba spustit se správnými argumenty. Takto vypadá názorné spuštění sktriptu (Také v sekci Synopsis):
  ./run.ps1 -project_name Rosabella -xml_folder RB_015 
.PARAMETER project_name
  Povinný: Jméno projektu, např. "Rosabella"
.PARAMETER xml_folder
  Povinný: Jméno souboru obsahující .fcpxml a sobour MEDIA obsahující klipy popsané .fcpxml souborem např. "RB_O15"
.PARAMETER xml_folder_dir
  Absolutní adresa souboru ve kterém se nachází XML soubor
.PARAMETER sheet_id
  ID google sheetu do kterého chcete exportovat data, pokud je argument nespecifikován vytvoří novou tabulku.
  lze ho zjisti z URL otevřené tabulky, které je ve formátu:
  https://docs.google.com/spreadsheets/d/ID/edit?gid=...#gid=...
.PARAMETER x
  Počátek, kde mají začínat data vložená do google sheets tabulky DEFAULT "A"
.PARAMETER y
  Počátek, kde mají začínat data vložená do google sheets tabulky DEFAULT "1"
.PARAMETER out_file
  Jméno souboru, do kterého se exportují první snímky z klipů z xml souboru DEFAULT "first_frames"
.SYNOPSIS
  ./run.ps1 Rosabella RB_015
  ./run.ps1 Goldilocks GL_120 -xml_folder_dir C:\Users\user\Documents\export\xml -sheet_id 1tLJlV7cBUErfAYelfAQ0hC_IEa4TvyZ8oS4hDfAg8 -x B -y 2 -out_file "test1"
#>
param( 
  [Parameter(
    Mandatory = $true,
    Position = 0
  )]
  [string]$project_name,
  [Parameter(
    Mandatory = $true,
    Position = 1
  )]
  [string]$xml_folder,
  [string]$xml_folder_dir = "",
  [string]$sheet_id = "",
  [string]$x = "A",
  [int32]$y = 1,
  [string]$out_file = "first_frames"
)
$input_list = $xml_folder_dir, $sheet_id, $x, $y, $out_file

$p = &{python -V} 2>&1
# check if an ErrorRecord was returned
if($p -is [System.Management.Automation.ErrorRecord]){
  Invoke-WebRequest -o python-installer.exe https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe
  python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
}

$re = "*WARNING*"
$error_output = pip show google-api-python-client google-auth-httplib2 google-auth-oauthlib 2>&1 

if ($error_output -like $re) {
  pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
}

$test = $false
foreach ($item in (Get-ChildItem)) {
  if ($item -like $xml_folder) {
    $test = $true
  }
  if ($item -like $out_file) {
    Remove-Item $out_file -Force -Recurse
  }
}

if ($test -eq $true) {
  Write-Host Proceeding to extract frames
} else {
  throw [System.IO.FileNotFoundException] "RB_015 missing or files already extracted"
}

mkdir first_frames > $null
foreach ($clip in Get-ChildItem -Path ".\RB_015\MEDIA" -Name) {
  .\ffmpeg\ffmpeg.exe `
  -i "RB_015\MEDIA\$($clip)" -ss "00:00:00" `
  -vframes 1 `
  ".\first_frames\$($clip.Substring(0, $clip.length - 3))jpg" `
  -hide_banner `
  -loglevel info
}

$arg_list = "--xml_folder_dir", "--sheet_id", "-x", "-y", "--out_file"

foreach ($i in 0..4) {
  if ($input_list[$i] -eq "") {
    $arg_list[$i] = ""
  }
}

python main.py $project_name $xml_folder $arg_list[0] $xml_folder_dir $arg_list[1] $sheet_id $arg_list[2] $x $arg_list[3] $y $arg_list[4] $out_file