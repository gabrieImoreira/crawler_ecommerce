from browser.actions.browser_actions import action_dict
from browser.crawler.default_crawler import AbstractCrawler
import json
from bs4 import BeautifulSoup


class GenericBrowserCrawler(AbstractCrawler):
    def __init__(self, loja):
        super().__init__()
        self.type = loja
        self.steps = json.loads(self.get_steps(self.type))
        if self.steps is None:
            raise ("Site não encontrado")

    def crawl(self, query):
        print(self.steps)
        # self.query = query
        # self.execute_before()
        # df = self.execute_main()
        # self.execute_after()
        # self.save_data()

    def execute_main(self):
        self.browser.get(f'{self.steps["link"]["path"]}{self.query.replace(" ", self.steps["link"]["connector"])}')
        time.sleep(5)
        self.content - self.extraction()
        df = self.transform_df(self.content)
        return df

    def execute_before(self):
        before = self.steps["script"]["after"]
        if before:
            for action in before:
                if action_dict[action] is None:
                    raise ("Ação não encontrada")
                action_dict[action](self.browser, after[before])

    def execute_after(self):
        after = self.steps["script"]["after"]
        if after:
            for action in after:
                if action_dict[action] is None:
                    raise ("Ação não encontrada")
                action_dict[action](self.browser, after[action])

    def extraction(self):
        self.html = self.browser.page_source

        soup = BeautifulSoup(self.html, "html.parser")

        if self.steps["search"]["custom"]:
            results = soup.find_all(self.steps["search"]["tag"], self.steps["search"]["custom"])
        else:
            results = soup.find_all(self.steps["search"]["tag"], class_=self.steps["search"]["class"])

        data = []

        for result in results:
            product = {}
            for step in self.steps["product"]:
                value = self.steps["product"][step]
                content = None
                try:
                    content = eval(value)
                except:
                    content = Non	
                product[step] = content
            data.append(product)
        self.browser.close()
        return data

    def transform_df(self, data):
        df = pd.DataFrame(data)
        df = df.assign(keyword=self.query)
        df = df.assign(dataTimeReference=datetime.now().isoformat())
        df = df.assign(crawlerType="Browser")

        return df

    def save_data(self, data):
        pass
        # df = pd.DataFrame(data)
        # df = df.assign(keyword=self.query)
        # df = df.assign(dataTimeReference=datetime.now().isoformat())
        # df = df.assign(crawlerType="Browser")

        # return df