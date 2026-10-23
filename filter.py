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
            keep_next_line = False
            for line in lines:
                if line.startswith("#EXTINF"):
                    if 'group-title="sports"' in line.lower() or 'group-title="Sports"' in line:
                        f.write(line + "\n")
                        keep_next_line = True
                    else:
                        keep_next_line = False
                elif keep_next_line and line.strip() and not line.startswith("#"):
                    f.write(line + "\n")
                    keep_next_line = False
        print("Sports playlist updated!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    filter_m3u()
