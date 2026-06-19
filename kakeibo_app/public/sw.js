// 家計簿アプリ Service Worker
// 方針:
//   - 同一オリジンの GET のみ扱う（GAS API = script.google.com への通信はそのまま素通し）
//   - network-first（最新を優先しつつ、オフライン時はキャッシュにフォールバック）
//   - 古いバージョンのキャッシュは activate 時に破棄
const CACHE = 'kakeibo-v1'

self.addEventListener('install', (event) => {
  self.skipWaiting()
})

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  )
})

self.addEventListener('fetch', (event) => {
  const { request } = event
  if (request.method !== 'GET') return
  const url = new URL(request.url)
  if (url.origin !== self.location.origin) return // 外部API(GAS)はキャッシュしない

  event.respondWith(
    fetch(request)
      .then((response) => {
        // ナビゲーション/静的アセットのみキャッシュ更新
        if (response.ok && (request.mode === 'navigate' || response.type === 'basic')) {
          const copy = response.clone()
          caches.open(CACHE).then((cache) => cache.put(request, copy))
        }
        return response
      })
      .catch(async () => {
        const cached = await caches.match(request)
        if (cached) return cached
        // オフライン時、未キャッシュのナビゲーションはトップにフォールバック
        if (request.mode === 'navigate') {
          const shell = await caches.match('/')
          if (shell) return shell
        }
        throw new Error('offline and not cached')
      })
  )
})
