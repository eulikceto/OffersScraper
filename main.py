from time import perf_counter
from src import *
from rich.console import Console
from rich.panel import Panel

produtos = []
precos = []
limit = 40
urls = [
    f"https://www.mercadolivre.com.br/ofertas?page={i}" for i in range(1, limit + 1)
]
console = Console()


async def main(save=False):
    init = perf_counter()
    async with aiohttp.ClientSession() as client:
        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_response(client, url)))

        console.log(":rocket: [i]Fetching Urls...[/i]")
        responses = await asyncio.gather(*tasks)
        console.log(":mag: [i]Scraping Data...[/i]")
        await asyncio.gather(*[scrape(precos, produtos, r) for r in responses])
        if save:
            console.log(":file_folder: Saving File...")
            await save_file(precos, produtos)
        console.log(":cake: [bold green]Done![bold green]\n")
        info_dict = {
            ":notebook: Urls": len(urls),
            ":shopping_cart: Products": len(produtos),
            ":alarm_clock: Elapsed Time": f"{perf_counter() - init:.2f}s"
        }

        console.print(
            Panel(
                f"{info_dict}",
                title="[bold yellow]INFO[bold yellow]",
                highlight=True
            )
        )


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    with console.status("[green][i]Extracting data...[/i][/]", spinner="moon"):
        asyncio.run(main(save=True))
