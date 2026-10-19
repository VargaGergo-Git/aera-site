"""Build roadmap.html from data/roadmap.json, reusing support.html's head and footer."""
import json, html, pathlib, re
root = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((root / "data/roadmap.json").read_text())
src = (root / "support.html").read_text()
head = src[: src.index('<div class="wrap page-head">')]
foot = src[src.index("<footer>"):]
head = head.replace("<title>Support · Aera</title>", "<title>Roadmap · Aera</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="What is being built in Aera now, what comes next, and how to ask for a feature.">', head)
head = head.replace("support.html\">", "roadmap.html\">", 1).replace(' aria-current="page">Support', '>Support')
def col(title, items):
    cards = "".join(f'<div class="card"><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></div>' for t, p in items)
    return f'<h2>{title}</h2><div class="rm-list">{cards}</div>'
body = f'''<style>
.rm-list{{display:grid;gap:12px;margin:12px 0 28px}}
@media (min-width:760px){{.rm-list{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
.rm-form{{display:grid;gap:10px;max-width:560px}}
.rm-form textarea,.rm-form input{{font:inherit;font-size:16px;padding:12px 14px;border-radius:12px;border:1px solid color-mix(in srgb,currentColor 22%,transparent);background:transparent;color:inherit}}
.rm-form textarea{{min-height:120px;resize:vertical}}
.rm-form button{{justify-self:start;min-height:44px;padding:0 22px;border:0;border-radius:999px;background:#1d1d1f;color:#fff;font:inherit;font-weight:600;cursor:pointer}}
@media (prefers-color-scheme:dark){{.rm-form button{{background:#f5f5f7;color:#000}}}}
</style>
<div class="wrap page-head">
  <p class="eyebrow">Aera</p>
  <h1>Roadmap</h1>
</div>
<div class="wrap legal">
  <p>What is being built, what comes next, and what is further out. Only planned work is listed here.</p>
  {col("Now", d["now"])}
  {col("Next", d["next"])}
  {col("Later", d["later"])}
  <h2 id="request">Ask for a feature</h2>
  <p>Tell us what you would like Aera to do. No account needed. Every request is read by a person.</p>
  <form class="rm-form" id="rmf">
    <textarea name="idea" required placeholder="What would you like Aera to do, and why?"></textarea>
    <input name="email" type="email" placeholder="Email, if you want a reply (optional)">
    <button type="submit">Send request</button>
  </form>
  <p class="meta">Last updated: {d["updated"]}</p>
</div>
<script>
document.getElementById("rmf").addEventListener("submit",function(e){{e.preventDefault();var f=e.target;
location.href="mailto:9qdf7rnr7z@privaterelay.appleid.com?subject="+encodeURIComponent("Aera feature request")+"&body="+encodeURIComponent(f.idea.value+(f.email.value?"\\n\\nReply to: "+f.email.value:""));}});
</script>

'''
(root / "roadmap.html").write_text(head + body + foot)
