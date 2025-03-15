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
            host="127.0.0.1",      # MySQL berjalan secara lokal di XAMPP
            port=3306,# Username default XAMPP
            user="root",   
            password="",           # Password default (kosong) kecuali sudah diubah
            database="tb_analisistbc" # Nama database yang sudah kamu buat
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
