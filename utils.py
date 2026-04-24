import requests

def validate_url(url):
    """
    Basic validation to check if the URL belongs to volby.cz.
    In QA, we never trust user input!
    """
    if not url.startswith("https://www.volby.cz/pls/ps2017nss/"):
        return False
    return True