# V1NNYX Mod (Fabric, Minecraft 1.21.11)

Rein clientseitige Mod. Funktioniert auf JEDEM Server (der Server braucht nichts
installiert). Toetest du einen Spieler, wird zufaellig ein Song aus deiner
Liste abgespielt (am besten nur der Refrain, 10-20 Sekunden).

## Teil 1: Mod bauen (einmalig)

Voraussetzungen: JDK 21, Gradle 9.2+ (oder IntelliJ IDEA, das Gradle selbst mitbringt).

    gradle build          (im Ordner V1NNYX-Mod)

Die fertige Datei liegt dann in  build/libs/v1nnyx-mod-1.0.0.jar
(NICHT die "-sources.jar"). Kopiere sie in  .minecraft/mods/

Du brauchst ausserdem (wie bei jeder Fabric-Mod):
  - Fabric Loader 0.18.x fuer 1.21.11
  - Fabric API fuer 1.21.11

## Teil 2: Deine Songs einbinden

Die Mod enthaelt nur einen kurzen Platzhalter-Sound. Eigene Songs:

  1. Audiodateien in  tools/songs_input/  legen
  2. In  tools/songs_input/songs.txt  eintragen:   datei.mp3 ; start ; dauer
  3. python tools/make_songs_pack.py   (braucht Python + ffmpeg)
  4. V1NNYX_Songs.zip nach .minecraft/resourcepacks/ kopieren,
     in Minecraft aktivieren und ganz nach oben schieben.

## Wie wird ein Kill erkannt?

Ueber die Todesnachricht des Servers (death.attack.player, death.attack.arrow ...):
Du bist der Killer und das Opfer steht in der Spielerliste (also ein Spieler,
kein Mob). Server mit eigenem Nachrichtenformat (Plugins, die Todesnachrichten
umbauen oder ausblenden) werden nicht erkannt.

## Test

  /playsound v1nnyx:kill_song master @s
