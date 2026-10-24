// inventaris.js - skrip khusus aplikasi (di luar skrip bawaan template)

$(function () {

  // 1. Tabel data: DataTables dengan teks bahasa Indonesia
  if ($("#tabelBarang").length) {
    $("#tabelBarang").DataTable({
      columnDefs: [{ orderable: false, targets: -1 }], // kolom Aksi tidak bisa diurutkan
      language: {
        search: "Cari:",
        lengthMenu: "Tampilkan _MENU_ data",
        info: "Menampilkan _START_ sampai _END_ dari _TOTAL_ data",
        infoEmpty: "Tidak ada data",
        zeroRecords: "Data tidak ditemukan",
        paginate: { previous: "Sebelumnya", next: "Berikutnya" },
      },
    });
  }

  // 2. Modal hapus: isi nama barang dan alamat form dari atribut data-* tombol
  $("#hapusModal").on("show.bs.modal", function (event) {
    var tombol = $(event.relatedTarget);
    $("#namaHapus").text(tombol.data("nama"));
    $("#formHapus").attr("action", tombol.data("action"));
  });

  // 3. Grafik dashboard: Chart.js, data dikirim dari Flask (window.DATA_GRAFIK)
  var kanvas = document.getElementById("grafikStok");
  if (kanvas && window.DATA_GRAFIK && window.Chart) {
    Chart.defaults.global.defaultFontFamily = "Nunito, -apple-system, sans-serif";
    new Chart(kanvas, {
      type: "bar",
      data: {
        labels: window.DATA_GRAFIK.label,
        datasets: [{
          label: "Total stok",
          backgroundColor: "#4e73df",
          hoverBackgroundColor: "#2e59d9",
          data: window.DATA_GRAFIK.nilai,
        }],
      },
      options: {
        maintainAspectRatio: false,
        legend: { display: false },
        scales: { yAxes: [{ ticks: { beginAtZero: true } }] },
      },
    });
  }
});
