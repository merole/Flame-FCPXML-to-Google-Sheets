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
- **Pozor!** Je důležité, aby v řádku s base64 stringami nebylo nic jiného a aby vedlejší řádek byl prázdný. Velikost obrázku je cca 100x200, upravte velikost buňky předem alesponň na tolik pixelů. (Pravé tlačítko na číslo sloupce/řádku > Změnit velikost řádku)
- Přidejte do google sheet skript z `apps_script.js`
  - Zkopírujte obsah souboru do pole v Rozšíření > Apps script
  - Pokud jste neupravovali hodnotu `X` ani `Y` pro `run.ps1`, soubour neměňte. Pokud jste zvolili jiný sloupec nebo řádek změňte honotu `Let X = <>` Čísluje se od jedné, tz. pro sloupec *A* by byl `1`. **Pokud** nechcete, aby byly vytvořeny obrázky do řádků, kde už jsou, nastavte `Y`na stejnou hodnotu jako při spuštění `run.ps1`.
  - Znovu načtěte tabulku pomocí tlačítka refresh v prohlížeči, nahoře by se mělo objevit tlčítka *Base64 to jpg*
  - Zmáčkněte *Execute*
  - Znovu obnovte tabulku, všechny obrázky by se měli načíst
### Doporučení pro formátování
- Řádek s base64 stringami nastavte na *Formát -> Obtékání -> Ustřihávání*
- Náhledy jsou OverGrid obrázky, neposouvají se tudíž s buňkou, ani nereagují na jakékoliv formátování buňky. Nastavte proto velikost buňek předem.
- Zbytek outputů nastavte na zarovnání doprostřed v obou osách