# Link Opener Bot

Bot untuk membuka link yang diberikan pengguna sebanyak **1000 kali** dengan jeda **0,8 detik**, menggunakan **satu tab yang sama** (tanpa berpindah tab).

Sekarang mendukung dua mode:

1. **Lokal** (`bot.py`) — jalankan di komputer sendiri
2. **Online (Free Tier)** (`app.py`) — web interface yang bisa di-deploy gratis

---

## Fitur

- Input link dari pengguna (web form atau CLI)
- Membuka link 1000× dengan jeda 0.8 detik
- Satu page/tab saja (Playwright)
- Mode headless
- Progress real-time di web interface
- Siap deploy ke Render / Railway free tier

---

## Cara 1: Jalankan Lokal

```bash
git clone https://github.com/astiakanlol/link-opener-bot.git
cd link-opener-bot
pip install -r requirements.txt
playwright install chromium

# CLI
python bot.py https://contoh.com

# atau Web lokal
python app.py
# buka http://localhost:5000
```

---

## Cara 2: Deploy Online (Free Tier) — Direkomendasikan

### Opsi A: Render (paling mudah)

1. Buka [https://render.com](https://render.com) → Sign up (gratis, tidak wajib kartu kredit)
2. Klik **New +** → **Web Service**
3. Connect repository GitHub `astiakanlol/link-opener-bot`
4. Pengaturan:
   - **Name**: `link-opener-bot` (bebas)
   - **Runtime**: Docker
   - **Instance Type**: Free
5. Klik **Create Web Service**
6. Tunggu deploy selesai (5–10 menit pertama kali)
7. Buka URL yang diberikan Render (contoh: `https://link-opener-bot-xxxx.onrender.com`)

> Catatan Render Free: Service akan sleep setelah ~15 menit tidak aktif. Saat dibuka lagi, butuh 30–60 detik untuk bangun. Setelah job dimulai, biarkan tab browser tetap terbuka sampai selesai (~13–14 menit).

### Opsi B: Railway

1. Buka [https://railway.app](https://railway.app)
2. New Project → Deploy from GitHub repo
3. Pilih repository ini
4. Railway otomatis mendeteksi Dockerfile
5. Deploy → dapatkan public URL

Railway memberikan free credit terbatas setiap bulan.

---

## Struktur File

| File | Keterangan |
|------|------------|
| `app.py` | Web interface (Flask) — untuk online |
| `bot.py` | Versi CLI lokal |
| `Dockerfile` | Untuk deploy Docker (Render/Railway) |
| `requirements.txt` | Dependensi |
| `README.md` | Dokumentasi |

---

## Catatan Penting

- Proses 1000× membutuhkan waktu sekitar **13–14 menit**.
- Gunakan hanya pada website milik sendiri atau yang secara eksplisit mengizinkan.
- Free tier memiliki batasan resource. Jika terlalu sering error memory, kurangi jumlah pengulangan di kode.
- Satu job berjalan pada satu waktu (untuk menjaga stabilitas free tier).

---

## Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Service sleep di Render | Buka URL lagi, tunggu 30–60 detik, lalu mulai job |
| Timeout / memory error | Kurangi `times=1000` menjadi 200–300 di `app.py` |
| Browser gagal launch | Pastikan menggunakan Dockerfile resmi Playwright |
