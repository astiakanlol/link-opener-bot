# Link Opener Bot

Bot sederhana untuk membuka link yang diberikan pengguna secara berulang sebanyak **1000 kali** dengan jeda **0,8 detik** antar setiap pembukaan, menggunakan **satu tab yang sama** (tanpa berpindah tab).

## Fitur

- Menerima input link dari pengguna
- Membuka link berulang 1000x
- Jeda 0.8 detik setiap request
- Menggunakan satu page/tab saja (Playwright)
- Mode headless (bisa dijalankan di background)
- Bekerja untuk hampir semua jenis link (HTTP/HTTPS)

## Persyaratan

- Python 3.8+
- Playwright

## Instalasi

```bash
pip install -r requirements.txt
playwright install chromium
```

## Cara Menjalankan

```bash
python bot.py
```

Kemudian masukkan URL yang ingin dibuka berulang kali.

Atau langsung dengan argument:

```bash
python bot.py https://contoh.com
```

## Catatan Penting

- Gunakan hanya pada website milik sendiri atau yang diizinkan.
- Penggunaan berlebihan dapat melanggar Terms of Service situs target dan dapat dianggap sebagai aktivitas yang tidak diinginkan.
- Script ini dirancang untuk keperluan testing/load testing sederhana.

## Struktur

- `bot.py` — script utama
- `requirements.txt` — dependensi
