#!/bin/bash

echo "--- Memulai Proses Backup ke GitHub ---"

# 1. Masuk ke folder radio
cd ~/radio-stb

# 2. Ambil perubahan terbaru dari GitHub (jika ada)
git pull origin main

# 3. Kumpulkan semua file yang berubah
git add .

# 4. Buat catatan otomatis dengan tanggal dan jam
catatan="Backup Otomatis Tanggal $(date +'%d-%m-%Y %H:%M')"
git commit -m "$catatan"

# 5. Kirim ke GitHub
echo "Sedang mengunggah ke GitHub..."
git push origin main

echo "--- Backup Selesai! ---"
