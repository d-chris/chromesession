from chromesession import chrome

with chrome() as driver:
    driver.get("https://www.google.com")
    print(driver.title)
