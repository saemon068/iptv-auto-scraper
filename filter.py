import urllib.request

url = "https://raw.githubusercontent.com/maybetv/Jo/refs/heads/main/Zoh.m3u"
output_file = "sports.m3u"

def filter_m3u():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            lines = response.read().decode('utf-8').splitlines()

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            
            block = []
            for line in lines:
                line_str = line.strip()
                
                if not line_str:
                    continue
                if line_str.startswith("#EXTM3U"):
                    continue
                    
                # চ্যানেলের প্রতিটি লাইন (EXTINF, KODIPROP ইত্যাদি) ব্লকে জমা হবে
                block.append(line_str)
                
                # লাইনটি যদি # দিয়ে শুরু না হয়, তার মানে এটি ভিডিও লিংক (চ্যানেলের ব্লক শেষ)
                if not line_str.startswith("#"):
                    # চেক করবো এই ব্লকে group-title="Sports" আছে কিনা
                    is_sports = False
                    for b in block:
                        if b.startswith("#EXTINF") and 'group-title="sports"' in b.lower():
                            is_sports = True
                            break
                    
                    # স্পোর্টস চ্যানেল হলে পুরো ব্লক (DRM Key সহ) ফাইলে সেভ করবে
                    if is_sports:
                        for b in block:
                            f.write(b + "\n")
                            
                    # পরের চ্যানেলের জন্য ব্লক খালি করে দেওয়া
                    block = []
                    
        print("Sports playlist updated with full DRM keys!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    filter_m3u()
