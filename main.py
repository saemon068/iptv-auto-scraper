import urllib.request
import datetime
import os

url = "https://ashtv.com.bd/server/playlist.m3u"
output_file = "playlist.m3u"

def fetch_and_format_playlist():
    try:
        # সার্ভার থেকে ডেটা নেওয়া
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        lines = content.split('\n')
        
        channels = []
        current_extinf = ""
        
        # শুধু দরকারি লাইনগুলো (চ্যানেল নাম এবং লিংক) ফিল্টার করা
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                current_extinf = line
            elif line.startswith("http") and current_extinf:
                channels.append((current_extinf, line))
                current_extinf = "" # Reset for next
                
        channel_count = len(channels)
        
        # নতুন চ্যানেলের লিস্ট তৈরি করা
        channels_text = ""
        for extinf, link in channels:
            channels_text += f"{extinf}\n{link}\n\n"
            
        channels_text = channels_text.strip()
        
        # আগের ফাইল চেক করা (নতুন আপডেট এসেছে কি না দেখার জন্য)
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                old_content = f.read()
                # আগের ফাইলের শুধু চ্যানেলের অংশটুকু আলাদা করা
                if "#=================================" in old_content:
                    old_channels_text = old_content.split("#=================================")[-1].strip()
                    if old_channels_text == channels_text:
                        print("কোনো নতুন আপডেট আসেনি। আগের কোডই বহাল আছে।")
                        return # কোনো পরিবর্তন হয়নি, তাই ফাইল সেভ হবে না
        
        # বাংলাদেশ সময় (UTC+6)
        tz = datetime.timezone(datetime.timedelta(hours=6))
        now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        
        # আপনার কাস্টম হেডার
        header = f"""#EXTM3U
#=================================
# 🖥️ Developed by: S.A.Emon
# 🔗 Telegram: https://t.me/Obiram_tv
# 🕒 Last Updated: {now} (BD Time)
# 📺 Channels Count: {channel_count}
#================================="""

        # ফাইনাল কন্টেন্ট জোড়া লাগানো
        final_content = f"{header}\n\n{channels_text}\n"
        
        # নতুন ফাইল সেভ করা
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"প্লেলিস্ট সফলভাবে আপডেট হয়েছে! মোট চ্যানেল: {channel_count}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_and_format_playlist()
