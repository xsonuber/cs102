import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    # PUT YOUR CODE HERE

    arrtitle = []
    arrlinks = []
    arrauthor= []
    arrpoints= []
    title = parser.select(".storylink")
    points = parser.select(".score")
    subtext = parser.select(".subtext")

    for i in title:
        arrtitle.append(i.text)
        link = i.get("href", None)
        if link.startswith("item"):
            arrlinks.append(url + link)
        else:
            arrlinks.append(link)

    for i in range(len(subtext)):
        author = subtext[i].select(".hnuser")
        if author == []:
            author = "Anonymous"
        else:
            author = author[0].text
        arrauthor.append(author)
        points = subtext[i].select(".score")
        if points == []:
            points = 0
        else:
            points = int(points[0].text.split()[0])
        arrpoints.append(points)

    for i in range(len(title)):
        news_list.append(
            {
                "title": arrtitle[i],
                "url": arrlinks[i],
                "author": arrauthor[i],
                "points": arrpoints[i],
            }
        )

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE
    link = parser.select(".morelink")[0]["href"]
    return str(link)


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news

