from abc import ABC, abstractmethod
from browser.providers.browser_provider import GenericBrowser
from browser.tools.redis import RedisClient
from browser.tools.mongo import MongoConnection

class AbstractCrawler(ABC):

    def __init__(self):
        self.redis = RedisClient.get()
        self.mongo = MongoConnection()
        self.browser = GenericBrowser().get_browser()

    @abstractmethod
    def crawl(self):
        pass
    
    @abstractmethod
    def execute_main(self):
        pass

    @abstractmethod
    def execute_before(self):
        pass

    @abstractmethod
    def execute_after(self):
        pass
    
    @abstractmethod
    def extraction(self):
        pass

    def get_steps(self, site):
        try:
            return self.redis.get(site)
        except:
            raise ("Redis não encontrado")

    @abstractmethod
    def save_data(self, data):
        try:
            self.mongo.save_dataframe(data)
        except:
            raise ("Erro ao salvar os dados no MongoDB")

