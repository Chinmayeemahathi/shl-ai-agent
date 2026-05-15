import requests
from bs4 import BeautifulSoup

url = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("STATUS:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

print(soup.title)