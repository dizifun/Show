import requests
import json
import time

# --- BİLGİLERİNİ BURAYA YAZ ---
EMAIL = "fatmanurrkrkmzz186@gmail.com"
# Şifreni tırnakların içine yaz (Boşluk bırakma!)
PASSWORD = "Lordmaster5557."

# API URL'LERİ (Basit ve çalışan yapıya döndük)
LOGIN_URL = "https://api.gain.tv/auth/signin"
BASE_VIDEO_URL = "https://api.gain.tv/videos/"

# HEADER
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "x-gain-platform": "web",
    "Origin": "https://www.gain.tv",
    "Referer": "https://www.gain.tv/"
}

def login():
    print(f"🔑 Giriş yapılıyor: {EMAIL}")
    
    # HATA BURADAYDI: Artık "Request" kutusu yok, direkt veriyoruz.
    payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    # _culture parametresini de URL'ye ek olarak gönderiyoruz
    params = {"_culture": "tr-tr"}
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Token'ı alalım
            token = data.get("token") or data.get("accessToken")
            
            if token:
                print("✅ GİRİŞ BAŞARILI! Token alındı.")
                return token
            else:
                print(f"⚠️ Giriş OK ama Token yok. Gelen: {data}")
                return None
        else:
            print(f"❌ Giriş Başarısız! Hata Kodu: {response.status_code}")
            print(f"Sunucu Cevabı: {response.text}")
            return None
    except Exception as e:
        print(f"🔥 Bağlantı Hatası: {e}")
        return None

def get_video_details(video_id, token):
    # Video URL'sini oluştur
    url = BASE_VIDEO_URL + video_id
    
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.get(url, headers=auth_headers)
        if response.status_code == 200:
            data = response.json()
            title = data.get("title", "Bilinmiyor")
            print(f"✅ Veri çekildi: {title} ({video_id})")
            return data
        else:
            print(f"❌ {video_id} çekilemedi. Kod: {response.status_code}")
            return None
    except Exception as e:
        print(f"🔥 Hata: {e}")
        return None

def main():
    token = login()
    if not token:
        print("⛔ Token alınamadı, çıkış yapılıyor.")
        return

    # Şimdilik test videosu (Bu çalışınca tüm listeyi ekleyeceğiz)
    target_ids = ["EFQ3X5f4"] 
    
    all_data = []
    print(f"\n🚀 {len(target_ids)} içerik taranacak...")

    for vid in target_ids:
        data = get_video_details(vid, token)
        if data:
            all_data.append(data)
        time.sleep(1)

    # Dosyayı kaydet
    print("\n💾 Dosya kaydediliyor...")
    with open("gain_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=4, ensure_ascii=False)
    print("🏁 İşlem tamamlandı.")

if __name__ == "__main__":
    main()