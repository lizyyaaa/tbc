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
    # Cek format file
    file_extension = uploaded_file.name.split(".")[-1]
    if file_extension == "csv":
        df = pd.read_csv(uploaded_file)
    elif file_extension == "xlsx":
        df = pd.read_excel(uploaded_file)

    # Menampilkan data awal
    st.subheader("📌 Data Awal")
    st.write(df.head())

    # Kategori pertanyaan
    kategori_rumah = ['status_rumah', 'langit_langit', 'lantai', 'dinding', 'jendela_kamar_tidur',
                      'jendela_ruang_keluarga', 'ventilasi', 'lubang_asap_dapur', 'pencahayaan']
    kategori_sanitasi = ['sarana_air_bersih', 'jamban', 'sarana_pembuangan_air_limbah', 
                         'sarana_pembuangan_sampah', 'sampah']
    kategori_perilaku = ['perilaku_merokok', 'anggota_keluarga_merokok', 'membuka_jendela_kamar_tidur',
                         'membuka_jendela_ruang_keluarga', 'membersihkan_rumah', 'membuang_tinja',
                         'membuang_sampah', 'kebiasaan_ctps', 'memiliki_hewan_ternak']

    # Cleaning Data
    st.subheader("🧹 Cleaning Data")
    df_cleaned = df.fillna(df.median(numeric_only=True)).drop_duplicates()
    st.write(df_cleaned.head())

    # Fungsi hitung skor kelayakan
    def hitung_skor(df, kategori, bobot):
        skor = []
        for _, row in df.iterrows():
            total_skor = 0
            max_skor = 0
            for kolom in kategori:
                if kolom in bobot and row[kolom] in bobot[kolom]:
                    total_skor += bobot[kolom][row[kolom]]
                    max_skor += 5
            persentase_kelayakan = (total_skor / max_skor) * 100 if max_skor > 0 else 0
            skor.append(persentase_kelayakan)
        df["Skor Kelayakan"] = skor
        return df

    # Definisi bobot untuk setiap kategori
    bobot_rumah = {
        "langit_langit": {"Ada": 5, "Tidak ada": 1},
        "lantai": {"Ubin/keramik/marmer": 5, "Tanah": 1},
        "dinding": {"Permanen": 5, "Semi permanen": 3, "Bukan tembok": 1},
        "jendela_kamar_tidur": {"Ada": 5, "Tidak ada": 1},
        "jendela_ruang_keluarga": {"Ada": 5, "Tidak ada": 1},
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
    df_rumah = hitung_skor(df_cleaned[kategori_rumah].dropna(), kategori_rumah, bobot_rumah)
    df_sanitasi = hitung_skor(df_cleaned[kategori_sanitasi].dropna(), kategori_sanitasi, bobot_sanitasi)
    df_perilaku = hitung_skor(df_cleaned[kategori_perilaku].dropna(), kategori_perilaku, bobot_perilaku)

    # Menampilkan hasil
    st.subheader("🏠 Skor Kelayakan Rumah")
    st.write(df_rumah.head())

    st.subheader("🚰 Skor Kelayakan Sanitasi")
    st.write(df_sanitasi.head())

    st.subheader("🛡️ Skor Kelayakan Perilaku")
    st.write(df_perilaku.head())

    # Label Layak/Tidak Layak
    threshold = 70
    df_rumah["Label"] = df_rumah["Skor Kelayakan"].apply(lambda x: "Layak" if x >= threshold else "Tidak Layak")
    df_sanitasi["Label"] = df_sanitasi["Skor Kelayakan"].apply(lambda x: "Layak" if x >= threshold else "Tidak Layak")
    df_perilaku["Label"] = df_perilaku["Skor Kelayakan"].apply(lambda x: "Layak" if x >= threshold else "Tidak Layak")

    # Persentase Tidak Layak
    persentase_tidak_layak_rumah = (df_rumah["Label"].value_counts().get("Tidak Layak", 0) / len(df_rumah)) * 100
    persentase_tidak_layak_sanitasi = (df_sanitasi["Label"].value_counts().get("Tidak Layak", 0) / len(df_sanitasi)) * 100
    persentase_tidak_layak_perilaku = (df_perilaku["Label"].value_counts().get("Tidak Layak", 0) / len(df_perilaku)) * 100

    # Menampilkan hasil persentase
    st.subheader("📊 Persentase Tidak Layak")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rumah Tidak Layak", f"{persentase_tidak_layak_rumah:.2f}%")
    col2.metric("Sanitasi Tidak Layak", f"{persentase_tidak_layak_sanitasi:.2f}%")
    col3.metric("Perilaku Tidak Baik", f"{persentase_tidak_layak_perilaku:.2f}%")

    # Visualisasi
    st.subheader("📊 Visualisasi Data")
    fig, ax = plt.subplots()
    sns.histplot(df_rumah["Skor Kelayakan"], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

else:
    st.info("Silakan unggah file untuk memulai analisis.")
