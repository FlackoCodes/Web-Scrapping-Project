import csv
import time
import requests
from bs4 import BeautifulSoup
from lxml import etree


def extract_product_data(product_div):
    """
    Extracts product data from a product div.
    """
    # Extract the product URL
    product_url_element = product.select_one('a.a-link-normal')
    try:
         product_url = product_url_element['href']
    except (TypeError, KeyError):
        product_url = ''



    # Extract the product name
    product_name = product_div.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
    product_name = product_name.text if product_name else ''

    # Extract the price
    price = product_div.find('span', {'class': 'a-offscreen'})
    price = price.text if price else ''

    # Extract the ratings
    ratings = product_div.find('span', {'class': 'a-icon-alt'})
    ratings = ratings.text if ratings else ''

    # Extract the number of reviews
    reviews = product_div.find('span', {'class': 'a-size-base s-underline-text'})
    reviews = reviews.text if reviews else ''

    # Return the extracted data
    return product_url, product_name, price, ratings, reviews


def get_product_details(URL, headers):
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    asin = soup.select_one('#ASIN')['value'] if soup.select_one('#ASIN') else ''
    manufacturer = soup.select_one('#bylineInfo').text.strip() if soup.select_one('#bylineInfo') else ''
    product_description = soup.select_one('#productTitle').text.strip() if soup.select_one('#productTitle') else ''
    return asin, product_description, manufacturer


URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"

file = open('amazon_scraped_data2.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Write headers to the csv file
writer.writerow(["Product URL", "ASIN", "Product Description", "Manufacturer"])

# Loop through all 20 pages
for page in range(1, 21):
    page_url = f"{URL}&page={page}"
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    product_list = soup.select('.s-result-item')

    # Loop through all products on the page
    for product in product_list:
        product_url = product.select_one('a.a-link-normal')['href']
        asin, product_description, manufacturer = get_product_details(product_url, headers)
        # Extract product data from the product div
        product_data = extract_product_data(product)
        # Write product details to the csv file
        writer.writerow([product_data[0], asin, product_description, manufacturer])
        
    time.sleep(15)

file.close()
