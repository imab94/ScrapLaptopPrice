import re
import requests
from bs4 import BeautifulSoup
import json

laptops = {}

for li in range(0,30):
    fetch_laptop_price = f"https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={li}"
    resp = requests.get(fetch_laptop_price)
    soup = BeautifulSoup(resp.content, 'html.parser')
    div_tags = soup.find_all("div", attrs={"class": "_2kHMtA"})

    for div in div_tags:
        text = div.text.strip()
        try:
            # extract laptop name
            laptop_name = re.search(r'Add to Compare(.+)-', text).group(1).strip()
            # Extract laptop price
            laptop_price = re.search(r'₹(\d+(,\d+)*)', text).group(1)
            # Extract laptop description
            laptop_description = re.search(r'\)(.*)\d{1,2}% off', text).group(1).strip()
            # Extract rating
            rating = re.findall(r'([\d\.]+)\sRatings', text)
            # Reviews Extract
            reviews =  re.search(r'&\s*(\d+\s*Reviews)',text)
            if reviews:
                reviews = reviews.group(1).strip()
            else:
                reviews = "No Reviews Found"

            if rating:
                rating = rating[0]
            else:
                rating = "Not found"

            laptops[laptop_name] = {
                'Name': laptop_name,
                'Price': laptop_price,
                'Description': laptop_description,
                "Rating":rating,
                "Reviews":reviews
            }
        except:
            pass

# write the laptops data to a JSON file
with open('laptops.json', 'w') as file:
    json.dump(laptops, file, indent=4)
