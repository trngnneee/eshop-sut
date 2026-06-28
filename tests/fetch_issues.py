import urllib.request
import json
import codecs

url = "https://api.github.com/repos/trngnneee/eshop-sut/issues?state=all&per_page=100"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
        with codecs.open("tests/issues_list.txt", "w", "utf-8") as f:
            for issue in data:
                title = issue['title']
                f.write(f"#{issue['number']}: {title} ({issue['html_url']})\n")
        print("Success! Saved issues list to tests/issues_list.txt")
except Exception as e:
    print(f"Error fetching issues: {e}")
