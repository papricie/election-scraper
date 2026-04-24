import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

BASE_URL = "https://www.volby.cz/pls/ps2017nss/"

def get_soup(url):
    """Downloads a page and returns a BeautifulSoup object."""
    resp = requests.get(url)
    resp.encoding = "utf-8"
    return BeautifulSoup(resp.text, "html.parser")

def parse_obec(url, nazev_obce):
    """Parses data for a single municipality."""
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

    for s, h in zip(strany, hlasy):
        data[s] = h

    return data

def get_municipality_links(url_okres):
    """Extracts links and names of all municipalities from the district page."""
    soup = get_soup(url_okres)
    tabulky = soup.find_all("table", class_="table")

    obec_links = []
    for tabulka in tabulky:
        for tr in tabulka.find_all("tr"):
            cislo_td = tr.find("td", class_="cislo")
            nazev_td = tr.find("td", class_="overflow_name")
            if cislo_td and nazev_td:
                a = cislo_td.find("a", href=True)
                if a and "xobec=" in a["href"]:
                    url = urljoin(BASE_URL, a["href"])
                    nazev_obce = nazev_td.text.strip()
                    obec_links.append((url, nazev_obce))
    return list(dict.fromkeys(obec_links))