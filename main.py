import requests
import json
import time
import os

# --- BİLGİLERİNİ BURAYA DİKKATLİCE YAZ ---
# Tırnak işaretlerini silmemeye dikkat et.
EMAIL = "fatmanurrkrkmzz186@gmail.com"
PASSWORD = "Lordmaster5557."  # <-- Şifreni buraya yazdığından emin ol

# API URL'LERİ
LOGIN_URL = "https://api.gain.tv/v1/auth/signin?_culture=tr-tr"
BASE_VIDEO_URL = "https://api.gain.tv/v1/videos/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://www.gain.tv",
    "Referer": "https://www.gain.tv/"
}

def login():
    print(f"🔑 Giriş deneniyor: {EMAIL}")
    payload = {"email": EMAIL, "password": PASSWORD}
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token") or data.get("accessToken")
            if token:
                print("✅ Giriş başarılı! Token alındı.")
                return token
            else:
                print("⚠️ Yanıt 200 OK ama Token bulunamadı!")
                print(f"Gelen Veri: {data}")
                return None
        else:
            print(f"❌ Giriş Başarısız! Kod: {response.status_code}")
            print(f"Sunucu Cevabı: {response.text}")
            return None
    except Exception as e:
        print(f"🔥 Bağlantı hatası (Login): {e}")
        return None

def get_video_details(video_id, token):
    url = BASE_VIDEO_URL + video_id
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Veri çekildi: {video_id}")
            return data
        else:
            print(f"❌ Video Çekilemedi ({video_id}). Kod: {response.status_code}")
            return None
    except Exception as e:
        print(f"🔥 Video Hatası: {e}")
        return None

def main():
    all_data = []
    
    try:
        token = login()
        if token:
            target_ids = ["EFQ3X5f4"] # Test ID
            print(f"\nToplam {len(target_ids)} içerik taranacak...")

            for vid in target_ids:
                data = get_video_details(vid, token)
                if data:
                    all_data.append(data)
                time.sleep(1)
        else:
            print("⚠️ Token alınamadığı için video çekme işlemi atlandı.")

    except Exception as e:
        print(f"🔥 Genel Hata: {e}")
    
    finally:
        # Hata olsa bile dosyayı oluştur ki GitHub Action hata vermesin
        print("\n💾 Dosya kaydediliyor...")
        with open("gain_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        print(f"🏁 gain_data.json oluşturuldu. (İçerik sayısı: {len(all_data)})")

if __name__ == "__main__":
    main()
