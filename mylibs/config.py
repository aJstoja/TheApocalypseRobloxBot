# This is start of orginal config python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!
# VERSION 1.0.1
# SNAPSHOT: None


from platform import system
from typing import Optional
import subprocess
import importlib
import shutil
import sys
import os

now = 1
savepath = None
mode: None | int = None


# --- Funkcje pomocnicze ---
def get_package_manager():
    if shutil.which("apt"):
        return "apt"

    if shutil.which("dnf"):
        return "dnf"

    if shutil.which("pacman"):
        return "pacman"

    return None


def prompt_yes_no(question: str) -> bool:
    """Zadaje pytanie T/N i zwraca True dla 'tak'."""
    while True:
        answer = input(f"{question} [T/n]: ").strip().lower()
        if answer in ("t", "tak", "y", "yes", ""):
            return True
        if answer in ("n", "nie", "no"):
            return False
        print("Nie rozumiem. Odpowiedz 'T' (tak) lub 'N' (nie).")


def install_system_package(package_name: str) -> bool:
    """Instaluje pakiet systemowy, używając wykrytego menedżera pakietów."""

    pkg_mgr = get_package_manager()
    if not pkg_mgr:
        print("[BŁĄD] Nie wykryto menedżera pakietów (apt, dnf, pacman).")
        return False

    if not shutil.which("sudo"):
        print("[BŁĄD] 'sudo' nie jest dostępne. Nie mogę zainstalować pakietów.")
        return False

    install_commands = {
        "apt": f"sudo apt update && sudo apt install -y {package_name}",
        "dnf": f"sudo dnf install -y {package_name}",
        "pacman": f"sudo pacman -S --noconfirm {package_name}"
    }

    cmd = install_commands[pkg_mgr]
    print(f"🔧 Instaluję pakiet: '{package_name}'...")
    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Pomyślnie zainstalowano '{package_name}'.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Błąd podczas instalacji '{package_name}': {e}")
        return False


def ensure_command_available(
        command_name: str,
        package_name: Optional[str] = None,
        critical: bool = True
) -> bool:
    """
    Sprawdza, czy komenda jest dostępna. Jeśli nie, pyta o instalację.
    Zwraca True, jeśli komenda jest dostępna po wykonaniu funkcji.
    """
    if shutil.which(command_name):
        return True

    pkg_name = package_name or command_name
    print(f"⚠️ Nie znaleziono komendy: '{command_name}' (pakiet: '{pkg_name}').")

    if not prompt_yes_no(f"Czy chcesz doinstalować pakiet '{pkg_name}'?"):
        if critical:
            print(f"[BŁĄD] Krytyczny pakiet '{pkg_name}' jest wymagany do działania programu.")
            sys.exit(1)
        print(f"[INFO] Pominięto instalację '{pkg_name}'.")
        return False

    if install_system_package(pkg_name):
        # Sprawdź ponownie po instalacji
        if shutil.which(command_name):
            return True
        else:
            print(f"[BŁĄD] Instalacja '{pkg_name}' się nie powiodła lub komenda nadal nie jest w PATH.")
            if critical:
                sys.exit(1)
            return False

    if critical:
        sys.exit(1)
    return False


# --- Główna funkcja sprawdzająca ---

def check_linux_setup():
    """Sprawdza i instaluje wszystkie zależności na Linuksie."""
    import pytesseract
    print("Rozpoczynam sprawdzanie zależności dla Linuksa")

    # 1. Sprawdzenie narzędzi do automatyzacji GUI
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    print(f"\nWykryto sesję typu: {session_type}")

    if session_type == "wayland":
        print("Sesja Wayland wymaga 'ydotool'.")
        ensure_command_available("ydotool", "ydotool", critical=True)
        # Informacja o demonie ydotool, który może być potrzebny
        if not shutil.which("ydotoold"):
            print("[INFO] 'ydotool' czasem wymaga uruchomienia demona 'ydotoold'.")
            print("       Jeśli skrypt nie będzie reagować na mysz/klawiaturę, uruchom 'ydotoold' w osobnym terminalu.")
    else:  # Zakładamy X11 lub inne
        print("Sesja X11 (lub inna) zaleca 'xdotool'.")
        if not ensure_command_available("xdotool", "xdotool", critical=False):
            # Jeśli xdotool nie jest zainstalowany, spróbuj z ydotool jako alternatywą
            print("Próbuję z alternatywą 'ydotool'...")
            ensure_command_available("ydotool", "ydotool", critical=True)

    # 2. Sprawdzenie obsługi GUI w Pythonie (tkinter)
    try:
        import tkinter
        print("\n✅ Moduł 'tkinter' jest dostępny.")
    except ImportError:
        print("\n⚠️ Moduł 'tkinter' nie jest dostępny.")
        # Nazwy pakietów z tkinterem
        tk_packages = {"apt": "python3-tk", "dnf": "python3-tkinter", "pacman": "tk"}
        pkg_mgr = get_package_manager()
        pkg_name = tk_packages.get(pkg_mgr, "python3-tk")

        if prompt_yes_no(f"Czy chcesz doinstalować '{pkg_name}'?"):
            if install_system_package(pkg_name):
                try:
                    import tkinter
                    print("✅ 'tkinter' pomyślnie zainstalowany.")
                except ImportError:
                    print("[BŁĄD] 'tkinter' nadal nie działa po instalacji.")
                    sys.exit(1)
            else:
                print("[BŁĄD] Nie udało się zainstalować 'tkinter'.")
                sys.exit(1)
        else:
            print("[BŁĄD] 'tkinter' jest wymagany do działania skryptu.")
            sys.exit(1)

    # 3. Sprawdzenie Tesseract OCR
    try:
        pytesseract.get_tesseract_version()
        print("\n✅ Silnik Tesseract OCR jest dostępny.")
    except pytesseract.TesseractNotFoundError:
        print("\n⚠️ Silnik Tesseract OCR nie został znaleziony.")
        # Nazwy pakietów z Tesseractem
        tesseract_packages = {"apt": "tesseract-ocr", "dnf": "tesseract", "pacman": "tesseract"}
        pkg_mgr = get_package_manager()
        pkg_name = tesseract_packages.get(pkg_mgr, "tesseract-ocr")

        if prompt_yes_no(f"Czy chcesz doinstalować '{pkg_name}'?"):
            if install_system_package(pkg_name):
                # Sprawdź ponownie
                try:
                    pytesseract.get_tesseract_version()
                    print("✅ Tesseract pomyślnie zainstalowany.")
                except pytesseract.TesseractNotFoundError:
                    print("[BŁĄD] Tesseract nadal nie jest dostępny po instalacji.")
                    sys.exit(1)
            else:
                print("[BŁĄD] Nie udało się zainstalować Tesseract.")
                sys.exit(1)
        else:
            raise ModuleNotFoundError("[BŁĄD] Tesseract jest wymagany do działania skryptu.")

    if not shutil.which("wmctrl"):
        if prompt_yes_no(
                "Brak wmctrl. To nie jest wymagane, ale zalecane bo pozwoli zaznaczyć okno automatycznie. Czy chcesz go doinstalować"):
            if install_system_package("wmctrl"):
                print("Najprawdopodobniej pomyślnie zainstalowano wmctrl (:")
            else:
                print(
                    "Niestety wystąpił problem podczas instalacji ): aby kontynuować z dodatkowymi funkcjami (zaznaczaniem Robloxa/Sobera) uruchom w oddzielnym terminalu `sudo apt install wmctrl`.")
        else:
            print(
                "Anulowałeś instalację wmctrl ): aby kontynuować z dodatkowymi funkcjami (zaznaczaniem Robloxa/Sobera) uruchom w oddzielnym terminalu `sudo apt install wmctrl`.")

    print("\n--- Wszystkie zależności dla Linuksa zostały sprawdzone ---")


def system_check():
    curr_os = system()
    if curr_os == "Linux":
        session_type = os.environ.get("XDG_SESSION_TYPE")
        print(f"session_type: {session_type}, skonfiguruj.")
    elif curr_os == "Windows":
        print("skonfiguruj.")
    elif curr_os == "Darwin":
        print("czyli nieobsługiwany system (:")
        raise SystemError("MacOS nie jest wspierany przez mój program ):")
    else:
        print("czyli nieobsługiwany system (:")
        raise SystemError(f"Nie wykryto poprawnie systemu (co to za system {curr_os}?)")


def install_dependencies():
    # Wspólne pakiety dla wszystkich systemów
    required_packages = [
        "psutil",  # Do zarządzania procesami (kill)
        "mss",  # Do szybkich screenshotów
        "pyautogui",  # Do kontroli myszy i klawiatury (Windows/Linux)
        "pillow",  # Do obróbki obrazów (PIL)
        "pytesseract",  # Wrapper do Tesseract OCR
        "opencv-python-headless",  # Do zaawansowanej obróbki obrazu (bez GUI)
        "numpy"  # Operacje numeryczne na obrazach (dla OpenCV)
    ]
    # Dodatkowe pakiety TYLKO dla Windows
    if system() == "Windows":
        required_packages += ["pygetwindow", "pywin32"]

    print("Sprawdzanie bibliotek Python...")
    missing_packages = []
    for pkg in required_packages:
        twotimeserror = False
        first_time = True
        while missing_packages or first_time:
            missing_packages = []
            first_time = False

            try:
                print(f"Próba importu {pkg}")
                notorginalnames = {"pillow": "PIL", "opencv-python-headless": "cv2", "pywin32": "os"}
                importlib.import_module(notorginalnames.get(pkg, pkg))
                print("Powodzenie!")
            except ImportError:
                print(f"Error! Dodawanie {pkg} do listy niezainstalowanych zależności programu.")
                missing_packages.append(pkg)

            error_times = 0
            while missing_packages:
                if twotimeserror:
                    print("Błąd wystąpił ponownie (?). Próba ponownej instalacji...")

                print(f"Zostanie uruchomiona komenda:\n{sys.executable} -m pip install {" ".join(missing_packages)}")
                if mode != 1:
                    odp = input(f"Brak bibliotek\n{missing_packages}\nZainstalować je poprzez pip? ").strip().lower()
                    while odp not in ["n", "t", "y"]:
                        odp = input(
                            f"Nie rozumiem. Brak bibliotek\n{missing_packages}\nZainstalować je poprzez pip? ").strip().lower()
                else:
                    if error_times > 5:
                        raise ConnectionError(
                            f"Te biblioteki:\n{missing_packages}\nsą wymagane do działania skryptu. Zainstaluj je samemu lub uruchom program ponownie. (błąd internetu na 99%)")
                    error_times += 1
                    print(f"Automatycznie instaluję brakujące pakiety z powodu trybu 1.")
                    odp = "t"

                if odp == "n":
                    raise ImportError(
                        f"Te biblioteki:\n{missing_packages}\nsą wymagane do działania skryptu. Zainstaluj je samemu lub uruchom program ponownie i wpisz `t` by program działał.")

                toinstall = "".join(missing_packages)
                subprocess.check_call([sys.executable, "-m", "pip", "install", *toinstall])
                twotimeserror = True


def tesseract_config(path):
    import pytesseract
    try:
        pytesseract.get_tesseract_version()
        print("Tesseract zainstalowany i zkonfigurowany!")
        return
    except pytesseract.TesseractNotFoundError:
        print("Tesseract wymaga konfiguracji...")

    if system() == "Windows":

        print("Pobieranie Tesseract dla Windows...")

        url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.4.0.20240606.exe"
        os.makedirs(os.path.join(path, "donottouchme"), exist_ok=True)

        installer_path = os.path.join(path, "donottouchme", "tesseract_installer.exe")
        if os.path.exists(installer_path): os.remove(installer_path)

        import urllib.request

        # Use urlopen to get a file-like response object
        with urllib.request.urlopen(url) as response:
            with open(installer_path, 'wb') as f:
                while True:
                    # Read data in 8192-byte chunks
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    f.write(chunk)

        print("Uruchamianie instalatora Tesseract...")
        subprocess.run([installer_path, "/S"], check=True)

        os.remove(installer_path)

        tess_path = r'C:\Program Files\Tesseract-OCR'
        if os.path.exists(tess_path):
            print("Zainstalowano Tesseract w: ", tess_path)
            pytesseract.pytesseract.tesseract_cmd = os.path.join(tess_path, "tesseract.exe")
        else:
            raise ImportError("[ERROR] Instalacja Tesseract nie powiodła się.")

    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def print_status():
    global now

    now += 1

    def getchar(cp, cd):
        return "•" if cp == cd else "✓" if cp > cd else " "

    print()
    print(f"Setup katalogu [1/5] [{getchar(now, 1)}]")
    print(f"Instalowanei zależności [2/5] [{getchar(now, 2)}]")
    print(f"Sprawdzanie oddzielnego setup-u dla linux-a [3/5] [{getchar(now, 3)}]")
    print(f"Konfigurowanie pytesseract (tylko windows, linux zawiera w [2/5]) [4/5] [{getchar(now, 4)}]")
    print(f"Konfigurowanie slotów [5/5] [{getchar(now, 5)}]")
    print()


def slots_config():
    custom_food = False
    if mode == 4:
        custom_food = prompt_yes_no("Tryb 4: czy chcesz ustawić swoje jedzenie (bot będzie działał dokładniej jeżeli tak, jeżeli nie to konfiguracja == tryb 3)")

    if custom_food:
        has_bottle = prompt_yes_no("Czy obecnie patrzysz się na Water Rain Collector posiadając na pasku butelkę")

        bottle_slot = 0
        if has_bottle:
            slot_input = input(
                "Pamiętaj o posiadaniu pustego slotu nr. 1 (lub czegoś nie powodującego przesunięcie (jedzenie, a nie narzędzie)). Podaj slot butelki (liczba 1-9 włącznie): ")
            while slot_input not in [str(_) for _ in range(1, 10)]:
                slot_input = input(
                    "Nie rozumiem. Pamiętaj o posiadaniu pustego slotu nr. 1. Podaj slot butelki (liczba 1-9 włącznie): ")
            bottle_slot = int(slot_input)
            input("Jeżeli ta butelka jest pełna, wypij wodę w niej, po czym kliknij ENTER.")

        slots = list(range(1, 10))
        if bottle_slot in slots:
            slots.remove(bottle_slot)

        food = {
            "Chips": {"Hunger": 25, "Thirst": 0,
                      "Keywords": ["chips", "czips", "czipsy", "chipsy", "chi", "chip", "czi", "czip"]},
            "Blueberry": {"Hunger": 7, "Thirst": 4,
                          "Keywords": ["blueberry", "blueberrys", "jagoda", "jagody", "jag", "blu", "blue"]},
            "Strawberry": {"Hunger": 10, "Thirst": 5,
                           "Keywords": ["strawberry", "strawberrys", "truskawka", "truskawki", "tru", "trus", "str",
                                        "stra",
                                        "straw"]},
            "Potato": {"Hunger": 15, "Thirst": 0,
                       "Keywords": ["potato", "potatos", "potatoes", "ziemniak", "ziemniaka", "ziemniaki", "zie",
                                    "ziem",
                                    "ziemn", "pot", "pota"]},
            "Bread": {"Hunger": 20, "Thirst": 0,
                      "Keywords": ["bread", "breads", "chleb", "chleby", "chlebów", "hleb", "hleby", "hlebów", "chlep",
                                   "chlepy", "chlepów", "hlep", "hlepy", "hlepów", "chl", "chle", "hle", "bre",
                                   "brea"]},
            "Artic Fruit": {"Hunger": 100, "Thirst": 100,
                            "Keywords": ["artic fruit", "owoc arktyczny", "arktyczny owoc", "art", "fru", "owo", "ark",
                                         "artic fruits", "arktycznych owoców"]},
            "Cooked Beans": {"Hunger": 40, "Thirst": 15,
                             "Keywords": ["cooked beans", "beans", "bea", "ugotowana fasolka", "ugotowane fasolki",
                                          "fasolka", "fasoli", "fas"]},
            "Cooked Corn": {"Hunger": 40, "Thirst": 15,
                            "Keywords": ["cooked corn", "corn", "cor", "ugotowana kukurydza", "ugotowane kukurydze",
                                         "kukurydza", "kukurydze", "kuk"]},
            "Cooked Tomatoes": {"Hunger": 25, "Thirst": 50,
                                "Keywords": ["cooked tomatoes", "tomatoes", "tom", "ugotowany pomidor",
                                             "ugotowane pomidory", "pomidor", "pomidory", "pom"]},
            "Coconut": {"Hunger": 10, "Thirst": 50,
                        "Keywords": ["coconut", "coconuts", "coc", "coco", "kokos", "kokosy", "kokosów", "kok",
                                     "koko"]},
            "Cooked Potato": {"Hunger": 40, "Thirst": 0,
                              "Keywords": ["cooked potato", "gotowany ziemniak", "gotowane ziemniaki",
                                           "cooked potatoes"]},
        }

        slots_items = [None] * 10

        while slots:
            current_slot = slots[0]
            inp = input(f"Co masz w slocie {current_slot} (napisz `?` po więcej info)? ").strip()

            if inp.lower().strip() == "?":
                print("Musisz podać w formacie {num}x{item}, przykład: 5xStrawberry")
                print("Jako {num} ma być ilość tego itemu w TYLKO TYM SLOCIE")
                print("Jako {item} ma być jedzenie, `0` jeżeli pusto lub `custom`")
                print("Dostępne: Strawberry, Blueberry, Potato, Chips...")
                print("Do sprawdzenia wszystkich możliwych \"jedzeń\" wpisz `keywords`")
                continue

            elif inp.lower().strip() == "keywords":
                print("Wszystkie dostępne produkty spożywcze + ich keyword-y:\n")
                for fd in food.keys():
                    print(f"Jedzenie {fd} ma takie keywords-y: {food[fd]["Keywords"]}")
                print("\n")
                continue

            if "x" not in inp:
                if inp == "0":
                    slots_items[current_slot] = None
                    slots.pop(0)
                    continue
                print("Błąd: Brak znaku 'x' w nazwie (np. 5xPotato).")
                continue

            try:
                parts = inp.split('x', 1)
                it_count = int(parts[0])
                it_name = parts[1].strip()
            except (ValueError, IndexError):
                print("Błąd formatu. Użyj {liczba}x{nazwa}.")
                continue

            if it_name.lower() == "custom":
                print("Podałeś `custom`. Poproszę o kilka danych.")
                c_name = input("Podaj nazwę tego jedzenia: ")
                c_hunger = int(input("Głód (0-100): ") or 0)
                c_thirst = int(input("Pragnienie (0-100): ") or 0)

                it_stats = {"name": c_name, "hunger": min(c_hunger, 100), "thirst": min(c_thirst, 100), "stack": it_count,
                            "slot": slots[0]}

                print(f"Czyli: {it_stats['stack']}x {it_stats['name']} (H:{it_stats['hunger']}, T:{it_stats['thirst']})?")
                if input("T/N: ").lower() == "t":
                    slots_items[slots[0]] = it_stats
                    slots.pop(0)
                continue

            found_item = None
            food_prop = None

            # Szukanie w bazie
            if it_name.capitalize() in food:
                found_item = it_name.capitalize()
                food_prop = food[found_item].copy()
            else:
                for f_name, f_prop in food.items():
                    if it_name.lower() in f_prop["Keywords"]:
                        found_item = f_name
                        food_prop = f_prop.copy()
                        break

            if found_item is None:
                print("Nie wykryto itemu. Wpisz `?` lub użyj `{num}xcustom`.")
                continue

            if it_count > 20:
                print(f"Ostrzeżenie: {it_count} to chyba więcej niż max stack (chyba 20)!")
                if not prompt_yes_no("Kontynuować"):
                    continue

            slots_items[current_slot] = {
                "hunger": food_prop["Hunger"],
                "thirst": food_prop["Thirst"],
                "name": found_item,
                "stack": it_count,
                "slot": slots[0]
            }
            slots.pop(0)
            slots_items.pop(0)
    else:
        has_bottle = True
        print("Ponieważ masz tryb 1, 2 lub 3, MUSISZ mieć butelkę i patrzeć się na Rain Collector.")
        while True:
            odp = input("Podaj slot butelki: ")
            if odp.isdigit():
                bottle_slot = int(odp)
                if 1 <= bottle_slot <= 9:
                    break
            print("Błąd: Podaj liczbę od 1 do 9.", end="\nPowtórz jeszcze raz. ")

        while True:
            print("Pominięto ustawianie slotów jedzenia (będzie mniej pytań).")
            food_slots = [int() for _ in input("Podaj sloty jedzenia oddzielone przecinkami (np. 2,3,5): ").strip().split(", ")]
            medicine_slots = [int(_) for _ in input("Podaj sloty medykamentów (tabletek `Medications`) oddzielone przecinkami (np. 4,6): ").strip().split(", ")]

            slots_items = [food_slots, medicine_slots]
            for i in range(1, 10):
                fs = i in food_slots
                ms = i in medicine_slots
                bs = i == bottle_slot
                if fs and ms or fs and bs or ms and bs:
                    print(f"\nBłąd: Slot {i} jest przypisany do więcej niż jednej kategorii (jedzenie/medykamenty/butelka) (podaj sloty jeszcze raz).")
                    continue
            break


    return has_bottle, bottle_slot, slots_items


# Uruchomienie sprawdzania przed startem
def main_config(spth, _mode):
    global savepath, mode

    savepath = spth
    mode = _mode

    print("Wybrano język polski bo mi się nie chciało pisać innych bo po co (:")
    print("Tryb (o jak dużo mam się pytać, 1 to najmniej 4 to najwięcej):", mode)
    curr_os = system()
    print(f"System: {curr_os}, ", end='')

    # Wspólne pakiety dla wszystkich systemów
    required_packages = [
        "psutil",  # Do zarządzania procesami (kill)
        "mss",  # Do szybkich screenshotów
        "pyautogui",  # Do kontroli myszy i klawiatury (Windows/Linux)
        "pillow",  # Do obróbki obrazów (PIL)
        "pytesseract",  # Wrapper do Tesseract OCR
        "opencv-python-headless",  # Do zaawansowanej obróbki obrazu (bez GUI)
        "numpy"  # Operacje numeryczne na obrazach (dla OpenCV)
    ]
    # Dodatkowe pakiety TYLKO dla Windows
    if system() == "Windows":
        required_packages += ["pygetwindow", "pywin32"]

    print("Wszystkie wymagane biblioteki: ", required_packages,
          ", potrzebujesz jeszcze " if system() == "Linux" else "",
          "ydotool (bo wayland), " if system() == "Linux" and os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland" else "xdotool (bo x11), ",
          "python3-th, python3-dev oraz (opcjonalnie) wmctrl ponieważ masz linuxa (a na windowsie byłoby potrzebne jeszcze pygetwindow i pywin32)" if system() == "Linux" else "")
    system_check()

    print(
        "Notatka: po pierwszym uruchomieniu programu stworzy on plik .theapocalypsedefaultcatalog. Jeżeli to Ci przeszkadza zatrzymaj program i nie uruchamiaj go. (:")
    print(
        "Inna notatka: zalecam na robienie jednocześnie nagrania ekranu, co w przypadku ewentualnego błędu ułatwi mi jego odnalezienie")

    print_status()  # [2/5]
    install_dependencies()
    print_status()  # [3/5]
    check_linux_setup()
    print_status()  # [4/5]
    tesseract_config(path=savepath)
    print_status()  # [5/5]
    hb, bs, si = slots_config()
    print_status()

    savepath = os.path.abspath(savepath)
    return hb, bs, savepath, si


# This is end of orginal config python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!