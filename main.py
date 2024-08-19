import csv
from dataclasses import asdict, dataclass

import httpx
from selectolax.parser import HTMLParser


@dataclass
class Product:
    name: str
    category: str
    price: str
    img_url: str
    url: str


def get_html(page: str) -> str:
    with httpx.Client() as client:
        base_url = f"https://mandcdrugstore.com/ecommerce/products/products-m-c?sortBy=grid&page={page}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
        }
        r = client.get(base_url, headers=headers, timeout=None)
        html = HTMLParser(r.text)
        return html


def get_products(html):
    products = html.css("div.product-display")
    url_prefix = "https://mandcdrugstore.com"
    results = []
    for product in products:
        new_product = Product(
            name=product.css_first("h3.product-display-name").text().strip(),
            category=product.css_first("div.tagline.product-brand").text().strip(),
            price=product.css_first("div.price").text().strip().replace("$", ""),
            img_url=url_prefix + product.css_first("img").attributes["src"],
            url=url_prefix + product.css_first("a").attributes["href"],
        )
        results.append(asdict(new_product))
    return results


def to_csv(products):
    with open("products.csv", "a") as f:
        writer = csv.DictWriter(
            f, fieldnames=["name", "category", "price", "img_url", "url"]
        )
        writer.writerows(products)


# with httpx.Client() as client:
#     base_url = (
#         "https://mandcdrugstore.com/ecommerce/products/products-m-c?sortBy=grid&page=2"
#     )
#     headers = {
#         "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
#     }
#     r = client.get(base_url, headers=headers)
#     print(r.status_code)


def main():
    for i in range(250, 289):
        html = get_html(str(i))
        products = get_products(html)
        to_csv(products)


if __name__ == "__main__":
    main()
