import requests
import re
from time import sleep
from bs4 import BeautifulSoup


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Example: Extract all paragraphs
    paragraphs = soup.find_all('p')
    text_content = ' '.join([para.get_text() for para in paragraphs])
    return text_content


def scrape_links(url, already_used_urls=None):
    if already_used_urls is None:
        already_used_urls = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href == None:
            pass
        elif re.search("www\.esme\.fr", href) and not re.search("/journal-article/", href) and not re.search('fr/.*\.', href) and href not in already_used_urls:
            urls.append(href)
    return urls


def total_scrape(url, already_used_urls=None, text=""):
    sleep(0.2)
    if already_used_urls is None:
        already_used_urls = []
    print(url)
    already_used_urls += [url]
    text += url + ': ' + scrape_website(url)[74:-900] + '\n\n'
    links = scrape_links(url, already_used_urls)
    for link in links:
        if link not in already_used_urls:
            already_used_urls, text = total_scrape(link, already_used_urls, text)
    return already_used_urls, text


total_scraping = []
url = 'https://www.esme.fr/'
data = total_scrape(url)
print(data)

with open('esme_website_data.txt', 'w', encoding='utf-8') as file:
    file.write(data[1] + "À Propos de L'ESME À Propos de L'ESME Depuis près de 120 ans, l’ESME est l’école d’ingénieurs qui s’engage dans la transformation positive de nos mondes. Elle forme des ingénieurs sur 3 grands domaines : le numérique, l’IA, la robotique et l’énergie, dans l’objectif de transformer le monde de demain. La formation pluridisciplinaire de l’ESME et son ouverture vers de très nombreux domaines la prédestine à former des ingénieurs capables d’accompagner les transformations énergétiques et numériques des entreprises et des organisations. Depuis sa création, près de 17 000 ingénieurs ont été diplômés. L’école délivre un diplôme reconnu par l’Etat et accrédité par la CTI.  PROCHAINRDV PROCHAINRDV JOURNÉE PORTES OUVERTES Presse Infos pratiques Accréditations Établissement d’enseignement supérieur privé – Inscription au Rectorat de Créteil – Cette école est membre de IONIS Education Group comme :")
