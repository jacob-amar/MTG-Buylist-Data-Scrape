from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "cardprices.csv"
f = open(filename, "w")
headers = "set, card_name, condition, language, price\n"
f.write(headers)

standard_sets = {"rivals_of_ixalan" : "7233",
                 "ixalan" : "6323",
                 "dominaria" : "7283",
                 "core_set_2019" : "7373",
                 "guilds_of_ravnica" : "7414",
                 "ravnica_allegiance" : "7423"}

for sets,code in standard_sets.items():
    for i in range(1,2):
        my_url = 'https://store.channelfireball.com/buylist/magic/'+code+'?filter%5B11%5D=&filter%5B255%5D=&filter%5B256%5D=Regular&filter%5B5%5D=&filter%5B8%5D=&filter_by_stock=&filtered=1&page=' + str(i) + '&sort_by_price=1'
        #opening connection, grabbing the page, closing connection
        uClient = uReq(my_url)
        page_html = uClient.read()
        uClient.close()
        
        #html parsing
        page_soup = soup(page_html, "html.parser")
        #grabs each product
        products = page_soup.findAll("div",{"class":"image-meta"})   
        
        for container in products:
            subcontainer = container.find("div",{"class":"meta credit"})
            card_name = container.div.a["title"]
            condition = subcontainer.div.div.span.span.text
            try: 
                price = container.find("span",{"class":"regular price"}).text
            except:
                continue
            
            f.write(sets + "," + card_name.replace(",","") + "," + condition + "," + price + "\n")

f.close()
