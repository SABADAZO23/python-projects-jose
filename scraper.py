import urllib.request
import re

url = 'http://example.com'
response = urllib.request.urlopen(url)
html = response.read().decode()

titles = re.findall(r'<h2>(.*?)</h2>', html)
for title in titles:
    print("Título:", title)