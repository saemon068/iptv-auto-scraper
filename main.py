import urllib.request

# আপনার দেওয়া লিংক
url = "http://beta.ashtv.com.bd/server/iptv.m3u?v=1776601355539"
output_file = "playlist.m3u"

# সার্ভার ব্লক এড়াতে User-Agent যোগ করা হলো
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req) as response, open(output_file, 'wb') as out_file:
        out_file.write(response.read())
    print("Playlist successfully downloaded and saved as playlist.m3u")
except Exception as e:
    print(f"Error downloading playlist: {e}")
