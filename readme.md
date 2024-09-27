# FCPXML to Google Sheets (Flame generated XML to Google sheets)
## O repozitáři
- Tento repozitář obsahuje PowerShell a Python skript. Dále obsahuje také soubor apps_script.js, který není určen pro spouštění nýbrž kopírování. Obsahuje také spustitelný soubor ffmpeg.exe
- Pro spuštění skriptu je potřebná instalace Pythonu
  - Pokud nemáte python napište do PowerShell `python` a nainstalujte ze Storu
- Terminál vypisuje podrobné chybové hlášky, sledujte je, debug hlášky v script.log
- If by any chance you found this on the Internet and think it might be useful, just translate it using ChatGpt, cant be bothered
- Author: Erik Sabol, erik.sab18@gmail.com, neváhejte mě kontaktovat s jakýmikoliv problémy 
Proveďte následující kroky pro parsování vašeho xml souboru do lidsky čitelné formy v Google Sheets.
### Vytvoření Google projektu 
- Vytvoř Google cloud projekt ![Zde](https://developers.google.com/workspace/guides/create-project)
- Postupujte podle návodu ![Zde](https://developers.google.com/workspace/guides/create-project)
- Pouze kroky
  - Set up your environment
  - Configure the OAuth consent screen
  - Authorize credentials for a desktop application
- Hlavně přejmenujte stažený soubor na `credentials.json` a umístěte jej do stejné složky jako skript 
TENTO SKRIPT FUNGUJE POUZE PRO WINDOWS 10+
### Spuštění skriptu
- Ze stránky projektu > Code > Download as zip > extrahujte
- Shift+Right Click do složky se skriptem > Open PowerShell window
- spusťte skrip `run.ps1` podle specifikací, které získáte spuštěním příkazu v apliakci PowerShell
  > Get-help ./run.ps1 -Detailed
### Úprava v google sheets
- **Pozor!** Je důležité, aby v řádku s base64 stringami nebylo nic jiného a aby vedlejší řádek byl prázdný. Velikost obrázku je cca 100x200, upravte velikost buňky předem alesponň na tolik pixelů. (Pravé tlačítko na číslo sloupce/řádku > Změnit velikost řádku)
- Přidejte do google sheet skript z `apps_script.js`
  - Zkopírujte obsah souboru do pole v Rozšíření > Apps script
  - Pokud jste neupravovali hodnotu `X` ani `Y` pro `run.ps1`, soubour neměňte. Pokud jste zvolili jiný sloupec nebo řádek změňte honotu `Let X = <>` Čísluje se od jedné, tz. pro sloupec *A* by byl `1`. **Pokud** nechcete, aby byly vytvořeny obrázky do řádků, kde už jsou, nastavte `Y` na stejnou hodnotu jako při spuštění `run.ps1`.
  - Znovu načtěte tabulku pomocí tlačítka refresh v prohlížeči, nahoře by se mělo objevit tlčítka *Base64 to jpg*
  - Zmáčkněte *Execute*
  - Znovu obnovte tabulku, všechny obrázky by se měly načíst
### Doporučení pro formátování
- Řádek s base64 stringami nastavte na *Formát -> Obtékání -> Ustřihávání*
- Náhledy jsou OverGrid obrázky, neposouvají se tudíž s buňkou, ani nereagují na jakékoliv formátování buňky. Nastavte proto velikost buňek předem.
- Zbytek outputů nastavte na zarovnání doprostřed v obou osách
