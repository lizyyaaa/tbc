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
        kategori_rumah = ['status_rumah', 'langit_langit', 'lantai', 'dinding', 'jendela_kamar_tidur',
                          'jendela_ruang_keluarga', 'ventilasi', 'lubang_asap_dapur', 'pencahayaan']
        kategori_sanitasi = ['sarana_air_bersih', 'jamban', 'sarana_pembuangan_air_limbah', 
                             'sarana_pembuangan_sampah', 'sampah']
        kategori_perilaku = ['perilaku_merokok', 'anggota_keluarga_merokok', 'membuka_jendela_kamar_tidur',
                             'membuka_jendela_ruang_keluarga', 'membersihkan_rumah', 'membuang_tinja',
                             'membuang_sampah', 'kebiasaan_ctps', 'memiliki_hewan_ternak']
        
        # Fungsi hitung skor kelayakan
        def hitung_skor(df, kategori):
            if not set(kategori).issubset(df.columns):
                return None
            
            skor = df[kategori].notnull().sum(axis=1) / len(kategori) * 100
            df_skor = df[kategori].copy()
            df_skor["Skor Kelayakan"] = skor
            return df_skor
        
        # Menghitung skor kelayakan
        df_rumah = hitung_skor(df_cleaned, kategori_rumah)
        df_sanitasi = hitung_skor(df_cleaned, kategori_sanitasi)
        df_perilaku = hitung_skor(df_cleaned, kategori_perilaku)
        
        # Menampilkan hasil
        if df_rumah is not None:
            st.subheader("🏠 Skor Kelayakan Rumah")
            st.write(df_rumah.head())
        if df_sanitasi is not None:
            st.subheader("🚰 Skor Kelayakan Sanitasi")
            st.write(df_sanitasi.head())
        if df_perilaku is not None:
            st.subheader("🛡️ Skor Kelayakan Perilaku")
            st.write(df_perilaku.head())
        
        # Persentase Tidak Layak
        threshold = 70
        def hitung_persentase(df):
            return (df["Skor Kelayakan"] < threshold).sum() / len(df) * 100 if df is not None else 0
        
        persentase_tidak_layak_rumah = hitung_persentase(df_rumah)
        persentase_tidak_layak_sanitasi = hitung_persentase(df_sanitasi)
        persentase_tidak_layak_perilaku = hitung_persentase(df_perilaku)
        
        # Menampilkan hasil persentase
        st.subheader("📊 Persentase Tidak Layak")
        col1, col2, col3 = st.columns(3)
        col1.metric("Rumah Tidak Layak", f"{persentase_tidak_layak_rumah:.2f}%")
        col2.metric("Sanitasi Tidak Layak", f"{persentase_tidak_layak_sanitasi:.2f}%")
        col3.metric("Perilaku Tidak Baik", f"{persentase_tidak_layak_perilaku:.2f}%")
        
        # Visualisasi
        st.subheader("📊 Visualisasi Data")
        fig, ax = plt.subplots()
        if df_rumah is not None:
            sns.histplot(df_rumah["Skor Kelayakan"], bins=20, kde=True, ax=ax)
        st.pyplot(fig)
        
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
else:
    st.info("Silakan unggah file untuk memulai analisis.")
