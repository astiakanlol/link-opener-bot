#!/usr/bin/env python3
"""
Link Opener Bot - Web Interface
Jalankan di free tier (Render, Railway, dll).
User menempelkan link, bot membuka 1000 kali dengan jeda 0.8 detik
menggunakan satu page/tab yang sama.
"""

import os
import threading
import time
from flask import Flask, request, render_template_string, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

app = Flask(__name__)

# Status global sederhana (untuk free tier, cukup satu job pada satu waktu)
job_status = {
    "running": False,
    "url": "",
    "current": 0,
    "total": 1000,
    "success": 0,
    "fail": 0,
    "message": "Siap menerima link",
    "logs": []
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Link Opener Bot</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            background: #1e293b;
            border-radius: 16px;
            padding: 32px;
            max-width: 560px;
            width: 100%;
            box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.5);
        }
        h1 {
            font-size: 1.75rem;
            margin-bottom: 8px;
            color: #f8fafc;
        }
        .subtitle {
            color: #94a3b8;
            margin-bottom: 24px;
            font-size: 0.95rem;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: #cbd5e1;
        }
        input[type="url"] {
            width: 100%;
            padding: 14px 16px;
            border: 1px solid #334155;
            border-radius: 10px;
            background: #0f172a;
            color: #f1f5f9;
            font-size: 1rem;
            margin-bottom: 16px;
        }
        input[type="url"]:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.3);
        }
        button {
            width: 100%;
            padding: 14px;
            background: #3b82f6;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover:not(:disabled) {
            background: #2563eb;
        }
        button:disabled {
            background: #475569;
            cursor: not-allowed;
        }
        .status {
            margin-top: 24px;
            padding: 16px;
            background: #0f172a;
            border-radius: 10px;
            border: 1px solid #334155;
        }
        .status h3 {
            font-size: 0.9rem;
            color: #94a3b8;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        .progress {
            font-size: 1.5rem;
            font-weight: 700;
            color: #38bdf8;
            margin-bottom: 4px;
        }
        .meta {
            color: #94a3b8;
            font-size: 0.9rem;
        }
        .logs {
            margin-top: 16px;
            max-height: 180px;
            overflow-y: auto;
            font-family: ui-monospace, monospace;
            font-size: 0.8rem;
            color: #64748b;
            line-height: 1.5;
        }
        .note {
            margin-top: 20px;
            font-size: 0.8rem;
            color: #64748b;
            line-height: 1.5;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Link Opener Bot</h1>
        <p class="subtitle">Membuka link 1000× dengan jeda 0,8 detik (satu tab)</p>

        <form id="form">
            <label for="url">Tempel link di sini</label>
            <input type="url" id="url" name="url" placeholder="https://contoh.com" required>
            <button type="submit" id="btn">Mulai Buka Link</button>
        </form>

        <div class="status" id="status">
            <h3>Status</h3>
            <div class="progress" id="progress">0 / 1000</div>
            <div class="meta" id="meta">Siap menerima link</div>
            <div class="logs" id="logs"></div>
        </div>

        <p class="note">
            Proses memakan waktu sekitar 13–14 menit. Jangan tutup tab ini selama proses berjalan.
            Gunakan hanya pada situs yang Anda miliki atau yang diizinkan.
        </p>
    </div>

    <script>
        const form = document.getElementById('form');
        const btn = document.getElementById('btn');
        const progress = document.getElementById('progress');
        const meta = document.getElementById('meta');
        const logs = document.getElementById('logs');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('url').value.trim();
            if (!url) return;

            btn.disabled = true;
            btn.textContent = 'Sedang berjalan...';

            try {
                const res = await fetch('/start', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({url})
                });
                const data = await res.json();
                if (!data.ok) {
                    alert(data.message || 'Gagal memulai');
                    btn.disabled = false;
                    btn.textContent = 'Mulai Buka Link';
                    return;
                }
                pollStatus();
            } catch (err) {
                alert('Error: ' + err.message);
                btn.disabled = false;
                btn.textContent = 'Mulai Buka Link';
            }
        });

        async function pollStatus() {
            const res = await fetch('/status');
            const data = await res.json();

            progress.textContent = `${data.current} / ${data.total}`;
            meta.textContent = data.message;

            if (data.logs && data.logs.length) {
                logs.innerHTML = data.logs.slice(-15).map(l => `<div>${l}</div>`).join('');
                logs.scrollTop = logs.scrollHeight;
            }

            if (data.running) {
                setTimeout(pollStatus, 2000);
            } else {
                btn.disabled = false;
                btn.textContent = 'Mulai Buka Link';
                if (data.current > 0) {
                    meta.textContent = `Selesai • Berhasil: ${data.success} | Gagal: ${data.fail}`;
                }
            }
        }

        // Cek status saat halaman dimuat
        pollStatus();
    </script>
</body>
</html>
"""


def run_opener(url: str):
    global job_status
    job_status["running"] = True
    job_status["url"] = url
    job_status["current"] = 0
    job_status["success"] = 0
    job_status["fail"] = 0
    job_status["logs"] = []
    job_status["message"] = f"Sedang membuka: {url}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = context.new_page()

            for i in range(1, 1001):
                job_status["current"] = i
                try:
                    response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                    status = response.status if response else "N/A"
                    job_status["success"] += 1
                    log = f"[{i}/1000] Status {status}"
                except Exception as e:
                    job_status["fail"] += 1
                    log = f"[{i}/1000] Error: {str(e)[:60]}"

                job_status["logs"].append(log)
                if len(job_status["logs"]) > 50:
                    job_status["logs"] = job_status["logs"][-50:]

                if i < 1000:
                    time.sleep(0.8)

            browser.close()
            job_status["message"] = "Selesai"
    except Exception as e:
        job_status["message"] = f"Error fatal: {str(e)[:100]}"
        job_status["logs"].append(job_status["message"])
    finally:
        job_status["running"] = False


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/start", methods=["POST"])
def start():
    global job_status
    if job_status["running"]:
        return jsonify({"ok": False, "message": "Masih ada proses yang berjalan. Tunggu sampai selesai."})

    data = request.get_json() or {}
    url = (data.get("url") or "").strip()

    if not url:
        return jsonify({"ok": False, "message": "URL tidak boleh kosong"})

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Jalankan di background thread
    thread = threading.Thread(target=run_opener, args=(url,), daemon=True)
    thread.start()

    return jsonify({"ok": True, "message": "Proses dimulai"})


@app.route("/status")
def status():
    return jsonify(job_status)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
