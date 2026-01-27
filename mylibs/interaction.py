# This is start of orginal interaction python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!
# VERSION 1.1.0
# SNAPSHOT: None


import os
from platform import system
from typing import Union, Optional, Tuple
import subprocess
import shutil
import re
from pathlib import Path
import cv2
from PIL import Image
import pytesseract


machine_type = system() if system() != "Linux" else os.environ.get("XDG_SESSION_TYPE")


def select_roblox(game_name: str | None = None) -> bool | None:
    """
    Aktywuje okno gry (Roblox/Sober) i minimalizuje konsolę, by nie przeszkadzała.

    :param game_name: Nazwa okna do znalezienia ("Roblox" na Windows, "Sober" na Linux). Jeżeli None próbuje wykryć po systemie (Windows/Linux)
    :returns Zwraca to, czy się udało zaznaczyć okno, jeżeli None oznacza iż nie wiem (:
    """

    if game_name is None:
        game_name = "Roblox" if machine_type == "Windows" else "Sober"
    print(f"Próbuję aktywować: {game_name}...")

    # --- WINDOWS ---
    if system() == "Windows":
        try:
            import pygetwindow as gw
            import win32gui
            import win32con

            # 1. Znajdź i aktywuj okno gry
            windows = gw.getWindowsWithTitle(game_name)
            if not windows:
                print(f"Nie znaleziono okna '{game_name}'")
                return False

            game_win = windows[0]
            if game_win.isMinimized:
                game_win.restore()

            # Ustaw "Always on Top" - kluczowe, żeby klikać w grę
            hwnd = game_win._hWnd
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
            win32gui.SetForegroundWindow(hwnd)

            # 2. Zmniejsz i przesuń NASZĄ konsolę (żeby nie zasłaniała)
            # Pobierz handle konsoli
            console_hwnd = win32gui.GetForegroundWindow()  # To powinno być nasze okno przed przełączeniem

            # Ustawienia konsoli: lewy górny róg, mały rozmiar
            # x=10, y=10, szer=400, wys=300
            win32gui.SetWindowPos(console_hwnd, win32con.HWND_NOTOPMOST,
                                  10, 10, 400, 300,
                                  win32con.SWP_SHOWWINDOW)

            print(f"Aktywowano {game_name}, konsola przesunięta.")
            return True

        except Exception as e:
            print(f"[BŁĄD Windows] {e}")
            return False

    # --- LINUX ---
    else:
        # Sprawdzamy czy mamy wmctrl (najlepsze narzędzie do tego)
        if not shutil.which("wmctrl"):
            print("Ostrzeżenie: brak wmctrl. Zainstaluj: sudo apt install wmctrl aby korzystać z dodatkowych funkcji (zaznaczanie Sober-a) lub zignoruj to ostrzeżenie i samemu zaznacz roblox-a")
            return False

        try:
            # -a aktywuje okno po nazwie
            # To działa lepiej niż xdotool, bo podnosi okno z innego workspace'u
            result = subprocess.run(
                ["wmctrl", "-a", game_name],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"✅ Aktywowano {game_name} (przez wmctrl).")
                return True
            else:
                print(f"❌ wmctrl nie znalazł okna '{game_name}'.")
                return False
        except Exception as e:
            print(f"[BŁĄD Linux] {e}")
            return False

def use_slot(number: int) -> None:
    """
    Zaznacza podany slot poprzez zaznaczenie/odznaczenie (jeżeli był aktywny) slotu 1 potem zaznaczenie i odznaczenie slotu 2 i na końcu zaznaczenie podanego slotu

    :param number: Slot do zaznaczenia
    """
    if not (1 <= number <= 9):
        raise ValueError("Liczba musi być w zakresie 1‑9!")

    _type_number(1)
    _type_number(2)
    _type_number(2)
    _type_number(number)
    _left_click()

def _left_click() -> None:
    """
    Kliknięcie lewym przyciskiem myszy w aktualnej pozycji kursora.
    Działa na: Windows / X11 / Wayland.
    """
    import subprocess
    import pyautogui
    import time
    if machine_type == "Windows":
        pyautogui.click()

    elif machine_type == "X11":
        subprocess.run(["xdotool" if shutil.which("xdotool") else "ydotool", "click", "1"], check=True)

    elif machine_type == "Wayland":
        subprocess.run(["ydotool", "click", "1"], check=True)

    time.sleep(0.15)  # krótka stabilizacja

def _type_number(number: int) -> None:
    """
    Wpisz liczbę od 1 do 9.
    :param number: liczba w zakresie 1‑9
    """
    import subprocess
    import pyautogui
    import time
    if not (1 <= int(number) <= 9):
        raise ValueError("Liczba musi być w zakresie 1‑9!")

    num_str = str(int(number))

    if machine_type == "Windows":
        pyautogui.typewrite(num_str)

    elif machine_type == "X11":
        subprocess.run(["xdotool", "type", num_str], check=True)

    elif machine_type == "Wayland":
        subprocess.run(["ydotool", "type", num_str], check=True)

    time.sleep(0.1)

def take_screenshot(filename: str = "screenshot.png") -> Path:
    """
    Robi screenshot całego ekranu i zapisuje go.
    :param filename: Nazwa pliku (domyślnie: screenshot.png)
    :return: Path do zapisanego pliku
    """
    from pathlib import Path
    import mss.tools
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # główny monitor
        sct_img = sct.grab(monitor)

        output_path = Path(filename).resolve()
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output_path)

    return output_path

def kill_roblox_or_sober() -> None:
    """
    Zabija proces Roblox-a.
    """
    print("Zabijam roblox-a....")
    import psutil

    target = "Roblox" if machine_type == "Windows" else "Sober"
    killed = False

    if machine_type == "Windows":
        for proc in psutil.process_iter(['name']):
            proc_name = proc.info['name'].lower()

            if target.lower() in proc_name:
                try:
                    proc.kill()
                    print(f"Zabito proces: {proc.info['name']}")
                    killed = True
                except psutil.AccessDenied:
                    print(f"Brak uprawnień do zabicia: {proc.info['name']}")
                except Exception as e:
                    print(f"Błąd: {e}")

        if not killed:
            print(f"Nie znaleziono procesu: {target}")

    else:
        subprocess.run("flatpak kill org.vinegarhq.Sober", shell=True)

def _ocr_image(image: Image.Image | Path, lang: str = "eng") -> str:
    """
    Wykonuje OCR na obrazku.

    :param image: Obiekt Image lub ścieżka do pliku
    :param lang: Język OCR (domyślnie: eng)
    :return: rozpoznany tekst
    """
    if isinstance(image, Path):
        image = Image.open(image)

    # Preprocessing dla lepszego OCR
    # Konwersja do skali szarości + zwiększenie kontrastu
    image = image.convert("L")

    text = pytesseract.image_to_string(image, lang=lang, config="--psm 6")
    return text.strip()

def _parse_stats(text: str) -> list[tuple[int, int]] | None:
    """
    Parsuje tekst, szukając wzorca "XX/YY".

    Oczekiwany format:
        100/100
        XX/100
        XX/100

    :param text: tekst z OCR
    :return: lista [(wartość, max), ...] lub None jeśli błędny format
    """
    # Wzorzec: liczba / liczba (z opcjonalnymi spacjami)
    pattern = r'(\d+)\s*/\s*(\d+)'
    matches = re.findall(pattern, text)

    if not matches:
        return None

    result: list[tuple[int, int]] = []
    for val, max_val in matches:
        result.append((int(val), int(max_val)))

    return result

def _find_template(
        image: str | Path,
        template_path: Union[str, Path],
        threshold: float = 0.8
) -> Optional[Tuple[int, int, int, int]]:
    """
    Wyszukuje wzorzec na parametrze, ignorując przezroczystość (kanał alpha).

    :param image: Zdjęcie, na którym mam wyszukać wzorca.
    :param template_path: Ścieżka do pliku PNG ze wzorcem (musi mieć kanał alpha).
    :param threshold: Próg pewności (0,8 = 80%).
    :return: Krotka (x, y, w, h) lub None, jeśli nie znaleziono.
    """
    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku wzorca: {template_path}")

    image = Path(image)
    if not image.exists():
        raise FileNotFoundError(f"Nie znaleziono pliku zdjęcia: {image}")
    image = cv2.imread(str(image), cv2.IMREAD_UNCHANGED)

    screen_gray = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)

    # 2. Wczytaj wzorzec
    template = cv2.imread(str(template_path), cv2.IMREAD_UNCHANGED)
    if template is None:
        return None

    # Sprawdź, czy ma kanał alpha
    if template.shape[2] != 4:
        print("[OSTRZEŻENIE] Wzorzec nie ma kanału alpha. Dopasowanie może być niedokładne.")
        # Tworzymy sztuczną maskę (wszystko nieprzezroczyste)
        mask = None
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    else:
        # Rozdzielamy kolory i alphę
        b, g, r, a = cv2.split(template)
        template_gray = cv2.cvtColor(template[..., :3], cv2.COLOR_BGR2GRAY)
        # Maska: tam, gdzie alpha > 0, tam szukamy
        _, mask = cv2.threshold(a, 1, 255, cv2.THRESH_BINARY)

    h, w = template_gray.shape

    # 3. Dopasowanie
    # TM_CCOEFF_NORMED jest najlepsze dla szablonów z maską
    res = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED, mask=mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        x, y = max_loc
        return tuple([x, y, w, h])

    return None


def check_roblox_stats(
        screenshot_path: Path | str,
        savepath: Path | str,
        health_bar_path: Path | str = "health_bar.png"
) -> Tuple[list[tuple[int, int]], Image.Image] | None:
    """
    Funkcja sprawdza zdrowie, najedzenie i napicie gracza na podstawie
    zrzutu ekranu. Zwraca listę trzech par (wartość, maksymalna wartość),
    które reprezentują zdrowie, najedzenie i napicie, oraz obraz zrzutu ekranu
    z obszaru pod health bar-em. Jeżeli nie uda się znaleźć health bar-a,
    funkcja zwraca wartość None.

    :param screenshot_path: Ścieżka do zrzutu ekranu
    :param savepath: Ścieżka do pliku health_bar.png
    :return: Lista trzech par (wartość, maksymalna wartość) i obraz lub None
    """
    if isinstance(screenshot_path, str):
        screenshot_path = Path(screenshot_path)
    if isinstance(savepath, str):
        savepath = Path(savepath)
    if isinstance(health_bar_path, str):
        health_bar_path = Path(health_bar_path)

    # 1. Przytnij obraz do obszaru poniżej health_bar-a
    pos = _find_template(
        image=screenshot_path,
        template_path=health_bar_path,
    )

    if not pos:
        print("Nie znaleziono paska zdrowia, zwracam None")
        return None


    # 3. OCR
    img = Image.open(screenshot_path)
    mp = list(map(int, pos))
    cropped = img.crop((0, mp[1], mp[0] + mp[2], img.size[1]))
    text = _ocr_image(cropped)
    print(f"Wynik OCR:\n{text}")

    # 3. Parsuj statystyki
    stats = _parse_stats(text)

    # 4. Walidacja
    if stats is None or len(stats) != 3:
        return None

    return stats, cropped



# This is end of orginal interaction python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!