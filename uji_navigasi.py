# uji_navigasi.py
# Pengujian otomatis untuk Soal 3: memastikan tidak ada broken link.
# Cara pakai (dari folder project, venv aktif):  python uji_navigasi.py
#
# Skrip ini membuka aplikasi lewat test client Flask (tanpa perlu menjalankan
# server), menelusuri semua link, file CSS/JS/gambar, lalu mencatat statusnya.
# Setelah itu menguji alur form tambah, edit, dan hapus.

import re
import sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from app import app
from data import BARANG


class PengumpulUrl(HTMLParser):
    """Mengumpulkan semua alamat (href, src, action) dari sebuah halaman HTML."""

    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("a", "link") and a.get("href"):
            self.urls.append(a["href"])
        elif tag in ("script", "img") and a.get("src"):
            self.urls.append(a["src"])
        elif tag == "form" and a.get("action", "") and a.get("method", "get").lower() == "get":
            self.urls.append(a["action"])  # form POST diuji terpisah di bawah


def url_internal(url):
    """True jika url mengarah ke server Flask ini (bukan CDN / anchor kosong)."""
    if not url or url.startswith(("#", "mailto:", "javascript:", "http://", "https://", "//")):
        return False
    return True


def telusuri(client):
    antrean, terlihat, hasil = ["/"], set(), []
    while antrean:
        url = antrean.pop(0)
        bersih = urlparse(url)._replace(fragment="").geturl()
        if bersih in terlihat:
            continue
        terlihat.add(bersih)

        respons = client.get(bersih)
        hasil.append((bersih, respons.status_code))

        if respons.status_code == 200 and "text/html" in respons.content_type:
            pengumpul = PengumpulUrl()
            pengumpul.feed(respons.get_data(as_text=True))
            for u in pengumpul.urls:
                if url_internal(u):
                    antrean.append(u)
        elif respons.status_code == 200 and "text/css" in respons.content_type:
            # CSS memanggil font/gambar lewat url(...); alamatnya relatif terhadap file CSS
            folder = bersih.rsplit("/", 1)[0]
            for u in re.findall(r"url\(['\"]?([^)'\"]+)['\"]?\)", respons.get_data(as_text=True)):
                u = u.split("?")[0].split("#")[0]
                if url_internal(u) and not u.startswith("data:"):
                    antrean.append(urljoin(folder + "/", u))
    return hasil


def cetak_tabel(hasil):
    print(f"{'No':<4}{'URL':<62}{'Status':<8}Hasil")
    print("-" * 82)
    for no, (url, status) in enumerate(hasil, start=1):
        print(f"{no:<4}{url:<62}{status:<8}{'OK' if status == 200 else 'BROKEN'}")


def uji_form(client):
    """Uji fungsional form. Mengembalikan daftar (nama_uji, lulus)."""
    laporan = []
    awal = len(BARANG)

    # 1. Tambah dengan data kosong harus ditolak dan menampilkan pesan error
    r = client.post("/barang/tambah", data={}, follow_redirects=True)
    laporan.append(("Tambah barang kosong ditolak",
                    r.status_code == 200 and b"wajib diisi" in r.data and len(BARANG) == awal))

    # 2. Tambah dengan data valid
    data = {"nama": "Penghapus Putih", "kategori": "Alat Tulis",
            "stok": "30", "stok_min": "10", "harga": "2000"}
    r = client.post("/barang/tambah", data=data, follow_redirects=True)
    laporan.append(("Tambah barang valid berhasil",
                    b"berhasil ditambahkan" in r.data and len(BARANG) == awal + 1))

    baru = BARANG[-1]
    # 3. Edit
    data["stok"] = "5"
    r = client.post(f"/barang/{baru['id']}/edit", data=data, follow_redirects=True)
    laporan.append(("Edit barang berhasil", b"berhasil diperbarui" in r.data and baru["stok"] == 5))

    # 4. Hapus
    r = client.post(f"/barang/{baru['id']}/hapus", follow_redirects=True)
    laporan.append(("Hapus barang berhasil", b"telah dihapus" in r.data and len(BARANG) == awal))

    # 5. Pencarian
    r = client.get("/barang?q=pensil")
    laporan.append(("Pencarian 'pensil' menemukan data", b"Pensil 2B" in r.data))

    # 6. Halaman yang tidak ada harus memakai halaman 404 buatan sendiri
    r = client.get("/halaman-ngawur")
    laporan.append(("Halaman tidak ada menampilkan 404", r.status_code == 404 and b"tidak ditemukan" in r.data))
    return laporan


def main():
    client = app.test_client()

    print("=== A. Penelusuran link dan aset statis ===\n")
    hasil = telusuri(client)
    cetak_tabel(hasil)
    rusak = [h for h in hasil if h[1] != 200]
    print(f"\nTotal URL diuji : {len(hasil)}")
    print(f"OK              : {len(hasil) - len(rusak)}")
    print(f"BROKEN          : {len(rusak)}")

    print("\n=== B. Uji fungsional form dan route ===\n")
    laporan = uji_form(client)
    gagal = 0
    for nama, lulus in laporan:
        print(f"[{'LULUS' if lulus else 'GAGAL'}] {nama}")
        gagal += 0 if lulus else 1

    print("\nKESIMPULAN:", "semua pengujian lulus." if not rusak and not gagal else "ada yang gagal, periksa daftar di atas.")
    sys.exit(1 if rusak or gagal else 0)


if __name__ == "__main__":
    main()
