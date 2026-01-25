import yt_dlp
import os
import datetime

# Hedef Playlist ve Çıktı Dosyası
PLAYLIST_URL = "https://www.dailymotion.com/playlist/x72eij"
OUTPUT_FILE = "playlist.m3u"

def get_stream_link(video_url):
    """Tek bir videonun en iyi m3u8 linkini çeker."""
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': 'best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return info.get('url'), info.get('title')
    except Exception:
        return None, None

def generate_m3u():
    """Playlisti tarar ve dosyayı oluşturur."""
    print("🔄 Playlist taranıyor...")
    
    # Playlist içindeki videoların listesini al (detaylara girmeden)
    ydl_opts_list = {
        'quiet': True,
        'extract_flat': True, # Hızlı tarama için
        'ignoreerrors': True,
    }
    
    entries = []
    with yt_dlp.YoutubeDL(ydl_opts_list) as ydl:
        try:
            result = ydl.extract_info(PLAYLIST_URL, download=False)
            if 'entries' in result:
                entries = result['entries']
        except Exception as e:
            print(f"❌ Playlist hatası: {e}")
            return

    # M3U İçeriğini Hazırla
    m3u_content = "#EXTM3U\n"
    m3u_content += f"#EXTREM: Bu liste {datetime.datetime.now()} tarihinde güncellendi.\n"

    success_count = 0
    
    for entry in entries:
        if not entry: continue
        
        # 'extract_flat' kullandığımız için tam URL'yi oluşturmamız gerekebilir
        video_url = entry.get('url')
        if not video_url:
            video_url = f"https://www.dailymotion.com/video/{entry.get('id')}"

        print(f"⏳ İşleniyor: {entry.get('title', 'Bilinmeyen')}")
        
        # Her video için taze tokenlı linki al
        stream_url, title = get_stream_link(video_url)
        
        if stream_url:
            m3u_content += f"#EXTINF:-1 group-title=\"Dailymotion\",{title}\n"
            m3u_content += f"{stream_url}\n"
            success_count += 1
    
    # Dosyayı yaz
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"\n✅ İşlem tamam! Toplam {success_count} kanal eklendi.")

if __name__ == "__main__":
    generate_m3u()
