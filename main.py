import requests
import json
import time

# --- BİLGİLERİ BURAYA AÇIK AÇIK YAZIYORUZ ---
EMAIL = "fatmanurrkrkmzz186@gmail.com"
PASSWORD = "Lordmaster5557."  # <-- Şifreni tırnakların içine yaz

# Proje ID (Senin bulduğun)
PROJECT_ID = "2da7kf8jf"

# API URL'LERİ
LOGIN_URL = f"https://api.gain.tv/{PROJECT_ID}/CALL/User/signin?__culture=tr-tr"

# Video Detay URL'si
CONTENT_URL = f"https://api.gain.tv/{PROJECT_ID}/CALL/Media/GetClientContent?__culture=tr-tr"

# Tarayıcı gibi görünmek için Header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def login():
    """Sisteme giriş yapıp Token alır"""
    print("🔑 Giriş yapılıyor...")
    
    payload = {
        "Request": {
            "Email": EMAIL,
            "Password": PASSWORD
        }
    }
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("Success"):
                result = data.get("Result", {})
                token = result.get("Token") or result.get("AccessToken")
                print(f"✅ Giriş başarılı! Token alındı.")
                return token
            else:
                print(f"❌ Giriş başarısız (API Mesajı): {data.get('Message')}")
                return None
        else:
            print(f"❌ Sunucu Hatası: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Hata: {e}")
        return None

def get_video_details(video_id, token):
    """Tek bir videonun detaylarını çeker"""
    payload = {
        "Request": {
            "MediaId": video_id,
            "IncludeOpencast": True
        }
    }
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.post(CONTENT_URL, json=payload, headers=auth_headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("Success"):
                print(f"✅ {video_id} verisi çekildi.")
                return data.get("Result")
            else:
                print(f"❌ {video_id} alınamadı.")
                return None
        else:
            print(f"❌ HTTP Hatası: {response.status_code}")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

def main():
    # 1. Giriş Yap
    token = login()
    if not token:
        print("Token alınamadığı için işlem durduruldu.")
        return

    # 2. Videoları Çek
    # Buraya test için senin videonu yazdım.
    # Tüm listeyi bulduğumuzda burayı güncelleyeceğiz.
    target_ids = ["EFQ3X5f4"] 
    
    all_data = []
    print(f"\n🚀 {len(target_ids)} adet video taranıyor...")

    for vid in target_ids:
        data = get_video_details(vid, token)
        if data:
            all_data.append(data)
        time.sleep(1) 

    # 3. Kaydet
    if all_data:
        with open("gain_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        print("\n🏁 İşlem tamam. 'gain_data.json' dosyası oluşturuldu.")

if __name__ == "__main__":
    main()