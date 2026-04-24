from unittest.mock import patch, Mock

from scraper.logic import get_municipality_links, parse_obec

DISTRICT_HTML = """
<html>
  <body>
    <table class="table">
      <tr>
        <td class="cislo"><a href="/pls/ps2017nss/ps32?xobec=12345">1</a></td>
        <td class="overflow_name">Testovice</td>
      </tr>
    </table>
  </body>
</html>
"""

MUNICIPALITY_HTML = """
<html>
  <body>
    <table>
      <td headers="sa2">100</td>
      <td headers="sa3">90</td>
      <td headers="sa6">85</td>
      <td class="overflow_name">Party A</td>
      <td headers="sb3">50</td>
    </table>
  </body>
</html>
"""


@patch("scraper.logic.requests.get")
def test_get_municipality_links(mock_get):
    response = Mock()
    response.encoding = "utf-8"
    response.text = DISTRICT_HTML
    response.raise_for_status = Mock()
    mock_get.return_value = response

    result = get_municipality_links("https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ")

    assert result == [
        ("https://www.volby.cz/pls/ps2017nss/ps32?xobec=12345", "Testovice")
    ]


@patch("scraper.logic.requests.get")
def test_parse_obec(mock_get):
    response = Mock()
    response.encoding = "utf-8"
    response.text = MUNICIPALITY_HTML
    response.raise_for_status = Mock()
    mock_get.return_value = response

    result = parse_obec("https://www.volby.cz/pls/ps2017nss/ps32?xobec=12345", "Testovice")

    assert result["Kód obce"] == "12345"
    assert result["Název obce"] == "Testovice"
    assert result["Voliči v seznamu"] == "100"
    assert result["Vydané obálky"] == "90"
    assert result["Platné hlasy"] == "85"
    assert result["Party A"] == "50"
