import mysql.connector

def get_connection():
    """
    Membuat koneksi ke MySQL menggunakan XAMPP.
    Pastikan:
      - MySQL di XAMPP sudah berjalan
      - Username dan password sesuai dengan pengaturan di XAMPP
      - Database yang ingin digunakan sudah dibuat (misalnya: tb_database)
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",      # MySQL berjalan secara lokal di XAMPP
            user="root",           # Username default XAMPP
            password="",           # Password default (kosong) kecuali sudah diubah
            database="tb_analisistbc" # Nama database yang sudah kamu buat
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
