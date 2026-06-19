// PWA アイコン生成スクリプト（依存ライブラリなし / Node 標準 zlib のみ）
//   実行: node scripts/gen-icons.mjs
//   出力: public/icon-192.png, icon-512.png, icon-512-maskable.png, apple-touch-icon.png
//
// デザイン: アプリ基調色(インディゴ #4f46e5)の角丸スクエア背景に
//          白いコイン + ¥ シンボルをベクター計算でラスタライズ。
import { deflateSync } from 'node:zlib'
import { writeFileSync, mkdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, join } from 'node:path'

const PRIMARY = [79, 70, 229] // #4f46e5
const WHITE = [255, 255, 255]
const __dirname = dirname(fileURLToPath(import.meta.url))
const OUT = join(__dirname, '..', 'public')

// --- 幾何ヘルパ -----------------------------------------------------------
function distToSegment(px, py, ax, ay, bx, by) {
  const dx = bx - ax
  const dy = by - ay
  const len2 = dx * dx + dy * dy
  let t = len2 === 0 ? 0 : ((px - ax) * dx + (py - ay) * dy) / len2
  t = Math.max(0, Math.min(1, t))
  const cx = ax + t * dx
  const cy = ay + t * dy
  return Math.hypot(px - cx, py - cy)
}

// 角丸スクエアの符号付き距離（内側で負）
function sdRoundRect(px, py, cx, cy, half, radius) {
  const qx = Math.abs(px - cx) - (half - radius)
  const qy = Math.abs(py - cy) - (half - radius)
  const ax = Math.max(qx, 0)
  const ay = Math.max(qy, 0)
  return Math.hypot(ax, ay) + Math.min(Math.max(qx, qy), 0) - radius
}

// 1ピクセルの色を 3x3 サブサンプルで求める（簡易アンチエイリアス）
function sampleColor(x, y, N, maskable) {
  const cx = N / 2
  const cy = N / 2
  // maskable はセーフエリア確保のため図形を 80% に縮小し背景は全面
  const inset = maskable ? N * 0.1 : 0
  const bgHalf = N / 2
  const bgRadius = maskable ? 0 : N * 0.22
  const coinR = (N / 2 - inset) * 0.62
  const r = coinR // ¥ の基準半径
  // ¥ のストローク（中心基準の相対座標）
  const segs = [
    // 左アーム
    [cx - 0.42 * r, cy - 0.5 * r, cx, cy - 0.05 * r],
    // 右アーム
    [cx + 0.42 * r, cy - 0.5 * r, cx, cy - 0.05 * r],
    // 縦棒
    [cx, cy - 0.05 * r, cx, cy + 0.55 * r],
    // 上の横バー
    [cx - 0.34 * r, cy + 0.08 * r, cx + 0.34 * r, cy + 0.08 * r],
    // 下の横バー
    [cx - 0.34 * r, cy + 0.28 * r, cx + 0.34 * r, cy + 0.28 * r],
  ]
  const stroke = 0.12 * r

  const S = 3
  let rr = 0, gg = 0, bb = 0, aa = 0
  for (let sy = 0; sy < S; sy++) {
    for (let sx = 0; sx < S; sx++) {
      const px = x + (sx + 0.5) / S
      const py = y + (sy + 0.5) / S
      let col = null
      // ¥ シンボル（最前面・インディゴ）
      let inYen = false
      for (const [ax, ay, bx, by] of segs) {
        if (distToSegment(px, py, ax, ay, bx, by) <= stroke / 2) { inYen = true; break }
      }
      const inCoin = Math.hypot(px - cx, py - cy) <= coinR
      const inBg = sdRoundRect(px, py, cx, cy, bgHalf, bgRadius) <= 0
      if (inCoin && inYen) col = PRIMARY
      else if (inCoin) col = WHITE
      else if (inBg) col = PRIMARY
      if (col) { rr += col[0]; gg += col[1]; bb += col[2]; aa += 255 }
    }
  }
  const n = S * S
  return [Math.round(rr / n), Math.round(gg / n), Math.round(bb / n), Math.round(aa / n)]
}

// --- PNG エンコード -------------------------------------------------------
const CRC_TABLE = (() => {
  const t = new Uint32Array(256)
  for (let n = 0; n < 256; n++) {
    let c = n
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
    t[n] = c >>> 0
  }
  return t
})()
function crc32(buf) {
  let c = 0xffffffff
  for (let i = 0; i < buf.length; i++) c = CRC_TABLE[(c ^ buf[i]) & 0xff] ^ (c >>> 8)
  return (c ^ 0xffffffff) >>> 0
}
function chunk(type, data) {
  const len = Buffer.alloc(4)
  len.writeUInt32BE(data.length, 0)
  const typeBuf = Buffer.from(type, 'ascii')
  const crc = Buffer.alloc(4)
  crc.writeUInt32BE(crc32(Buffer.concat([typeBuf, data])), 0)
  return Buffer.concat([len, typeBuf, data, crc])
}
function encodePng(N, rgba) {
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10])
  const ihdr = Buffer.alloc(13)
  ihdr.writeUInt32BE(N, 0)
  ihdr.writeUInt32BE(N, 4)
  ihdr[8] = 8 // bit depth
  ihdr[9] = 6 // color type RGBA
  // 残り(圧縮/フィルタ/インターレース)は 0
  const raw = Buffer.alloc((N * 4 + 1) * N)
  for (let y = 0; y < N; y++) {
    raw[y * (N * 4 + 1)] = 0 // filter type none
    rgba.copy(raw, y * (N * 4 + 1) + 1, y * N * 4, (y + 1) * N * 4)
  }
  const idat = deflateSync(raw, { level: 9 })
  return Buffer.concat([sig, chunk('IHDR', ihdr), chunk('IDAT', idat), chunk('IEND', Buffer.alloc(0))])
}

function render(N, maskable = false) {
  const rgba = Buffer.alloc(N * N * 4)
  for (let y = 0; y < N; y++) {
    for (let x = 0; x < N; x++) {
      const [r, g, b, a] = sampleColor(x, y, N, maskable)
      const i = (y * N + x) * 4
      rgba[i] = r; rgba[i + 1] = g; rgba[i + 2] = b; rgba[i + 3] = a
    }
  }
  return encodePng(N, rgba)
}

mkdirSync(OUT, { recursive: true })
const targets = [
  ['icon-192.png', 192, false],
  ['icon-512.png', 512, false],
  ['icon-512-maskable.png', 512, true],
  ['apple-touch-icon.png', 180, false],
]
for (const [name, size, maskable] of targets) {
  writeFileSync(join(OUT, name), render(size, maskable))
  console.log(`generated public/${name} (${size}x${size})`)
}
