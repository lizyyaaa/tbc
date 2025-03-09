import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from datetime import datetime

# Atur tema Seaborn
sns.set_theme(style="whitegrid")

# Inisialisasi session_state untuk data gabungan
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame()

# Sidebar: Navigasi
nav = st.sidebar.radio("Navigasi", ["Home", "Visualisasi"])

# Fungsi download chart
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

# Fungsi untuk menampilkan chart dan download
def tampilkan_dan_download():
    st.pyplot(plt.gcf())
    download_chart()
    plt.clf()

# ================================
# Halaman Home: Input & Upload Data
# ================================
if nav == "Home":
    st.title("🏠 Home - Input & Upload Data")
    st.markdown("### Upload file CSV dan masukkan data baru secara manual. Data yang diinput akan digabungkan dan ditampilkan.")
    
    # Widget Upload CSV
    uploaded_file = st.file_uploader("📂 Upload file CSV", type=["csv"])
    if uploaded_file is not None:
        try:
            df_csv = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
            st.success("File CSV berhasil diupload!")
        except Exception as e:
            st.error(f"Error membaca file: {e}")
            df_csv = pd.DataFrame()
    else:
        df_csv = pd.DataFrame()

    # Option dictionary untuk input data tambahan
    option_dict = {
        "puskesmas": ['Puskesmas Kedungmundu', 'Puskesmas Sekaran', 'Puskesmas Karangdoro', 'Puskesmas Rowosari', 'Puskesmas Bandarharjo', 'Puskesmas Pegandan', 'Puskesmas Mangkang', 'Puskesmas Candilama', 'Puskesmas Karang Malang', 'Puskesmas Ngaliyan', 'Puskesmas Lebdosari', 'Plamongan Sari', 'Puskesmas Purwoyoso', 'Puskesmas Bangetayu', 'Puskesmas Pandanaran', 'Puskesmas Mijen', 'Puskesmas Ngesrep', 'Puskesmas Karangayu', 'Puskesmas Tambakaji', 'Puskesmas Padangsari', 'Puskesmas Halmahera', 'Puskesmas Miroto', 'Puskesmas Genuk', 'bulusan', 'Puskesmas Bugangan', 'Puskesmas Tlogosari Wetan', 'Puskesmas Poncol', 'Puskesmas Pudak Payung', 'Puskesmas Kagok', 'Puskesmas Krobokan', 'Puskesmas Manyaran', 'Puskesmas Tlogosari Kulon', 'Puskesmas Karanganyar', 'Puskesmas Gunungpati', 'Puskesmas Ngemplak Simongan', 'Puskesmas Srondol', 'Puskesmas Gayamsari', 'Puskesmas Bulu Lor'],
        "gender": ['L', 'P'],
        "city": ['Semarang', 'Luar Kota'],
        "regency": ['Tembalang', 'Gunungpati', 'Semarang Timur', 'Semarang Utara', 'Gajahmungkur', 'Tugu', 'Candisari', 'Mijen', 'Ngaliyan', 'Semarang Barat', 'Pedurungan', 'Genuk', 'Semarang Selatan', 'Banyumanik', 'Luar Kota', 'Semarang Tengah', 'Gayamsari'],
        "kelurahan": ['Tandang', 'Sukorejo', 'Sendangmulyo', 'Sambiroto', 'Kemijen', 'Rejomulyo', 'Sendangguwo', 'Meteseh', 'Dadapsari', 'Petompon', 'Karangrejo', 'Lempongsari', 'Bendungan', 'Mangkang Wetan', 'Karanganyar Gunung', 'Sampangan', 'Tanjungmas', 'Kalisegoro', 'Karangmalang', 'Wates', 'Sekaran', 'Jangli', 'Kalibanteng Kulon', 'Penggaron Kidul', 'Bandarharjo', 'Purwoyoso', 'Pedurungan Kidul', 'Kedungmundu', 'Patemon', 'Sembungharjo', 'Bringin', 'Randusari', 'Wonoplumbon', 'Rowosari', 'Ngesrep', 'Tinjomoyo', 'Karangayu', 'Podorejo', 'Karangroto', 'Kalipancur', 'Wonosari', 'Sumurboto', 'Plamongansari', 'Padangsari', 'Bambankerep', 'Mangkang Kulon', 'Mangunharjo', 'Pedalangan', 'Jomblang', 'Kedungpane', 'Ngadirgo', 'Cangkiran', 'Luar Kota', 'Rejosari', 'Jatingaleh', 'Tambakaji', 'Mlatibaru', 'Ngaliyan', 'Gabahan', 'Miroto', 'Genuksari', 'Salamanmloyo', 'Bulusan', 'Bugangan', 'Kebonagung', 'Bulustalan', 'Gisikdrono', 'Tambakharjo', 'Muktiharjo Lor', 'Ngijo', 'Mijen', 'Wonolopo', 'Jabungan', 'Kuningan', 'Tlogomulyo', 'Banjardowo', 'Bubakan', 'Gondoriyo', 'Bendan Duwur', 'Gajahmungkur', 'Bendan Ngisor', 'Purwodinatan', 'Kramas', 'Kudu', 'Mugassari', 'Penggaron Lor', 'Bangetayu Wetan', 'Bangunharjo', 'Kembangsari', 'Pandansari', 'Sekayu', 'Karangtempel', 'Gedawang', 'Karangkidul', 'Bojongsalaman', 'Trimulyo', 'Bangetayu Kulon', 'Gebangsari', 'Jatibarang', 'Tambangan', 'Wonodri', 'Pudakpayung', 'Pedurungan Tengah', 'Candi', 'Kranggan', 'Tlogosari Wetan', 'Tawangsari', 'Palebon', 'Mlatibaru', 'Tegalsari', 'Wonotingal', 'Manyaran', 'Kembangarum', 'Barusari', 'Krapyak', 'Gemah', 'Tugurejo', 'Mangunsari', 'Nongkosawit', 'Karangturi', 'Tlogosari Kulon', 'NgemplakSimongan', 'Krobokan', 'Srondol Wetan', 'Banyumanik', 'Gunungpati', 'Jagalan', 'Pindrikan Lor', 'Jatisari', 'Srondol Kulon', 'Randugarut', 'Kaligawe', 'Tawangmas', 'Brumbungan', 'Siwalan', 'Tambakrejo', 'Sadeng', 'Sawah Besar', 'Jatirejo', 'Plalangan', 'Pakintelan', 'Kauman', 'Pandean Lamper', 'Gayamsari', 'Sambirejo', 'Sarirejo', 'Bongsari', 'Pindrikan Kidul', 'Sumurejo', 'Terboyo Wetan', 'Muktiharjo Kidul', 'Pedurungan Lor', 'Kalicari', 'Cabean', 'Karanganyar', 'Panggung Lor', 'Purwosari', 'Panggung Kidul', 'Bulu Lor', 'Plombokan', 'Kaliwiru', 'Pangangan', 'Kalibanteng Kidul', 'Jrakah'],
        "type_tb": [1.0, 2.0],
        "status_hamil": ['Tidak', 'Ya'],
        "pekerjaan": ['Tidak Bekerja', 'Ibu Rumah Tangga', 'Pegawai Swasta', 'Lainnya', 'Pelajar / Mahasiswa', 'Wiraswasta', 'Nelayan', 'Petani', 'Pensiunan', 'TNI / Polri'],
        "pekerjaan_kepala_keluarga": ['Lainnya', 'Tidak Bekerja', 'Pegawai Swasta', 'Wiraswasta', 'Pelajar / Mahasiswa', 'Nelayan', 'Ibu Rumah Tangga', 'Petani', 'Pensiunan', 'PNS', 'TNI / Polri'],
        "total_pendapatan_keluarga_per_bulan": ['1.000.000 - < 2.000.000', '2.000.000 - < 3.000.000', '< 1.000.000', '0', '3.000.000 - < 4.000.000', '>= 4.000.000'],
        "pola_asuh": ['Orang Tua', 'Lainnya', 'Kakek / Nenek', 'Penitipan'],
        "status_pernikahan": ['Belum Kawin', 'Kawin', 'Cerai Mati', 'Cerai Hidup'],
        "status_pernikahan_orang_tua": ['Kawin', 'Cerai Mati', 'Belum Kawin', 'Cerai Hidup'],
        "kepemilikan_jkn": ['Ya', 'Tidak'],
        "perilaku_merokok": ['Tidak', 'Ya'],
        "anggota_keluarga_merokok": ['Ya', 'Tidak'],
        "mendapatkan_bantuan": ['Tidak', 'Ya'],
        "status_imunisasi": ['Tidak Lengkap', 'Lengkap'],
        "status_gizi": ['Underweight', 'Normal', 'Wasting', 'Kurang', 'Overweight', 'Obesitas'],
        "status_rumah": ['Lainnya', 'Pribadi', 'Orang Tua', 'Kontrak', 'Kost', 'Asrama'],
        "langit_langit": ['Tidak ada', 'Ada'],
        "lantai": ['Ubin/keramik/marmer', 'Tanah', 'Kurang Baik', 'Papan/anyaman bambu/plester retak berdebu', 'Baik'],
        "dinding": ['Permanen (tembok pasangan batu bata yang diplester)', 'Semi permanen bata/batu yang tidak diplester/papan kayu', 'Bukan tembok (papan kayu/bambu/ilalang)'],
        "jendela_kamar_tidur": ['Tidak ada', 'Ada'],
        "jendela_ruang_keluarga": ['Ada', 'Tidak ada'],
        "ventilasi": ['Kurang Baik', 'Ada,luas ventilasi < 10% dari luas lantai', 'Tidak Ada', 'Baik', 'Ada, luas ventilasi > 10% dari luas lantai'],
        "lubang_asap_dapur": ['Ada, luas ventilasi < 10% dari luas lantai dapur', 'Tidak Ada', 'Ada, luas ventilasi > 10% luas lantai dapur/exhaust vent'],
        "pencahayaan": ['Kurang Baik', 'Tidak terang', 'Baik', 'Terang', 'Kurang jelas untuk membaca normal', 'Kurang terang', 'Dapat digunakan untuk membaca normal'],
        "sarana_air_bersih": ['Ada,bukan milik sendiri & memenuhi syarat kesehatan', 'Ada,milik sendiri & tidak memenuhi syarat kesehatan', 'Ada, bukan milik sendiri & tidak memenuhi syarat kesehatan', 'Ada,milik sendiri & memenuhi syarat kesehatan', 'Tidak Ada'],
        "jamban": ['Ada tutup & septic tank', 'Ada, leher angsa', 'Ada,bukan leher angsa ada tutup & septic tank', 'Ada,bukan leher angsa ada tutup & dialirkan ke sungai', 'Tidak Ada', 'Ada, bukan leher angsa tidak bertutup & dialirkan ke sungai'],
        "sarana_pembuangan_air_limbah": ['Ada, diresapkan ke selokan terbuka', 'Tidak ada, sehingga tergenang dan tidak teratur di halaman/belakang rumah', 'Ada, bukan milik sendiri & memenuhi syarat kesehatan', 'Ada, diresapkan tetapi mencemari sumber air (jarak <10m)', 'Ada, dialirkan ke selokan tertutup ("&"saluran kota) utk diolah lebih lanjut'],
        "sarana_pembuangan_sampah": ['Ada, tetapi tidak kedap air dan tidak tertutup', 'Tidak Ada', 'Ada, kedap air dan tidak tertutup', 'Ada, kedap air dan tertutup'],
        "sampah": ['Lainnya (Sungai)', 'Dikelola Sendiri (Pilah Sampah)', 'Bakar', 'Petugas', 'dll'],
        "membuka_jendela_kamar_tidur": ['Tidak pernah dibuka', 'Kadang-kadang dibuka', 'Setiap hari dibuka'],
        "membuka_jendela_ruang_keluarga": ['Tidak pernah dibuka', 'Kadang-kadang dibuka', 'Setiap hari dibuka'],
        "membersihkan_rumah": ['Tidak pernah dibersihkan', 'Kadang-kadang', 'Setiap hari dibersihkan'],
        "membuang_tinja": ['Setiap hari ke jamban', 'Dibuang ke sungai/kebun/kolam/sembarangan'],
        "membuang_sampah": ['Dibuang ke sungai/kebun/kolam/sembarangan / dibakar', 'Kadang-kadang dibuang ke tempat sampah', 'Dibuang ke tempat sampah/ada petugas sampah', 'Dilakukan pilah sampah/dikelola dengan baik'],
        "kebiasaan_ctps": ['Tidak pernah CTPS', 'Kadang-kadang CTPS', 'CTPS setiap aktivitas'],
        "memiliki_hewan_ternak": ['Tidak', 'Ya'],
        "kandang_hewan": []  # Kosong, bisa diisi teks
    }

    st.markdown("## Form Input Data Manual Tambahan")
    with st.form(key="manual_form"):
        input_manual = {}
        # Untuk setiap kolom pada option_dict, gunakan selectbox jika ada opsi, jika tidak, gunakan text_input.
        for col, options in option_dict.items():
            if options:
                input_manual[col] = st.selectbox(f"{col}", options)
            else:
                input_manual[col] = st.text_input(f"{col}", value="")
        # Untuk kolom 'pasien', gunakan text_input agar bisa diisi ID atau keterangan lain.
        input_manual["pasien"] = st.text_input("Pasien (ID atau keterangan)", value="")
        # Tambahkan dua kolom tanggal: date_start dan tgl_kunjungan
        input_manual["date_start"] = st.text_input("Tanggal Start (YYYY-MM-DD)", value=datetime.today().strftime("%Y-%m-%d"))
        input_manual["tgl_kunjungan"] = st.text_input("Tanggal Kunjungan (YYYY-MM-DD)", value=datetime.today().strftime("%Y-%m-%d"))
        submitted_manual = st.form_submit_button(label="Submit Data Manual Tambahan")
    
    if submitted_manual:
        try:
            input_manual["date_start"] = pd.to_datetime(input_manual["date_start"])
            input_manual["tgl_kunjungan"] = pd.to_datetime(input_manual["tgl_kunjungan"])
        except Exception as e:
            st.error("Format tanggal tidak valid. Gunakan format YYYY-MM-DD.")
        df_manual = pd.DataFrame([input_manual])
        st.success("Data manual tambahan berhasil ditambahkan!")
        st.dataframe(df_manual)
        # Gabungkan data manual tambahan dengan data CSV (jika ada)
        if not df_csv.empty:
            df_combined = pd.concat([df_csv, df_manual], ignore_index=True)
        else:
            df_combined = df_manual.copy()
        st.session_state["data"] = df_combined
        st.info("Data gabungan telah disimpan. Buka halaman Visualisasi untuk melihat chart.")
    elif not st.session_state["data"].empty:
        st.markdown("### Data Gabungan Saat Ini")
        st.dataframe(st.session_state["data"])

# ================================
# Halaman Visualisasi
# ================================
elif nav == "Visualisasi":
    st.title("📈 Visualisasi Data")
    if st.session_state["data"].empty:
        st.warning("Data belum tersedia. Silakan upload file CSV atau input data manual di halaman Home.")
    else:
        df = st.session_state["data"]
        st.subheader("Data yang Digunakan")
        st.dataframe(df)
        
        # Preprocessing dasar: imputasi, hapus duplikasi, konversi tanggal
        kolom_numerik = df.select_dtypes(include=['number']).columns
        kolom_kategori = df.select_dtypes(include=['object']).columns
        df[kolom_kategori] = df[kolom_kategori].apply(lambda x: x.fillna(x.mode()[0]))
        df[kolom_numerik] = df[kolom_numerik].apply(lambda x: x.fillna(x.mean()))
        df = df.drop_duplicates()
        if "date_start" in df.columns:
            df["date_start"] = pd.to_datetime(df["date_start"], errors="coerce")
            df["year_month"] = df["date_start"].dt.to_period("M").astype(str)
        
        # Definisi kategori untuk analisis skor (sesuaikan dengan data)
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
        
        # Pastikan kolom-kolom tersebut ada
        if all(col in df.columns for col in kategori_rumah + kategori_sanitasi + kategori_perilaku):
            df_rumah = df[kategori_rumah].dropna()
            df_sanitasi = df[kategori_sanitasi].dropna()
            df_perilaku = df[kategori_perilaku].dropna()

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

            # Visualisasi sesuai pilihan
            if pilihan == "📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak":
                st.subheader("📊 Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak")
                kategori_overall = ["Rumah Tidak Layak", "Sanitasi Tidak Layak", "Perilaku Tidak Baik"]
                persentase_overall = [persentase_tidak_layak_rumah, persentase_tidak_layak_sanitasi, persentase_tidak_baik_perilaku]
                sorted_idx = sorted(range(len(persentase_overall)), key=lambda i: persentase_overall[i], reverse=True)
                kategori_overall = [kategori_overall[i] for i in sorted_idx]
                persentase_overall = [persentase_overall[i] for i in sorted_idx]

                plt.figure(figsize=(8, 4))
                plt.bar(kategori_overall, persentase_overall, color=['red', 'orange', 'blue'])
                plt.xlabel("Kategori", fontsize=12)
                plt.ylabel("Persentase (%)", fontsize=12)
                plt.title("Persentase Rumah, Sanitasi, dan Perilaku Tidak Layak", fontsize=14, fontweight="bold")
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
                plt.xlabel("Kondisi Rumah", fontsize=12)
                plt.ylabel("Jumlah", fontsize=12)
                plt.title("Perbandingan Rumah Layak dan Tidak Layak", fontsize=14, fontweight="bold")
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
                plt.xlabel("Kondisi Rumah", fontsize=12)
                plt.ylabel("Persentase (%)", fontsize=12)
                plt.title("Persentase Rumah Layak dan Tidak Layak", fontsize=14, fontweight="bold")
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
                    plt.text(value + 1, idx, f"{value} rumah ({pct:.1f}%)", va='center', fontsize=11)
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
            st.warning("Data tidak memiliki kolom yang dibutuhkan untuk analisis skor. Silakan periksa data Anda.")
