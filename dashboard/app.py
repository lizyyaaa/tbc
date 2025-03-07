import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Kelayakan", layout="wide")

# Judul aplikasi
st.title("📊 Dashboard Kelayakan Rumah, Sanitasi, dan Perilaku")

# Sidebar untuk unggah file
st.sidebar.header("📂 Upload File Anda")
uploaded_file = st.sidebar.file_uploader("Unggah file CSV atau Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Deteksi format file
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension == "csv":
            df = pd.read_csv(uploaded_file, sep=None, engine='python')  # Deteksi delimiter otomatis
        elif file_extension == "xlsx":
            df = pd.read_excel(uploaded_file)
        
        # Menampilkan data awal
        st.subheader("📌 Data Awal")
        st.write(df.head())
        
        # Cleaning Data
        st.subheader("🧹 Cleaning Data")
        df_cleaned = df.drop_duplicates().fillna(df.median(numeric_only=True))
        st.write(df_cleaned.head())
        
        # Kategori pertanyaan
        kategori_rumah = ['langit_langit', 'lantai', 'dinding', 'jendela_kamar_tidur',
                          'jendela_ruang_keluarga', 'ventilasi', 'lubang_asap_dapur', 'pencahayaan']
        kategori_sanitasi = ['sarana_air_bersih', 'jamban', 'sarana_pembuangan_air_limbah', 
                             'sarana_pembuangan_sampah', 'sampah']
        kategori_perilaku = ['perilaku_merokok', 'anggota_keluarga_merokok', 'membuka_jendela_kamar_tidur',
                             'membuka_jendela_ruang_keluarga', 'membersihkan_rumah', 'membuang_tinja',
                             'membuang_sampah', 'kebiasaan_ctps']
        
        # Fungsi hitung skor kelayakan
        def hitung_skor(df, kategori, bobot):
            skor = []
            for _, row in df.iterrows():
                total_skor = 0
                max_skor = 0
                for kolom in kategori:
                    if kolom in bobot and row[kolom] in bobot[kolom]:
                        total_skor += bobot[kolom][row[kolom]]
                        max_skor += 5  # Maksimum skor tiap pertanyaan
                persentase_kelayakan = (total_skor / max_skor) * 100 if max_skor > 0 else 0
                skor.append(persentase_kelayakan)
            df["Skor Kelayakan"] = skor
            df["Label"] = df["Skor Kelayakan"].apply(lambda x: "Layak" if x >= 70 else "Tidak Layak")
            return df
        
        # Definisi bobot untuk setiap kategori
        bobot_rumah = {
            "langit_langit": {"Ada": 5, "Tidak ada": 1},
            "lantai": {"Ubin/keramik/marmer": 5, "Tanah": 1},
            "dinding": {"Permanen": 5, "Semi permanen": 3, "Bukan tembok": 1},
            "jendela_kamar_tidur": {"Ada": 5, "Tidak ada": 1},
            "ventilasi": {"Baik": 5, "Kurang Baik": 2, "Tidak Ada": 1},
            "lubang_asap_dapur": {"Ada": 5, "Tidak Ada": 1},
            "pencahayaan": {"Terang": 5, "Tidak Terang": 1}
        }

        bobot_sanitasi = {
            "sarana_air_bersih": {"Ada,milik sendiri & memenuhi syarat": 5, "Tidak Ada": 1},
            "jamban": {"Ada, leher angsa": 5, "Tidak Ada": 1},
            "sarana_pembuangan_air_limbah": {"Dialirkan ke saluran kota": 5, "Tidak ada": 1},
            "sarana_pembuangan_sampah": {"Ada, kedap air": 5, "Tidak Ada": 1},
            "sampah": {"Petugas": 5, "Sungai": 1}
        }

        bobot_perilaku = {
            "perilaku_merokok": {"Tidak": 5, "Ya": 1},
            "anggota_keluarga_merokok": {"Tidak": 5, "Ya": 1},
            "membuka_jendela_kamar_tidur": {"Setiap hari": 5, "Tidak pernah": 1},
            "membersihkan_rumah": {"Setiap hari": 5, "Tidak pernah": 1},
            "membuang_tinja": {"Setiap hari ke jamban": 5, "Sembarang": 1},
            "membuang_sampah": {"Dikelola baik": 5, "Sungai": 1},
            "kebiasaan_ctps": {"CTPS setiap aktivitas": 5, "Tidak pernah CTPS": 1}
        }
        
        # Menghitung skor kelayakan
        df_rumah = hitung_skor(df_cleaned, kategori_rumah, bobot_rumah)
        df_sanitasi = hitung_skor(df_cleaned, kategori_sanitasi, bobot_sanitasi)
        df_perilaku = hitung_skor(df_cleaned, kategori_perilaku, bobot_perilaku)
        
        # Menampilkan hasil
        st.subheader("📊 Perbandingan Kategori Tidak Layak")
        fig, ax = plt.subplots(figsize=(8, 5))
        kategori = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
        persentase = [
            (df_rumah["Label"].value_counts().get("Tidak Layak", 0) / len(df_rumah)) * 100,
            (df_sanitasi["Label"].value_counts().get("Tidak Layak", 0) / len(df_sanitasi)) * 100,
            (df_perilaku["Label"].value_counts().get("Tidak Layak", 0) / len(df_perilaku)) * 100
        ]
        ax.bar(kategori, persentase, color=['red', 'orange', 'blue'])
        ax.set_xlabel("Kategori")
        ax.set_ylabel("Persentase (%)")
        ax.set_title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
        ax.set_ylim(0, 100)
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        for i, v in enumerate(persentase):
            ax.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
else:
    st.info("Silakan unggah file untuk memulai analisis.")
