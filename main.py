experimental = False  # Ustaw na True, aby włączyć funkcje eksperymentalne (niezalecane, może powodować błędy)

# NIE ZMNIENIAJ NIC PONIŻEJ TEJ LINII!
VERSION = "1.1.1"
SNAPSHOT = "None"

# PONIŻEJ TEJ LINII MOŻESZ ZMIENIAĆ, ALE TYLKO JEŚLI WIESZ, CO ROBISZ I JESTEŚ TEGO PEWIEN!

import inspect
import urllib.request
import sys
import os
import importlib


if experimental:
    print("Włączono tryb eksperymentalny. Uważaj, mogą wystąpić błędy.")
    print("btw obecnie on nic nie robi (:")


def mainbot(*_):
    raise NotImplementedError("mainbot jeszcze nie został zaimportowany.")


def main_config(*_):
    raise NotImplementedError("main_config jeszcze nie został zaimportowany.")


odp = None
while odp not in ["1", "2", "3", "4"]:
    print("Wybierz jak bardzo chcesz mieć zaawansowanego setup-a:\n 1) Najmniej (zrób wszystko co trzeba, bez ŻADNYCH pytań, kontynuacja w bieżącym katalogu)\n 2) Średnio (zrób wszystko co trzeba, lecz podaj listę zależności)\n 3) Prawie maksymalnie (zalecane, choćby za pierwszym razem, chyba że Ci się nie chce (; ) (zrób wszystko co trzeba, z pytaniami tak/nie, wybierz katalog do trzymania plików programu)\n 4) Maksmylanie zaawansowany (pozwól mi WSZYSTKO wybrać samemu)")
    odp = input("" if odp is None else "Nie rozumiem. " + "Który tryb wybierasz (1/2/3/4): ").lower().strip()
mode = int(odp)

if mode == 4:
    print("Aby włączyć opcje eksperymentalne, musisz edytować plik main.py samemu (zamień na górze pliku experimental=False na experimental=True, nie zalecane, tylko do snapshot-ów).")

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


maxlogs = 10_000
maxscreenshots = 10_000

savepath = None
if os.path.exists(".theapocalypsedefaultcatalog"):
    savepath = open(".theapocalypsedefaultcatalog").read()

    print("Znaleziono .theapocalypsedafaultcatalog, sprawdzanie poprawności...")

    if not os.path.exists(savepath):
        odp = input(f"Podany katalog {savepath} nie istnieje. Stworzyć go [T/Y/n]? ").lower().strip()
        while odp not in ["t", "y", "n"]:
            odp = input("Nie rozumiem, powtórz: ").lower().strip()
        conf = True

        if odp == "n":
            raise FileNotFoundError("Jeżeli chcesz skonfigurować, to usuń/zmień nazwę pliku '.theapocalypsedefaultcatalog', lub wpisz 't'/'y'")
        print(f"\nTworzę katalog {savepath}...")
        os.makedirs(savepath)
        print("Utworzono!")

    for pth in ["logs", "screenshots", "cropedscreenshots", "nieruszajmnie"]:
        os.makedirs(os.path.join(savepath, pth), exist_ok=True)

    else:
        missing = []
        for pth in ["logs", "screenshots", "cropedscreenshots", "nieruszajmnie"]:
            if not os.path.exists(os.path.join(savepath, pth)):
                missing.append(pth)

        if len(missing) > 0:
            print(f"Brakuje katalogów: {', '.join(missing)}. Tworzę je...")
            for pth in missing:
                os.makedirs(os.path.join(savepath, pth), exist_ok=True)
            print("Utworzono brakujące katalogi!")
        else:
            print("Wszystkie katalogi istnieją!")

else:
    print("Pierwsze uruchomienie (:")
    print()
    print(f"Setup katalogu [1/5] [•]")
    print(f"Instalowanei zależności [2/5] [ ]")
    print(f"Sprawdzanie oddzielnego setup-u dla linux-a [3/5] [ ]")
    print(f"Konfigurowanie pytesseract (tylko windows, linux zawiera w [2/5]) [4/5] [ ]")
    print(f"Konfigurowanie slotów [5/5] [ ]")
    print()

    if os.path.exists(".theapocalypsedefaultcatalog"):
        raise FileExistsError(
            "Plik .theapocalypsedefaultcatalog nie powinien istnieć, ale istnieje. W nim jest zapisywany katalog gdzie program trzyma swoje pliki.")

    print(f"Ten program będzie także tworzył/edytował/usuwał swoje pliki (np. logi).\n"
          f"Czy mogę mieć te pliki w obecnym katalogu ({os.path.abspath(__file__)}), czy powinienem utworzy oddzielny katalog?\n"
          f"1) Tak (twórz oddzielny katalog)\n"
          f"2) Nie (korzystaj z obecnego katalogu)")
    if mode in [1, 2]:
        print("Wybieram opcję 2, bez pytań (tryb najmniej zaawansowany/średnio zaawansowany).")
        odp = "2"
    else:
        odp = input("Podaj opcję (1/2): ").lower().strip()
    while odp not in ["1", "2"]:
        odp = input("Nie rozumiem. Podaj opcję (1/2): ").lower().strip()

    if odp == "1":
        savepath = input("Podaj nazwę katalogu: ")
        if os.path.exists(savepath) and not os.path.isdir(savepath):
            raise FileExistsError(f"Plik o nazwie {savepath} już istnieje i nie jest katalogiem, nie mogę utworzyć katalogu o tej samej nazwie.")
        elif os.path.isdir(savepath):
            odp = input(
                f"Katalog {savepath} obecnie istnieje. Czy mogę mimo to kontynuować (T/Y/n)? ").lower().strip()
            while odp not in ["t", "y", "n"]:
                odp = input(
                    f"Nie rozumiem, powtórz. Katalog {savepath} obecnie istnieje. Czy mogę mimo to kontynuować (T/Y/N)? ").lower().strip()

            if odp == "n":
                raise FileExistsError("Użytkownik tak wybrał (przejrzyj ostatnią swoją wypowiedź).")
        else:
            os.mkdir(savepath)
            print(f"Utworzono katalog {savepath}!")

    elif odp == "2":
        print("Kontynuuję z plikami w obecnym katalogu.")
        savepath = "."
    else:
        linnia = inspect.currentframe().f_lineno
        raise ValueError(f"Nieprawidłowa odpowiedź (to nie powinno się wydarzyć, zgłoś błąd na githubie, info dla mnie: {linnia=}).")

    with open(".theapocalypsedefaultcatalog", "w") as f:
        f.write(savepath)

    for pth in ["logs", "screenshots", "cropedscreenshots", "nieruszajmnie"]:
        try:
            os.makedirs(os.path.join(savepath, pth), exist_ok=True)
        except FileExistsError:
            pass

    print("Ustawianie logowania do pliku...")

    for i in range(maxlogs, -1, -1):
        if os.path.exists(
                os.path.join(savepath, "logs", f"log_{i}.txt" if i > 0 else f"last.txt")):
            if i == maxlogs:
                os.remove(os.path.join(savepath, "logs",f"log_{i}.txt"))
                continue

            elif i > 0:
                os.rename(os.path.join(savepath, "logs",f"log_{i}.txt"),
                          os.path.join(savepath, "logs", f"log_{i + 1}.txt"))

            elif i == 0:
                os.rename(os.path.join(savepath, "logs", f"last.txt"),
                          os.path.join(savepath, "logs",f"log_1.txt"))

    print("Włączam logowanie do pliku (tego jeszcze nie będzie)")
    sys.stdout = Tee(os.path.join(savepath, "logs", "last.txt"))
    print("Logowanie do pliku włączone! (to już jest)")


def download_myfile(filename: str, is_image: bool = False) -> None:
    catalog_name = "nieruszajmnie"
    download_link = f"https://raw.githubusercontent.com/aJstoja/TheApocalypseRobloxBot/main/{"images" if is_image else "mylibs"}/" + filename
    print(f"Wymagany jest plik {filename}. Pobieram {filename} z: {download_link}")
    try:
        urllib.request.urlretrieve(download_link, os.path.join(savepath, catalog_name, filename))
        print(f"Pomyślnie pobrano: {os.path.join(savepath, catalog_name, filename)}")
    except Exception as e:
        print(f"except Exception as e: {e=}, {str(e)=} (to są logi dla mnie, jeżeli problem cały czas informuje pls poinformuj mnie o tym na githubie)")
        raise ConnectionError(f"Błąd w pobieraniu. Sprawdź połączenie z internetem, jeżeli błąd dalej istnieje spróbuj pobrać {filename} z {download_link} i przenieś ten plik do {os.path.join(savepath, catalog_name, filename)} lub ponownie uruchom program")


def import_mylib(libname: str, package_name: str = None) -> None:
    def pth_join(*args):
        return os.path.join(*args).replace(os.path.sep, ".")

    if package_name is None:
        importlib.import_module(pth_join(savepath, "nieruszajmnie", libname))
    else:
        importlib.import_module(pth_join(savepath, "nieruszajmnie", libname), package_name)


def check_myfile(libname: str, is_image: bool = False) -> bool | None:
    def check_is_valid_mylib(libname: str) -> bool:
        if not (os.path.exists(os.path.join(savepath, "nieruszajmnie", libname)) and os.path.isfile(os.path.join(savepath, "nieruszajmnie", libname))):
            return False
        return True

        file = open(os.path.join(savepath, "nierszajmnie", libname), "r").read()

        st = f"# This is start of orginal {libname} python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!\n"
        en = f"\n# This is end of orginal {libname} python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!"
        return file.startswith(st) and file.endswith(en)

    if is_image:
        if os.path.exists(os.path.join(savepath, "nieruszajmnie", libname)) and os.path.isfile(os.path.join(savepath, "nieruszajmnie", libname)):
            print(f"Znaleziono zdjęcie {libname} w katalogu nieruszajmnie.")
            return True
        else:
            while not os.path.exists(os.path.join(savepath, "nieruszajmnie", libname)) and os.path.isfile(os.path.join(savepath, "nieruszajmnie", libname)):
                print(f"Nie znaleziono zdjęcia {libname} w katalogu nieruszajmnie.")
                odp = input(" Pobrać je? (T/Y/n): ").lower().strip()
                while odp not in ["t", "y", "n"]:
                    odp = input("Nie rozumiem, powtórz. Pobrać je? (T/Y/n): ").lower().strip()

                if odp == "n":
                    return False

                download_myfile(libname + ".png", is_image=True)
            return True

    err_num = 0
    while not check_is_valid_mylib(libname):
        if err_num > 5:
            raise ConnectionError("Wystąpił bład z pobieraniem aż 5 razy. Przejrzyj logi. Jeżeli problem występuje nie z twojej winy powiadom mnie na GitHub-ie.")

        err_num += 1
        download_myfile(libname + ".py")

    return True



def get_version(libname: str) -> tuple[str, str]:
    version, snapshot = open(os.path.join(savepath, "mylibs", libname), "r").read().split("\n")[1:3]
    return version[11:], snapshot[12:]


def get_newest_versions():
    try:
        print("Sprawdzam update-y...")
        with urllib.request.urlopen("https://raw.githubusercontent.com/aJstoja/TheApocalypseRobloxBot/main/README.md") as response:
            readme = response.read().decode("utf-8").split("\n")
        print("Pobrano wersje, sprawdzam...")
        versions = [_.split(":") for _ in readme[readme.index("#### Najnowsze wersje plików:")+1:]]
        dct = {}
        for _ in range(len(versions) - 1):
            version, snapshot = versions[_][1].split(" | ")
            dct[versions[_][0][2:].strip()] = [version.strip(), snapshot.strip()]
        return dct

    except Exception as e:
        print(f"except Exception as e: {e=}, {str(e)=} (to są logi dla mnie, jeżeli problem cały czas informuje pls poinformuj mnie o tym na githubie)")
        input("Błąd w pobieraniu najnowszych wersji. Sprawdź połączenie z internetem, jeżeli błąd dalej istnieje spróbuj ponownie uruchomić program. Kliknięcie ENTER oznacza to, że wiesz że być może masz starą wersję (być może niedziałającą) i chcesz kontynuować.")


newest_versions = get_newest_versions()
if newest_versions['main.py'][0] != VERSION:
    print(f"Twoja wersja main.py ({VERSION}) jest nieaktualna. Najnowsza wersja to {newest_versions['main.py'][0]}. Automatyczne uaktualnianie...")
    os.remove(os.path.abspath(__file__))
    download_myfile("main.py")
    print("Uaktualniono! Restart programu...")
    os.execl(sys.executable, sys.executable, *sys.argv)

if newest_versions['main.py'][1] != SNAPSHOT and experimental:
    print(f"Twoja wersja main.py ({SNAPSHOT}) jest starsza niż najnowsza ({newest_versions['main.py'][1]}). Automatyczne uaktualnianie do eksperymentalnej wersji...")
    os.remove(os.path.abspath(__file__))
    download_myfile("main.py")
    print("Uaktualniono! Uruchamiam ponownie program (flaga experimental=True zamieni się na experimental=False, będzie trzeba to przywrócić dla eksperymentalnego trybu.).")
    os.execl(sys.executable, sys.executable, *sys.argv)


for lib in ["config", "interaction", "mainbot"]:
    check_myfile(lib)
    ver, snap = get_version(lib)
    if ver != newest_versions[lib][0]:
        print(f"Plik {lib} jest nieaktualny. Automatyczne uaktualnianie...")
        os.remove(os.path.join(savepath, "niezmieniaj", lib))
        check_myfile(lib)

    if experimental and snap != newest_versions[lib][1]:
        print(f"Plik {lib} ma starszy snapshot niż najnowszy. Automatyczne uaktualnianie do eksperymentalnej wersji:")
        odp = input("Czy na pewno to zrobić? (T/Y/n): ").lower().strip()
        if odp not in ["t", "y", "tak", "yes"]:
            raise PermissionError("Użytkownik nie pozwolił na uaktualnienie do eksperymentalnej wersji. Jeżeli nie chcesz uaktualniać, wyłącz tryb eksperymentalny w main.py (ustaw experimental=False).")

        print(f"Uaktualnianie {lib} do eksperymentalnej wersji.")
        os.remove(os.path.join(savepath, "niezmieniaj", lib))
        check_myfile(lib)
        print("Uaktualniono!")


skip_healthbar_config = True
selected_health_bar = "health_bar.png"
if mode == 4:
    while True:
        odp = input("Czy chcech konfigurować pasek zdrowia ręcznie (T/Y/n)? ").lower().strip()
        if odp in ["t", "y"]:
            skip_healthbar_config = False
            break
        elif odp == "n":
            break
        print("Nie rozumiem. Powtórz.")

if skip_healthbar_config:
    print("Pobieram wspólny health bar. Jeżeli chcesz mieć swój własny, uruchom ponownie program i wybierz tryb 4.")
    while not check_myfile(f"health_bar_toall", is_image=True):
        print("Pobieranie nie powiodło się. Spróbuj ponownie.")
    selected_health_bar = "health_bar_toall"
else:
    all_hp_bars = [120, 125, 130, 135, 140, 150, 163, 175, 188, 200, 260]
    for hp in all_hp_bars:
        check_myfile(f"health_bar_{hp}")

    healthbars = [_[11:14] for _ in os.listdir(os.path.join(savepath, "nieruszajmnie")) if _.startswith("health_bar_") and _.endswith(".png")]

    if not os.path.exists(os.path.join(savepath, "niezmieniaj", "MYOWNHEALTHBAR.png")):
        print(f"Jeżeli masz swój pasek zdrowia, którego nie ma na tej liście: {healthbars} wrzuć go do {os.path.join(savepath, "niezmieniaj", "MYOWNHEALTHBAR.png")} i uruchom ponownie program")
    elif os.path.exsists(os.path.join(savepath, "niezmieniaj", "MYOWNHEALTHBAR.png")) and not os.path.isfile(os.path.join(savepath, "niezmieniaj", "MYOWNHEALTHBAR.png")):
        raise FileExistsError(f"Plik {os.path.join(savepath, "niezmieniaj", "MYOWNHEALTHBAR.png")} powinien być plikiem, a nie katalogiem lub innym typem pliku.")
    else:
        print(f"Znaleziono {os.path.join(savepath, 'niezmieniaj', 'MYOWNHEALTHBAR.png')}, używam go jako wzorca health bar-a.")
        selected = "custom"

    while len(healthbars) == 0:
        print("Nie znaleziono żadnego zainstalowanego paska zdrowia.")

        for hp in all_hp_bars:
            check_myfile(f"health_bar_{hp}")

    selected = None

    while not selected:
        odp = input(f"Wybierz, ile masz maks HP (dostępne {", ".join(healthbars)}), lub jeżeli nie m twojego na liście wpisz `i`: ")
        while odp not in healthbars and odp != "i":
            odp = input(f"Nie rozumiem, powtórz. Wybierz, ile masz maks HP (dostępne {', '.join(healthbars)}), lub jeżeli nie m twojego na liście wpisz `i`: ")

        if odp == "i":
            for hp in all_hp_bars:
                check_myfile(f"health_bar_{hp}")
            print(f"Jeżeli nie ma wyżej twojego paska zdrowia, zrób jego screena usuń tło, wrzuć to do: {os.path.join(savepath, 'niezmieniaj', 'MYOWNHEALTHBAR.png')} i uruchom ponownie program.")

        else:
            if check_myfile(f"health_bar_{odp}.png"):
                selected_health_bar = int(odp)
                print(f"Wybrano pasek zdrowia dla {selected_health_bar} maks HP.")
            else:
                print("Bład w pobieraniu. Spróbuj ponownie.")

        healthbars = [_[11:14] for _ in os.listdir(os.path.join(savepath, "nieruszajmnie")) if _.startswith("health_bar_") and _.endswith(".png")]

health_bar_pth = os.path.join(savepath, "nieruszajmnie", selected_health_bar if selected_health_bar != "custom" else "MYOWNHEALTHBAR") + ".png"

import_mylib("config", "main_config")

has_bottle, bottle_slot, savepath, si = main_config(savepath, mode=mode)

import_mylib("mainbot")

print("\n\nKonfiguracja zakończona!")
print(si, "\n")
input("\nKliknij ENTER by uruchomić program.\n\n")
mainbot(_savepath=savepath, _maxscreenshots=maxscreenshots, _has_bottle=has_bottle, _bottle_slot=bottle_slot, _si=si, _mode=mode, _experimental=experimental)
