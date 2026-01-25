import yt_dlp
import json

def get_ok_ru_m3u8(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best'  # En yüksek kaliteyi hedefle
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            # Ok.ru genellikle doğrudan m3u8 formatı sağlar
            m3u8_url = info.get('url')
            title = info.get('title', 'Kurtlar Vadisi')
            return {"title": title, "url": m3u8_url}
        except Exception as e:
            print(f"Hata: {e}")
            return None

# Örnek Link (Playlist veya tek video olabilir)
video_urls = [
    "https://ok.ru/video/11380833323681"
]

results = []
for url in video_urls:
    data = get_ok_ru_m3u8(url)
    if data:
        results.append(data)

# M3U Formatında Kaydet
with open("playlist.m3u", "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    for item in results:
        f.write(f"#EXTINF:-1, {item['title']}\n")
        f.write(f"{item['url']}\n")

# JSON Formatında da Kaydet (Uygulaman için daha iyi olabilir)
with open("links.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print("Linkler başarıyla güncellendi.")
