# This is start of orginal mainbot python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!
# VERSION 1.1.0
# SNAPSHOT: None

from pathlib import Path
import interaction
from typing import Dict
from time import sleep
from PIL import Image
import pytesseract
import numpy as np
import shutil
import cv2
import os


maxscreenshots = 10_000
si = [None] * 9
savepath = "."
bottle_slot = 0
has_bottle = None
mode = NotImplemented
experimental = False

def health_check_func():
    path = interaction.take_screenshot("notexistingfileihavehope.png")
    os.rename(os.path.abspath(path) if not os.path.isabs(path) else path,
              os.path.join(savepath, "nieruszajmnie", "newest_health_check.png"))

    result = interaction._find_template(os.path.join(savepath, "nieruszajmnie", "newest_health_check.png"),
                           os.path.join(savepath, "nieruszajmnie", "health_bar.png"))

    errtimes = 0
    while result is None:
        if errtimes > 5:
            interaction.kill_roblox_or_sober()
            raise RuntimeError("Nie znaleziono health bar-a po raz 5.")

        print(f"BŁĄD: Nie wykryto pełnego paska HP (po raz {errtimes}), próbuję ponownie")
        errtimes += 1
        path = interaction.take_screenshot("notexistingfileihavehope.png")
        os.rename(os.path.abspath(path) if not os.path.isabs(path) else path,
                  os.path.join(savepath, "nieruszajmnie", "newest_health_check.png"))

        result = interaction.find_template(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"),
                               os.path.join(savepath, "nieruszajmnie", "health_bar.png"))


def move_back(indir: str, filename: str, ext: str = ".txt", last: str = "last", mx: int = maxscreenshots) -> None:
    """
    Funkcja przenosi pliki z podanej ścieżki wstecz, zaczynając od ostatniego pliku.
    Jeżeli plik o danym indeksie już istnieje, to jest przenoszony do kolejnego indeksu.
    Ostatecznie, ostatni plik jest przenoszony na indeks 1.

    :param indir: ścieżka do folderu zawierającego pliki
    :param filename: nazwa plików
    :param ext: rozszerzenie plików
    :param last: nazwa pliku o indeksie 0
    :param mx: maksymalny indeks pliku
    :return: Nic
    """
    for scr in range(mx, -1, -1):
        if os.path.exists(os.path.join(savepath, indir, f"{filename}_{scr}{ext}" if scr > 0 else f"{last}{ext}")):
            if scr == mx:
                os.remove(os.path.join(savepath, indir, f"{filename}_{scr}{ext}"))
                continue

            elif scr > 0:
                os.rename(os.path.join(savepath, indir, f"{filename}_{scr}{ext}"),
                          os.path.join(savepath, indir, f"{filename}_{scr + 1}{ext}"))

            elif scr == 0:
                os.rename(os.path.join(savepath, indir, f"{last}{ext}"),
                          os.path.join(savepath, indir, f"{filename}_1{ext}"))



def get_stats():
    path = interaction.take_screenshot("notexistingfileihavehope.png")
    os.rename(os.path.abspath(path) if not os.path.isabs(path) else path,
              os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"))

    move_back("screenshots", "screenshot", ".png")

    shutil.copy(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"),
                os.path.join(savepath, "screenshots", "last.png"))


    result, cropped = interaction.check_roblox_stats(savepath=Path(savepath), screenshot_path=Path(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png")))
    # result = interaction.find_template(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"),
    #                        os.path.join(savepath, "nieruszajmnie", "health_bar.png"))

    errtimes = 0
    while result is None:
        print(f"BŁĄD: Nie wykryto pełnego paska HP (po raz {errtimes}), próbuję ponownie")
        errtimes += 1
        path = interaction.take_screenshot("notexistingfileihavehope.png")
        os.rename(os.path.abspath(path) if not os.path.isabs(path) else path,
                  os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"))

        shutil.copy(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"),
                    os.path.join(savepath, "screenshots", "last.png"))

        result, cropped = interaction.check_roblox_stats(savepath=Path(savepath), screenshot_path=Path(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png")))

        if errtimes > 5:
            raise RuntimeError("Nie znaleziono health bar-a po raz 5.")

    cropped.save(os.path.join(savepath, "nieruszajmnie", "newest_cropped_screenshot.png"))

    move_back("croppedscreenshots", "screenshot", ".png")

    shutil.copy(os.path.join(savepath, "nieruszajmnie", "newest_screenshot.png"),
                os.path.join(savepath, "croppedscreenshots", "last.png"))
    return interaction.check_roblox_stats(os.path.join(savepath, "croppedscreenshots", "last.png"), savepath)


def find_toeat(hunger, thirst, has_bottle) -> Dict | int:
    """
    Wyszukuje jedzenia, które można zjeść z najmniejszą możliwą stratą.

    :return: Dict -> element listy si, None -> brak jedzenia do zjedzenia bez strat
    """

    #:param si: Lista jedzeń   # noqa

    for slot in si:
        if slot is None or slot["stack"] == 0:
            continue

        if slot["hunger"] + hunger <= 101 and slot["thirst"] + thirst <= 101:
            return slot

        if has_bottle and slot["hunger"] + hunger <= 101:
            return slot

    looses = []
    for slot in si:
        if slot is None or slot["stack"] == 0:
            continue

        if not has_bottle:
            looses.append((100 - slot["hunger"], slot["slot"], 100 - slot["thirst"], slot))
        else:
            looses.append((100 - slot["thirst"], 100 - slot["hunger"], slot["slot"], slot))

    if looses:
        looses.sort()
        return looses[0][3]

    for slot in si:
        if slot is None or slot["stack"] == 0:
            continue

        if not (slot["hunger"] == 100 and hunger <= 5):
            continue

        if (not (slot["thirst"] == 100 and hunger <= 5)) and not has_bottle:
            continue

        return slot


def normal_mode_eat(stats=None):
    global si

    if stats is None:
        get_stats()

    old_hp = None
    old_food = None
    old_drink = None

    if stats[0][0] < stats[0][1]:  # health
        print(f"NIE MAM FULL HP, używam medicine (slot {si[1][0]}) i sprawdzam jedzenie i napicie.")
        interaction.use_slot(si[1][0])
        old_hp = stats[0][0]

    if stats[1][0] < 15:  # hunger
        print(f"Jem (slot {si[0][0]}).")
        interaction.use_slot(si[0][0])
        old_food = stats[1][0]

    if stats[2][0] < 50:  # thirst
        print(f"Piję wodę (slot {bottle_slot} x2 kliknięcie, przerwa 7s.).")
        interaction.use_slot(bottle_slot)
        sleep(7.5)
        interaction.use_slot(bottle_slot)
        old_drink = stats[2][0]

    if old_hp is not None or old_food is not None or old_drink is not None:
        print("Użyłem jakiegoś jedzenia/leku, sprawdzam czy się zmieniło czy slot się skończył.")
        stats_after = get_stats()
        if old_hp is not None:
            print("Zjadłem leki, sprawdzam czy zadziałały.")
            if stats_after[0][0] <= old_hp:
                print("Leki nie zadziałały, prawdopodobnie skończył się slot, usuwam go z listy.")
                if len(si[1]) > 0:
                    print(f"Usunąłem slot {si[1].pop(0)} z listy slotów z lekami. Próbuję ponownie.")
                    normal_mode_eat()
                else:
                    si[1] = None
                    print("Skończyły się wszystkie leki!")
        else:
            print("Zadziałały!")

        if old_food is not None:
            print("Zjadłem jedzenie, sprawdzam czy zadziałało.")
            if stats_after[1][0] <= old_food:
                print("Jedzenie nie zadziałało, prawdopodobnie skończył się slot, usuwam go z listy.")
                if len(si[0]) > 0:
                    print(f"Usunąłem slot {si[0].pop(0)} z listy slotów z jedzeniem.")
                    normal_mode_eat()
                else:
                    si[1] = None
                    print("Skończyło się całe jedzenie!")

        if old_drink is not None:
            print("Piłem, sprawdzam, czy na pewno myszka była dobrze ustawiona i napiłem się.")
            if stats_after[2][0] <= old_drink:
                print("Butelka nie zadziałała. Kończę program, bo to dziwne (nie powinno się zdarzyć).")
                interaction.kill_roblox_or_sober()
            else:
                print("Zadziałało!")


def mainbot(_has_bottle, _savepath, mxs, _si, _mode, _bottle_slot = 0, _experimental = False):
    """
    Główna funkcja bota.

    :param _has_bottle: Informacja o posiadaniu butelki
    :param _savepath: Ścieżka do folderu z konfiguracją
    :param mxs: Maksymalna ilość zrzutów ekranu
    :param _si: Lista jedzeń
    :param _bottle_slot: Slot butelki, 0 (default) jeżeli nie ma jej użytkownik
    """
    global maxscreenshots, si, savepath, bottle_slot, has_bottle, mode, experimental
    savepath = _savepath
    si = _si
    bottle_slot = _bottle_slot
    has_bottle = _has_bottle
    mode = _mode
    experimental = _experimental

    maxscreenshots = mxs
    to_next_screenshot = 0
    health_check = 0

    print("Następny screenshot za | Następny Health-check za\n\n            00:00            00:00", end='')

    while True:
        print(f"\033[22D{to_next_screenshot // 60}:{to_next_screenshot % 60}            {health_check // 60}:{health_check % 60}")

        # Zmniejszanie liczniku, jeżeli > 0
        if to_next_screenshot > 0:
            if health_check > 0:
                health_check -= 1
            else:
                print("Health check (robię screena i szukam na nim pełnego paska HP).")
                health_check_func()
                health_check = 10
                print(f"Następny screenshot za | Następny Health-check za\n\n            {to_next_screenshot // 60}:{to_next_screenshot % 60}            {health_check // 60}:{health_check % 60}")

            to_next_screenshot -= 1
            sleep(1)
            continue

        # Znajdywanie itemu
        stats = get_stats()

        if len(si) != 2:
            toeat = find_toeat(stats[1][0], stats[2][0])

            # Jedzenie jedzenia
            if toeat is not None:
                print(f"Jem {toeat["name"]} (slot: {toeat["slot"]}, fulldebug: {toeat=})")
                interaction.use_slot(toeat["slot"])
                continue
        else:
            # Zwykły tryb
            normal_mode_eat(stats)


        # Sprawdzanie, na jak długo najlepiej ustawić timer-a
        hunger, thirst = 100 - stats[1][0], 100 - stats[2][0]

        # Jeżeli mam butelkę, mogę prawie za darmo z-refill-ować wodę
        if has_bottle and thirst > 50:
            interaction.use_slot(bottle_slot)
            sleep(3)
            interaction.use_slot(bottle_slot)
            stats = get_stats()
            hunger, thirst = 100 - stats[1][0], 100 - stats[2][0]

        to_next_screenshot = min(thirst * 12, hunger * 20) - 30  # 1 thirst ~ 12 sec. 1 hunger ~ 20 sec. - 30 działanie programu (milisekundy) + ewentualny błąd w moich zapiskach

        print(
            f"Następny screenshot za | Następny Health-check za\n\n            {to_next_screenshot // 60}:{to_next_screenshot % 60}            {health_check // 60}:{health_check % 60}")


# This is end of orginal mainbot python file of TheApocalypse aJs_to_ja's Bot, this comment is REQUIRED to run program bcz of checking in main.py in line ~250. DO NOT REMOVE IT 4 SAFETY!