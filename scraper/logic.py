import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"


def get_soup(url):
    """Download a page and return a BeautifulSoup object."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    response.encoding = "utf-8"
    return BeautifulSoup(response.text, "html.parser")


def parse_obec(url, nazev_obce):
    """Parse data for a single municipality."""
    soup = get_soup(url)
    kod_obce = parse_qs(urlparse(url).query).get("xobec", ["N/A"])[0]

    def safe_find(headers):
        td = soup.find("td", {"headers": headers})
        return td.text.strip() if td else ""

    volici = safe_find("sa2")
    obalky = safe_find("sa3")
    platne = safe_find("sa6")
    strany = [td.text.strip() for td in soup.find_all("td", class_="overflow_name")]

    hlasy = []
    for td in soup.find_all("td"):
        headers = td.get("headers", "")
        if isinstance(headers, list):
            headers = " ".join(headers)
        if headers.endswith("sb3"):
            hlasy.append(td.text.strip())

    data = {
        "Kód obce": kod_obce,
        "Název obce": nazev_obce,
        "Voliči v seznamu": volici,
        "Vydané obálky": obalky,
        "Platné hlasy": platne,
    }
    for party, votes in zip(strany, hlasy):
        data[party] = votes
    return data


def get_municipality_links(url_okres):
    """Extract municipality links from a district page."""
    soup = get_soup(url_okres)
    tables = soup.find_all("table", class_="table")

    links = []
    for table in tables:
        for row in table.find_all("tr"):
            cislo_td = row.find("td", class_="cislo")
            nazev_td = row.find("td", class_="overflow_name")
            if cislo_td and nazev_td:
                anchor = cislo_td.find("a", href=True)
                if anchor and "xobec=" in anchor["href"]:
                    url = urljoin(BASE_URL, anchor["href"])
                    name = nazev_td.text.strip()
                    links.append((url, name))
    return list(dict.fromkeys(links))
