import requests
import json
import os
from datetime import datetime

# Hedef URL (Veri kaynağı)
SOURCE_URL = "https://raw.githubusercontent.com/9850392751/99456571/main/736519378"

# M3U Link Çözme Mantığı
# NOT: Verideki 'link' sadece bir ID (örn: "50"). Bunun çalışması için
# ID'nin başına sunucu adresi gelmeli. Aşağıdaki formatı biliyorsan değiştir.
# Şimdilik ID'yi olduğu gibi veya varsayılan bir yapıda bırakıyoruz.
def resolve_link(link_id):
    # ÖRNEK SENARYO: Eğer bu ID'ler bir m3u dosyasına gidiyorsa:
    # return f"http://ornek-sunucu.com/get.php?id={link_id}"
    
    # ŞİMDİLİK: Link ID'sini direkt döndürüyoruz veya placeholder yapıyoruz.
    return link_id 

def main():
    try:
        print(f"[{datetime.now()}] Veri çekiliyor...")
        response = requests.get(SOURCE_URL)
        response.raise_for_status()
        
        # Gelen veri string formatında olduğu için parse ediyoruz
        data = response.json()
        
        # 'ormoxChnlx' anahtarı altındaki listeyi alıyoruz
        channels = data.get("ormoxChnlx", [])
        
        clean_channels = []
        m3u_content = "#EXTM3U\n"

        print(f"[{datetime.now()}] {len(channels)} adet içerik işleniyor...")

        for item in channels:
            # Gerekli verileri ayıkla
            name = item.get("isim", "Bilinmeyen Kanal").replace("**", "").strip() # Yıldızları temizle
            image = item.get("resim", "")
            cat = item.get("kategori", "Genel")
            link_id = item.get("link", "")
            
            # Linki çöz (veya formatla)
            stream_url = resolve_link(link_id)

            # 1. Temiz JSON için obje oluştur
            clean_obj = {
                "name": name,
                "category": cat,
                "logo": image,
                "url": stream_url,
                "original_id": link_id
            }
            clean_channels.append(clean_obj)

            # 2. M3U satırını oluştur
            # Format: #EXTINF:-1 tvg-logo="url" group-title="kategori", İsim
            m3u_content += f'#EXTINF:-1 tvg-logo="{image}" group-title="{cat}", {name}\n'
            m3u_content += f'{stream_url}\n'

        # Çıktı klasörü oluştur
        if not os.path.exists("output"):
            os.makedirs("output")

        # Temiz JSON kaydet
        with open("output/playlist.json", "w", encoding="utf-8") as f:
            json.dump(clean_channels, f, ensure_ascii=False, indent=4)
            print(f"[{datetime.now()}] JSON dosyası kaydedildi: output/playlist.json")

        # M3U kaydet
        with open("output/playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            print(f"[{datetime.now()}] M3U dosyası kaydedildi: output/playlist.m3u")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
