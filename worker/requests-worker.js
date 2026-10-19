// Feature requests API for aerahealth.app/requests.html. Cloudflare Worker + one KV namespace (REQ).
// No accounts: one vote per browser id per post, plus a per-IP daily post limit.
// Statuses are set by Gergő with the ADMIN_KEY secret: POST /status {id,status|hidden|title}.
// Anyone can add a detail under a request: POST /comment {id,text}.
const STATUSES = ["open", "review", "planned", "progress", "done"];
const ORIGIN = "https://aerahealth.app";
const cors = { "Access-Control-Allow-Origin": ORIGIN, "Access-Control-Allow-Methods": "GET,POST,OPTIONS", "Access-Control-Allow-Headers": "content-type,x-admin-key" };
const json = (d, s = 200) => new Response(JSON.stringify(d), { status: s, headers: { "content-type": "application/json", ...cors } });
const clean = (s, n) => String(s || "").replace(/[<>]/g, "").trim().slice(0, n);
async function all(env) { return JSON.parse((await env.REQ.get("posts")) || "[]"); }
async function save(env, p) { await env.REQ.put("posts", JSON.stringify(p)); }

export default {
  async fetch(req, env) {
    if (req.method === "OPTIONS") return new Response(null, { headers: cors });
    const url = new URL(req.url), ip = req.headers.get("cf-connecting-ip") || "x";
    if (req.method === "GET" && url.pathname === "/posts") {
      const p = await all(env);
      return json(p.filter(x => !x.hidden).map(({ id, title, details, votes, status, created, comments }) => ({ id, title, details, votes, status, created, comments: (comments || []).filter(c => !c.hidden).map(c => ({ text: c.text, at: c.at })) })));
    }
    if (req.method !== "POST") return json({ error: "not found" }, 404);
    const body = await req.json().catch(() => ({}));
    if (url.pathname === "/posts") {
      const day = new Date().toISOString().slice(0, 10), k = `rl:${ip}:${day}`;
      const n = +((await env.REQ.get(k)) || 0);
      if (n >= 5) return json({ error: "limit" }, 429);
      const title = clean(body.title, 120), details = clean(body.details, 2000), email = clean(body.email, 200);
      if (title.length < 4) return json({ error: "title" }, 400);
      const p = await all(env);
      const post = { id: crypto.randomUUID().slice(0, 8), title, details, votes: 1, status: "open", created: Date.now() };
      p.push(post); await save(env, p);
      if (email) await env.REQ.put(`email:${post.id}`, email);
      await env.REQ.put(k, String(n + 1), { expirationTtl: 90000 });
      if (body.voter) await env.REQ.put(`v:${post.id}:${clean(body.voter, 64)}`, "1");
      return json(post);
    }
    if (url.pathname === "/vote") {
      const id = clean(body.id, 16), voter = clean(body.voter, 64);
      if (!id || voter.length < 8) return json({ error: "bad" }, 400);
      const key = `v:${id}:${voter}`, had = await env.REQ.get(key);
      const p = await all(env), post = p.find(x => x.id === id);
      if (!post) return json({ error: "missing" }, 404);
      if (had) { await env.REQ.delete(key); post.votes = Math.max(0, post.votes - 1); }
      else { await env.REQ.put(key, "1"); post.votes++; }
      await save(env, p);
      return json({ id, votes: post.votes, voted: !had });
    }
    if (url.pathname === "/comment") {
      const day = new Date().toISOString().slice(0, 10), k = `rc:${ip}:${day}`;
      const n = +((await env.REQ.get(k)) || 0);
      if (n >= 20) return json({ error: "limit" }, 429);
      const id = clean(body.id, 16), text = clean(body.text, 600);
      if (text.length < 2) return json({ error: "text" }, 400);
      const p = await all(env), post = p.find(x => x.id === id);
      if (!post) return json({ error: "missing" }, 404);
      const c = { text, at: Date.now() };
      (post.comments = post.comments || []).push(c);
      await save(env, p);
      await env.REQ.put(k, String(n + 1), { expirationTtl: 90000 });
      return json(c);
    }
    if (url.pathname === "/status") {
      if (req.headers.get("x-admin-key") !== env.ADMIN_KEY) return json({ error: "no" }, 403);
      const p = await all(env), post = p.find(x => x.id === body.id);
      if (!post) return json({ error: "missing" }, 404);
      if (body.status && STATUSES.includes(body.status)) post.status = body.status;
      if ("hidden" in body) post.hidden = !!body.hidden;
      if (body.title) post.title = clean(body.title, 120);
      await save(env, p);
      return json(post);
    }
    return json({ error: "not found" }, 404);
  }
};
