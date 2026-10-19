# Stadtführer-App · Klick-Prototyp

Ein klickbarer Prototyp der Stadtführer-App. Er zeigt den Ablauf von der Begrüßung über das Profil und die Tourplanung bis zur Tour unterwegs und zum Tour-Tagebuch.

Zum Ausprobieren einfach die Seite öffnen. Am Handy läuft die App-Ansicht im Vollbild. Am Computer öffnet sich die Web-Ansicht, mit der man Touren am großen Bildschirm vorbereitet und aufs Handy schickt. Über „App-Ansicht“ oben rechts sieht man dort auch die App in einem Handy-Rahmen.

Orte, Texte und der App-Name sind Platzhalter.

## Was wo liegt

- `index.html`: der fertige Prototyp, den GitHub Pages anzeigt. Diese Datei wird gebaut, nicht von Hand geändert.
- `quellen/`: die Entwurfsdateien aus dem Design-Canvas. `Prototyp.dc.html` ist die App, `Web.dc.html` die Web-Ansicht, die übrigen Dateien sind die einzelnen Bildschirme und Farbwelten für die Doku.
- `werkzeuge/`: Skripte zum Bauen, für die Bilder der Doku und für den Klick-Test.

## Änderungen machen

Geändert wird in `quellen/`, danach wird `index.html` neu gebaut:

```
cd werkzeuge
npm install
python3 build_combined.py ../quellen/Prototyp.dc.html ../quellen/Web.dc.html "$PWD/node_modules/@fontsource" ../index.html
```

Bilder der einzelnen Bildschirme (braucht Playwright mit Chromium):

```
python3 render.py ../quellen "$PWD/node_modules/@fontsource" bilder
```

Klick-Test für App und Web-Ansicht:

```
python3 test_prototyp.py "$PWD/../index.html" testbilder web
```
