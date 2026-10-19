"""Build requests.html (feature request board) from support.html's head and footer."""
import pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "support.html").read_text()
head = src[: src.index('<div class="wrap page-head">')]
foot = src[src.index("<footer>"):]
head = head.replace("<title>Support · Aera</title>", "<title>Feature requests · Aera</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="Ask for a feature in Aera and vote for the ideas you want most. No account needed.">', head)
head = head.replace('href="https://aerahealth.app/support.html"', 'href="https://aerahealth.app/requests.html"')
head = head.replace(' aria-current="page">Support', '>Support')
body = (root / "scripts/requests_body.html").read_text()
(root / "requests.html").write_text(head + body + foot)
