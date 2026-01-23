import requests
import json
import time
import os

# --- BİLGİLERİNİ BURAYA YAZ ---
EMAIL = "fatmanurrkrkmzz186@gmail.com"
PASSWORD = "Lordmaster5557." # <-- Şifreni tekrar yazmayı unutma!

# DÜZELTME: /v1 kısmını kaldırdık, doğrusu buymuş.
LOGIN_URL = "https://api.gain.tv/auth/signin" 
BASE_VIDEO_URL = "https://api.gain.tv/videos/" # Buradan da v1'i kaldırdık tedbiren

# Tarayıcıyı %100 taklit eden başlıklar
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Origin": "https://www.gain.tv",
    "Referer": "https://www.gain.tv/",
    "x-gain-platform": "web", # Bu başlık bazen zorunlu olabiliyor
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
}

def login():
    print(f"🔑 Giriş deneniyor: {EMAIL}")
    print(f"📡 İstek gönderiliyor: {LOGIN_URL}")
    
    payload = {"email": EMAIL, "password": PASSWORD}
    # _culture parametresini ayrı gönderiyoruz, daha sağlıklı
    params = {"_culture": "tr-tr"}
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Token genellikle 'token' ya da 'accessToken' olarak döner
            token = data.get("token") or data.get("accessToken")
            
            if token:
                print("✅ GİRİŞ BAŞARILI! Token alındı.")
                return token
            else:
                print("⚠️ Giriş yapıldı ama Token json içinde bulunamadı.")
                print(f"Gelen Veri Başlığı: {str(data)[:200]}...") # Verinin başını göster
                return None
        else:
            print(f"❌ Giriş Başarısız! Kod: {response.status_code}")
            print(f"Sunucu Cevabı: {response.text}")
            return None
            
    except Exception as e:
        print(f"🔥 Bağlantı hatası (Login): {e}")
        return None

def get_video_details(video_id, token):
    # Video detay URL'si bazen v1 isteyebilir, bazen istemez. 
    # Önce v1'siz deniyoruz, olmazsa v1 ekleriz.
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
            # Test için senin videon
            target_ids = ["EFQ3X5f4"] 
            print(f"\nToplam {len(target_ids)} içerik taranacak...")

            for vid in target_ids:
                data = get_video_details(vid, token)
                if data:
                    all_data.append(data)
                time.sleep(1)
        else:
            print("⚠️ Token alınamadı, işlem durduruluyor.")

    except Exception as e:
        print(f"🔥 Genel Hata: {e}")
    
    finally:
        # Dosyayı her türlü oluşturuyoruz ki GitHub hata vermesin
        print("\n💾 Dosya kaydediliyor...")
        with open("gain_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        print(f"🏁 İşlem bitti. (İçerik sayısı: {len(all_data)})")

if __name__ == "__main__":
    main()
