
import requests, random
from bs4 import BeautifulSoup

# to pass through anti-scraper
user_agent_lst = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 13.1; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:108.0) Gecko/20100101 Firefox/108.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:102.0) Gecko/20100101 Firefox/102.0'
]

user_agent = user_agent_lst[random.randint(0,len(user_agent_lst)-1)]
headers =  {'user-agent': user_agent}

response = requests.get("https://donnons.org/annonces/Haute-Savoie", headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

# print(soup.find_all("article"))
page_count = soup.find(class_= "page-count").text
nb_pages = page_count.replace('Page 1 de ', "")
# print(nb_pages)

# to store all article 
article_lst = []

for page_number in range(1,int(nb_pages)+1) : 
    # print(page_number)
    # print(f"https://keepinuse.ch/annonces/page/{page_number}/")
    response = requests.get(f"https://keepinuse.ch/annonces/page/{page_number}/", headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    article = soup.find_all("article")
    # print(article)
    for art in article:
        article_h2 = art.h2
        ad_title = article_h2.text
        ad_link = article_h2.find('a', href=True)['href']
        # print(ad_link)
        ad_localisation = art.find_all("li")
        ad_address = ad_localisation[-1].text
        ad_city = ad_address.split(' ')[-1]
        ad_description = art.find_all(class_="entry-content subheader")
        # article_lst.append((ad_title, ad_city))
        article_lst.append((ad_title, ad_city, ad_link))

for j in article_lst:
    print(j[0] + ' \t\t ' + j[1] + ' \t\t ' + j[2])
#     print(j[0] + ' ; ' + j[1] )