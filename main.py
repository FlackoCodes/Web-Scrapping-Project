import csv
import time
import requests
from bs4 import BeautifulSoup

def extract_product_data(product_div):
    """
    Extracts product data from a product div.
    """
    # Extract the product URL
    product_url = product_div.find('a', {'class': 'a-link-normal'})
    product_url = product_url['href'] if product_url else ''
    
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

# Open a CSV file for writing the scraped data
file = open('amazon_scraped_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(file)

# Write the header row for the CSV file
writer.writerow(['Product URL', 'Product Name', 'Price', 'Ratings', 'Reviews'])

# Loop over the 20 pages of the site
for page in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&page={page}&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    product_divs = soup.find_all('div', {'class': 's-result-item'})

    # Loop over the product divs
    for product_div in product_divs:
        # Extract the product data
        product_data = extract_product_data(product_div)
        
        # Write the scraped data to the CSV file
        writer.writerow(product_data)

    time.sleep(15)


file.close()
