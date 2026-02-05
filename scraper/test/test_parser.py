from bs4 import BeautifulSoup
from scraper.parser import *

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



def test_pick_best_container():
    html = """
    <html>
        <body>
            <nav>Menu</nav>
            <div>
                bla bla blaa.
            </div>

            <section>
                <h1>Main Title</h1>
                <p>
                    Maraqlı fürsətləri araşdırın, karyeranızı 
                    inkişaf etdirin və təsir göstərin. Bu gün 
                    ABB Karyera Platformasında yenilikçi komandamıza qoşulun!
                </p>
            </section>
            <footer>Footer info</footer>
        </body>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    container = pick_best_container(soup)

    text = container.get_text(separator=" ", strip=True)

    assert "Main Title" in text
    assert "inkişaf etdirin və təsir göstərin" in text
    print("container test passed")


def test_extract_clean_lines():
    html = """
    <html>
        <body>
            <h1>Welcome to ABB</h1>
            <p>Hi</p>
            <p>This is a proper paragraph with enough wordsdss</p>
            <ul>
                <li>Short</li>
                <li>This list item has meaningful content.</li>
            </ul>
        </body>
    </html>
    """

    soup = BeautifulSoup(html, "html.parser")
    lines = extract_clean_lines(soup)

    assert "Welcome to ABB" in lines
    assert "This is a proper paragraph with enough wordsdss" in lines
    assert "This list item has meaningful content." in lines

    # filtered out
    assert "Hi" not in lines
    assert "Short" not in lines
        
    print("clean lines test passed")


from scraper.parser import parse


def test_parse_clean_output():
    html = """
    <html>
        <head>
            <title>ABB Vakansiya</title>
        </head>
        <body>
            <nav>Menu</nav>

            <section>
                <h1>Join ABB today</h1>
                <p>Build your future with us.</p>
                <p>
                    ABB bank sektorunun ən iri bankı olub,
                    fərdi və korporativ müştərilərlə birgə,
                    kiçik və orta sahibkarlığa innovativ 
                    bankçılıq xidmətləri göstərir.
                </p>
            </section>

            <footer>Footer</footer>
        </body>
    </html>
    """

    result = parse(html)

    assert result["title"] == "ABB Vakansiya"

    assert isinstance(result["clean_lines"], list)
    assert len(result["clean_lines"]) > 0

    assert "Join ABB today" in result["clean_lines"]
    assert "ABB bank sektorunun ən iri bankı olub" in result["clean_text"]

    assert "Menu" not in result["clean_text"]
    assert "Footer" not in result["clean_text"]

    print("parse clean output test passed")

    