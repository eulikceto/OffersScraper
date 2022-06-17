import aiohttp
import asyncio
from bs4 import BeautifulSoup, SoupStrainer
import pandas as pd

STRAINER = SoupStrainer("li", class_="promotion-item default")

async def get_response(client: aiohttp.ClientSession, url: str) -> aiohttp.ClientResponse:
    r = await client.get(url)
    return r


async def scrape(pricelist: list, productlist: list, r: aiohttp.ClientResponse) -> None:
    soup = BeautifulSoup(await r.text(), "lxml", parse_only=STRAINER)
    pricelist.extend(
        [price.span.text for price in soup.find_all("span", class_="promotion-item__price")]
    )
    productlist.extend(
        [produto.text for produto in soup.find_all("p", class_="promotion-item__title")]
    )


async def save_file(prices: list, products: list, filename="result.xlsx") -> None:
    data = {"Produto": products, "Preço Unitário": prices}
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
