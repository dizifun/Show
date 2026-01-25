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
        # 'fmp4' formatından kaçınmak için standart HLS (hls-...) formatlarını öncelikli hale getirdik
        # Bu, player uyumluluğunu (örneğin TS segmentleri) artırır.
        'format': 'bestvideo[protocol^=hls]+bestaudio/best[protocol^=hls]/best',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            # Linkin kendisini ve başlığını alıyoruz
            return info.get('url'), info.get('title')
    except Exception as e:
        print(f"⚠️ Link çekilemedi: {e}")
        return None, None

def generate_m3u():
    """Playlisti tarar ve dosyayı oluşturur."""
    print("🔄 Playlist taranıyor...")

    # Playlist içindeki videoların listesini al
    ydl_opts_list = {
        'quiet': True,
        'extract_flat': True,
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
    m3u_content += f"#EXTREM: Bu liste {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} tarihinde güncellendi.\n"

    success_count = 0

    for entry in entries:
        if not entry: continue

        video_url = entry.get('url')
        if not video_url:
            video_url = f"https://www.dailymotion.com/video/{entry.get('id')}"

        print(f"⏳ İşleniyor: {entry.get('title', 'Bilinmeyen')}")

        stream_url, title = get_stream_link(video_url)

        if stream_url:
            # Player'ların daha iyi tanıması için 'tvg-name' gibi basit etiketler ekleyebilirsin
            m3u_content += f"#EXTINF:-1 group-title=\"Dailymotion\",{title}\n"
            m3u_content += f"{stream_url}\n"
            success_count += 1

    # Dosyayı yaz
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_content)

    print(f"\n✅ İşlem tamam! Toplam {success_count} kanal eklendi.")

if __name__ == "__main__":
    generate_m3u()
