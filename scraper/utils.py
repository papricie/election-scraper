
def validate_url(url):
    """Basic validation for the district URL."""
    return url.startswith("https://www.volby.cz/pls/ps2017nss/")
