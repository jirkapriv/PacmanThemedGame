# Uživatelská dokumentace

Program je implementací klasické hry PacMan.
Hra je rozdělena do levelů s rostoucí obtížností na jedné mapě.
Hráč ovládá postavičku, která sbírá jídlo (bílé body), zatímco 4 nepřátelé se ji snaží eliminovat.
Cílem je dosáhnout levelu 4 a poté už jen nasbírat co nejvyšší skore...

## Program se spustí příkazem:
python main.py

## Ovládání
Hráč se ovládá šipkami na klávesnici.
Pohyb je bufferovaný, pokud není vybraný směr momentálně možný, program si ho pamatuje a provede ho, jakmile bude možný pokud ho hráč nezmění.
Nasbírání všech bodů zvyšuje úroveň a obtížnost.

## Powerupy
Na mapě jsou 4 větší kolečka.
Po jejich sebrání získává hráč čas, kdy ho nepřátelé nevidí a nemohou ho eliminovat ani pronásledovat.
Timer nahoře ukazuje délku efektu.

## Nepřátelé
Nepřátelé pronásledují hráče, pokud je v dosahu (vision_tiles).
Pokud se nepřítel dotkne hráče a efekt neviditelnosti není aktivní, hra končí a hráč musí začít od začátku.

## Požadavky
Nainstalovaný Python
Balíčky: pygame, pytmx

Balíčky lze nainstalovat příkazem:
pip install pygame pytmx