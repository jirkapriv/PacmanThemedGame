# Programátorská dokumentace

Projekt je rozdělen do následující struktury, kde main.py je vstupní soubor.
Skripty jsou psány v Pythonu a struktura je navržena pomocí objektově orientovaného programování (OOP).

main.py
scripts
  config
    config.py
  entities
    enemies.py
    player.py
  game
    game.py
  map
    map.py
  state
    play_state.py
  
Po spuštění main.py se vytvoří instance hry (Game), která pracuje se stavy hry, zatím pouze Play_State.

Play_State pracuje s mapou a entitamy.
Některé třídy používají proměnné ze souboru config pro snadné změny vlastností hry.

Tento stav (Play_State) ještě se stavem Game_Over se mezi sebou přepínají. Program je strukturován takto pro snadnou rozšiřitelnost, například přidání menu nebo pauznutí.

## Mapa
Mapa je vytvořena pomocí programu Tiled.
Do Tiled se importují obrázky a mapa se z nich sestaví.
Každému "tajlu" je možné přiřadit vlastnosti, například "Collides" pro zdi.
Tiled vygeneruje pole čísel reprezentující různé typy obrázků.
Program může podle toho rozhodnout, zda hráč může projít.

## Pixel Art
Pixel art je kreslen v programu Aseprite.


Jednotlive funkce jsou popsany v kodu