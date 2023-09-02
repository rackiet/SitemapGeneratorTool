# 🌐 Sitemap Generator Tool 🛠️

## 🌟 Overview 🌟

📝 Sitemap Generator adalah sebuah alat Python 🐍 yang digunakan untuk membuat sitemap XML 🗂️ untuk website Anda 🌍. Alat ini membaca daftar URL dari sebuah file teks 📄 dan menghasilkan sitemap XML sesuai dengan spesifikasi [Sitemaps protocol](https://www.sitemaps.org/protocol.html) 📑.

## ✨ Fitur ✨

- 📃 Membaca daftar URL dari file `listwebsite.txt`.
- 🎚️ Mengatur `priority` dan `changefreq` untuk setiap URL.
- 📆 Menggunakan tanggal awal dan akhir untuk elemen `lastmod`.
- 📦 Membuat chunk sitemap setiap 500 URL.
- 📊 Menampilkan progress bar saat proses berlangsung.

## 🚀 Instalasi 🚀

1️⃣ Clone repositori ini atau download sebagai ZIP 🗄️.
2️⃣ Buka terminal 🖥️ dan navigasi ke folder di mana kode sumber berada.
3️⃣ Jalankan `pip install tqdm` 📦 untuk menginstal library tqdm yang digunakan untuk progress bar 📊.

## 🤔 Cara Menggunakan 🤔

### 🔧 Setup 🔧

1️⃣ Buat file `listwebsite.txt` 📄 dan masukkan semua URL yang ingin Anda tambahkan ke sitemap. Satu URL per baris 🖋️.

### 🎮 Menjalankan Program 🎮

1️⃣ Buka terminal 🖥️ dan navigasi ke folder di mana kode sumber berada.
2️⃣ Jalankan `python nama_file.py` ⏩ (ganti `nama_file.py` dengan nama file Python Anda 📄).

### 💡 Input 💡

Program akan meminta beberapa input 🖊️:

1️⃣ Tanggal awal dalam format DD-MM-YYYY 🗓️.
2️⃣ Tanggal akhir dalam format DD-MM-YYYY 📅.
3️⃣ Priority (e.g., 1.0) 🌟.
4️⃣ Changefreq (e.g., always, hourly, daily) ⏲️.

### 📤 Output 📤

- 📜 Sitemap akan disimpan dalam file dengan format `sitemap1.xml`, `sitemap2.xml`, dan seterusnya 🗂️.

## 🤝 Kontribusi 🤝

🐛 Jika Anda menemukan bug atau ingin menambahkan fitur, silakan buat sebuah issue atau pull request 👥.

## 📜 Lisensi 📜

MIT 🔒
