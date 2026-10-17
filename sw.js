/* Souffle de Glace — service worker
   - code : réseau d'abord (les mises à jour arrivent), cache en secours hors ligne
   - sons : cache d'abord, téléchargés une fois puis conservés
   VERSION est remplacée par l'identifiant du commit au déploiement. */
const VERSION = "__VERSION__";
const APP = "souffle-app-" + VERSION;
const SONS = "souffle-sons";
const FONTS = "souffle-polices";

const SHELL = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "reglages.json",
  "icones/icone-192.png",
  "icones/icone-512.png",
  "icones/apple-touch-icon.png"
];

const abs = p => new URL(p, self.registration.scope).href;
const isAudio = url => /\/sons\/.+\.(mp3|m4a|aac|wav|aif|aiff|caf|flac|ogg|opus|mp4)$/i.test(url.pathname);

self.addEventListener("install", ev => {
  ev.waitUntil((async () => {
    const c = await caches.open(APP);
    await Promise.all(SHELL.map(p => c.add(abs(p)).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener("activate", ev => {
  ev.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith("souffle-app-") && k !== APP).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

/* réseau d'abord, avec un délai court pour ne pas faire attendre en réseau faible */
async function networkFirst(req, cacheName, timeoutMs = 3500){
  const cache = await caches.open(cacheName);
  // « no-cache » : toujours revérifier auprès du serveur (GitHub Pages autorise 10 min de cache)
  const fresh = req.mode === "navigate"
    ? fetch(req.url, { cache:"no-cache", credentials:"same-origin" })
    : fetch(new Request(req, { cache:"no-cache" }));
  try {
    const res = await Promise.race([
      fresh,
      new Promise((_, rej) => setTimeout(() => rej(new Error("délai")), timeoutMs))
    ]);
    if (res && res.ok) cache.put(req, res.clone());
    return res;
  } catch(e){
    const hit = await cache.match(req, { ignoreSearch:true });
    if (hit) return hit;
    if (req.mode === "navigate"){
      const shell = await cache.match(abs("index.html"));
      if (shell) return shell;
    }
    throw e;
  }
}

async function cacheFirst(req, cacheName){
  const cache = await caches.open(cacheName);
  const hit = await cache.match(req, { ignoreSearch:true });
  if (hit) return hit;
  const res = await fetch(req);
  if (res && (res.ok || res.type === "opaque")) cache.put(req, res.clone());
  return res;
}

self.addEventListener("fetch", ev => {
  const req = ev.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.origin === location.origin){
    if (isAudio(url)) return ev.respondWith(cacheFirst(req, SONS));
    return ev.respondWith(networkFirst(req, APP));
  }
  if (url.hostname === "fonts.googleapis.com" || url.hostname === "fonts.gstatic.com"){
    return ev.respondWith(cacheFirst(req, FONTS));
  }
});

/* À chaque ouverture, la page demande une vérification : on télécharge les sons
   manquants (pour une séance sans réseau) et on oublie ceux retirés du dépôt. */
let checking = null;
self.addEventListener("message", ev => {
  if (!ev.data || ev.data.type !== "check-sounds") return;
  const client = ev.source;
  if (!checking) checking = checkSounds(client).finally(() => { checking = null; });
  ev.waitUntil(checking);
});

async function checkSounds(client){
  let list;
  try {
    const res = await networkFirst(new Request(abs("sons/sons.json"), { cache:"no-cache" }), APP);
    list = await res.json();
  } catch(e){ return; }

  const paths = [
    ...(list.respiration || []), ...(list.apnee || []),
    ...Object.values(list.voix || {}), ...Object.values(list.souffle || {})
  ];
  const wanted = new Set(paths.map(abs));
  const cache = await caches.open(SONS);

  // oublie les sons qui ne sont plus dans le dépôt
  for (const req of await cache.keys()){
    if (!wanted.has(req.url)) await cache.delete(req);
  }

  const missing = [];
  for (const u of wanted){ if (!(await cache.match(u))) missing.push(u); }
  if (!missing.length) return;

  const post = msg => { try { client && client.postMessage(msg); } catch(e){} };
  let done = 0, failed = 0;
  post({ type:"cache-progress", done, total:missing.length });
  // les courts d'abord (voix, souffle), puis les musiques
  const short = new Set([...Object.values(list.voix || {}), ...Object.values(list.souffle || {})].map(abs));
  missing.sort((a, b) => (short.has(b) ? 1 : 0) - (short.has(a) ? 1 : 0));
  for (const u of missing){
    try {
      const res = await fetch(u);
      if (!res.ok) throw 0;
      await cache.put(u, res);
    } catch(e){ failed++; }
    done++;
    post({ type:"cache-progress", done, total:missing.length });
  }
  post({ type:"cache-done", failed });
}
