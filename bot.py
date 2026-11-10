#!/usr/bin/env python3
"""
Link Opener Bot
Membuka URL yang diberikan sebanyak 1000 kali
dengan jeda 0.8 detik antar pembukaan,
menggunakan satu page/tab yang sama (tanpa berpindah tab).
"""

import sys
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError


def open_link_repeatedly(url: str, times: int = 1000, delay: float = 0.8):
    """
    Membuka URL berulang kali menggunakan satu page Playwright.
    """
    print(f"Memulai pembukaan link: {url}")
    print(f"Jumlah pengulangan : {times}")
    print(f"Jeda antar request : {delay} detik")
    print("-" * 50)

    with sync_playwright() as p:
        # Launch browser in headless mode (bisa diubah ke headless=False jika ingin melihat)
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        # Hanya satu page/tab yang digunakan sepanjang proses
        page = context.new_page()

        success_count = 0
        fail_count = 0

        for i in range(1, times + 1):
            try:
                # Navigasi ke URL di page yang sama (tidak membuka tab baru)
                response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                status = response.status if response else "N/A"
                print(f"[{i:4d}/{times}] Status: {status} | URL dibuka")
                success_count += 1
            except PlaywrightTimeoutError:
                print(f"[{i:4d}/{times}] Timeout saat membuka URL")
                fail_count += 1
            except Exception as e:
                print(f"[{i:4d}/{times}] Error: {str(e)[:80]}")
                fail_count += 1

            # Jeda 0.8 detik sebelum request berikutnya (kecuali setelah yang terakhir)
            if i < times:
                time.sleep(delay)

        browser.close()

    print("-" * 50)
    print(f"Selesai.")
    print(f"Berhasil : {success_count}")
    print(f"Gagal    : {fail_count}")


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1].strip()
    else:
        url = input("Masukkan link yang ingin dibuka berulang kali: ").strip()

    if not url:
        print("Error: URL tidak boleh kosong.")
        sys.exit(1)

    # Pastikan URL memiliki scheme
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        print(f"URL dilengkapi menjadi: {url}")

    open_link_repeatedly(url, times=1000, delay=0.8)


if __name__ == "__main__":
    main()
