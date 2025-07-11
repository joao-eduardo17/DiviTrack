import re
import httpx
from bs4 import BeautifulSoup

class FiiScraper:
    def __init__(self, code: str):
        self.code = code
        self.url = f"https://www.fundsexplorer.com.br/funds/{code}"
        self.headers = {"User-Agent": "Mozilla/5.0"}

    async def get_price(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")

        price_div = soup.find("div", class_="headerTicker__content__price")

        if price_div:
            brute_price = price_div.find("p").text.strip()
            regex_value = re.search(r"[\d.,]+", brute_price)
        else:
            return None

        if regex_value:
            value = regex_value.group(0).replace(",", ".")
            price = float(value)

        return price

    async def get_dividend(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")

        indicators = soup.find_all("div", class_="indicators__box")

        if indicators:
            paragraphs = indicators[1].find_all("p")
            brute_price = paragraphs[1].find("b").text.strip()
        else:
            return None

        regex_value = re.search(r"[\d.,]+", brute_price)

        if regex_value:
            value = regex_value.group(0).replace(",", ".")
            price = float(value)

        return price
