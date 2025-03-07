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

        # Menghitung skor kelayakan
        df_rumah = hitung_skor(df_cleaned, kategori_rumah, bobot_rumah)
        
        # Menampilkan hasil
        st.subheader("🏠 Skor Kelayakan Rumah")
        st.write(df_rumah.head())
        
        # Persentase Tidak Layak
        persentase_tidak_layak = (df_rumah["Label"].value_counts().get("Tidak Layak", 0) / len(df_rumah)) * 100
        st.subheader("📊 Persentase Rumah Tidak Layak")
        st.metric("Rumah Tidak Layak", f"{persentase_tidak_layak:.2f}%")
        
        # Visualisasi
        st.subheader("📊 Visualisasi Skor Kelayakan Rumah")
        fig, ax = plt.subplots()
        sns.histplot(df_rumah["Skor Kelayakan"], bins=20, kde=True, ax=ax)
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
else:
    st.info("Silakan unggah file untuk memulai analisis.")
