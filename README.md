# InvenTrack - Prototipe Sistem Informasi Manajemen Inventaris (Flask)

ETS Pengembangan Sistem Berbasis Web. Template: **SB Admin 2** oleh Start Bootstrap (lisensi MIT).

## Cara menjalankan

```
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Buka http://127.0.0.1:5000 di browser.

Catatan: Google Fonts (Nunito) dimuat dari internet. Tanpa internet aplikasi tetap jalan, hanya jenis hurufnya berganti.

## Struktur proyek

```
ets_inventaris/
├── app.py               # route dan logika Flask
├── data.py              # data contoh dan identitas kelompok
├── uji_navigasi.py      # pengujian otomatis (Soal 3)
├── requirements.txt
├── templates/           # base.html (layout) + halaman yang mewarisinya
│   ├── base.html  dashboard.html  barang.html
│   ├── form_barang.html  profil.html  404.html
└── static/
    ├── css/             # sb-admin-2.min.css, custom.css
    ├── js/              # sb-admin-2.min.js, inventaris.js
    ├── img/             # gambar profil
    └── vendor/          # jquery, bootstrap, chart.js, datatables, fontawesome
```

## Daftar route

| URL | Function | Keterangan |
|-----|----------|------------|
| `/` | `dashboard` | Ringkasan stok, grafik, daftar restok |
| `/barang` | `barang` | Tabel data (mendukung `?q=` untuk pencarian) |
| `/barang/tambah` | `tambah_barang` | Form tambah (GET dan POST) |
| `/barang/<id>/edit` | `edit_barang` | Form edit (GET dan POST) |
| `/barang/<id>/hapus` | `hapus_barang` | Hapus (POST dari modal) |
| `/profil` | `profil` | Identitas kelompok, user flow, FAQ |

## Pengujian

Pengujian otomatis (tanpa menjalankan server):

```
python uji_navigasi.py
```

Skrip ini menelusuri semua link, CSS, JS, gambar, dan font, mencatat status tiap URL, lalu menguji alur tambah, edit, hapus, pencarian, dan halaman 404.

Pengujian manual komponen interaktif (jalankan `python app.py`):

- [ ] Klik tombol bulat di dasar sidebar: sidebar terlipat dan terbuka lagi
- [ ] Klik menu "Data Barang" di sidebar: submenu terbuka dan tertutup
- [ ] Klik ikon lonceng dan nama pengguna: dropdown terbuka
- [ ] Klik "Tentang Aplikasi": modal terbuka, tombol Tutup menutupnya
- [ ] Halaman Daftar Barang: kolom Cari, urutan kolom, dan pagination bekerja
- [ ] Klik ikon tong sampah: modal konfirmasi hapus terbuka
- [ ] Halaman Profil & Bantuan: accordion FAQ membuka dan menutup
- [ ] Buka DevTools (F12), tab Network: tidak ada status 404 berwarna merah
