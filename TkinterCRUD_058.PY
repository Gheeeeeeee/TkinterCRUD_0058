import sqlite3  # Digunakan untuk berinteraksi dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Digunakan untuk membuat GUI

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa_.db')  # Membuat atau membuka database 'nilai_siswa_.db'
    cursor = conn.cursor()  # Menyiapkan cursor untuk eksekusi query
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        nama_siswa TEXT NOT NULL, 
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        prediksi_fakultas TEXT
    )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi ke database

# Fungsi untuk mengambil semua data siswa dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa_.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa')  # Mengambil semua data dari tabel nilai_siswa
    rows = cursor.fetchall()  # Mengambil semua baris hasil query
    conn.close()  # Menutup koneksi
    return rows  # Mengembalikan data yang diambil

# Fungsi untuk menyimpan data siswa ke dalam database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute(''' 
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    ''', (nama, biologi, fisika, inggris, prediksi))  # Menggunakan placeholder untuk menghindari SQL injection
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk memperbarui data siswa di database berdasarkan ID
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa_.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  # Menentukan ID yang akan diupdate
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghapus data siswa dari database berdasarkan ID
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa_.db')  # Membuka koneksi ke database
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))  # Menghapus data berdasarkan ID
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai siswa
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"  # Prediksi fakultas Kedokteran jika nilai Biologi tertinggi
    elif fisika > biologi and fisika > inggris:
        return "Teknik"  # Prediksi fakultas Teknik jika nilai Fisika tertinggi
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"  # Prediksi fakultas Bahasa jika nilai Bahasa Inggris tertinggi
    else:
        return "Tidak diketahui"  # Jika tidak ada nilai tertinggi yang jelas

# Fungsi untuk menangani pengiriman data baru (tambah data siswa)
def submit():
    try:
        # Mengambil data dari input form
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Validasi: Nama siswa tidak boleh kosong
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        # Menghitung prediksi fakultas berdasarkan nilai siswa
        prediksi = calculate_prediction(biologi, fisika, inggris)

        # Menyimpan data ke database
        save_to_database(nama, biologi, fisika, inggris, prediksi)
        messagebox.showinfo("Sukses", f"Data Berhasil disimpan!\nPrediksi fakultas: {prediksi}")
        clear_inputs()  # Mengosongkan form input
        populate_table()  # Memperbarui tabel data siswa

    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data siswa yang sudah ada
def update():
    try:
        if not selected_record_id.get():  # Memastikan ada data yang dipilih untuk diupdate
            raise ValueError("Pilih data dari tabel untuk di-update.")

        record_id = int(selected_record_id.get())  # Mengambil ID yang dipilih
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        # Validasi: Nama siswa tidak boleh kosong
        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")
        
        # Menghitung prediksi fakultas berdasarkan nilai siswa
        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)
        messagebox.showinfo("Sukses", "Data Berhasil diperbarui!")
        clear_inputs()  # Mengosongkan form input
        populate_table()  # Memperbarui tabel data siswa

    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data siswa yang dipilih
def delete():
    try:
        if not selected_record_id.get():  # Memastikan ada data yang dipilih untuk dihapus
            raise ValueError("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())  # Mengambil ID yang dipilih
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data Berhasil dihapus!")
        clear_inputs()  # Mengosongkan form input
        populate_table()  # Memperbarui tabel data siswa

    except ValueError as e:  # Menangani kesalahan input
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan form input setelah operasi
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi ulang tabel dengan data terbaru dari database
def populate_table():
    for row in tree.get_children():  # Menghapus data lama dari tabel
        tree.delete(row)
    for row in fetch_data():  # Mengambil dan menampilkan data baru dari database
        tree.insert('', 'end', values=row)

# Fungsi untuk mengisi form input berdasarkan data yang dipilih dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]  # Mengambil baris yang dipilih di tabel
        selected_row = tree.item(selected_item)['values']  # Mengambil data dari baris yang dipilih

        # Mengisi form input dengan data yang dipilih
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:  # Menangani kesalahan jika tidak ada baris yang dipilih
        messagebox.showerror("Error", "Pilih data yang valid")

# Membuat database dan tabel saat aplikasi dimulai
create_database()

# Membuat window utama dengan Tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")  # Menentukan judul window

# Variabel untuk menyimpan input dari form
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Menambahkan label dan input untuk nama siswa dan nilai-nilai lainnya
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Bahasa Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Menambahkan tombol untuk operasi CRUD (Tambah, Update, Hapus)
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Menambahkan tabel untuk menampilkan data siswa
columns = ('id', 'nama_siswa', 'biologi', 'fisika', 'inggris', 'prediksi_fakultas')
tree = ttk.Treeview(root, columns=columns, show='headings')

# Menentukan heading untuk setiap kolom
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center')

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menghubungkan event klik pada tabel untuk mengisi form input dengan data yang dipilih
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data awal dari database
populate_table()

# Menjalankan aplikasi GUI
root.mainloop()
