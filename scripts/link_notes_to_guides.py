#!/usr/bin/env python3
"""Add a 'Related guides' line above Sources on field notes that a guide expands on.

Idempotent: the line is marked with data-related-guides and replaced on each run.
Edit MAP and re-run after adding a guide.
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAP = {
    "what-is-hrv": [("apple-watch-hrv-normal-range", "Apple Watch HRV: what is normal, and why is mine low?")],
    "why-should-a-watch-compare-me-to-myself": [("apple-watch-hrv-normal-range", "Apple Watch HRV: what is normal, and why is mine low?")],
    "what-does-a-sleep-score-mean": [("what-is-a-good-sleep-score", "What is a good sleep score on Apple Watch?")],
    "how-much-sleep-you-actually-need": [("what-is-a-good-sleep-score", "What is a good sleep score on Apple Watch?")],
    "watch-sleep-stages-are-an-estimate": [("what-is-a-good-sleep-score", "What is a good sleep score on Apple Watch?"),
                                           ("apple-watch-sleep-and-training-without-a-subscription", "Apple Watch sleep and training, no subscription needed")],
    "what-is-sleep-debt": [("should-i-run-after-bad-sleep", "Should I run after a bad night's sleep?")],
    "what-does-a-readiness-score-mean": [("should-i-run-after-bad-sleep", "Should I run after a bad night's sleep?")],
    "how-long-will-this-route-take-me": [("plan-a-running-route", "How to plan a running route")],
    "what-is-zone-2-training": [("zone-2-heart-rate-running", "Zone 2 heart rate: find yours, run it with Apple Watch")],
    "what-are-heart-rate-zones": [("zone-2-heart-rate-running", "Zone 2 heart rate: find yours, run it with Apple Watch")],
    "why-is-my-resting-heart-rate-up": [("apple-watch-resting-heart-rate", "Apple Watch resting heart rate: what's normal for runners")],
    "what-is-sleeping-heart-rate": [("apple-watch-resting-heart-rate", "Apple Watch resting heart rate: what's normal for runners")],
    "what-is-vo2max-on-a-watch": [("apple-watch-vo2-max", "Apple Watch VO2 max: how accurate, what's good, how to raise it")],
}

def main():
    changed = 0
    for note, guides in MAP.items():
        p = ROOT / "notes" / f"{note}.html"
        if not p.exists():
            continue
        guides = [(g, t) for g, t in guides if (ROOT / "guides" / f"{g}.html").exists()]
        if not guides:
            continue
        s = p.read_text(encoding="utf-8")
        orig = s
        s = re.sub(r'\n[ ]*<p class="meta" data-related-guides>.*?</p>', "", s)
        links = " · ".join(f'<a href="../guides/{g}.html">{t}</a>' for g, t in guides)
        line = f'<p class="meta" data-related-guides>Related guide{"s" if len(guides) > 1 else ""}: {links}</p>\n'
        new, n = re.subn(r"(\n[ ]*<h2>Sources</h2>)", "\n  " + line.rstrip("\n") + r"\1", s, count=1)
        if n and new != orig:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"notes updated: {changed}")


if __name__ == "__main__":
    main()
