/* The review page's only server code, run by Cloudflare.
   It remembers a fingerprint of every review the page has ever shown (a
   SHA-256 code made on the customer's phone from the review's words), so no
   two customers are ever shown the same review. No review text, names, phone
   details or anything personal reaches this code: just the 64-character code,
   stored with the time.
   Everything else (the page, logo, icons) is served as plain files from public/. */

const HEX64 = /^[0-9a-f]{64}$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/api/claim") return claim(request, env);
    return env.ASSETS.fetch(request);
  },
};

// POST {"hs": [1 to 5 fingerprints]} -> {"i": n}: the first fingerprint nobody
// has been shown yet (now taken for good), or -1 if every one was already used.
async function claim(request, env) {
  if (request.method !== "POST") return json({ error: "use POST" }, 405, { allow: "POST" });
  if (Number(request.headers.get("content-length") || 0) > 2000) return json({ error: "too big" }, 413);
  let body;
  try { body = await request.json(); } catch { return json({ error: "bad request" }, 400); }
  const hs = body && Array.isArray(body.hs) ? body.hs : [];
  if (!hs.length || hs.length > 5 || !hs.every((h) => typeof h === "string" && HEX64.test(h))) return json({ error: "bad request" }, 400);
  const now = Date.now();
  for (let i = 0; i < hs.length; i++) {
    // the primary key makes this all-or-nothing: only one customer can ever take a fingerprint
    const r = await env.DB.prepare("INSERT OR IGNORE INTO seen (h, at) VALUES (?1, ?2)").bind(hs[i], now).run();
    if (r.meta.changes === 1) return json({ i });
  }
  return json({ i: -1 });
}

function json(obj, status = 200, extra = {}) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra },
  });
}
