import requests
import json
import time

# --- BİLGİLERİNİ BURAYA YAZ ---
EMAIL = "fatmanurrkrkmzz186@gmail.com"  # Senin e-postan
PASSWORD = "Lordmaster5557."       # Gain şifreni tırnak içine yaz

# API URL'LERİ
LOGIN_URL = "https://api.gain.tv/v1/auth/signin?_culture=tr-tr"
BASE_VIDEO_URL = "https://api.gain.tv/v1/videos/"

# HEADER AYARLARI
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def login():
    """Sisteme giriş yapıp Token alır"""
    print(f"🔑 {EMAIL} ile giriş yapılıyor...")
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            token = data.get("token") or data.get("accessToken")
            print("✅ Giriş başarılı! Token alındı.")
            return token
        else:
            print(f"❌ Giriş başarısız! Kod: {response.status_code}")
            print(f"Mesaj: {response.text}")
            return None
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None

def get_video_details(video_id, token):
    """Tek bir videonun detaylarını çeker"""
    url = BASE_VIDEO_URL + video_id
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Bilinmiyor")
            print(f"✅ Çekildi: {title} ({video_id})")
            return data
        else:
            print(f"❌ {video_id} çekilemedi. Kod: {response.status_code}")
            return None
    except Exception as e:
        print(f"Video hatası: {e}")
        return None

def main():
    token = login()
    if not token:
        return

    # --- BURASI ÖNEMLİ ---
    # Şu an elimizde "Tüm Filmlerin Listesi" olmadığı için 
    # sadece senin test videonu ve örnek bir ID'yi çekiyoruz.
    # Liste API'sini bulduğumuzda burayı değiştireceğiz.
    
    target_ids = ["EFQ3X5f4"] # Test için senin videon
    
    all_data = []

    print(f"\nToplam {len(target_ids)} video taranacak...\n")

    for vid in target_ids:
        data = get_video_details(vid, token)
        if data:
            all_data.append(data)
        time.sleep(1) # Seri istek atıp ban yememek için bekleme

    # Veriyi kaydet
    with open("gain_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    
    print(f"\n🏁 İşlem tamam. {len(all_data)} video 'gain_data.json' dosyasına kaydedildi.")

if __name__ == "__main__":
    main()
