from bs4 import BeautifulSoup, Tag

def remove_tags(_soup: BeautifulSoup) -> None:
    """
    Input: soup
    Output: None, just removes html tags consisting of no content
    """

    no_content_tags = ["script", "style", "noscript", "nav", "footer", "header", "aside", "form"]
    
    for tag in _soup.find_all(no_content_tags):
        tag.decompose()

def get_text_len(_tag) -> int:
    """
    Input: tag
    Output: Length of the clean text inside a given tag
    """
    return len(_tag.get_text(separator=" ", strip=True))

def find_candidates(_soup: BeautifulSoup):
    """
    Input: soup
    Output: List of tags that mightve contained needed content
    """
    return _soup.find_all(["main", "article", "section", "div"])

def pick_best_container(_soup: BeautifulSoup):
    """
    Input: soup
    Output: Container with the most text
    """

    candidates = find_candidates(_soup)

    if candidates:
        return max(candidates, key=get_text_len)
    
    if _soup.body:
        return _soup.body

    return _soup

def worth_keeping(_text: str):
    """
    Input: text, usually one line
    Output: True if the line of text is worth keeping, False if not
    """
    return len(_text.strip().split()) >= 2


def extract_clean_lines(_container: Tag):
    """
    Input: container tag
    Output: list of readable text lines
    """
    relevant_tags: list[Tag] = _container.find_all(["h1", "h2", "h3", "p", "li", "ul", "tr", "td", "th", "dl", "dt", "dd"])

    lines: list[str] = []
    seen: set[str] = set()

    for i in relevant_tags:
        text: str = i.get_text(" ", strip=True)

        if not text:
            continue

        if not worth_keeping(text):
            continue

        if text in seen:
            continue

        seen.add(text)
        lines.append(text)

    return lines




def parse(_html: str):
    """
    Input: raw HTML string
    Output: dict with title, clean_lines, clean_text
    """
    soup = BeautifulSoup(_html, "html.parser")

    remove_tags(soup)

    container = pick_best_container(soup)

    clean_lines = extract_clean_lines(container)

    clean_text = "\n".join(clean_lines)

    title = None
    
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    elif clean_lines:
        title = clean_lines[0]

    return {
        "title": title,
        "clean_lines": clean_lines,
        "clean_text": clean_text,
    }
