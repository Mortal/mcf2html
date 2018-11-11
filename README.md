mcf2html
========

Python script to view CEWE's "My Cewe Fotobook" (MCF) format as HTML.

Tested on a CEWE A4 book.

The script `mcf2json.py` reads an MCF file and outputs a JSON fragment
which must be inserted in the bottom of `view.html`.

Many features are unsupported, including:

* Backgrounds
* Borders
* Images rotated inside the CEWE fotobook program
* Text

Basically, only plain unrotated images are supported.

Open `view.html` in a modern web browser and use left and right arrow
to switch pages.

License
-------

SPDX-License-Identifier: GPL-2.0-or-later
