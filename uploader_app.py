import streamlit as st
import os
import json
import time
from PIL import Image
import streamlit.components.v1 as components

# --- 1. KONFIGURASI PATH ---
# Sesuaikan path ini dengan folder di STB Anda
DB_FILE = "data_web.json"
IMG_DIR = "images"
SAVE_DIR = "musik"
SAVE_IKLAN_DIR = "musik/iklan"

# Pastikan folder tersedia
for d in [IMG_DIR, SAVE_IKLAN_DIR, SAVE_DIR]:
    if not os.path.exists(d): 
        os.makedirs(d)

# --- 2. FUNGSI DATA ---
def load_data():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    # Data Default jika file kosong/error
    return {
        "nama_radio": "Radio Al Misbah", 
        "slogan": "", 
        "deskripsi": "", 
        "video1":"", "video2":"", "video3":"", 
        "infaq":"", "jadwal":"", "kota":"Gresik",
        "url_stream": "https://radio.1st0p-k0p1.my.id/live",
        "produk":[]
    }

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# --- 3. TAMPILAN UTAMA ---
st.set_page_config(page_title="Admin Radio Al Misbah", layout="wide")

# Sidebar Login
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/306/306066.png", width=100)
st.sidebar.title("Panel Admin")
password = st.sidebar.text_input("Password", type="password")

if password == "admin123":
    data = load_data()
    menu = st.sidebar.radio("Navigasi", [
        "🎙️ Live Broadcast", 
        "📝 Profil & Informasi", 
        "🛒 Marketplace", 
        "🎵 Manajemen Musik", 
        "📢 Manajemen Iklan"
    ])

    # --- MENU 1: LIVE BROADCAST ---
    if menu == "🎙️ Live Broadcast":
        st.header("🎙️ Siaran Langsung (Mic)")
        st.info("Fitur ini mengirim suara dari Browser ke Server. Gunakan koneksi HTTPS agar Mic aktif.")
        
        broadcast_html = f"""
        <div style="background: #1a5c37; padding: 30px; border-radius: 15px; text-align: center; color: white;">
            <button id="startBtn" style="background: #d4af37; color: #1a5c37; border: none; padding: 15px 30px; border-radius: 8px; cursor: pointer; font-size: 18px; font-weight: bold;">🔴 MULAI BICARA</button>
            <button id="stopBtn" style="background: #dc3545; color: white; border: none; padding: 15px 30px; border-radius: 8px; cursor: pointer; font-size: 18px; display: none;">⏹️ BERHENTI</button>
            <p id="status" style="margin-top: 15px;">Status: Standby</p>
        </div>
        <script>
            let mediaRecorder;
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');
            const status = document.getElementById('status');
            startBtn.onclick = async () => {{
                try {{
                    const stream = await navigator.mediaDevices.getUserMedia({{ audio: true }});
                    mediaRecorder = new MediaRecorder(stream);
                    status.innerText = "🔴 MIC AKTIF: Suara Anda sedang diproses...";
                    startBtn.style.display = "none";
                    stopBtn.style.display = "inline-block";
                    mediaRecorder.start(1000);
                }} catch (err) {{ alert("Gagal akses Mic! Pastikan HTTPS aktif."); }}
            }};
            stopBtn.onclick = () => {{
                mediaRecorder.stop();
                status.innerText = "Status: Siaran Berakhir";
                startBtn.style.display = "inline-block";
                stopBtn.style.display = "none";
            }};
        </script>
        """
        components.html(broadcast_html, height=200)

    # --- MENU 2: PROFIL & INFORMASI ---
    elif menu == "📝 Profil & Informasi":
        st.header("📝 Informasi Web & Jadwal")
        
        col1, col2 = st.columns(2)
        with col1:
            data['nama_radio'] = st.text_input("Nama Radio", data.get('nama_radio'))
            data['slogan'] = st.text_input("Slogan", data.get('slogan'))
            data['kota'] = st.text_input("Kota (Jadwal Sholat)", data.get('kota'))
            data['url_stream'] = st.text_input("URL Streaming Radio", data.get('url_stream'))
        
        with col2:
            data['jadwal'] = st.text_area("Jadwal Kajian (Gunakan enter untuk baris baru)", data.get('jadwal'), height=115)
            data['infaq'] = st.text_area("Informasi Infaq", data.get('infaq'), height=115)

        st.write("---")
        st.subheader("📺 Link Video YouTube (ID Saja)")
        v_col = st.columns(3)
        data['video1'] = v_col[0].text_input("Video Utama", data.get('video1'), help="Contoh: dQw4w9WgXcQ")
        data['video2'] = v_col[1].text_input("Video Samping 1", data.get('video2'))
        data['video3'] = v_col[2].text_input("Video Samping 2", data.get('video3'))
        
        if st.button("💾 Simpan Perubahan Web"):
            save_data(data)
            st.success("Data berhasil di-update ke data_web.json!")
            st.balloons()

    # --- MENU 3: MARKETPLACE ---
    elif menu == "🛒 Marketplace":
        st.header("🛒 Manajemen Produk")
        with st.expander("➕ Tambah Produk Baru"):
            with st.form("form_produk"):
                n = st.text_input("Nama Barang")
                h = st.text_input("Harga")
                w = st.text_input("WA (Contoh: 628123...)")
                f = st.file_uploader("Foto Produk", type=['jpg','png'])
                if st.form_submit_button("Tambah Ke Toko"):
                    if n and h and f:
                        img_name = f"prod_{int(time.time())}.jpg"
                        Image.open(f).convert('RGB').save(os.path.join(IMG_DIR, img_name), quality=70)
                        if 'produk' not in data: data['produk'] = []
                        data['produk'].append({"nama":n, "harga":h, "wa":w, "img":img_name})
                        save_data(data)
                        st.rerun()

        st.subheader("Daftar Produk Aktif")
        for i, p in enumerate(data.get('produk', [])):
            c1, c2, c3 = st.columns([1, 4, 1])
            c1.image(os.path.join(IMG_DIR, p['img']), width=80)
            c2.write(f"**{p['nama']}** \n💰 {p['harga']} | 📱 {p['wa']}")
            if c3.button("Hapus", key=f"del_{i}"):
                data['produk'].pop(i)
                save_data(data)
                st.rerun()

    # --- MENU 4 & 5: MUSIK & IKLAN ---
    elif menu in ["🎵 Manajemen Musik", "📢 Manajemen Iklan"]:
        folder = SAVE_DIR if "Musik" in menu else SAVE_IKLAN_DIR
        st.header(menu)
        uploaded_files = st.file_uploader("Pilih file MP3", type=['mp3'], accept_multiple_files=True)
        if uploaded_files and st.button("🚀 Upload Sekarang"):
            for f in uploaded_files:
                with open(os.path.join(folder, f.name), "wb") as fs:
                    fs.write(f.getbuffer())
            st.success(f"{len(uploaded_files)} file berhasil diunggah!")
            st.rerun()
        
        st.write("---")
        st.subheader("Daftar File di Server")
        files = [f for f in os.listdir(folder) if f.endswith('.mp3')]
        for f in files:
            c1, c2 = st.columns([5, 1])
            c1.text(f"🎵 {f}")
            if c2.button("🗑️", key=f"del_f_{f}"):
                os.remove(os.path.join(folder, f))
                st.rerun()

else:
    st.warning("Silakan masukkan password di sidebar untuk mengakses admin.")
