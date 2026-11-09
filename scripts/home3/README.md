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
- `lines.py` also holds `STORE`: the alt text of the ten store pictures, in each store's own order. The build fills the carousel from it (`h/store/{,hu/,de/}lNN.webp`, the light store set at 600 x 1304).
- `frames_web.js` and the `h/store/{t,d}NN.webp` and `h/field.webp` layers belong to the old night-green strip. The page no longer uses them.

Pictures live in `h/`.

## Motion

The page plays like the film. Everything is time-based, plays once when it comes into view and is off under reduced motion. Nothing is pinned and nothing is tied to the scroll position.

- The kit is in `chrome.py`, so every page has it: `<head>` sets `html.mo` when motion is allowed; `.kin` headlines arrive word by word, `.rv` blocks rise in (`--d` delays one). If the page script fails, `mo` comes off after 3.5 s and everything shows. Inner pages get it on their page head and closing band without any markup. Pages cross-fade into each other, and the light and dark switch opens from the button.
- The hero phone plays `h/film.mp4`: the app's own replay of the Budapest run with the English words blurred out of the footage. The title and the four figures are drawn over it in the page's language from a table read off the recording (in `page-en.html`, the arrays `D`, `S`, `P`, `H`). `h/film.webp` is the last frame: the still before the film loads, under Save-Data and under reduced motion.
- Figures marked `.ct` count up. Body age starts at the calendar age and each ledger row takes its part off. Ledgers marked `.led.sq` build row by row.
- "A look inside" is a carousel of the store pictures (`.flow`). Without script it is a row you swipe.

## Words

- Slogan (headline): "Replay your run. Understand your body."
- Proof (always line two): "Every number explained. No guessing." HU "Minden számhoz jár magyarázat. Semmi találgatás." DE "Jede Zahl erklärt. Kein Rätselraten."
- Terms (beside a download button): "Free to start. No account."
- A feature is called what the app calls it in that language.
- Never "AI", hype, exclamation marks or em dashes.
