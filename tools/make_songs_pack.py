#!/usr/bin/env python3
"""
V1NNYX Songs-Pack-Generator
===========================
Schneidet aus deinen eigenen Audiodateien den Refrain heraus und baut
daraus ein Resource Pack (V1NNYX_Songs.zip), das die Kill-Songs der
V1NNYX Mod ersetzt.

Benutzung:
  1. Lege deine Audiodateien (mp3, ogg, wav, m4a ...) in  tools/songs_input/
  2. Trage sie in  tools/songs_input/songs.txt  ein, eine pro Zeile:
         dateiname.mp3 ; Start-Sekunde ; Dauer-Sekunden
     z.B.   mein_song.mp3 ; 62 ; 20
  3. Starte:  python make_songs_pack.py
  4. Kopiere V1NNYX_Songs.zip nach .minecraft/resourcepacks/ und aktiviere
     das Pack in Minecraft ganz OBEN in der Liste.

Benoetigt: Python 3 und ffmpeg (muss im PATH sein).
"""
import json, re, shutil, subprocess, sys, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT = HERE / "songs_input"
LIST = INPUT / "songs.txt"
OUT_ZIP = HERE / "V1NNYX_Songs.zip"
BUILD = HERE / "_build"


def main():
    if shutil.which("ffmpeg") is None:
        sys.exit("FEHLER: ffmpeg wurde nicht gefunden. Bitte installieren (https://ffmpeg.org).")
    if not LIST.exists():
        sys.exit(f"FEHLER: {LIST} fehlt.")

    if BUILD.exists():
        shutil.rmtree(BUILD)
    sounds_dir = BUILD / "assets" / "v1nnyx" / "sounds"
    sounds_dir.mkdir(parents=True)

    entries = []
    for n, raw in enumerate(LIST.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split(";")]
        if len(parts) != 3:
            sys.exit(f"Zeile {n}: Format ist  datei ; start ; dauer")
        fname, start, dur = parts
        src = INPUT / fname
        if not src.exists():
            sys.exit(f"Zeile {n}: Datei nicht gefunden: {src}")
        name = re.sub(r"[^a-z0-9_]", "_", src.stem.lower())
        out = sounds_dir / f"{name}.ogg"
        fade_start = max(float(dur) - 1.5, 0)
        cmd = [
            "ffmpeg", "-y", "-loglevel", "error",
            "-ss", str(float(start)), "-t", str(float(dur)), "-i", str(src),
            "-af", f"afade=t=out:st={fade_start}:d=1.5",
            "-c:a", "libvorbis", "-q:a", "5", str(out),
        ]
        subprocess.run(cmd, check=True)
        entries.append({"name": f"v1nnyx:{name}", "stream": True})
        print(f"OK  {fname}  ->  {name}.ogg  ({dur}s ab {start}s)")

    if not entries:
        sys.exit("Keine Songs in songs.txt gefunden.")

    (BUILD / "assets" / "v1nnyx" / "sounds.json").write_text(
        json.dumps({"kill_song": {"replace": True, "sounds": entries}}, indent=2),
        encoding="utf-8",
    )
    (BUILD / "pack.mcmeta").write_text(json.dumps({
        "pack": {
            "pack_format": 75,
            "supported_formats": [34, 999],
            "description": "V1NNYX Kill-Songs",
        }
    }, indent=2), encoding="utf-8")

    if OUT_ZIP.exists():
        OUT_ZIP.unlink()
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in BUILD.rglob("*"):
            if p.is_file():
                z.write(p, p.relative_to(BUILD).as_posix())
    shutil.rmtree(BUILD)
    print(f"\nFertig: {OUT_ZIP}\nNach .minecraft/resourcepacks/ kopieren und aktivieren.")


if __name__ == "__main__":
    main()
