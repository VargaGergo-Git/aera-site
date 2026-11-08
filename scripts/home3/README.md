# The 3.4 home page

`python3 scripts/build_home.py` (or `build_home3.py` alone) writes index.html, hu.html and de.html.

- `page-en.html`: the approved page (site mock take 3, v12, 8 Nov 2026), English.
- `words.py`: every Hungarian and German line as an exact swap of the English one (`T`), plus `PICS`, the pictures with words in them. Change a line in `page-en.html` and the build stops until its row here matches.
- `loop_paths.json`: the runner's path on the route picture, per language.
- `head-<lang>.html`: title, description, social cards, canonical, hreflang, schema and the /#privacy redirect, kept from the earlier home.
- `faq-<lang>.html`: the questions; the FAQ schema in the head repeats them, so change both together.
- `frames_web.js`: renders the store strip's layers (`h/field.webp`, `h/store/{,hu/,de/}{t,d}NN.webp`). Run it in the project's store-picture folder (`mocks/store-3.4-dream-2026-11-06/src`) with `LAYER=field|text|dev`.

Pictures live in `h/`. Motion is time-based, plays in view and stops under reduced motion; nothing is tied to scrolling.
