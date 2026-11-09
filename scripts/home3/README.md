# The Aera site: one look, three languages

## The look (scripts/chrome.py)

One file holds the look every page shares: the colours and type, the header, the App Store badge, the closing band and the footer. In short:

- A warm white page, white panels, black type in one colour. One soft band of colour (peach to lavender, the Instagram poster's) behind the opening and the closing only.
- A panel says one thing: a small grey label, one big real figure, one sentence, then the real screen in a real iPhone. Where a number has working, the working is shown as a short ledger under it.
- Buttons are black pills. Links are black with a rule under them. Orange only where a route is drawn.
- Light and dark, with a switch in the footer.
- Never: dark green fields, glows on dark, uppercase labels, pills as decoration, a kicker over every headline.

## Building

```
python3 scripts/build_home.py        # index.html, hu.html, de.html (or build_home3.py alone)
python3 scripts/add_chrome.py        # every other page: the shared header, closing band, footer; refreshes styles.css
python3 scripts/add_beacon.py        # the visit counter on new pages
python3 scripts/add_campaign.py      # tags the App Store links per page (run after add_chrome.py)
```

`add_chrome.py` replaced `add_lang.py`. Run it after any generator that writes pages (`build_articles.py`, `build_guides_index.py`, `build_whats_new.py`, `build_requests.py`).

## The home page (this folder)

- `page-en.html`: the template. Text sits in `{{tokens}}`; the shared pieces come in at `<!--chrome:...-->` and `/*chrome:css*/`.
- `lines.py`: the words for the tokens, written per language for its own readers (not swapped line by line). Figures in the words match that language's screenshot.
- `words.py`: the kept widgets (the store strip, the card row, What's new, the footnotes) still carry English in the template; `T` swaps each fragment for Hungarian and German. Change one of those lines in `page-en.html` and the build stops until its row matches. `PICS` lists the pictures with words in them.
- `loop_paths.json`: the runner's path on the route picture, per language.
- `head-<lang>.html`: title, description, social cards, canonical, hreflang, schema and the /#privacy redirect.
- `faq-<lang>.html`: the questions; the FAQ schema in the head repeats them, so change both together.
- `frames_web.js`: renders the store strip's layers (`h/field.webp`, `h/store/{,hu/,de/}{t,d}NN.webp`). Run it in the project's store-picture folder with `LAYER=field|text|dev`.

Pictures live in `h/`. Motion is time-based, plays in view and stops under reduced motion; nothing is tied to scrolling.

## Words

- Slogan (headline): "Replay your run. Understand your body."
- Proof (always line two): "Every number explained. No guessing." HU "Minden számhoz jár magyarázat. Semmi találgatás." DE "Jede Zahl erklärt. Kein Rätselraten."
- Terms (beside a download button): "Free to start. No account."
- A feature is called what the app calls it in that language.
- Never "AI", hype, exclamation marks or em dashes.
