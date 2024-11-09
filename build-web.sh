#!/bin/bash
if [ -d web ]; then rm -r web; fi

mkdir web
cp game.py retro-pixel-cute-mono.bdf assets.* main_screen.png web
cd web

# Generamos el ejecutable
pyxel package . game.py
pyxel app2html web.pyxapp
mv web.html index.html
zip web.zip index.html retro-pixel-cute-mono.bdf
mv web.zip ../dist
cp index.html retro-pixel-cute-mono.bdf ../docs