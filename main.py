import requests
import json
import os
import time

# GITHUB SECRET'LARDAN ALINACAK BİLGİLER
EMAIL = os.environ.get("GAIN_EMAIL")
PASSWORD = os.environ.get("GAIN_PASSWORD")

# API URL'LERİ (Bunları Network sekmesinden teyit etmelisin)
LOGIN_URL = "https://api.gain.tv/v1/auth/signin?_culture=tr-tr" # Senin bulduğun URL
BASE_VIDEO_URL = "https://api.gain.tv/v1/videos/" # Video detay URL yapısı

# Tarayıcı gibi görünmek için Header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def login():
    """Sisteme giriş yapıp Token alır"""
    print("Giriş yapılıyor...")
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            # Token bazen 'token', bazen 'accessToken' olarak döner. Senin yanıtına göre 'token' aldık.
            token = data.get("token") or data.get("accessToken")
            print("✅ Giriş başarılı! Token alındı.")
            return token
        else:
            print(f"❌ Giriş başarısız! Kod: {response.status_code}, Mesaj: {response.text}")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

def get_video_details(video_id, token):
    """Tek bir videonun detaylarını çeker"""
    url = BASE_VIDEO_URL + video_id
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            print(f"✅ {video_id} verisi çekildi.")
            return response.json()
        else:
            print(f"❌ {video_id} çekilemedi. Kod: {response.status_code}")
            return None
    except Exception as e:
        print(f"Video hatası: {e}")
        return None

def main():
    if not EMAIL or not PASSWORD:
        print("❌ E-posta veya Şifre bulunamadı! GitHub Secrets ayarlarını kontrol et.")
        return

    token = login()
    if not token:
        return

    # --- ÖNEMLİ KISIM: TÜM LİSTEYİ ÇEKMEK ---
    # Buraya çekmek istediğin ID'leri yazmalısın. 
    # "Tümünü çekmek" için Gain'in "Katalog" API'sini bulmamız lazım.
    # Şimdilik örnek olarak senin videonu ve rastgele birkaç ID deniyoruz.
    target_ids = ["EFQ3X5f4"] 
    
    all_data = []

    for vid in target_ids:
        data = get_video_details(vid, token)
        if data:
            all_data.append(data)
        time.sleep(1) # Siteyi çökertmemek için her işlemde 1 saniye bekle

    # Veriyi kaydet
    with open("gain_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    print("🏁 İşlem tamamlandı. gain_data.json dosyası oluşturuldu.")

if __name__ == "__main__":
    main()
