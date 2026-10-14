from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/contact", methods=["POST"])
def contact():
    data = request.get_json()

    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()

    if not name or not email or not message:
        return jsonify({
            "success": False,
            "message": "Semua kolom wajib diisi."
        }), 400

    # Tambahkan integrasi email atau database di sini bila diperlukan.
    print(f"Pesan baru dari {name} ({email}): {message}")

    return jsonify({
        "success": True,
        "message": f"Terima kasih, {name}! Pesan Anda sudah diterima."
    })


if __name__ == "__main__":
    app.run(debug=True)