#!/usr/bin/env python3
import os
import sys
import time
import yt_dlp

# Read channel info from txt (format: name|group|logo|url)
channels = []
with open('youtube_channel_info.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 4:
                name, group, logo, url = parts[:4]
                channels.append((name, group, logo, url))

# Generate M3U
with open('youtube.m3u', 'w') as m3u_file:
    m3u_file.write('#EXTM3U x-tvg-url="https://epg.example.com/epg.xml"\n')  # Optional EPG

    for i, (name, group, logo, url) in enumerate(channels):
        try:
            ydl_opts = {
                'quiet': False,  # Verbose for logs
                'no_warnings': False,
                'format': 'bestvideo+bestaudio/best',  # Best for live HLS
                'get_url': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info.get('is_live'):
                    m3u_url = info['url']
                    if '.m3u8' in m3u_url:
                        extinf = f'#EXTINF:-1 tvg-name="{name}" tvg-logo="{logo}" group-title="{group}",{name}\n{m3u_url}\n'
                        m3u_file.write(extinf)
                        print(f"Success: {name} - {m3u_url}")
                    else:
                        print(f"Warning: No HLS for {name}")
                else:
                    print(f"Skipping: {name} not live")
        except Exception as e:
            print(f"Error for {name}: {str(e)}", file=sys.stderr)
        finally:
            if i < len(channels) - 1:
                time.sleep(5)  # Delay to avoid rate limits

print("M3U generation complete. Check last_run_error.log for issues.")
