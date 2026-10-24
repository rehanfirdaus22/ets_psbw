# app.py
# ETS - Prototipe antarmuka Sistem Informasi Manajemen Inventaris (InvenTrack)
# Framework: Flask  |  Template: SB Admin 2 (Start Bootstrap, lisensi MIT)

from flask import (
    Flask, render_template, request, redirect, url_for, flash, abort
)

from data import BARANG, KATEGORI, KELOMPOK

app = Flask(__name__)
app.secret_key = "ganti-dengan-kunci-rahasia-kelompokmu"  # dibutuhkan oleh flash()

APP_INFO = {
    "nama": "InvenTrack",
    "deskripsi": "Sistem Informasi Manajemen Inventaris Toko Alat Tulis",
    "versi": "1.0 (prototipe)",
    "tahun": 2026,
}


# ---------- Fungsi bantu ----------

def cari_barang(barang_id):
    """Mengembalikan data barang dengan id tertentu, atau None."""
    for item in BARANG:
        if item["id"] == barang_id:
            return item
    return None


def id_baru():
    return max((item["id"] for item in BARANG), default=0) + 1


def validasi_form(form):
    """Memeriksa isian form barang. Mengembalikan (data_bersih, daftar_error)."""
    errors = []
    nama = form.get("nama", "").strip()
    kategori = form.get("kategori", "").strip()

    if not nama:
        errors.append("Nama barang wajib diisi.")
    if kategori not in KATEGORI:
        errors.append("Pilih kategori yang tersedia.")

    angka = {}
    for kolom, label, minimal in (
        ("stok", "Stok", 0), ("stok_min", "Stok minimum", 0), ("harga", "Harga", 1)
    ):
        try:
            angka[kolom] = int(form.get(kolom, ""))
            if angka[kolom] < minimal:
                errors.append(f"{label} minimal {minimal}.")
        except ValueError:
            errors.append(f"{label} harus berupa angka bulat.")
            angka[kolom] = None

    data = {"nama": nama, "kategori": kategori, **angka}
    return data, errors


# ---------- Filter & context processor ----------

@app.template_filter("rupiah")
def format_rupiah(nilai):
    return "Rp " + f"{nilai:,}".replace(",", ".")


# Variabel di bawah otomatis tersedia di semua template
@app.context_processor
def data_global():
    stok_menipis = [b for b in BARANG if b["stok"] <= b["stok_min"]]
    return {"app_info": APP_INFO, "notif_stok": stok_menipis}


# ---------- Route ----------

@app.route("/")
def dashboard():
    total_stok = sum(b["stok"] for b in BARANG)
    nilai = sum(b["stok"] * b["harga"] for b in BARANG)
    menipis = [b for b in BARANG if b["stok"] <= b["stok_min"]]

    # data grafik: total stok per kategori
    label_grafik = KATEGORI
    nilai_grafik = [
        sum(b["stok"] for b in BARANG if b["kategori"] == k) for k in KATEGORI
    ]

    return render_template(
        "dashboard.html",
        jumlah_jenis=len(BARANG),
        total_stok=total_stok,
        nilai_inventori=nilai,
        menipis=menipis,
        label_grafik=label_grafik,
        nilai_grafik=nilai_grafik,
        terbaru=BARANG[-5:][::-1],
    )


@app.route("/barang")
def barang():
    q = request.args.get("q", "").strip()
    daftar = BARANG
    if q:
        daftar = [b for b in BARANG if q.lower() in b["nama"].lower()]
    return render_template("barang.html", daftar=daftar, q=q)


@app.route("/barang/tambah", methods=["GET", "POST"])
def tambah_barang():
    form_lama = {}
    if request.method == "POST":
        data, errors = validasi_form(request.form)
        if errors:
            for pesan in errors:
                flash(pesan, "danger")
            form_lama = request.form
        else:
            baru_id = id_baru()
            BARANG.append({"id": baru_id, "kode": f"BRG-{baru_id:03d}", **data})
            flash(f'Barang "{data["nama"]}" berhasil ditambahkan.', "success")
            return redirect(url_for("barang"))
    return render_template(
        "form_barang.html", judul="Tambah Barang", item=form_lama,
        kategori=KATEGORI, aksi=url_for("tambah_barang")
    )


@app.route("/barang/<int:barang_id>/edit", methods=["GET", "POST"])
def edit_barang(barang_id):
    item = cari_barang(barang_id)
    if item is None:
        abort(404)

    if request.method == "POST":
        data, errors = validasi_form(request.form)
        if errors:
            for pesan in errors:
                flash(pesan, "danger")
            item_tampil = request.form
        else:
            item.update(data)
            flash(f'Barang "{item["nama"]}" berhasil diperbarui.', "success")
            return redirect(url_for("barang"))
    else:
        item_tampil = item

    return render_template(
        "form_barang.html", judul="Edit Barang", item=item_tampil,
        kategori=KATEGORI, aksi=url_for("edit_barang", barang_id=barang_id)
    )


# Hapus hanya lewat POST (dipanggil dari modal konfirmasi di halaman data)
@app.route("/barang/<int:barang_id>/hapus", methods=["POST"])
def hapus_barang(barang_id):
    item = cari_barang(barang_id)
    if item is None:
        abort(404)
    BARANG.remove(item)
    flash(f'Barang "{item["nama"]}" telah dihapus.', "warning")
    return redirect(url_for("barang"))


@app.route("/profil")
def profil():
    return render_template("profil.html", kelompok=KELOMPOK)


@app.errorhandler(404)
def halaman_tidak_ditemukan(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
