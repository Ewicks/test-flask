from flask import Flask, render_template
app=Flask(__name__)

import requests
from bs4 import BeautifulSoup
import re
import time
import random

# AGENT_LIST = [
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
#     "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:24.0) Gecko/20100101 Firefox/24.0",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/91.0.4472.114 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
#     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/78.0.3904.70 Safari/537.36",
#     "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
# ]

baseurl = 'https://emaps.elmbridge.gov.uk/ebc_planning.aspx'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

r = requests.get('https://emaps.elmbridge.gov.uk/ebc_planning.aspx?pageno=1&template=AdvancedSearchResultsTab.tmplt&requestType=parseTemplate&USRN%3APARAM=&apptype%3APARAM=&status%3APARAM=&decision%3APARAM=&ward%3APARAM=&txt_search%3APARAM=&daterec_from%3APARAM=2022-09-17&daterec_to%3APARAM=2022-09-29&datedec_from%3APARAM=&datedec_to%3APARAM=&pagerecs=50&orderxyz%3APARAM=REG_DATE_DT%3ADESCENDING&SearchType%3APARAM=Advanced', headers=headers)

soup = BeautifulSoup(r.content, 'lxml')

houselist = soup.find_all('tr')

time.sleep(10)
linkslist = []

updatehouselist = []

addresslist = []

# Get all house sections that contain keyword in a list
# words_search_for = 'variation'
# words_search_for = 'extension'
words_search_for = 'variation|extension'


for house in houselist:
    if (house.find('td', string=re.compile((words_search_for), flags=re.I))):
        updatehouselist.append(house)


for house in updatehouselist:
    address = house.find('td', class_='address')
    addresslist.append(address.get_text())
    for link in house.find_all('a', href=True):
        homepagelinks = link['href']
        linkslist.append(homepagelinks)

contactlinkslist = []

for link in linkslist:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    atags = soup.find('div', id='atPubMenu').find('a')
    parturl = atags['href']
    contacturl = baseurl + parturl
    contactlinkslist.append(contacturl)

time.sleep(20)
contactnameslist = []

data = []

for link in contactlinkslist:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    atags = soup.find('div', class_='atPanelContainer').find('dd').find_next('dd').contents[0]
    contactnameslist.append(atags.get_text())

time.sleep(15)
for i, t in enumerate(zip(addresslist, contactnameslist)):
    it = (i, t)
    data.append(it)

# print(data)

@app.route('/')
def home():
	return render_template('home.html',data=data)

    
if __name__ == "__main__":
	app.run(debug=True)



# if __name__ == '__main__':
# 	app.run(debug=True)
# if __name__ == '__main__':
	# app.run(debug=True)