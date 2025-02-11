from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def scrape_news():

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background (no browser window)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = "https://www.thestar.com.my/news"
    driver.get(url)
    time.sleep(3)  # Wait for JavaScript to load content

    articles = []

    # Find news links inside <h2> tags
    news_items = driver.find_elements(By.CSS_SELECTOR, "h2 a")
    image_items = driver.find_elements(By.CSS_SELECTOR, "a img")  # Extracting images inside <a> tags

    for index, item in enumerate(news_items):
        title = item.text
        link = item.get_attribute("href")

        # Extract image if available
        image_url = ""
        if index < len(image_items):
            image_url = image_items[index].get_attribute("src")

        articles.append({"title": title, "link": link, "image": image_url})

    driver.quit()  # Close the browser
    return articles


# Test scraping separately
if __name__ == "__main__":
    news = scrape_news()
    print(news)


