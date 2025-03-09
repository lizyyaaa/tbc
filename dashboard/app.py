import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from datetime import datetime

# Atur tema Seaborn
sns.set_theme(style="whitegrid")

# Judul utama dengan emoji
st.title("📊 Dashboard Analisis Data TBC")

# Sidebar dengan judul dan emoji
st.sidebar.header("⚙️ Input & Navigasi")

# Upload File CSV di sidebar
uploaded_file = st.sidebar.file_uploader("📂 Upload file CSV", type=["csv"])

# Daftar visualisasi dengan "Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak" di posisi pertama
visualisasi_list = [
    "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak",
    "📈 Kebiasaan CTPS vs Jumlah Pasien",
    "🐑 Memiliki Hewan Ternak vs Jumlah Pasien",
    "🏠 Perbandingan Rumah Layak vs Tidak Layak (Jumlah)",
    "✅ Persentase Rumah Layak vs Tidak Layak",
    "🧩 Pie Chart Rumah Layak vs Tidak Layak",
    "🚰 Pie Chart Sanitasi Layak vs Tidak Layak",
    "🚩 Pie Chart Perilaku Baik vs Tidak Baik",
    "🏚️ Kategori Rumah Tidak Layak (Detail)",
    "🚽 Kategori Sanitasi Tidak Layak (Detail)",
    "🚮 Kategori Perilaku Tidak Sehat (Detail)"
]

# Pilihan visualisasi
pilihan = st.sidebar.selectbox("Pilih Visualisasi", visualisasi_list)

# Fungsi untuk menyimpan gambar ke BytesIO dan menampilkan tombol download
def download_chart():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    st.download_button(
        label="⬇️ Download Gambar",
        data=buffer,
        file_name="chart.png",
        mime="image/png"
    )
    buffer.close()

# Jika file diupload, lanjutkan
if uploaded_file:
    # Baca data
    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
    
    # --- Preprocessing ---
    kolom_numerik = df.select_dtypes(include=['number']).columns
    kolom_kategori = df.select_dtypes(include=['object']).columns
    df[kolom_kategori] = df[kolom_kategori].apply(lambda x: x.fillna(x.mode()[0]))
    df[kolom_numerik] = df[kolom_numerik].apply(lambda x: x.fillna(x.mean()))
    df = df.drop_duplicates()

    # Pastikan kolom date_start format datetime
    if "date_start" in df.columns:
        df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")
        df["year_month"] = df["date_start"].dt.to_period("M").astype(str)

    # Definisi kategori
    kategori_rumah = [
        'langit_langit', 'lantai', 'dinding', 'jendela_kamar_tidur',
        'jendela_ruang_keluarga', 'ventilasi', 'lubang_asap_dapur', 'pencahayaan'
    ]
    kategori_sanitasi = [
        'sarana_air_bersih', 'jamban', 'sarana_pembuangan_air_limbah', 
        'sarana_pembuangan_sampah', 'sampah'
    ]
    kategori_perilaku = [
        'perilaku_merokok', 'anggota_keluarga_merokok', 'membuka_jendela_kamar_tidur',
        'membuka_jendela_ruang_keluarga', 'membersihkan_rumah', 'membuang_tinja',
        'membuang_sampah', 'kebiasaan_ctps'
    ]

    # Pisahkan data
    df_rumah = df[kategori_rumah].dropna()
    df_sanitasi = df[kategori_sanitasi].dropna()
    df_perilaku = df[kategori_perilaku].dropna()

    # Fungsi hitung skor
    def hitung_skor(df_sub, kategori, bobot):
        skor = []
        for _, row in df_sub.iterrows():
            total_skor = 0
            max_skor = 0
            for kolom in kategori:
                if kolom in bobot and row[kolom] in bobot[kolom]:
                    total_skor += bobot[kolom][row[kolom]]
                    max_skor += 5
            skor.append((total_skor / max_skor) * 100 if max_skor else 0)
        df_sub["Skor Kelayakan"] = skor
        return df_sub

    # Bobot
    bobot_rumah = {
        "langit_langit": {"Ada": 5, "Tidak ada": 1},
        "lantai": {"Ubin/keramik/marmer": 5, "Baik": 4, "Kurang Baik": 3, "Papan/Anyaman Bambu/Plester Retak": 2, "Tanah": 1},
        "dinding": {"Permanen (tembok pasangan batu bata yang diplester)": 5, "Semi permanen bata/batu yang tidak diplester/papan kayu": 3, "Bukan tembok (papan kayu/bambu/ilalang)": 1},
        "jendela_kamar_tidur": {"Ada": 5, "Tidak ada": 1},
        "jendela_ruang_keluarga": {"Ada": 5, "Tidak ada": 1},
        "ventilasi": {"Baik": 5, "Ada, luas ventilasi > 10% dari luas lantai": 4, "Ada, luas ventilasi < 10% dari luas lantai": 3, "Kurang Baik": 2, "Tidak Ada": 1},
        "lubang_asap_dapur": {"Ada, luas ventilasi > 10% luas lantai dapur/exhaust vent": 5, "Ada, luas ventilasi < 10% dari luas lantai dapur": 3, "Tidak Ada": 1},
        "pencahayaan": {"Terang/Dapat digunakan membaca normal": 5, "Baik": 4, "Kurang Baik": 3, "Kurang Terang": 2, "Tidak Terang/Kurang Jelas untuk membaca": 1}
    }
    bobot_sanitasi = {
        "sarana_air_bersih": {
            "Ada,milik sendiri & memenuhi syarat kesehatan": 5,
            "Ada,bukan milik sendiri & memenuhi syarat kesehatan": 4,
            "Ada,milik sendiri & tidak memenuhi syarat kesehatan": 3,
            "Ada, bukan milik sendiri & tidak memenuhi syarat kesehatan": 2,
            "Tidak Ada": 1
        },
        "jamban": {
            "Ada, leher angsa": 5,
            "Ada tutup & septic tank": 4,
            "Ada,bukan leher angsa ada tutup & septic tank": 3,
            "Ada,bukan leher angsa ada tutup & dialirkan ke sungai": 2,
            "Ada, bukan leher angsa tidak bertutup & dialirkan ke sungai": 2,
            "Tidak Ada": 1
        },
        "sarana_pembuangan_air_limbah": {
            'Ada, dialirkan ke selokan tertutup ("&"saluran kota) utk diolah lebih lanjut': 5,
            "Ada, bukan milik sendiri & memenuhi syarat kesehatan": 4,
            "Ada, diresapkan ke selokan terbuka": 3,
            "Ada, diresapkan tetapi mencemari sumber air (jarak <10m)": 2,
            "Tidak ada, sehingga tergenang dan tidak teratur di halaman/belakang rumah": 1
        },
        "sarana_pembuangan_sampah": {
            "Ada, kedap air dan tertutup": 5,
            "Ada, kedap air dan tidak tertutup": 4,
            "Ada, tetapi tidak kedap air dan tidak tertutup": 3,
            "Tidak Ada": 1
        },
        "sampah": {
            "Petugas": 5,
            "Dikelola Sendiri (Pilah Sampah)": 4,
            "Bakar": 3,
            "dll": 2,
            "Lainnya (Sungai)": 1
        }
    }
    bobot_perilaku = {
        "perilaku_merokok": {"Tidak": 5, "Ya": 1},
        "anggota_keluarga_merokok": {"Tidak": 5, "Ya": 1},
        "membuka_jendela_kamar_tidur": {"Setiap hari dibuka": 5, "Kadang-kadang dibuka": 3, "Tidak pernah dibuka": 1},
        "membuka_jendela_ruang_keluarga": {"Setiap hari dibuka": 5, "Kadang-kadang dibuka": 3, "Tidak pernah dibuka": 1},
        "membersihkan_rumah": {"Setiap hari dibersihkan": 5, "Kadang-kadang": 3, "Tidak pernah dibersihkan": 1},
        "membuang_tinja": {"Setiap hari ke jamban": 5, "Dibuang ke sungai/kebun/kolam/sembarangan": 1},
        "membuang_sampah": {"Dibuang ke tempat sampah/ada petugas sampah": 5, "Dilakukan pilah sampah/dikelola dengan baik": 4, "Kadang-kadang dibuang ke tempat sampah": 3, "Dibuang ke sungai/kebun/kolam/sembarangan / dibakar": 1},
        "kebiasaan_ctps": {"CTPS setiap aktivitas": 5, "Kadang-kadang CTPS": 3, "Tidak pernah CTPS": 1}
    }

    # Hitung skor
    df_rumah = hitung_skor(df_rumah, kategori_rumah, bobot_rumah)
    df_sanitasi = hitung_skor(df_sanitasi, kategori_sanitasi, bobot_sanitasi)
    df_perilaku = hitung_skor(df_perilaku, kategori_perilaku, bobot_perilaku)

    threshold = 70
    def label_kelayakan(skor):
        return "Layak" if skor >= threshold else "Tidak Layak"

    df_rumah["Label"] = df_rumah["Skor Kelayakan"].apply(label_kelayakan)
    df_sanitasi["Label"] = df_sanitasi["Skor Kelayakan"].apply(label_kelayakan)
    df_perilaku["Label"] = df_perilaku["Skor Kelayakan"].apply(label_kelayakan)

    persentase_tidak_layak_rumah = (df_rumah[df_rumah["Label"] == "Tidak Layak"].shape[0] / df_rumah.shape[0]) * 100
    persentase_tidak_layak_sanitasi = (df_sanitasi[df_sanitasi["Label"] == "Tidak Layak"].shape[0] / df_sanitasi.shape[0]) * 100
    persentase_tidak_baik_perilaku = (df_perilaku[df_perilaku["Label"] == "Tidak Layak"].shape[0] / df_perilaku.shape[0]) * 100

    st.markdown(
        f"""
        **Persentase Rumah Tidak Layak**: {persentase_tidak_layak_rumah:.2f}%  
        **Persentase Sanitasi Tidak Layak**: {persentase_tidak_layak_sanitasi:.2f}%  
        **Persentase Perilaku Tidak Baik**: {persentase_tidak_baik_perilaku:.2f}%  
        """
    )

    # Fungsi untuk menampilkan chart dan download
    def tampilkan_dan_download():
        st.pyplot(plt.gcf())
        download_chart()
        plt.clf()

    # --- Visualisasi Berdasarkan Pilihan ---
    if pilihan == "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
        st.subheader("📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
        kategori_overall = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
        persentase_overall = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
        sorted_idx = sorted(range(len(persentase_overall)), key=lambda i: persentase_overall[i], reverse=True)
        kategori_overall = [kategori_overall[i] for i in sorted_idx]
        persentase_overall = [persentase_overall[i] for i in sorted_idx]

        plt.figure(figsize=(8, 4))
        plt.bar(kategori_overall, persentase_overall, color=['red', 'orange', 'blue'])
        plt.xlabel("Kategori")
        plt.ylabel("Persentase (%)")
        plt.title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
        plt.ylim(0, 100)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        for i, v in enumerate(persentase_overall):
            plt.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
        tampilkan_dan_download()

    elif pilihan == "📈 Kebiasaan CTPS vs Jumlah Pasien":
        st.subheader("📈 Kebiasaan CTPS vs Jumlah Pasien")
        data_ctps = df.groupby("kebiasaan_ctps")["pasien"].count().reset_index()
        data_ctps.columns = ["kebiasaan_ctps", "jumlah_pasien"]
        data_ctps = data_ctps.sort_values(by="jumlah_pasien", ascending=False)
        total_pasien_ctps = data_ctps["jumlah_pasien"].sum()
        data_ctps["persentase"] = (data_ctps["jumlah_pasien"] / total_pasien_ctps) * 100

        plt.figure(figsize=(8, 4))
        sns.barplot(x="jumlah_pasien", y="kebiasaan_ctps", data=data_ctps, palette="ch:s=.25,rot=-.25")
        plt.title("Kebiasaan CTPS vs Jumlah Pasien", fontsize=14, fontweight="bold")
        plt.xlabel("Jumlah Pasien", fontsize=12)
        plt.ylabel("Kebiasaan CTPS", fontsize=12)
        plt.grid(axis="x", linestyle="--", alpha=0.6)
        for idx, (value, pct) in enumerate(zip(data_ctps["jumlah_pasien"], data_ctps["persentase"])):
            plt.text(value + 1, idx, f"{value} ({pct:.1f}%)", va='center', fontsize=10, color="black")
        tampilkan_dan_download()

    elif pilihan == "🐑 Memiliki Hewan Ternak vs Jumlah Pasien":
        st.subheader("🐑 Memiliki Hewan Ternak vs Jumlah Pasien")
        data_ternak = df.groupby("memiliki_hewan_ternak")["pasien"].count().reset_index()
        data_ternak.columns = ["memiliki_hewan_ternak", "jumlah_pasien"]
        data_ternak = data_ternak.sort_values(by="jumlah_pasien", ascending=False)
        total_pasien_ternak = data_ternak["jumlah_pasien"].sum()
        data_ternak["persentase"] = (data_ternak["jumlah_pasien"] / total_pasien_ternak) * 100

        plt.figure(figsize=(8, 4))
        sns.barplot(x="jumlah_pasien", y="memiliki_hewan_ternak", data=data_ternak, palette="magma_r")
        plt.title("Memiliki Hewan Ternak vs Jumlah Pasien", fontsize=14, fontweight="bold")
        plt.xlabel("Jumlah Pasien", fontsize=12)
        plt.ylabel("Memiliki Hewan Ternak", fontsize=12)
        plt.grid(axis="x", linestyle="--", alpha=0.6)
        for idx, (value, pct) in enumerate(zip(data_ternak["jumlah_pasien"], data_ternak["persentase"])):
            plt.text(value + 1, idx, f"{value} ({pct:.1f}%)", va='center', fontsize=10, color="black")
        tampilkan_dan_download()

    elif pilihan == "🏠 Perbandingan Rumah Layak vs Tidak Layak (Jumlah)":
        st.subheader("🏠 Perbandingan Rumah Layak vs Tidak Layak (Jumlah)")
        jumlah_rumah_layak = df_rumah[df_rumah["Label"] == "Layak"].shape[0]
        jumlah_rumah_tidak_layak = df_rumah[df_rumah["Label"] == "Tidak Layak"].shape[0]
        kategori_rumah_status = ["Layak", "Tidak Layak"]
        jumlah_rumah = [jumlah_rumah_layak, jumlah_rumah_tidak_layak]

        plt.figure(figsize=(8, 4))
        plt.bar(kategori_rumah_status, jumlah_rumah, color=['green', 'red'])
        plt.xlabel("Kondisi Rumah")
        plt.ylabel("Jumlah")
        plt.title("Perbandingan Rumah Layak dan Tidak Layak")
        plt.ylim(0, max(jumlah_rumah) + 10)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        for i, v in enumerate(jumlah_rumah):
            plt.text(i, v + 2, str(v), ha="center", fontsize=10)
        tampilkan_dan_download()

    elif pilihan == "✅ Persentase Rumah Layak vs Tidak Layak":
        st.subheader("✅ Persentase Rumah Layak vs Tidak Layak")
        persentase_layak_rumah = 100 - persentase_tidak_layak_rumah
        kategori_rumah_pct = ["Layak", "Tidak Layak"]
        persentase_rumah = [persentase_layak_rumah, persentase_tidak_layak_rumah]

        plt.figure(figsize=(8, 4))
        plt.bar(kategori_rumah_pct, persentase_rumah, color=['green', 'red'])
        plt.xlabel("Kondisi Rumah")
        plt.ylabel("Persentase (%)")
        plt.title("Persentase Rumah Layak dan Tidak Layak")
        plt.ylim(0, 100)
        plt.grid(axis="y", linestyle="--", alpha=0.7)
        for i, v in enumerate(persentase_rumah):
            plt.text(i, v + 2, f"{v:.2f}%", ha="center", fontsize=10)
        tampilkan_dan_download()

    elif pilihan == "🧩 Pie Chart Rumah Layak vs Tidak Layak":
        st.subheader("🧩 Pie Chart Rumah Layak vs Tidak Layak")
        labels = ["Layak", "Tidak Layak"]
        sizes = [100 - persentase_tidak_layak_rumah, persentase_tidak_layak_rumah]
        colors = ['#4CAF50', '#E74C3C']
        explode = (0, 0.1)
        plt.figure(figsize=(8, 4))
        wedges, texts, autotexts = plt.pie(
            sizes, labels=labels, autopct='%1.1f%%', colors=colors,
            startangle=140, explode=explode, shadow=True,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.2}
        )
        for autotext in autotexts:
            autotext.set_fontsize(12)
            autotext.set_weight("bold")
        plt.title("Persentase Rumah Layak dan Tidak Layak", fontsize=14, fontweight="bold")
        tampilkan_dan_download()

    elif pilihan == "🚰 Pie Chart Sanitasi Layak vs Tidak Layak":
        st.subheader("🚰 Pie Chart Sanitasi Layak vs Tidak Layak")
        persentase_layak_sanitasi = 100 - persentase_tidak_layak_sanitasi
        labels_sanitasi = ["Layak", "Tidak Layak"]
        sizes_sanitasi = [persentase_layak_sanitasi, persentase_tidak_layak_sanitasi]
        colors_sanitasi = ['#3498DB', '#E74C3C']
        explode_sanitasi = (0, 0.1)
        plt.figure(figsize=(8, 4))
        wedges, texts, autotexts = plt.pie(
            sizes_sanitasi, labels=labels_sanitasi, autopct='%1.1f%%', colors=colors_sanitasi,
            startangle=140, explode=explode_sanitasi, shadow=True,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.2}
        )
        for autotext in autotexts:
            autotext.set_fontsize(12)
            autotext.set_weight("bold")
        plt.title("Persentase Sanitasi Layak dan Tidak Layak", fontsize=14, fontweight="bold")
        tampilkan_dan_download()

    elif pilihan == "🚩 Pie Chart Perilaku Baik vs Tidak Baik":
        st.subheader("🚩 Pie Chart Perilaku Baik vs Tidak Baik")
        persentase_baik_perilaku = 100 - persentase_tidak_baik_perilaku
        labels_perilaku = ["Baik", "Tidak Baik"]
        sizes_perilaku = [persentase_baik_perilaku, persentase_tidak_baik_perilaku]
        colors_perilaku = ['#1F77B4', '#FF7F0E']
        explode_perilaku = (0, 0.1)
        plt.figure(figsize=(8, 4))
        wedges, texts, autotexts = plt.pie(
            sizes_perilaku, labels=labels_perilaku, autopct='%1.1f%%', colors=colors_perilaku,
            startangle=140, explode=explode_perilaku, shadow=True,
            wedgeprops={'edgecolor': 'black', 'linewidth': 1.2}
        )
        for autotext in autotexts:
            autotext.set_fontsize(12)
            autotext.set_weight("bold")
        plt.title("Persentase Perilaku Baik dan Tidak Baik", fontsize=14, fontweight="bold")
        tampilkan_dan_download()

    elif pilihan == "🏚️ Kategori Rumah Tidak Layak (Detail)":
        st.subheader("🏚️ Kategori Rumah Tidak Layak (Detail)")
        df = df.fillna('')
        total_rumah = len(df)
        kategori_rumah_detail = {
            "Luas ventilasi ≤ 10% dari luas lantai": df['ventilasi'].str.contains('luas ventilasi < 10%', case=False, na=False).sum(),
            "Pencahayaan kurang terang, kurang jelas untuk membaca normal": df['pencahayaan'].str.contains('kurang terang', case=False, na=False).sum(),
            "Lubang asap dapur dengan luas ventilasi < 10% dari luas lantai dapur": df['lubang_asap_dapur'].str.contains('luas ventilasi < 10%', case=False, na=False).sum(),
            "Tidak Ada Jendela di Rumah": df['ventilasi'].str.contains('tidak ada', case=False, na=False).sum(),
            "Tidak Ada Langit-Langit": df['langit_langit'].str.contains('tidak ada', case=False, na=False).sum(),
            "Lantai Papan/anyaman bambu/plester retak berdebu": df['lantai'].str.contains('papan|anyaman bambu|plester retak', case=False, na=False).sum(),
            "Tidak ada lubang asap dapur": df['lubang_asap_dapur'].str.contains('tidak ada', case=False, na=False).sum(),
            "Lantai Tanah": df['lantai'].str.contains('tanah', case=False, na=False).sum(),
        }
        kategori_rumah_detail = {k: v for k, v in kategori_rumah_detail.items() if v > 0}
        df_kategori_rumah = pd.DataFrame(list(kategori_rumah_detail.items()), columns=['Kategori', 'Jumlah'])
        df_kategori_rumah['Persentase'] = (df_kategori_rumah['Jumlah'] / total_rumah) * 100
        df_kategori_rumah = df_kategori_rumah.sort_values(by='Jumlah', ascending=False)

        plt.figure(figsize=(8, 4))
        colors = sns.color_palette("viridis", len(df_kategori_rumah))
        ax = sns.barplot(x=df_kategori_rumah['Jumlah'], y=df_kategori_rumah['Kategori'], palette=colors)
        for idx, (value, pct) in enumerate(zip(df_kategori_rumah['Jumlah'], df_kategori_rumah['Persentase'])):
            plt.text(value + 1, idx, f"{value} rumah ({pct:.1f}%)", va='center')
        plt.xlabel("Jumlah Rumah", fontsize=12)
        plt.ylabel("Kategori Rumah Tidak Layak", fontsize=12)
        plt.title("Kategori Rumah Tidak Layak", fontsize=14, fontweight='bold')
        plt.xlim(0, df_kategori_rumah['Jumlah'].max() + 5)
        tampilkan_dan_download()

    elif pilihan == "🚽 Kategori Sanitasi Tidak Layak (Detail)":
        st.subheader("🚽 Kategori Sanitasi Tidak Layak (Detail)")
        total_rumah = len(df)
        kategori_sanitasi_detail = {
            "Jamban bukan leher angsa, tidak bertutup & dialirkan ke sungai": df['jamban'].apply(lambda x: 'tidak bertutup' in str(x).lower() and 'sungai' in str(x).lower()).sum(),
            "Sarana air bersih bukan milik sendiri & tidak memenuhi syarat kesehatan": df['sarana_air_bersih'].apply(lambda x: 'bukan milik sendiri' in str(x).lower() and 'tidak memenuhi' in str(x).lower()).sum(),
            "Tidak ada Sarana Air Bersih": df['sarana_air_bersih'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
            "SPAL diresapkan tetapi mencemari sumber air (jarak <10m)": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'diresapkan' in str(x).lower() and 'mencemari' in str(x).lower()).sum(),
            "Tidak ada jamban": df['jamban'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
            "Jamban bukan leher angsa, ada tutup & dialirkan ke sungai": df['jamban'].apply(lambda x: 'bukan leher angsa' in str(x).lower() and 'tutup' in str(x).lower() and 'sungai' in str(x).lower()).sum(),
            "Tidak ada Sarana Pembuangan Sampah": df['sarana_pembuangan_sampah'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
            "Tidak ada SPAL": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'tidak ada' in str(x).lower()).sum(),
            "Sarana air bersih milik sendiri & tidak memenuhi syarat kesehatan": df['sarana_air_bersih'].apply(lambda x: 'milik sendiri' in str(x).lower() and 'tidak memenuhi' in str(x).lower()).sum(),
            "Jamban bukan leher angsa, ada tutup & septic tank": df['jamban'].apply(lambda x: 'bukan leher angsa' in str(x).lower() and 'tutup' in str(x).lower() and 'septic tank' in str(x).lower()).sum(),
            "Sarana Pembuangan Sampah tidak kedap air dan tidak tertutup": df['sarana_pembuangan_sampah'].apply(lambda x: 'tidak kedap' in str(x).lower() and 'tidak tertutup' in str(x).lower()).sum(),
            "SPAL bukan milik sendiri & memenuhi syarat kesehatan": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'bukan milik sendiri' in str(x).lower() and 'memenuhi' in str(x).lower()).sum(),
            "SPAL diresapkan ke selokan terbuka": df['sarana_pembuangan_air_limbah'].apply(lambda x: 'diresapkan' in str(x).lower() and 'selokan terbuka' in str(x).lower()).sum(),
            "Sarana air bersih bukan milik sendiri & memenuhi syarat kesehatan": df['sarana_air_bersih'].apply(lambda x: 'bukan milik sendiri' in str(x).lower() and 'memenuhi' in str(x).lower()).sum(),
            "Sarana Pembuangan Sampah kedap air dan tidak tertutup": df['sarana_pembuangan_sampah'].apply(lambda x: 'kedap air' in str(x).lower() and 'tidak tertutup' in str(x).lower()).sum()
        }
        kategori_sanitasi_detail = {k: v for k, v in kategori_sanitasi_detail.items() if v > 0}
        df_kategori_sanitasi = pd.DataFrame(list(kategori_sanitasi_detail.items()), columns=['Kategori', 'Jumlah'])
        df_kategori_sanitasi['Persentase'] = (df_kategori_sanitasi['Jumlah'] / total_rumah) * 100
        df_kategori_sanitasi = df_kategori_sanitasi.sort_values(by='Jumlah', ascending=False)

        plt.figure(figsize=(8, 4))
        colors = sns.color_palette("crest", len(df_kategori_sanitasi))
        ax = sns.barplot(x=df_kategori_sanitasi['Jumlah'], y=df_kategori_sanitasi['Kategori'], palette=colors, edgecolor="black")
        for idx, (value, pct) in enumerate(zip(df_kategori_sanitasi['Jumlah'], df_kategori_sanitasi['Persentase'])):
            plt.text(value + 1, idx, f"{value} rumah ({pct:.1f}%)", va='center', fontsize=11, color='black')
        plt.xlabel("Jumlah Rumah", fontsize=12)
        plt.ylabel("Kategori Sanitasi Tidak Layak", fontsize=12)
        plt.title("Kategori Sanitasi Tidak Layak", fontsize=14, fontweight='bold')
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        tampilkan_dan_download()

    elif pilihan == "🚮 Kategori Perilaku Tidak Sehat (Detail)":
        st.subheader("🚮 Kategori Perilaku Tidak Sehat (Detail)")
        total_rumah = len(df)
        kategori_perilaku_detail = {
            "BAB di sungai / kebun / kolam / sembarangan": df['membuang_tinja'].apply(lambda x: any(word in str(x).lower() for word in ['sungai', 'kebun', 'kolam', 'sembarangan'])).sum(),
            "Tidak CTPS": df['kebiasaan_ctps'].apply(lambda x: 'tidak' in str(x).lower()).sum(),
            "Tidak pernah membersihkan rumah dan halaman": df['membersihkan_rumah'].apply(lambda x: 'tidak pernah' in str(x).lower()).sum(),
            "Buang sampah ke sungai / kebun / kolam / sembarangan / dibakar": df['membuang_sampah'].apply(lambda x: any(word in str(x).lower() for word in ['sungai', 'kebun', 'kolam', 'sembarangan', 'dibakar'])).sum(),
            "Tidak pernah buka jendela ruang keluarga": df['membuka_jendela_ruang_keluarga'].apply(lambda x: 'tidak pernah' in str(x).lower()).sum(),
            "Tidak pernah buka jendela kamar tidur": df['membuka_jendela_kamar_tidur'].apply(lambda x: 'tidak pernah' in str(x).lower()).sum(),
        }
        kategori_perilaku_detail = {k: v for k, v in kategori_perilaku_detail.items() if v > 0}
        df_kategori_perilaku = pd.DataFrame(list(kategori_perilaku_detail.items()), columns=['Kategori', 'Jumlah'])
        df_kategori_perilaku['Persentase'] = (df_kategori_perilaku['Jumlah'] / total_rumah) * 100
        df_kategori_perilaku = df_kategori_perilaku.sort_values(by='Jumlah', ascending=False)

        plt.figure(figsize=(8, 4))
        colors = sns.color_palette("Blues", len(df_kategori_perilaku))
        ax = sns.barplot(x=df_kategori_perilaku['Jumlah'], y=df_kategori_perilaku['Kategori'], palette=colors, edgecolor="black")
        for idx, (value, pct) in enumerate(zip(df_kategori_perilaku['Jumlah'], df_kategori_perilaku['Persentase'])):
            plt.text(value + 1, idx, f"{value} ({pct:.1f}%)", va='center', fontsize=11, color='black')
        plt.xlabel("Jumlah Rumah", fontsize=12)
        plt.ylabel("Kategori Perilaku Tidak Sehat", fontsize=12)
        plt.title("Kategori Perilaku Tidak Sehat", fontsize=14, fontweight='bold')
        plt.xticks(fontsize=11)
        plt.yticks(fontsize=11)
        tampilkan_dan_download()

    st.sidebar.success("Visualisasi selesai ditampilkan!")
else:
    st.warning("Silakan upload file CSV di sidebar terlebih dahulu.")
