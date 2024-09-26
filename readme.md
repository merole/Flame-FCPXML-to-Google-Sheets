# XML to spreadsheet
## O repozitáři
- Tento repozitář obsahuje PowerShell a Python skript. Dále obsahuje také soubor apps_script.js, který není určen pro spouštění nýbrž kopírování. Obsahuje také spustitelný soubor ffmpeg.exe
- Pro spuštění skriptu je potřebná instalace Pythonu, tu zajistí skript sám
Proveďte následující kroky pro parsování vašeho xml souboru do lidsky čitelné formy v google sheets.
TENTO SKRIPT FUNGUJE POUZE PRO WINDOWS 10+
### Spuštění skriptu
- spusťte skrip run.ps1 podle specifikací, které získáte spuštěním příkazu v apliakci PowerShell
  > Get-help ./run.ps1 -Detailed
### Úprava v google sheets
- Přidejte do google sheet script z apps_script.js
- - Zkopírujte obsah souboru do pole v Rozšíření > Apps script
- - Znovu načtěte tabulku, nahoře by se mělo objevit tlčítka Base64 to jpg
- - Zmáčkněte execute
- - Pozor! Je důležité, aby base64 stringy byly v řádku D, ve kterém není nic jiného a aby řádek E byl prázdný. Velikost obrázku je cca 100x200, upravte velikost buňky předem alesponň na tolik pixelů. (Pravé tlačítko na číslo sloupce/řádku > Změnit velikost řádku)
- - Poznámka: pokud by s tímto krokem byl problém jako například, že v řádku D už je něco jiného a nejde to smazat napište Erikovi (erik.sab18@gmail.com)