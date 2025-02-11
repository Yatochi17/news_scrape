from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_news():
    driver = None
    try:
        logger.info("Starting scrape_news function")

        # Configure Chrome options for Heroku
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--remote-debugging-port=9222')
        chrome_options.add_argument('--window-size=1920,1080')  # Set a specific window size
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        logger.info("Chrome options configured")

        # Check if running on Heroku
        if 'DYNO' in os.environ:
            logger.info("Running on Heroku")
            chrome_options.binary_location = '/usr/bin/google-chrome'
            driver = webdriver.Chrome(options=chrome_options)
        else:
            logger.info("Running locally")
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )

        url = "https://www.thestar.com.my/news"
        logger.info(f"Attempting to access URL: {url}")

        driver.get(url)
        logger.info("Page loaded successfully")

        # Wait for content to load with explicit wait
        wait = WebDriverWait(driver, 10)

        try:
            # Wait for h2 elements to be present
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h2 a")))
            logger.info("H2 elements found on page")

            # Get page source for debugging
            page_source = driver.page_source
            logger.info(f"Page source length: {len(page_source)}")

            articles = []
            news_items = driver.find_elements(By.CSS_SELECTOR, "h2 a")
            logger.info(f"Found {len(news_items)} news items")

            image_items = driver.find_elements(By.CSS_SELECTOR, "a img")
            logger.info(f"Found {len(image_items)} image items")

            for index, item in enumerate(news_items):
                try:
                    title = item.text
                    link = item.get_attribute("href")

                    image_url = ""
                    if index < len(image_items):
                        image_url = image_items[index].get_attribute("src")

                    if title and link:
                        articles.append({
                            "title": title,
                            "link": link,
                            "image": image_url
                        })
                        logger.info(f"Added article {index + 1}: {title[:50]}...")
                except Exception as e:
                    logger.error(f"Error processing article {index}: {str(e)}")
                    continue

            logger.info(f"Successfully scraped {len(articles)} articles")
            return articles

        except Exception as e:
            logger.error(f"Error during scraping: {str(e)}")
            return []

    except Exception as e:
        logger.error(f"Critical error in scrape_news: {str(e)}")
        return []

    finally:
        if driver:
            logger.info("Closing driver")
            driver.quit()


if __name__ == "__main__":
    news = scrape_news()
    print(f"Total articles scraped: {len(news)}")
    if len(news) > 0:
        print("First article:", news[0])
