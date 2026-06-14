# 🎵 Apple Music Discord RPC — Menu Bar App

Tampilkan lirik real-time Apple Music di Discord Rich Presence, berjalan sebagai menu bar app di macOS.

---

## Tampilan

**Menu bar:** `♪ Alonica`
**Dropdown:**
```
"I don't know the last time there were tears"
─────────────────────────
Pause RPC
─────────────────────────
Quit
```

**Discord:**
```
Listening to Apple Music
[Album Art]  Alonica
             "I don't know the last time..."
             LANY — a beautiful blur (deluxe)
             ━━━━━░░░░░  2:38 / 3:58
```

---

## Setup

### 1. Install dependencies

```bash
cd apple-music-rpc-app
pip3 install -r requirements.txt
```

### 2. Isi Discord Client ID

Buka `discord_rpc.py`, ganti:
```python
DISCORD_CLIENT_ID = "YOUR_CLIENT_ID_HERE"
```
dengan Application ID dari https://discord.com/developers/applications

### 3. Jalankan langsung (tanpa build)

```bash
python3 main.py
```

Icon `♪` akan muncul di menu bar kanan atas.

---

## Build jadi .app (opsional)

Kalau mau jadi app beneran yang bisa diklik:

```bash
pip3 install py2app
python3 setup.py py2app
```

Hasilnya ada di folder `dist/Apple Music RPC.app` — drag ke Applications folder.

### Auto-start saat login

Setelah build:
1. Buka **System Settings → General → Login Items**
2. Klik `+` dan pilih `Apple Music RPC.app`

---

## Troubleshooting

| Masalah | Solusi |
|---|---|
| Icon tidak muncul | Pastikan Discord desktop buka |
| Lirik tidak ada | Lagu mungkin tidak ada di LRCLIB |
| Album art tidak muncul | iTunes Search API kadang lambat, tunggu track berikutnya |
| "Invalid Client ID" | Cek DISCORD_CLIENT_ID di discord_rpc.py |

---

## Files

```
apple-music-rpc-app/
├── main.py          # Menu bar app (rumps)
├── tracker.py       # Loop utama, orkestrasi
├── apple_music.py   # AppleScript reader
├── lyrics.py        # LRCLIB fetcher + sync
├── discord_rpc.py   # Discord Rich Presence
├── album_art.py     # iTunes album art fetcher
├── requirements.txt
└── setup.py         # Build .app
```
