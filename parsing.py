import requests
from bs4 import BeautifulSoup
import config
from time import sleep


def download(url):
    resp = requests.get(url, stream=True)
    r = open(r"images/" + url.split("/")[-1], "wb")
    for value in resp.iter_content(1024*1024):
        r.write(value)
    r.close()
    return url.split("/")[-1]


headers = {
    "accept": "text/css,*/*;q=0.1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137"
}


def urls_by_year(year):
    #mem_urls = []
    url = f"https://memepedia.ru/tag/{str(year)}"

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    nav_links = soup.find("div", class_="nav-links")
    nums = nav_links.find_all("a")[-2].text
    for i in range(2, int(nums)+2):
        url = f"https://memepedia.ru/tag/{year}/page/{i}"

        cards = soup.find_all("li", class_="post-item post-item-four-column")

        for card in cards:
            #mem_urls.append(card.find("a").get("href"))
            yield card.find("a").get("href"), card.find("span", class_="count").text, card.find("a").get("title")

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "lxml")


def parse(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    name = soup.find("h1", class_="entry-title s-post-title bb-mb-el").text
    data = soup.find("figure")
    try:
        image_url = data.find("img").get("src")
        image_name = download(image_url)
    except AttributeError:
        image_name = None
    origin = []
    meaning = []

    block = soup.find("div", class_="js-mediator-article s-post-content s-post-small-el bb-mb-el")
    description = block.find("p").text
    h2_text = block.find_all("h2")

    text = h2_text[0].find_next_siblings("p", limit=config.ORIGIN_LINES)
    for line in text:
        cur_line = line.text.strip()
        if cur_line:
            origin.append(cur_line)

    for heads in h2_text:
        if heads.text == 'Значение':
            break
    text = heads.find_next_siblings("p", limit=config.MEANING_LINES)
    for line in text:
        cur_line = line.text.strip()
        if cur_line:
            meaning.append(cur_line)

    return name, image_name, description, origin, meaning, url


def parse_mems_by_years(start=2007, finish=2022):

    for year in range(start, finish+1):
        with open(f"mem_urls/{str(year)}", "w") as f:
            line_counter = 0
            for url, views, name in urls_by_year(year):
                line_counter += 1
                f.write(str(line_counter) + ' ' + views + ' ' + name + ' ' + url)
                f.write("\n")
        with open(f"mem_urls/mems_info", "a") as f:
            f.write(str(year)+' '+str(line_counter) + '\n')


#parse_mems_by_years()