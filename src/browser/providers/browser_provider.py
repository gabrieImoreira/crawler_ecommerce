import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class GenericBrowser:
    def __init__(self):
        self.browser =  None
        self.options = Options()
        self.default_options = [
            "--no-sandbox",
            "--disable--web-security",
            "--disable-dev-shm-usage",
            "--memory-pressure-off",
            "--ignore-certificate-errors",
        ]

    def get_browser(self, args: list[str] = None):
        new_args = args
        if args is None:
            new_args = self.default_options
        self.set_options(new_args)
        return webdriver.Chrome(options=self.options)
    
    def is_headless(self):
        headless = os.getenv("HEADLESS")
        if headless is None:
            self.options.add_argument("--headless")
    
    def set_options(self, args: list[str] | None):
        self.is_headless()
        self.set_proxy()
        if args:
            for opt in args:
                self.options.add_argument(opt)
        pass
            
    def set_proxy(self):
        if os.getenv("PROXY"):
            user = os.getenv("PROXY_USER")
            password = os.getenv("PROXY_PASSWORD")
            url = os.getenv("PROXY")
            port = os.getenv("PROXY_PORT")
            proxy_provider = f'http://{user}:{password}@{url}:{port}'
            self.option.add_argument(f"--proxy-server={proxy_provider}")
    
    def close():
        return self.browser.quit()