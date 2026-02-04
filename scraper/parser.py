from bs4 import BeautifulSoup

def remove_tags(_soup: BeautifulSoup) -> None:
    """
    Input: soup
    Output: None, just removes html tags consisting of no content
    """

    no_content_tags = ["script", "style", "noscript", "nav", "footer", "header", "aside", "form"]
    
    for tag in _soup.find_all(no_content_tags):
        tag.decompose()