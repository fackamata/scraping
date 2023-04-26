
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

departement = "Haute-Savoie" # TODO change for your own use

response = requests.get(f"https://donnons.org/annonces/{departement}", headers=headers)
# print(response)
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup)
# print(soup.find_all("article"))
page_count = soup.find(class_= "num-page").text
nb_pages = page_count.replace('Page 1 / ', "")


cities = set()

# to store all article 
list_of_ads = ['\t List of ads from donnons.org \n\n'] # to store all ads in a string

with open('lst_ads_tabular.csv', 'w') as file:

    for page_number in range(1,int(nb_pages)+1) : 
        response = requests.get(f"https://donnons.org/annonces/Haute-Savoie?page={page_number}/", headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        article = soup.find_all(class_="lst-annonce")
        for art in article:
            ad_title = art.h2.text
            ad_category = art.find(class_="categorie").text
            ad_city = art.find(class_="city").text
            ad_link = "https://donnons.org" + str(art['href']) 

            cities.add(ad_city.strip())

            data = [ad_title, ad_city.strip(), ad_category, ad_link]
            # write in csv file
            writer = csv.writer(file)
            writer.writerow(data) # write in csv file
            # list_of_ads += f"{ad_title} - {ad_city} - {ad_category} - {ad_link}" # store ad in list
            # print(data)
            list_of_ads += [f"{ad_title} \t{ad_city.strip()} \t{ad_category} \t{ad_link}"] # store ad in list

# for j in article_lst:
#     print(j[0] + ' \t\t ' + j[1] + ' \t\t ' + j[2])

# with open('cities_lst.txt', 'w') as file:
#     for city in cities:
#         file.write(city + '\n')   
# print(cities)

with open('lst_ads.txt','w') as text_file:
    for ad in list_of_ads:
        text_file.write(f"{ad} \n")

print("\n Ads are listed in files : lst_ads.txt or lst_ads_tabular.csv\n")