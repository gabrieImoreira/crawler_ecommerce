from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

class BrowserML:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable--web-security")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--memory-pressure-off")

        self.drive = webdriver.Chrome(options=self.chrome_options)

    def execute_command(self, query):
        self.drive.get(f"https://lista.mercadolivre.com.br/{query.replace(' ', '-')}")
        time.sleep(5)
        html = self.drive.page_source
        self.drive.quit()

        soup = BeautifulSoup(html, "html.parser")

        results = soup.find_all("div", class_="ui-search-result")

        data = []
        for result in results:
            link = None
            title = result.find("h2", class_="ui-search-item__title").text.strip()
            price = result.find("span", class_="andes-money-amount__fraction").text.strip()
            link_tag = result.find("a", class_="ui-search-link")
            if link_tag:
                link = link_tag["href"]
            data.append({"Produto": title, "Preço": price, "URL": link})
        
        return data

    def transform_df(self, query):
        data = self.execute_command(query)
        df = pd.DataFrame(data)
        
        return df


if __name__ == "__main__":
    crawler = BrowserML()
    dataframe = crawler.transform_df("iphone")
    print(dataframe.head())
    # ml.transform_df()