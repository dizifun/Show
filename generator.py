import yt_dlp

def get_real_stream_link(ok_ru_url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]', # En yüksek kalite
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(ok_ru_url, download=False)
            
            # Kaliteleri tara ve en yükseğini (1080p/720p) seç
            # Ok.ru genellikle 'metadata' içinde farklı kaliteler sunar
            formats = info.get('formats', [])
            
            # Player'ın kabul edeceği doğrudan MP4 veya M3U8 linkini bul
            real_link = info.get('url') 
            
            return real_link
        except Exception as e:
            return f"Hata: {e}"

# Örnek Kullanım
url = "https://ok.ru/video/11380833323681"
print(get_real_stream_link(url))
