from requests import get
from bs4 import BeautifulSoup


def request_news_html(url) -> BeautifulSoup:
    """Perform GET request to retrieve news data from web page in HTML format."""
    response = get(url)
    if response.status_code != 200:
        raise ConnectionError("Could not scrape news webpage :(")
    return BeautifulSoup(response.text, "html.parser")


def extract_stories_href(html):
    stories = html.find(
        'ul', class_="ssrcss-18so414-Grid e12imr580").find_all('li')
    stories = [story.find(
        'a') for story in stories]
    hrefs = [story.get('href') for story in stories if story]
    return hrefs


if __name__ == "__main__":
    bbc_url = "http://bbc.co.uk"
    html = request_news_html(bbc_url)
    print(extract_stories_href(html))
