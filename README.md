# E-Library

Aplikasi E-Library yang memungkinkan pengguna untuk melihat katalog buku, mengakses detail buku, dan melakukan preview terhadap buku dalam format PDF. Pengguna dapat menambahkan buku ke daftar favorit, mengedit detail buku, dan menghapus buku dari sistem.

## Fitur Utama

- **Katalog Buku**: Menampilkan daftar semua buku dengan informasi dasar (judul, penulis, genre, dll.).
- **Detail Buku**: Menyediakan informasi lengkap tentang buku, termasuk cover, deskripsi, penulis, genre, tahun terbit, jumlah halaman, dan kata-kata relevan.
- **Preview Buku**: Menampilkan halaman pertama buku dalam format PDF dengan navigasi ke halaman selanjutnya atau sebelumnya.
- **Favorit Buku**: Pengguna dapat menandai buku sebagai favorit.
- **Analisis Buku**: Menghitung dan menampilkan analisis terkait buku, seperti kata-kata relevan.
- **Manajemen Buku**: Admin dapat menambahkan, mengedit, dan menghapus buku.


## Instalasi

### Persyaratan

1. Python 3.x
2. Django
3. Pip (untuk instalasi dependensi)


## Information User Login

| Email | Password |
| -------- | -------- |
| admin@gmail.com   | Admin123    |

### Langkah Instalasi

1. **Clone repository:**
   ```bash
   git clone https://github.com/username/e-library.git
   cd e-library

2. **Install Virtualenv and activate:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   venv\Scripts\activate
   ```

3. **Instal dependensi::**
   ```bash
   pip install -r requirements.txt
   ```
   Install manual jika masih ada yang belum terinstall

4. **Siapkan database:**
   ```bash
   python manage.py makemigration
   ```
  and then
   
   ```bash
   python manage.py migrate

5. **Jalankan server:**
   ```bash
   python manage.py runserver
   ```
   Server akan berjalan di http://127.0.0.1:8000/









