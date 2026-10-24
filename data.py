# data.py
# Data contoh (dummy) untuk prototipe. Disimpan di memori, jadi akan kembali
# ke kondisi awal setiap kali server Flask dijalankan ulang.

KATEGORI = ["Alat Tulis", "Kertas", "Perlengkapan Kantor", "Elektronik"]

BARANG = [
    {"id": 1, "kode": "BRG-001", "nama": "Pulpen Gel Hitam 0.5 mm", "kategori": "Alat Tulis", "stok": 120, "stok_min": 30, "harga": 3500},
    {"id": 2, "kode": "BRG-002", "nama": "Pensil 2B", "kategori": "Alat Tulis", "stok": 8, "stok_min": 20, "harga": 2500},
    {"id": 3, "kode": "BRG-003", "nama": "Kertas HVS A4 80 gsm (rim)", "kategori": "Kertas", "stok": 45, "stok_min": 15, "harga": 52000},
    {"id": 4, "kode": "BRG-004", "nama": "Buku Tulis 58 Lembar", "kategori": "Kertas", "stok": 6, "stok_min": 25, "harga": 6000},
    {"id": 5, "kode": "BRG-005", "nama": "Stapler Kecil", "kategori": "Perlengkapan Kantor", "stok": 22, "stok_min": 5, "harga": 18000},
    {"id": 6, "kode": "BRG-006", "nama": "Map Plastik Folder", "kategori": "Perlengkapan Kantor", "stok": 75, "stok_min": 20, "harga": 4500},
    {"id": 7, "kode": "BRG-007", "nama": "Kalkulator Ilmiah", "kategori": "Elektronik", "stok": 3, "stok_min": 5, "harga": 135000},
    {"id": 8, "kode": "BRG-008", "nama": "Flashdisk 32 GB", "kategori": "Elektronik", "stok": 18, "stok_min": 10, "harga": 65000},
    {"id": 9, "kode": "BRG-009", "nama": "Spidol Whiteboard", "kategori": "Alat Tulis", "stok": 40, "stok_min": 12, "harga": 9500},
    {"id": 10, "kode": "BRG-010", "nama": "Kertas Foto A4 (pak)", "kategori": "Kertas", "stok": 14, "stok_min": 10, "harga": 38000},
]

# Identitas kelompok (ganti sesuai kelompokmu)
KELOMPOK = {
    "nama": "Kelompok 1",
    "mata_kuliah": "Pengembangan Sistem Berbasis Web",
    "anggota": [
        {"nama": "Aksa", "nrp": "1482500059"},
        {"nama": "Rehan", "nrp": "1482500061"},
        {"nama": "Erico", "nrp": "1482500062"},
    ],
}
