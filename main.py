import urllib.request
from pathlib import Path
import sys
import os


class Tee(object):
    def __init__(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        self.file = open(filename, "a")  # "a" dopisuje nową linię
        self.stdout = sys.stdout

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):  # Wymagane dla zachowania zgodności
        self.file.flush()
        self.stdout.flush()


maxscreenshots = 10_000

savepath = None
try:
    n = -1
    while os.path.exists(os.path.join(".", ".theapocalypsedefaultcatalog", str(n) if n != -1 else "")) and n < 100:
        n += 1

    savepath = open(".theapocalypsedefaultcatalog" + str(n)).read()
    os.makedirs(os.path.join(savepath, "logs", ""), exist_ok=True)

    for scr in range(100, -1, -1):
        if os.path.exists(
                os.path.join(savepath, "logs", f"log_{scr}.txt" if scr > 0 else "last.png")):
            if scr == 100:
                os.remove(os.path.join(savepath, "logs", f"log_{scr}.txt"))

            elif scr > 0:
                os.rename(os.path.join(savepath, "logs", f"log_{scr}.txt"),
                          os.path.join(savepath, "logs", f"log_{scr + 1}.txt"))

            elif scr == 0:
                os.rename(os.path.join(savepath, "logs", f"last.txt"),
                          os.path.join(savepath, "logs", f"log_1.txt"))

    sys.stdout = Tee("logs/last.txt")
    print(f"Logi będą przekierowywane do: {os.path.join(savepath, "logs", "last.txt")}")
    
except FileNotFoundError:
    print("Pierwsze uruchomienie (:")

link_to_download_mylibs = "https://raw.githubusercontent.com/aJstoja/TheApocalypseRobloxBot/main/README.md"

if not (Path(os.path.join(__file__, "..", "." if not savepath else savepath, "mylibs", ".")).is_dir() or Path(
        os.path.join(__file__, "..", "." if not savepath else savepath, "mylibs", ".")).is_dir()):
    raise FileNotFoundError(
        "Brak doinstalowanych moich zależności. Pobierz pełnego ZIP-a z https://github.com/aJstoja/TheApocalypseRobloxBot")

try:
    from mylibs.config import main_config
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Wymagany jest plik config.py w katalogu mylibs. Pobierz pełnego ZIP-a z https://github.com/aJstoja/TheApocalypseRobloxBot")

try:
    from mylibs.interaction import Interaction
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Wymagany jest plik interaction.py zawierający klasę Interaction w katalogu mylibs. Pobierz pełnego ZIP-a z https://github.com/aJstoja/TheApocalypseRobloxBot")

has_bottle, bottle_slot, savepath, si = main_config(savepath)

try:
    from mylibs.mainbot import mainbot
except ModuleNotFoundError:
    raise ModuleNotFoundError(
        "Wymagany jest plik config.py w katalogu mylibs. Pobierz pełnego ZIP-a z https://github.com/aJstoja/TheApocalypseRobloxBot")

print("\n\nKonfiguracja zakończona!")
print(si, "\n")
input("\nKliknij ENTER by uruchomić program.\n\n")
mainbot(savepath=savepath, maxscreenshots=maxscreenshots, has_bottle=has_bottle, bottle_slot=bottle_slot, si=si)
