import os
from flask import Flask, render_template, request, jsonify
import psycopg

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")


def get_db_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL belum diatur di environment variables.")
    return psycopg.connect(DATABASE_URL, sslmode="require")


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS pesan (
            id BIGSERIAL PRIMARY KEY,
            nama TEXT NOT NULL,
            email TEXT NOT NULL,
            isi_pesan TEXT NOT NULL,
            waktu TIMESTAMPTZ NOT NULL DEFAULT NOW()
        )
    """)


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

    try:
        with get_db_connection() as conn:
            init_db(conn)
            conn.execute(
                """
                INSERT INTO pesan (nama, email, isi_pesan)
                VALUES (%s, %s, %s)
                """,
                (name, email, message)
            )

        return jsonify({
            "success": True,
            "message": f"Terima kasih, {name}! Pesan Anda berhasil disimpan."
        })

    except RuntimeError:
        app.logger.error("DATABASE_URL belum dikonfigurasi.")
        return jsonify({
            "success": False,
            "message": "Database belum dikonfigurasi. Silakan hubungi pemilik website."
        }), 503
    except Exception:
        app.logger.exception("Gagal menyimpan pesan ke database.")
        return jsonify({
            "success": False,
            "message": "Pesan belum berhasil disimpan. Silakan coba lagi nanti."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
