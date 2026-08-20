(() => {
  "use strict";

  // ponytail: track the canonical GitHub Pages host only; add a custom host when
  // the public site actually moves rather than accepting arbitrary origins now.
  if (location.hostname !== "taeyongvv.github.io" || !crypto.randomUUID) return;

  const key = "ricecookey-web-visitor";
  let visitorId;
  try {
    visitorId = localStorage.getItem(key);
    if (!visitorId) {
      visitorId = crypto.randomUUID();
      localStorage.setItem(key, visitorId);
    }
  } catch {
    visitorId = crypto.randomUUID();
  }

  fetch("https://ricecookey-dashboard.vercel.app/api/web-analytics", {
    method: "POST",
    mode: "cors",
    credentials: "omit",
    keepalive: true,
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ visitor_id: visitorId, path: location.pathname || "/" }),
  }).catch(() => {});
})();
