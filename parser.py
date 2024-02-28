from time import sleep
import json
from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.teacode.com/online/udc/'
START_URL = BASE_URL + 'index.html'


def parse(url: str) -> dict:
    """
        Recursive function that collects data from all child pages.
        Function is only applicable to the site https://www.teacode.com/

        :url: Url of the page from which you need to collect data and find links to the following pages.
        :return: Nested dictionary where the keys are the UDC codes,
                 and the values contain the node name, child nodes, and the UDC code.
    """
    sleep(0.02)
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "lxml")
    target_tr = bs.find_all(attrs={'bgcolor': '#eaeaea'})

    result = dict()

    for tr in target_tr:
        tds = tr.find_all('td')
        name = tds[1].find("font").text
        if tds[0].find("a"):
            udc = tds[0].find("a").text
            if url == START_URL:
                href = BASE_URL + tds[0].find("a").attrs["href"][1:]
            else:
                href = 'https://' + '/'.join(url.split('/')[2:-1]) + '/' + tds[0].find("a").attrs["href"]
        else:
            udc = tds[0].find("font").text
            href = None

        if href:
            if udc not in result:
                result[udc] = {
                    'udc': udc,
                    'name': name,
                    'children': parse(href)
                }
            else:
                result[udc]['children'].update(parse(href))
        else:
            result[udc] = {
                'udc': udc,
                'name': name,
                'children': {}
            }

    return result


if __name__ == '__main__':

    # PARSING
    data = parse(START_URL)

    # saving the results in json format
    with open("udc_teacode.json", "w", encoding='utf-8') as fp:
        json.dump(data, fp, ensure_ascii=False)
    # saving the results in json format with indentation for readability
    with open("udc_teacode_indent.json", "w", encoding='utf-8') as fp:
        json.dump(data, fp, indent=4, ensure_ascii=False)


