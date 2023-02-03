import csv
import time
import requests
from bs4 import BeautifulSoup


URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

file = open('amazon_scraped_data2.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

def get_product_details(URL, headers):
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    product_description = soup.select_one('#productTitle').text.strip()
    asin = soup.select_one('#ASIN')['value']
    manufacturer = soup.select_one('#bylineInfo').text.strip()
    return asin, product_description, manufacturer

# Write headers to the csv file
writer.writerow(["ASIN", "Product Description", "Manufacturer"])

# Loop through all 16 pages
for page in range(1, 17):
    page_url = f"{URL}&page={page}"
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    product_list = soup.select('.s-result-item')

    # Loop through all products on the page
    for product in product_list:
        product_url = product.select_one('a.a-link-normal')['href']
        asin, product_description, manufacturer = get_product_details(product_url, headers)
        # Write product details to the csv file
        writer.writerow([asin, product_description, manufacturer])
        
    time.sleep(15)

file.close()
