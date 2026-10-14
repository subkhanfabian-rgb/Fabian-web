# Portfolio Fabian Subkhan

Website portfolio pribadi menggunakan HTML, CSS, JavaScript, dan Python Flask.

## Fitur

- Desain modern dan responsif
- Navbar sticky
- Dark mode dan light mode
- Animasi elemen ketika halaman digulir
- Skill dengan progress bar
- Project card dengan hover effect
- Form kontak terhubung dengan backend Flask
- Ikon media sosial menggunakan Font Awesome

## Struktur Folder

```text
portfolio/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── script.js
    └── images/
        ├── profile.jpg
        ├── project1.jpg
        ├── project2.jpg
        └── project3.jpg
```

## Cara Menjalankan

1. Pastikan Python sudah terpasang di komputer.

2. Buka terminal atau Command Prompt pada folder `portfolio`.

3. Buat virtual environment:

```bash
python -m venv venv
```

4. Aktifkan virtual environment.

Windows CMD:

```bash
venv\Scripts\activate
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

macOS atau Linux:

```bash
source venv/bin/activate
```

5. Instal dependency Flask:

```bash
pip install -r requirements.txt
```

6. Jalankan aplikasi:

```bash
python app.py
```

7. Buka browser dan kunjungi:

```text
http://127.0.0.1:5000
```

## Kustomisasi

- Ganti foto profil pada `static/images/profile.jpg`.
- Tambahkan gambar project pada `static/images/project1.jpg`, `project2.jpg`, dan `project3.jpg`.
- Ubah email, WhatsApp, Instagram, GitHub, dan LinkedIn pada file `templates/index.html`.
- Ganti tautan tombol `Lihat Project` dengan URL project atau repository GitHub Anda.
- Sesuaikan pendidikan, biodata, minat, serta daftar skill sesuai data pribadi.