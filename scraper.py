from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import time


def scrape_news():
    try:
        # Configure Chrome options for Heroku
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--remote-debugging-port=9222')

        # Check if running on Heroku (environment variable set in Heroku config)
        if 'DYNO' in os.environ:
            chrome_options.binary_location = '/usr/bin/google-chrome'
            driver = webdriver.Chrome(
                options=chrome_options
            )
        else:
            # Local development setup
            from webdriver_manager.chrome import ChromeDriverManager
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=chrome_options
            )

        url = "https://www.thestar.com.my/news"
        driver.get(url)

        # Add error handling for timeouts
        try:
            time.sleep(3)  # Wait for JavaScript to load content

            articles = []
            news_items = driver.find_elements(By.CSS_SELECTOR, "h2 a")
            image_items = driver.find_elements(By.CSS_SELECTOR, "a img")

            for index, item in enumerate(news_items):
                try:
                    title = item.text
                    link = item.get_attribute("href")

                    image_url = ""
                    if index < len(image_items):
                        image_url = image_items[index].get_attribute("src")

                    if title and link:  # Only add if we have at least title and link
                        articles.append({
                            "title": title,
                            "link": link,
                            "image": image_url
                        })
                except Exception as e:
                    print(f"Error processing article {index}: {str(e)}")
                    continue

            return articles

        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return []

        finally:
            driver.quit()

    except Exception as e:
        print(f"Critical error in scrape_news: {str(e)}")
        return []


if __name__ == "__main__":
    news = scrape_news()
    print(news)
