import requests
import json
import os
from datetime import datetime

# Hedef URL
SOURCE_URL = "https://raw.githubusercontent.com/9850392751/99456571/main/736519378"

# Scriptin veriyi çekerken kullanacağı başlıklar (GitHub vs. engellemesin diye)
FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
}

# Eğer yayınlar sabit bir Referer istiyorsa buraya yazabilirsin (Örn: "https://vavoo.to/")
# Boş bırakırsan eklemez.
GLOBAL_REFERER = "" 

def resolve_link(link_id):
    # NOT: Burası hala ID döndürüyor. Eğer sunucu yapısını biliyorsan güncelle.
    # Örnek: return f"http://yayin-sunucusu.com/live/user/pass/{link_id}.ts"
    return link_id 

def main():
    try:
        print(f"[{datetime.now()}] Veri çekiliyor...")
        
        # Veriyi çekerken Header kullanıyoruz
        response = requests.get(SOURCE_URL, headers=FETCH_HEADERS)
        response.raise_for_status()
        
        data = response.json()
        channels = data.get("ormoxChnlx", [])
        
        clean_channels = []
        m3u_content = "#EXTM3U\n"

        print(f"[{datetime.now()}] {len(channels)} adet içerik işleniyor...")

        for item in channels:
            # Temel verileri al
            name = item.get("isim", "Bilinmeyen Kanal").replace("**", "").strip()
            image = item.get("resim", "")
            cat = item.get("kategori", "Genel")
            link_id = item.get("link", "")
            
            # JSON içindeki özel User-Agent'ı al
            custom_ua = item.get("userAgent", "")
            
            # Linki çöz
            base_url = resolve_link(link_id)
            
            # --- HEADER MANTIĞI ---
            # M3U oynatıcıları için URL sonuna header ekliyoruz (|User-Agent=X&Referer=Y)
            stream_url_with_headers = base_url
            header_parts = []

            # 1. User-Agent Ekle (Varsa JSON'dan, yoksa genelden)
            if custom_ua:
                header_parts.append(f"User-Agent={custom_ua}")
            else:
                header_parts.append(f"User-Agent={FETCH_HEADERS['User-Agent']}")

            # 2. Referer Ekle (Varsa)
            if GLOBAL_REFERER:
                header_parts.append(f"Referer={GLOBAL_REFERER}")
            
            # Parçaları birleştirip URL sonuna ekle (| işareti ile)
            if header_parts:
                stream_url_with_headers += "|" + "&".join(header_parts)

            # --- JSON ve M3U OLUŞTURMA ---

            # 1. Temiz JSON Objesi
            clean_obj = {
                "name": name,
                "category": cat,
                "logo": image,
                "url": base_url, # Ham URL
                "headers": {     # Headerları ayrı obje olarak da tutuyoruz
                    "User-Agent": custom_ua if custom_ua else FETCH_HEADERS['User-Agent'],
                    "Referer": GLOBAL_REFERER
                },
                "full_playable_url": stream_url_with_headers # Oynatıcıya verilecek hazır link
            }
            clean_channels.append(clean_obj)

            # 2. M3U Satırı
            m3u_content += f'#EXTINF:-1 tvg-logo="{image}" group-title="{cat}", {name}\n'
            m3u_content += f'{stream_url_with_headers}\n'

        # Klasör kontrolü
        if not os.path.exists("output"):
            os.makedirs("output")

        # Kaydet: JSON
        with open("output/playlist.json", "w", encoding="utf-8") as f:
            json.dump(clean_channels, f, ensure_ascii=False, indent=4)
            print(f"[{datetime.now()}] JSON kaydedildi (Headerlar eklendi).")

        # Kaydet: M3U
        with open("output/playlist.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_content)
            print(f"[{datetime.now()}] M3U kaydedildi (User-Agent destekli).")

    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    main()
