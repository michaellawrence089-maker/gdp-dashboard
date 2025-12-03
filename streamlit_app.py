import streamlit as st
import matplotlib.pyplot as plt

# PROGRAM UTAMA PERHITUNGAN BIAYA OPERASIONAL PENGEBORAN BATUBARA (VERSI STREAMLIT)

# FUNGSI BANTUAN UMUM
def format_rupiah(nominal: float) -> str:
    """Memformat angka menjadi format Rupiah yang rapi"""
    return f"Rp{nominal:,.2f}"

# FUNGSI PERHITUNGAN BAHAN BAKAR & EMISI
def hitung_konsumsi_bahan_bakar(jenis_mesin: str, waktu_menit: float) -> float:
    """Menghitung konsumsi bahan bakar berdasarkan jenis mesin dan waktu operasi"""
    waktu_jam = waktu_menit / 60
    konsumsi_per_jam = {
        "Tekanan": 8.5,
        "Air Blasting": 12.0,
        "Pompa Hidrolik": 15.5,
    }
    return konsumsi_per_jam.get(jenis_mesin, 0) * waktu_jam


def hitung_biaya_bahan_bakar(konsumsi_liter: float, harga_per_liter: float) -> float:
    """Menghitung total biaya bahan bakar"""
    return konsumsi_liter * harga_per_liter


def hitung_emisi_co2(konsumsi_liter: float) -> float:
    """Menghitung estimasi emisi CO2 dari konsumsi bahan bakar"""
    FAKTOR_EMISI = 2.68
    return konsumsi_liter * FAKTOR_EMISI


# FUNGSI ANALISIS TEKNIS
def klasifikasi_tingkat_kesulitan(tekanan: float, kedalaman: float) -> str:
    """Mengklasifikasikan tingkat kesulitan pengeboran"""
    if kedalaman > 50 and tekanan < 100:
        return "SANGAT SULIT"
    elif kedalaman > 30 and tekanan < 150:
        return "SULIT"
    elif kedalaman > 15:
        return "SEDANG"
    else:
        return "MUDAH"


def hitung_efisiensi_biaya(biaya_aktual: float, target_biaya: float) -> float:
    """Menghitung persentase efisiensi biaya"""
    if target_biaya > 0:
        efisiensi = ((target_biaya - biaya_aktual) / target_biaya) * 100
        return efisiensi
    return 0.0


def rekomendasi_mesin_berdasarkan_kondisi(kedalaman_rata2: float, tingkat_kesulitan: str) -> str:
    """Memberikan rekomendasi mesin untuk proyek selanjutnya"""
    if tingkat_kesulitan in ["SANGAT SULIT", "SULIT"] and kedalaman_rata2 > 30:
        return "Pompa Hidrolik"
    elif tingkat_kesulitan == "SEDANG" and kedalaman_rata2 > 20:
        return "Air Blasting"
    else:
        return "Tekanan"


# FUNGSI FEEDBACK DAN EVALUASI
def beri_feedback_efisiensi(efisiensi_bahan_bakar: float) -> str:
    """Memberikan feedback berdasarkan efisiensi bahan bakar"""
    if efisiensi_bahan_bakar > 5.0:
        return "⭐ EXCELLENT - Efisiensi bahan bakar sangat baik!"
    elif efisiensi_bahan_bakar > 3.5:
        return "✅ GOOD - Efisiensi bahan bakar dalam batas optimal"
    elif efisiensi_bahan_bakar > 2.0:
        return "⚠  FAIR - Efisiensi bahan bakar perlu ditingkatkan"
    else:
        return "❌ POOR - Efisiensi bahan bakar tidak optimal, perlu evaluasi mesin"


def beri_feedback_biaya(efisiensi_biaya: float) -> str:
    """Memberikan feedback berdasarkan efisiensi biaya"""
    if efisiensi_biaya > 15:
        return "💰 SANGAT EKONOMIS - Biaya operasional sangat efisien"
    elif efisiensi_biaya > 5:
        return "💵 EKONOMIS - Biaya operasional efisien"
    elif efisiensi_biaya > 0:
        return "📊 CUKUP - Biaya operasional dalam batas wajar"
    else:
        return "🚨 TIDAK EKONOMIS - Biaya operasional melebihi target"


def beri_feedback_lingkungan(total_emisi: float) -> str:
    """Memberikan feedback berdasarkan dampak lingkungan"""
    if total_emisi < 50:
        return "🌿 RAMAH LINGKUNGAN - Emisi CO2 rendah"
    elif total_emisi < 150:
        return "🌱 CUKUP RAMAH - Emisi CO2 dalam batas wajar"
    elif total_emisi < 300:
        return "🏭 PERLU PERHATIAN - Emisi CO2 cukup tinggi"
    else:
        return "🌫 TINGGI - Emisi CO2 sangat tinggi, perlu strategi mitigasi"


def beri_feedback_penggunaan_program(nama_pengguna: str, jumlah_percobaan: int) -> str:
    """Memberikan feedback tentang penggunaan program oleh user"""
    if jumlah_percobaan >= 5:
        return f"👏 Hebat {nama_pengguna}! Anda telah melakukan {jumlah_percobaan} percobaan - komitmen yang mengesankan!"
    elif jumlah_percobaan >= 3:
        return f"👍 Good job {nama_pengguna}! {jumlah_percobaan} percobaan menunjukkan ketelitian yang baik."
    else:
        return f"💡 Tips {nama_pengguna}: Coba lebih banyak percobaan untuk data yang lebih akurat!"


def hitung_performa_keseluruhan(
    efisiensi_bahan_bakar: float, efisiensi_biaya: float, total_pengeboran: float
) -> float:
    """Menghitung skor performa keseluruhan (0-100)"""
    skor_efisiensi = min(efisiensi_bahan_bakar * 15, 40)
    skor_biaya = min(max(efisiensi_biaya, 0) * 2, 30)
    skor_produktivitas = min(total_pengeboran / 2, 30)
    return skor_efisiensi + skor_biaya + skor_produktivitas


# PENGATURAN HALAMAN STREAMLIT
st.set_page_config(
    page_title="KalkuBor - Biaya Operasional Pengeboran Batubara",
    layout="wide",
)

with st.container():
    center = st.columns(3)[1]
    with center:
        st.image("C:\\Users\\Michael\\Documents\\LOGO.jpg", width=300)
st.title("Program Perhitungan Biaya Operasional Pengeboran Batubara")
st.caption("Program by: Kelompok 7 Berpikir Komputasional K-28")

# INPUT IDENTITAS PENGGUNA
col_nama, col_info = st.columns([2, 3])
with col_nama:
    nama_anda = st.text_input("Masukkan Nama Anda", value="Operator")
with col_info:
    st.info(
        "Isi data di sidebar untuk memulai perhitungan. "
        "Klik tombol **Hitung** setelah semua input terisi."
    )

# SIDEBAR - PENGATURAN UMUM
st.sidebar.header("⚙️ Pengaturan Umum")
jenis_mesin = st.sidebar.selectbox(
    "Jenis mesin pengeboran",
    ["Tekanan", "Air Blasting", "Pompa Hidrolik"],
)

n = st.sidebar.number_input(
    "Jumlah percobaan",
    min_value=1,
    max_value=20,
    value=3,
    step=1,
)

biaya_per_jam = st.sidebar.number_input(
    "Biaya operasional per jam (Rp)",
    min_value=0.0,
    value=1_000_000.0,
    step=100_000.0,
)

harga_bahan_bakar = st.sidebar.number_input(
    "Harga bahan bakar per liter (Rp)",
    min_value=0.0,
    value=15_000.0,
    step=500.0,
)

# konstanta efisiensi mesin (batuan lunak seperti batubara)
k = 0.04  # m/bar/menit

st.sidebar.markdown("---")
st.sidebar.write("🔢 Konstanta efisiensi (k) = **0.04 m/bar/menit**")

# INPUT DATA PERCOBAAN
st.header("📥 Input Data Percobaan")
st.write("Atur tekanan dan target kedalaman untuk setiap percobaan.")

data_percobaan = []
for i in range(int(n)):
    with st.expander(f"Percobaan ke-{i + 1}", expanded=(i == 0)):
        c1, c2 = st.columns(2)
        with c1:
            tekanan = st.number_input(
                f"Tekanan (bar) - Percobaan {i + 1}",
                min_value=0.0,
                value=100.0,
                step=5.0,
                key=f"tekanan_{i}",
            )
        with c2:
            target_kedalaman = st.number_input(
                f"Target kedalaman (m) - Percobaan {i + 1}",
                min_value=0.0,
                value=20.0,
                step=1.0,
                key=f"kedalaman_{i}",
            )
        data_percobaan.append(
            {
                "tekanan": tekanan,
                "target_kedalaman": target_kedalaman,
            }
        )

# TOMBOL HITUNG
hitung = st.button("▶️ Hitung Biaya & Performa")

if hitung:
    # variabel akumulasi
    total_biaya_semua = 0.0
    total_pengeboran_semua = 0.0
    total_konsumsi_bahan_bakar = 0.0
    total_biaya_bahan_bakar = 0.0
    total_emisi_co2 = 0.0
    target_biaya_ideal = 0.0
    tekanan_total = 0.0
    kedalaman_total = 0.0

    hasil_percobaan = []

    for i, perc in enumerate(data_percobaan):
        nilai_input = perc["tekanan"]
        target_kedalaman = perc["target_kedalaman"]

        if nilai_input <= 0 or target_kedalaman <= 0:
            continue

        # Perhitungan (mengacu ke kode awal)
        kecepatan = k * nilai_input  # m/menit
        if kecepatan == 0:
            continue
        waktu = target_kedalaman / kecepatan  # menit
        biaya_total = (waktu / 60) * biaya_per_jam  # ubah ke jam
        total_pengeboran = waktu * kecepatan * k  # m (mengikuti rumus di kode asli)

        # Perhitungan tambahan
        konsumsi_bahan_bakar = hitung_konsumsi_bahan_bakar(jenis_mesin, waktu)
        biaya_bahan_bakar = hitung_biaya_bahan_bakar(
            konsumsi_bahan_bakar, harga_bahan_bakar
        )
        emisi_co2 = hitung_emisi_co2(konsumsi_bahan_bakar)
        tingkat_kesulitan = klasifikasi_tingkat_kesulitan(
            nilai_input, target_kedalaman
        )

        # Akumulasi
        tekanan_total += nilai_input
        kedalaman_total += target_kedalaman

        total_biaya_semua += biaya_total
        total_pengeboran_semua += total_pengeboran
        total_konsumsi_bahan_bakar += konsumsi_bahan_bakar
        total_biaya_bahan_bakar += biaya_bahan_bakar
        total_emisi_co2 += emisi_co2
        target_biaya_ideal += biaya_total * 0.9  # Target 10% lebih murah

        jam = int(waktu // 60)
        menit = int(waktu % 60)

        hasil_percobaan.append(
            {
                "Percobaan": i + 1,
                "Tekanan (bar)": nilai_input,
                "Target kedalaman (m)": target_kedalaman,
                "Kecepatan (m/menit)": round(kecepatan, 2),
                "Waktu (jam)": jam + menit / 60,
                "Biaya operasional": biaya_total,
                "Total pengeboran (m)": total_pengeboran,
                "BBM (liter)": konsumsi_bahan_bakar,
                "Biaya BBM": biaya_bahan_bakar,
                "Emisi CO2 (kg)": emisi_co2,
                "Tingkat kesulitan": tingkat_kesulitan,
            }
        )

    if not hasil_percobaan:
        st.warning("Tidak ada percobaan valid. Pastikan tekanan dan kedalaman > 0.")
    else:
        # RINGKASAN HASIL
        st.header("📊 Ringkasan Hasil Percobaan")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total biaya semua percobaan",
                format_rupiah(total_biaya_semua),
            )
        with col2:
            st.metric(
                "Total hasil pengeboran",
                f"{total_pengeboran_semua:.2f} m",
            )
        with col3:
            rata2_pengeboran = total_pengeboran_semua / len(hasil_percobaan)
            st.metric(
                "Rata-rata hasil pengeboran",
                f"{rata2_pengeboran:.2f} m",
            )

        st.subheader("Detail Per Percobaan")
        st.dataframe(hasil_percobaan, use_container_width=True)

        # ANALISIS BAHAN BAKAR & LINGKUNGAN
        st.header("⛽ Analisis Bahan Bakar & Lingkungan")
        col_bbm1, col_bbm2, col_bbm3 = st.columns(3)
        with col_bbm1:
            st.metric(
                "Total konsumsi bahan bakar",
                f"{total_konsumsi_bahan_bakar:.2f} liter",
            )
        with col_bbm2:
            st.metric(
                "Total biaya bahan bakar",
                format_rupiah(total_biaya_bahan_bakar),
            )
        with col_bbm3:
            st.metric(
                "Total estimasi emisi CO2",
                f"{total_emisi_co2:.2f} kg",
            )

        efisiensi_bahan_bakar = 0.0
        if total_pengeboran_semua > 0 and total_konsumsi_bahan_bakar > 0:
            efisiensi_bahan_bakar = total_pengeboran_semua / total_konsumsi_bahan_bakar
            st.write(
                f"**Efisiensi bahan bakar:** {efisiensi_bahan_bakar:.2f} m/liter"
            )
            st.success(beri_feedback_efisiensi(efisiensi_bahan_bakar))

        # ANALISIS EFISIENSI BIAYA
        st.header("💸 Analisis Efisiensi Biaya")
        efisiensi_biaya = hitung_efisiensi_biaya(
            total_biaya_semua, target_biaya_ideal
        )

        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            st.metric("Biaya aktual", format_rupiah(total_biaya_semua))
        with col_c2:
            st.metric("Target biaya ideal", format_rupiah(target_biaya_ideal))
        with col_c3:
            st.metric("Efisiensi biaya", f"{efisiensi_biaya:.1f}%")

        st.info(beri_feedback_biaya(efisiensi_biaya))

        # ANALISIS DAMPAK LINGKUNGAN
        st.header("🌍 Analisis Dampak Lingkungan")
        st.warning(beri_feedback_lingkungan(total_emisi_co2))

        # ============================================================
        # 📊 GRAFIK & DIAGRAM VISUALISASI HASIL
        # (diletakkan di dalam blok 'else' sehingga tidak menyebabkan
        #  indent/parse error dan hanya muncul jika ada hasil valid)
        # ============================================================

        st.header("📉 Grafik dan Diagram Visualisasi")

        tekanan_list = [p["Tekanan (bar)"] for p in hasil_percobaan]
        kedalaman_list = [p["Target kedalaman (m)"] for p in hasil_percobaan]
        biaya_list = [p["Biaya operasional"] for p in hasil_percobaan]
        bbm_list = [p["BBM (liter)"] for p in hasil_percobaan]
        emisi_list = [p["Emisi CO2 (kg)"] for p in hasil_percobaan]
        percobaan_ke = [p["Percobaan"] for p in hasil_percobaan]

        # --- GRAPH 1: Grafik Tekanan vs Kedalaman ---
        st.subheader("Grafik Tekanan vs Kedalaman")
        fig1, ax1 = plt.subplots()
        ax1.plot(tekanan_list, kedalaman_list, marker='o')
        ax1.set_xlabel("Tekanan (bar)")
        ax1.set_ylabel("Kedalaman (m)")
        ax1.set_title("Hubungan Tekanan dan Kedalaman")
        st.pyplot(fig1)

        # --- GRAPH 2: Grafik Biaya Operasional per Percobaan ---
        st.subheader("Grafik Biaya Operasional per Percobaan")
        fig2, ax2 = plt.subplots()
        ax2.bar(percobaan_ke, biaya_list)
        ax2.set_xlabel("Percobaan ke-")
        ax2.set_ylabel("Biaya Operasional (Rp)")
        ax2.set_title("Biaya Operasional Setiap Percobaan")
        st.pyplot(fig2)

        # --- GRAPH 3: Diagram Konsumsi Bahan Bakar ---
        st.subheader("Diagram Konsumsi Bahan Bakar")
        fig3, ax3 = plt.subplots()
        ax3.plot(percobaan_ke, bbm_list, marker='s')
        ax3.set_xlabel("Percobaan ke-")
        ax3.set_ylabel("Konsumsi BBM (liter)")
        ax3.set_title("Konsumsi Bahan Bakar per Percobaan")
        st.pyplot(fig3)

        # --- GRAPH 4: Pie Chart Persentase Emisi CO2 ---
        st.subheader("Diagram Pie Emisi CO2")
        fig4, ax4 = plt.subplots()
        # jika semua emisi 0, pie akan error; tangani kasus ini
        if sum(emisi_list) > 0:
            ax4.pie(
                emisi_list,
                labels=[f"Percobaan {i}" for i in percobaan_ke],
                autopct="%1.1f%%",
            )
        else:
            ax4.text(0.5, 0.5, "Tidak ada emisi untuk ditampilkan", ha='center', va='center')
        ax4.set_title("Proporsi Emisi CO2 per Percobaan")
        st.pyplot(fig4)

        # REKOMENDASI UNTUK PROYEK SELANJUTNYA
        st.header("🧭 Rekomendasi untuk Proyek Selanjutnya")
        rata2_kedalaman = total_pengeboran_semua / len(hasil_percobaan)
        tekanan_rata_rata = tekanan_total / len(hasil_percobaan)
        tingkat_kesulitan_dominan = klasifikasi_tingkat_kesulitan(
            tekanan_rata_rata, rata2_kedalaman
        )
        rekomendasi = rekomendasi_mesin_berdasarkan_kondisi(
            rata2_kedalaman, tingkat_kesulitan_dominan
        )

        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.metric("Rata-rata kedalaman", f"{rata2_kedalaman:.2f} m")
        with col_r2:
            st.metric("Rata-rata tekanan", f"{tekanan_rata_rata:.2f} bar")
        with col_r3:
            st.metric("Tingkat kesulitan", tingkat_kesulitan_dominan)
        with col_r4:
            st.metric("Rekomendasi mesin", rekomendasi)

        # EVALUASI PERFORMA KESELURUHAN
        st.header("📈 Evaluasi Performa Keseluruhan")
        performa_keseluruhan = hitung_performa_keseluruhan(
            efisiensi_bahan_bakar, efisiensi_biaya, total_pengeboran_semua
        )

        st.metric(
            "Skor Performa Keseluruhan",
            f"{performa_keseluruhan:.1f} / 100",
        )

        if performa_keseluruhan >= 80:
            st.success("🎉 SELAMAT! Performa proyek sangat memuaskan!")
        elif performa_keseluruhan >= 60:
            st.info("👍 Bagus! Performa proyek memenuhi ekspektasi.")
        else:
            st.warning(
                "💡 Saran: Perlu optimasi lebih lanjut untuk meningkatkan performa."
            )

        # FEEDBACK DARI DEVELOPER
        st.header("💬 Feedback dari Developer")
        st.write(beri_feedback_penggunaan_program(nama_anda, int(n)))

        # PENUTUP
        st.success(
            f"Terima kasih telah menggunakan program ini, {nama_anda}! "
            "Semoga analisis ini bermanfaat untuk perencanaan proyek Anda."
        )
else:
    st.info("Silakan lengkapi input dan tekan tombol **Hitung Biaya & Performa**.")
