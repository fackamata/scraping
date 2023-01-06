
import requests, random
from bs4 import BeautifulSoup
import csv


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
# print(response)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
# print(soup.find_all("article"))
page_count = soup.find(class_= "num-page").text
nb_pages = page_count.replace('Page 1 / ', "")


# to store all article 
# article_lst = []
with open('donnon_list_of_ads.csv', 'w') as file:

    for page_number in range(1,int(nb_pages)+1) : 
        response = requests.get(f"https://donnons.org/annonces/Haute-Savoie?page={page_number}/", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        article = soup.find_all(class_="lst-annonce")
        for art in article:
            # print(art['href'])
            ad_title = art.h2.text
            # ad_link = article_h2.find('a', href=True)['href']
            ad_category = art.find(class_="categorie").text
            ad_city = art.find(class_="city").text
            ad_link = "https://donnons.org" + str(art['href']) 
            # print(ad_link)
            data = [ad_title, ad_city.strip(), ad_category, ad_link]
            
            writer = csv.writer(file)
            writer.writerow(data)

# for j in article_lst:
#     print(j[0] + ' \t\t ' + j[1] + ' \t\t ' + j[2])