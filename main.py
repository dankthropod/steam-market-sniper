import time
import yaml
from selenium import webdriver

# Read the configuration file
with open('config.yml') as f:
    config = yaml.safe_load(f)

# Define the Chrome driver and options
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# Loop through each URL in the configuration file
for item in config['items']:
    url = item['url']
    threshold_price = item['threshold_price']
    print(f"Checking {url} for price under {threshold_price}...")

    # Infinite loop to search for the price
    while True:
        driver.get(url)
        time.sleep(5)  # wait for the page to load

        # Find the current price of the item
        try:
            price_element = driver.find_element_by_css_selector('.market_listing_price_with_fee')
            price = float(price_element.text.strip().replace(',', '.').replace('$', ''))
        except:
            # Price element not found, skip this iteration
            continue

        # Check if the price is below the threshold
        if price < threshold_price:
            print(f"Price of {url} is below {threshold_price}!")
            # TODO: send an alert or notification to the user

        # Wait for some time before refreshing the page
        time.sleep(60)
