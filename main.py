import requests
import json
import os
import time

# --- AYARLAR ---
# GitHub Secret'lardan gelecek bilgiler
EMAIL = os.environ.get("GAIN_EMAIL")
PASSWORD = os.environ.get("GAIN_PASSWORD")

# Senin bulduğun Proje ID
PROJECT_ID = "2da7kf8jf"

# API URL'LERİ (Senin verdiğin yeni linkler)
# Giriş URL'si
LOGIN_URL = f"https://api.gain.tv/{PROJECT_ID}/CALL/User/signin?__culture=tr-tr"

# Video Detay URL'si (Tahmini yapıdır, çalışmazsa Network'ten 'GetClientContent'i bulmalısın)
# Gain'in bu altyapısında genellikle video detayları bu adrese sorulur:
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
    
    # Gain'in bu versiyonunda payload yapısı genellikle böyledir:
    payload = {
        "Request": {
            "Email": EMAIL,     # Bazen "UserName" veya "Email" olabilir
            "Password": PASSWORD
        }
    }
    
    try:
        response = requests.post(LOGIN_URL, json=payload, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            # Yanıt başarılı mı kontrol et
            if data.get("Success"):
                # Token genellikle Result -> Token içindedir
                result = data.get("Result", {})
                token = result.get("Token") or result.get("AccessToken")
                print(f"✅ Giriş başarılı! Token alındı.")
                return token
            else:
                print(f"❌ Giriş başarısız (API Hatası): {data.get('Message')}")
                return None
        else:
            print(f"❌ Sunucu Hatası: {response.status_code}")
            return None
    except Exception as e:
        print(f"⚠️ Kritik Hata: {e}")
        return None

def get_video_details(video_id, token):
    """Tek bir videonun detaylarını çeker"""
    
    # Bu altyapıda genellikle POST isteği ile detay sorulur
    payload = {
        "Request": {
            "MediaId": video_id,
            "IncludeOpencast": True
        }
    }
    
    # Token'ı Header'a ekle
    auth_headers = HEADERS.copy()
    auth_headers["Authorization"] = f"Bearer {token}"
    
    try:
        response = requests.post(CONTENT_URL, json=payload, headers=auth_headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("Success"):
                print(f"✅ {video_id} verisi başarıyla çekildi.")
                return data.get("Result") # Sadece video detay kısmını döndür
            else:
                print(f"❌ {video_id} verisi alınamadı: {data.get('Message')}")
                return None
        else:
            print(f"❌ HTTP Hatası ({video_id}): {response.status_code}")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

def main():
    if not EMAIL or not PASSWORD:
        print("❌ E-posta veya Şifre bulunamadı! GitHub Secrets ayarlarını kontrol et.")
        return

    # 1. Giriş Yap
    token = login()
    if not token:
        return

    # 2. Çekilecek Videoları Belirle
    # BURASI ÖNEMLİ: Şimdilik sadece senin bildiğin ID'yi çekiyoruz.
    # 1. Adımdaki "Liste URL'sini" bulduğunda buraya tüm listeyi çeken kodu ekleyeceğiz.
    target_ids = ["EFQ3X5f4"] 
    
    all_data = []

    print(f"\n🚀 {len(target_ids)} adet video taranacak...")

    for vid in target_ids:
        data = get_video_details(vid, token)
        if data:
            all_data.append(data)
        time.sleep(1) # Hız sınırı

    # 3. Veriyi Kaydet
    if all_data:
        with open("gain_data.json", "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=4, ensure_ascii=False)
        print("\n🏁 İşlem tamamlandı. 'gain_data.json' dosyası oluşturuldu.")
    else:
        print("\n⚠️ Hiçbir veri çekilemedi.")

if __name__ == "__main__":
    main()