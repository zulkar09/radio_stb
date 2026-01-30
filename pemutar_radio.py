import shout
import os
import time
import json

def start_radio():
    s = shout.Shout()
    s.host = 'icecast'
    s.port = 8000
    s.user = 'source'
    s.password = 'hackme' # Pastikan sama dengan config icecast
    s.mount = '/autodj'
    s.format = 'mp3'
    s.protocol = 'http'

    print("Mencoba hubungkan ke Icecast...")
    while True:
        try:
            s.open()
            print("✅ TERHUBUNG: AutoDJ Aktif")
            break
        except Exception as e:
            print(f"❌ Gagal: {e}. Ulangi 5 detik...")
            time.sleep(5)

    while True:
        # Folder di dalam kontainer docker
        musik_dir = "/app/musik"
        files = sorted([f for f in os.listdir(musik_dir) if f.endswith('.mp3')])
        
        if not files:
            print("⚠️ Folder musik kosong.")
            time.sleep(10)
            continue

        for file_name in files:
            file_path = os.path.join(musik_dir, file_name)
            print(f"🎵 Memutar: {file_name}")
            
            # Update Status ke JSON agar tampil di Web
            try:
                with open("/app/web-content/data_web.json", "r") as f:
                    data = json.load(f)
                data['status_radio'] = f"📻 Memutar: {file_name}"
                with open("/app/web-content/data_web.json", "w") as f:
                    json.dump(data, f, indent=4)
            except: pass

            try:
                with open(file_path, 'rb') as f:
                    while True:
                        buf = f.read(4096)
                        if not buf: break
                        s.send(buf)
                        s.sync()
            except Exception as e:
                print(f"Error: {e}")
                continue

if __name__ == "__main__":
    start_radio()
