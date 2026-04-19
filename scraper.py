import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import pytz
from datetime import datetime

# Website URL
BASE_URL = "http://180.94.28.28/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": BASE_URL
}

def get_raw_m3u8_link(play_url):
    try:
        res = requests.get(play_url, headers=headers, timeout=10)
        if res.status_code == 200:
            # Token soho m3u8 link khuje ber korar regex
            match = re.search(r'(http://[^\s"\'<>]+\.m3u8[^\s"\'<>]*)', res.text)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Error fetching token: {e}")
    return None

def scrape_iptv():
    try:
        response = requests.get(BASE_URL, headers=headers, timeout=10)
        if response.status_code != 200:
            print("Website a dhoka jacche na!")
            return

        soup = BeautifulSoup(response.text, "html.parser")
        
        # Bangladesh Time (BST) set kora
        bd_time = datetime.now(pytz.timezone('Asia/Dhaka')).strftime('%Y-%m-%d %I:%M %p')
        m3u_content = f"#EXTM3U\n# Last Scraped: {bd_time} (BST)\n\n"
        
        ul_tag = soup.find('ul', id='vidlink')
        if not ul_tag:
            print("Channel list paowa jayni!")
            return

        channels = ul_tag.find_all('li')
        count = 0

        for li in channels:
            try:
                category = li.get('class', ['Other'])[0]
                a_tag = li.find('a')
                if not a_tag: continue
                
                onclick_text = a_tag.get('onclick', '')
                link_match = re.search(r"href='(.*?)'", onclick_text)
                
                if link_match:
                    relative_link = link_match.group(1)
                    play_url = urljoin(BASE_URL, relative_link)
                    
                    channel_name = relative_link.split('=')[-1].replace('-', ' ')
                    img_tag = a_tag.find('img')
                    logo_url = urljoin(BASE_URL, img_tag.get('src')) if img_tag else ""
                    
                    # Deep Scraping: Token anar function call kora
                    real_m3u8_link = get_raw_m3u8_link(play_url)
                    
                    if real_m3u8_link:
                        m3u_content += f'#EXTINF:-1 tvg-id="" tvg-name="{channel_name}" tvg-logo="{logo_url}" group-title="{category}",{channel_name}\n'
                        m3u_content += f'{real_m3u8_link}\n'
                        count += 1
                        print(f"Added: {channel_name}")
                    
            except Exception as e:
                pass

        if count > 0:
            with open("playlist.m3u", "w", encoding="utf-8") as file:
                file.write(m3u_content)
            print(f"\nSuccess! Total {count} channels saved.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_iptv()
