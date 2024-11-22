from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Configure Chrome browser options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Launch the browser and open the Cookie Clicker game
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

# Locate the main cookie element
cookie = driver.find_element(By.XPATH, '//*[@id="cookie"]')

# Locate all store items and get their IDs
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_li = [it.get_attribute("id") for it in items]

# Set timers
timeout = time.time() + 5  # 5-second interval for upgrades
five_min = time.time() + 60 * 5  # Script runs for 5 minutes

while True:
    # Continuously click the cookie
    cookie.click()

    # Every 5 seconds, check for available upgrades
    if time.time() > timeout:
        # Get all item costs
        costs = driver.find_elements(By.CSS_SELECTOR, "#store div b")
        cost_li = [it.text.strip().replace(",", "") for it in costs]

        # Create a dictionary mapping items to their costs
        it_co = {}
        for i in range(len(cost_li)):
            try:
                cost = int(cost_li[i].split("-")[1])  # Extract cost
            except:
                continue  # Skip if no cost is available
            item = cost_li[i].split("-")[0]  # Extract item name
            it_co[item] = cost

        # Get the current amount of money
        cur_mon = driver.find_element(By.XPATH, '//*[@id="money"]').text
        cur_mon = int(cur_mon.replace(",", ""))

        # Find all upgrades that can be afforded
        affordable_upgrades = {key: value for key, value in it_co.items() if value <= cur_mon}

        # If upgrades are available, buy the most expensive one
        if affordable_upgrades:
            max_upgrade = max(affordable_upgrades, key=affordable_upgrades.get)
            print(f"Buying {max_upgrade}")
            to_click = driver.find_element(By.CSS_SELECTOR, f"#buy{max_upgrade}")
            to_click.click()

        # Reset the timer for upgrades
        timeout = time.time() + 5
