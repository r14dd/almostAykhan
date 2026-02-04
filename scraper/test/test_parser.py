from bs4 import BeautifulSoup
from scraper.parser import remove_tags

def test_remove_script():
    html = """
    <html>
        <body>
            <header><h1>Banner</h1></header>
            <form>
                <label>Username:</label>
                <input type="text">
            </form>
            <main>Meni hech vaxt silme ha.</main>
            <footer>Contact us at almostAykhan@abb.az</footer>
        </body>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    remove_tags(soup)

    text = soup.get_text()

    assert "Banner" not in text
    assert "Username" not in text
    assert "Contact us" not in text

    assert "Meni hech vaxt silme ha." in text

    print("remove tags test passed")
