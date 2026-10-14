import json
import os
import urllib.error
import urllib.request

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Atur kedua variabel ini di Vercel:
# RESEND_API_KEY = API key dari https://resend.com/api-keys
# CONTACT_EMAIL = alamat email tujuan menerima pesan
# Untuk pengujian awal, FROM_EMAIL boleh memakai onboarding@resend.dev.
# Resend membatasi alamat penerima untuk sender uji coba; verifikasi domain
# di Resend jika ingin mengirim ke penerima lain / memakai alamat pengirim sendiri.
FROM_EMAIL = os.environ.get("FROM_EMAIL", "onboarding@resend.dev")
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "subkhanfabian@gmail.com")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or not email or not message:
        return jsonify({
            "success": False,
            "message": "Semua kolom wajib diisi."
        }), 400

    if len(name) > 150 or len(email) > 254 or len(message) > 10000:
        return jsonify({
            "success": False,
            "message": "Ada kolom yang terlalu panjang."
        }), 400

    api_key = os.environ.get("RESEND_API_KEY")
    if not api_key:
        app.logger.error("RESEND_API_KEY belum dikonfigurasi.")
        return jsonify({
            "success": False,
            "message": "Layanan email belum dikonfigurasi. Silakan coba lagi nanti."
        }), 503

    payload = {
        "from": FROM_EMAIL,
        "to": [CONTACT_EMAIL],
        "reply_to": email,
        "subject": f"Pesan portfolio baru dari {name}",
        "text": (
            f"Ada pesan baru dari website portfolio.\n\n"
            f"Nama: {name}\n"
            f"Email: {email}\n\n"
            f"Pesan:\n{message}"
        )
    }

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Fabian-Portfolio/1.0"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            if 200 <= response.status < 300:
                return jsonify({
                    "success": True,
                    "message": f"Terima kasih, {name}! Pesan berhasil dikirim."
                })

        return jsonify({
            "success": False,
            "message": "Email belum berhasil dikirim. Silakan coba lagi."
        }), 502

    except urllib.error.HTTPError as error:
        # Jangan kirim detail provider / secret ke browser.
        error_body = error.read().decode("utf-8", errors="replace")
        app.logger.error("Resend menolak email (HTTP %s): %s", error.code, error_body)
        return jsonify({
            "success": False,
            "message": "Email gagal dikirim. Periksa konfigurasi email di Vercel."
        }), 502
    except Exception:
        app.logger.exception("Gagal mengirim email kontak.")
        return jsonify({
            "success": False,
            "message": "Terjadi kendala saat mengirim email. Silakan coba lagi."
        }), 502


if __name__ == "__main__":
    app.run(debug=True)
