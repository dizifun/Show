import requests
import re
from datetime import datetime
import time

def get_playlist_videos(playlist_id):
    """
    Dailymotion playlist'inden tüm videoları çeker
    """
    videos = []
    page = 1
    limit = 100  # Her sayfada maksimum video sayısı
    
    print(f"📋 Playlist çekiliyor: {playlist_id}")
    
    while True:
        try:
            # Dailymotion API - Playlist videos endpoint
            api_url = f"https://api.dailymotion.com/playlist/{playlist_id}/videos"
            params = {
                'fields': 'id,title,stream_live_hls_url,channel',
                'limit': limit,
                'page': page
            }
            
            response = requests.get(api_url, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'list' in data and len(data['list']) > 0:
                    videos.extend(data['list'])
                    print(f"  📄 Sayfa {page}: {len(data['list'])} video bulundu")
                    
                    # Daha fazla sayfa var mı kontrol et
                    if data.get('has_more', False):
                        page += 1
                        time.sleep(0.5)  # Rate limit için bekleme
                    else:
                        break
                else:
                    break
            else:
                print(f"  ❌ API Hatası: {response.status_code}")
                break
                
        except Exception as e:
            print(f"  ❌ Hata: {str(e)}")
            break
    
    print(f"✅ Toplam {len(videos)} video bulundu\n")
    return videos

def get_stream_url(video_id):
    """
    Video ID'sinden stream URL'sini çeker
    """
    try:
        # Video detaylarını al
        api_url = f"https://api.dailymotion.com/video/{video_id}"
        params = {
            'fields': 'stream_live_hls_url,qualities'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Canlı yayın URL'si varsa onu kullan
            if 'stream_live_hls_url' in data and data['stream_live_hls_url']:
                return data['stream_live_hls_url']
            
            # Yoksa qualities içinden en iyi kaliteyi al
            if 'qualities' in data:
                qualities = data['qualities']
                # Öncelik sırası: 1080, 720, 480, 380, 240
                for quality in ['1080', '720', '480', '380', '240']:
                    if quality in qualities and qualities[quality]:
                        for item in qualities[quality]:
                            if item.get('type') == 'application/x-mpegURL':
                                return item.get('url')
        
        return None
        
    except Exception as e:
        print(f"    ⚠️ Stream URL alınamadı: {str(e)}")
        return None

def normalize_stream_url(url):
    """
    fmp4 formatındaki URL'leri standart formata çevirir
    """
    if not url:
        return None
        
    # fmp4 içeren URL'leri tespit et
    if 'fmp4' in url and 'manifest.m3u8' in url:
        # Video ID'yi çıkar
        match = re.search(r'/video/(\d+)/', url)
        if match:
            video_id = match.group(1)
            base_url = url.split('/sec(')[0]
            sec_token = re.search(r'/sec\((.*?)\)', url)
            
            if sec_token:
                token = sec_token.group(1)
                # Video ID'den standart path oluştur
                parts = [video_id[i:i+3] for i in range(0, len(video_id), 3)]
                new_url = f"{base_url}/sec({token})/video/{'/'.join(parts)}/{video_id}_mp4_h264_aac.m3u8"
                return new_url
    
    return url

def validate_stream_url(url):
    """
    Stream URL'sini kontrol eder
    """
    if not url:
        return False, "URL bulunamadı"
        
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://www.dailymotion.com/',
            'Origin': 'https://www.dailymotion.com'
        }
        response = requests.head(url, headers=headers, timeout=10, allow_redirects=True)
        
        if response.status_code in range(200, 400):
            return True, "OK"
        else:
            return False, f"HTTP {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def process_playlist(playlist_id):
    """
    Playlist'i işler ve stream bilgilerini çıkarır
    """
    videos = get_playlist_videos(playlist_id)
    streams = []
    
    for idx, video in enumerate(videos, 1):
        video_id = video.get('id')
        title = video.get('title', f'Video {idx}')
        channel = video.get('channel', 'Bilinmeyen')
        
        print(f"🔄 [{idx}/{len(videos)}] {title}")
        
        # Stream URL'sini al
        stream_url = get_stream_url(video_id)
        
        if stream_url:
            # URL'yi normalize et
            normalized_url = normalize_stream_url(stream_url)
            
            # URL'yi test et
            is_valid, status = validate_stream_url(normalized_url)
            
            if is_valid:
                streams.append({
                    'name': title,
                    'url': normalized_url,
                    'group': channel,
                    'id': video_id
                })
                print(f"  ✅ Stream çalışıyor")
            else:
                # Normalize edilmiş çalışmazsa orijinali dene
                is_valid_orig, _ = validate_stream_url(stream_url)
                if is_valid_orig:
                    streams.append({
                        'name': title,
                        'url': stream_url,
                        'group': channel,
                        'id': video_id
                    })
                    print(f"  ✅ Stream çalışıyor (Orijinal)")
                else:
                    print(f"  ❌ Stream çalışmıyor: {status}")
        else:
            print(f"  ⚠️ Stream URL bulunamadı")
        
        # Rate limit için kısa bekleme
        time.sleep(0.3)
    
    return streams

def create_m3u_playlist(streams, playlist_id):
    """
    M3U playlist dosyası oluşturur
    """
    m3u_content = '#EXTM3U\n'
    m3u_content += f'# Dailymotion Playlist: {playlist_id}\n'
    m3u_content += f'# Güncelleme: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n'
    m3u_content += f'# Toplam Kanal: {len(streams)}\n'
    m3u_content += f'# Kaynak: https://www.dailymotion.com/playlist/{playlist_id}\n\n'
    
    for stream in streams:
        # Özel karakterleri temizle
        clean_name = stream['name'].replace('"', "'").strip()
        clean_group = stream['group'].replace('"', "'").strip()
        
        m3u_content += f'#EXTINF:-1 tvg-id="{stream["id"]}" tvg-name="{clean_name}" group-title="{clean_group}",{clean_name}\n'
        m3u_content += f'{stream["url"]}\n\n'
    
    return m3u_content

def main():
    print("=" * 70)
    print("📺 Dailymotion Playlist to M3U Generator")
    print("=" * 70)
    print()
    
    # Playlist ID'leri (x72eij formatında)
    playlists = [
        'x72eij',  # Buraya başka playlist ID'leri ekleyebilirsiniz
    ]
    
    all_streams = []
    
    for playlist_id in playlists:
        print(f"\n{'='*70}")
        print(f"🎬 İşleniyor: https://www.dailymotion.com/playlist/{playlist_id}")
        print(f"{'='*70}\n")
        
        streams = process_playlist(playlist_id)
        all_streams.extend(streams)
        
        print(f"\n✅ Bu playlist'ten {len(streams)} çalışan kanal eklendi\n")
    
    if all_streams:
        # M3U dosyası oluştur
        playlist_content = create_m3u_playlist(all_streams, playlists[0])
        
        # Dosyaya kaydet
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write(playlist_content)
        
        print("\n" + "=" * 70)
        print(f"✅ BAŞARILI! playlist.m3u oluşturuldu")
        print(f"📊 Toplam: {len(all_streams)} çalışan kanal")
        print("=" * 70)
    else:
        print("\n❌ Hiç çalışan stream bulunamadı!")
        # Boş dosya oluşturma
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n# Çalışan stream bulunamadı\n')

if __name__ == "__main__":
    main()