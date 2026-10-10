"""HRV guides (EN/HU/DE)."""
from article_kit import keys, shot, pull
from article_figs import hrv_band

HRV_KEYS = {
    "en": [("32–93 ms", "range of average SDNN across 44 studies of healthy adults", "Nunan et al. 2010"),
           ("~29%", "average gap between Apple Watch HRV and a chest strap", "O'Grady et al. 2024"),
           ("7 days", "of your readings before Aera calls anything typical or low", "Aera")],
    "hu": [("32–93 ms", "az SDNN átlaga 44 vizsgálatban, egészséges felnőtteknél", "Nunan és mtsai, 2010"),
           ("~29%", "ennyivel tér el átlagosan az Apple Watch HRV-je a mellkaspántos méréstől", "O'Grady és mtsai, 2024"),
           ("7 nap", "ennyi mérés kell, mielőtt az Aera bármit tipikusnak vagy alacsonynak nevez", "Aera")],
    "de": [("32–93 ms", "Spanne der mittleren SDNN in 44 Studien mit gesunden Erwachsenen", "Nunan et al. 2010"),
           ("~29 %", "mittlere Abweichung der Apple-Watch-HRV vom Brustgurt", "O'Grady et al. 2024"),
           ("7 Tage", "deiner Messungen, bevor Aera etwas typisch oder niedrig nennt", "Aera")],
}
HRV_SHOT = {
    "en": ("Aera's HRV and resting heart rate tiles, each marked Typical against the person's own usual range", "HRV in Aera", "Each tile holds last night against your own usual range from the last two weeks, and says Typical, Below your usual or Notably low. No population scale."),
    "hu": ("Az Aera HRV- és Nyugalmi pulzus csempéje, mindkettőn Tipikus jelzés a saját megszokott tartományhoz képest", "HRV az Aerában", "A csempe a múlt éjszakát ahhoz méri, ami nálad az elmúlt két hétben megszokott volt, és ennyit ír: Tipikus, A szokásos alatt vagy Jóval alacsonyabb. Népességi skála nincs."),
    "de": ("Die Kacheln HRV und Ruheherzfrequenz in Aera, beide Typisch gemessen am eigenen üblichen Bereich", "HRV in Aera", "Jede Kachel misst die letzte Nacht an deinem üblichen Bereich der letzten zwei Wochen: Typisch, Niedriger als üblich oder Auffällig niedrig. Keine Bevölkerungsskala."),
}
HRV_PULL = {
    "en": "Two healthy 40-year-olds can sit 40 ms apart and both be fine.",
    "hu": "Két egészséges negyvenéves HRV-je között is lehet 40 ms különbség, és mindketten rendben vannak.",
    "de": "Zwei gesunde 40-Jährige können 40 ms auseinanderliegen, und beiden geht es gut.",
}

# file: (lang, [(anchor_regex, position 'after'|'before', block_name, html)])
ARTICLES = {}
for lang, fn, trend_h2, aera_h2 in [
    ("en", "apple-watch-hrv-normal-range.html", "Read the trend, not the morning", "How Aera does this"),
    ("hu", "apple-watch-hrv-ertek.html", None, None),
    ("de", "apple-watch-hrv-normalwert.html", None, None),
]:
    ARTICLES[fn] = (lang, [
        ("lead", "keys", keys(HRV_KEYS[lang])),
        ("h2:2", "pull", pull(HRV_PULL[lang])),
        ("h2:4", "fig", hrv_band(lang)),
        ("aera", "shot", shot("hrv-tiles", *HRV_SHOT[lang])),
    ])
