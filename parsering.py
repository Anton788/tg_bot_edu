from bs4 import BeautifulSoup
import urllib.request
import json
from multiprocessing.dummy import Pool


def get_html_code(url):
    r = urllib.request.urlopen(url)
    return r.read()


class Docs:
    def __init__(self, t='', d='', u='', m_u='', ta='', txt='', dat=''):
        self.title = t
        self.description = d
        self.url = u
        self.main_url = m_u
        self.tags = ta
        self.text = txt
        self.data = dat


class Theme:
    def __init__(self, d='', i='', l=''):
        self.description = d
        self.title = i
        self.url = l


def get_main_titles():
    b = urllib.request.urlopen('https://www.rbc.ru/story/filter/ajax?offset=0&limit=200')
    s2 = json.loads(b.read())['html']
    s3 = BeautifulSoup(s2, "html.parser")
    s4 = s3.find_all('div', class_= 'item item_story js-story-item')
    pr = []
    for i in s4:
        link = i.find('a')['href']
        item_title = i.find_all('span')[0].text
        describ = (i.find_all('span')[1]).text.lstrip()
        p = Theme(describ, item_title, link)
        pr.append(p)
    return pr


def doc_text_parser(html):
    s = BeautifulSoup(html, "html.parser")
    table = s.find('div', class_="article__text")
    table_1 = s.find(class_="article__tags__block")
    k = 0
    text = ''
    table_tx = table.find_all('p')
    for i in table_tx:
        if i.find('div') is None:
            text += i.text
        else:
            pass
    try:
        tags = table_1.find_all('a')
        list_of_tags = list()
        for j in tags:
            list_of_tags.append(j["href"])
    except:
        list_of_tags = list()
    result = list()
    result.append(text)
    result.append(list_of_tags)
    return result


def item_parser(url):
    num = str.find(url, 'y/')
    i_list = 'https://www.rbc.ru/filter/ajax?story=' + url[num + 2:] + '&offset=0&limit=40'
    k1 = urllib.request.urlopen(i_list).read()
    k = json.loads(k1)['html']
    s = BeautifulSoup(k, "html.parser")
    doc = []
    s1 = s.find_all('div', class_="item item_story-single js-story-item")
    for i in s1:
        link = i.find('a')['href']
        ht = get_html_code(link)
        c= doc_text_parser(ht)
        title = i.find_all('span')[0].text
        text = i.find_all('span')[1].text.lstrip()
        time = i.find_all('span')[2]
        info = time.find('span').text
        elem = Docs(title, text, link, url, c[1], c[0], info)
        doc.append(elem)
    return doc


def finally_parse():
    pr = get_main_titles()
    info = list()
    quickly_info = list()
    for i in pr:
        info.append((i.url))
    po = Pool(processes=10)
    res = po.map_async(item_parser, info)
    quickly_info.append(res.get())
    return quickly_info
