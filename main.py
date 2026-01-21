import urllib.request
import sys
import os
import importlib


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
    print()
    print(f"Setup katalogu [1/5] [•]")
    print(f"Instalowanei zależności [2/5] [ ]")
    print(f"Sprawdzanie oddzielnego setup-u dla linux-a [3/5] [ ]")
    print(f"Konfigurowanie pytesseract (tylko windows, linux zawiera w [2/5]) [4/5] [ ]")
    print(f"Konfigurowanie slotów [5/5] [ ]")
    print()


    def catalog_setup():
        global savepath

        if savepath is None:
            print(f"Ten program będzie także tworzył/edytował/usuwał swoje pliki (np. logi).\n"
                  f"Czy mogę mieć te pliki w obecnym katalogu ({os.path.abspath(__file__)}), czy powinienem utworzy oddzielny katalog?\n"
                  f"1) Tak\n"
                  f"2) Nie")
            odp = input("Podaj opcję (1/2): ").lower().strip()
            while odp not in ["1", "2"]:
                odp = input("Nie rozumiem. Podaj opcję (1/2): ").lower().strip()

            if odp == "1":
                savepath = input("Podaj nazwę katalogu: ")
                try:
                    os.mkdir(savepath)
                    print(f"Utworzono katalog {savepath}!")
                except FileExistsError:
                    odp = input(
                        f"Katalog {savepath} obecnie istnieje. Czy mogę mimo to kontynuować (T/Y/N)? ").lower().strip()
                    while odp not in ["t", "y", "n"]:
                        odp = input(
                            f"Nie rozumiem, powtórz. Katalog {savepath} obecnie istnieje. Czy mogę mimo to kontynuować (T/Y/N)? ").lower().strip()

                    if odp == "n":
                        raise FileExistsError("Użytkownik tak wybrał (przejrzyj ostatnią swoją wypowiedź).")
            elif odp == "2":
                print("Kontynuuję z plikami w obecnym katalogu.")
                savepath = "."

            _n = -1
            while os.path.exists(os.path.join(".theapocalypsedefaultcatalog", str(_n) if _n != -1 else "")):
                _n += 1

            if _n > 100:
                raise FileExistsError("Czemu masz 100 plików .theapocalypsedefaultcatalog(liczba który to jest plik)?")

            with open(".theapocalypsedefaultcatalog" + str(_n) if _n != -1 else "", "w") as f:
                f.write(savepath)

            for nameofdir in ["logs", "screenshots", "cropedscreenshots", "nieruszajmnie"]:
                try:
                    os.makedirs(os.path.join(savepath, nameofdir), exist_ok=True)
                except FileExistsError:
                    pass

            raiseerror = True
            tries = 0
            while raiseerror:
                try:
                    tries += 1
                    urllib.request.urlretrieve("https://dzialak.waw.pl/jn/health_bar.png",
                                           os.path.join(savepath, "nieruszajmnie", 'health_bar.png'))
                    raiseerror = False
                except Exception as e:
                    if tries < 5:
                        print(f"Podczas pobierania wystąpił błąd {e}. Próbuję ponownie... (próba: {tries}/5)")
                    else:
                        raise ConnectionError(f"Pięć razy wystąpił błąd w pobieraniu. Spróbuj ponownie, sprawdź połączenie z internetem, lub umieść health_bar.png w {os.path.join('savepath', 'nieruszajmnie', 'health_bar.png')}")

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

            sys.stdout = Tee(os.path.join(savepath, "logs", "last.txt"))
            print("Logowanie do pliku włączone!")
            return savepath
        else:
            print("Znaleziono .theapocalypsedafaultcatalog, sprawdzanie poprawności...")
            conf = None

            # CASADE POMÓŻ sprawdzanie poprawności:
            if os.path.exists(savepath):
                print("Podany katalog istnieje!", end=' ')
            else:
                odp = input(f"Podany katalog {savepath} nie istnieje. Stworzyć go? ").lower().strip()
                while odp not in ["t", "y", "n"]:
                    odp = input("Nie rozumiem, powtórz: ").lower().strip()
                conf = True

                if odp == "n":
                    raise FileNotFoundError("Jeżeli chcesz skonfigurować, to usuń/zmień nazwę pliku '.theapocalypsedefaultcatalog', lub wpisz 't'/'y'")
                print(f"\nTworzę katalog {savepath}...")
                os.makedirs(savepath)
                print("Utworzono!")

            for pth in ["logs", "screenshots", "cropedscreenshots", "nieruszajmnie"]:
                if os.path.exists(os.path.join(savepath, pth)):
                    print(end=f"({pth} istnieje) ")
                else:
                    print(f"Brak {pth}...")
                    sectime = False
                    while not conf:
                        odp = input(f"Stworzyć ten katalog? ").lower().strip()
                        while odp not in ["t", "y", "n"]:
                            odp = input("Nie rozumiem, powtórz: ").lower().strip()
                        conf = True

                        if odp == "n":
                            raise FileNotFoundError(
                                "Jeżeli chcesz skonfigurować, to usuń/zmień nazwę pliku '.theapocalypsedefaultcatalog', lub wpisz 't'/'y'")
                        print(f"\nTworzę katalog {os.path.join(savepath, pth)}...")
                        os.makedirs(os.path.join(savepath, pth))
                        print("Utworzono!")
            
            raiseerror = True
            tries = 0
            while raiseerror:
                try:
                    tries += 1
                    urllib.request.urlretrieve("https://dzialak.waw.pl/jn/health_bar.png",
                                           os.path.join(savepath, "nieruszajmnie", 'health_bar.png'))
                    raiseerror = False
                except Exception as e:
                    if tries < 5:
                        print(f"Podczas pobierania wystąpił błąd {e}. Próbuję ponownie... (próba: {tries}/5)")
                    else:
                        raise ConnectionError(f"Pięć razy wystąpił błąd w pobieraniu. Spróbuj ponownie, sprawdź połączenie z internetem, lub umieść health_bar.png w {os.path.join('savepath', 'nieruszajmnie', 'health_bar.png')}")

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

            sys.stdout = Tee(os.path.join(savepath, "logs", "last.txt"))
            print("Logowanie do pliku włączone!")
            
            return savepath
                


    savepath = catalog_setup()


def download_mylib(libname: str) -> None:

    download_link = "https://raw.githubusercontent.com/aJstoja/TheApocalypseRobloxBot/main/mylibs/" + libname
    print(f"Wymagany jest plik {libname} w katalogu mylibs. Pobieram {libname} z: {download_link}")
    try:
        urllib.request.urlretrieve(download_link, os.path.join(savepath, "mylibs", libname))
        print(f"Pomyślnie pobrano: {os.path.join(savepath, "mylibs", libname)}")
    except Exception as e:
        print(f"except Exception as e: {e=}, {str(e)=} (to są logi dla mnie, jeżeli problem cały czas informuje pls poinformuj mnie o tym na githubie)")
        raise ConnectionError(f"Błąd w pobieraniu. Sprawdź połączenie z internetem, jeżeli błąd dalej istnieje spróbuj pobrać {libname} z {download_link} i przenieś {libname} do {os.path.join(savepath, "mylibs", libname)} lub ponownie uruchom program")


def import_mylib(libname: str, package_name: str = None) -> None:
    if package_name is None:
        importlib.import_module(savepath + ".mylibs." + libname)
    else:
        importlib.import_module(savepath + ".mylibs." + libname, package_name)


def check_mylib(libname: str) -> None:
    def check_is_falid_mylib(libname: str) -> bool:
        if not (os.path.exists(os.path.join(savepath, "mylibs", libname)) and os.path.isfile(os.path.join(savepath, "mylibs", libname))):
            return False

        file = open(os.path.join(savepath, "mylibs", libname), "r").read()

        st = f"# This is start of orginal {libname} python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!\n"
        en = f"\n# This is end of orginal {libname} python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!"
        return file.startswith(st) and file.endswith(en)

    err_num = 0
    while not check_is_falid_mylib(libname):
        if err_num > 5:
            raise ConnectionError("Wystąpił bład z pobieraniem aż 5 razy. Przejrzyrz logi. Jeżeli problem występuje nie z twojej winy powiadom mnie na GitHub-ie.")

        err_num += 1
        download_mylib(libname + ".py")

for lib in ["config", "interaction", "mainbot"]:
    check_mylib(lib)

import_mylib("config", "main_config")

has_bottle, bottle_slot, savepath, si = main_config(savepath)

import_mylib("mainbot")

print("\n\nKonfiguracja zakończona!")
print(si, "\n")
input("\nKliknij ENTER by uruchomić program.\n\n")
mainbot(savepath=savepath, maxscreenshots=maxscreenshots, has_bottle=has_bottle, bottle_slot=bottle_slot, si=si)
