from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

web = 'https://500.co/companies'
path = 'C:/path/to/chromedriver'  # introduce path here

# Creating the driver
driver_service = Service(executable_path=path)
driver = webdriver.Chrome(service=driver_service)
driver.implicitly_wait(600)  # set implicit wait time to 10 min
driver.get(web)

# Initialize variables
all_data = []

while True:
    # Finding Elements
    containers = driver.find_elements(by='xpath', value='//div[@class="grid table-row"]')

    for container in containers:
        data = {}
        try:
            data['Name'] = container.find_element(by='xpath', value='.//div[@class="table-value company-name"]').text
        except:
            data['Name'] = ""
        try:
            data['Industry'] = container.find_element(by='xpath', value='.//div[@class="span-3 m-span-6"][1]/div[2]').text
        except:
            data['Industry'] = ""
        try:
            data['Sub_Industry'] = container.find_element(by='xpath', value='.//div[@class="span-3 m-span-6"][2]/div[2]').text
        except:
            data['Sub_Industry'] = ""
        try:
            data['Location'] = container.find_element(by='xpath', value='.//div[@class="span-3 m-span-12"]/div[2]').text
        except:
            data['Location'] = ""

        all_data.append(data)

    # Check if there is a "Next" button to go to the next page
    next_button = driver.find_elements(by='xpath', value='//div[@class="pages"]/ul/li[@class="next"]')
    if not next_button:
        break  # Stop pagination if there is no "Next" button

    # Click on the "Next" button to navigate to the next page
    next_button[-1].click()
    time.sleep(10)  # Add a short delay for the next page to load

# Exporting data to a CSV file
df_headlines = pd.DataFrame(all_data)
df_headlines.to_csv('500Companies_6.csv', index=False)

# Wait for 10 minutes before closing the browser
time.sleep(600)
driver.quit()
