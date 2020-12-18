key = #app key
from urllib.request import urlopen
import json
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
def sendemail(url, condition, condition, price):
    msg = MIMEMultipart()
    msg['From'] = "jrschmiedlebay@gmail.com"
    msg['To'] = "jrschmiedlebay@gmail.com"
    msg['Subject'] = title
    
    body = "<a href=\"" + url + "\">" + title + "</a>" + "<br><p>Condition: " + condition + "</p><p>Price: " + price + "</p>"
    msg.attach(MIMEText(body, 'html'))
    print(msg)

    server = smtplib.SMTP("secureus24.sgcpanel.com", 587)
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

searches = []

with open("searches.txt", "r") as searchfile:
    searches = searchfile.readlines()

with open("itemid.txt", "r") as itemfile:
    itemids = itemfile.read().splitlines()
for item in searches:
    search = item.split(',')[0]
    MaxPrice = item.split(',')[1]
    negative = item.split(",")[2:]
    url = ('http://svcs.ebay.com/services/search/FindingService/v1\
?OPERATION-NAME=findItermsByKeywords\
&sortOrder=PricePlusShippingLowest\
&buyerPostalCode=27540&SERVICE-VERSION-1.13.0\
&SECURITY-APPNAME=' + key +
'&RESPONSE-DATA-FORMAT=JSON\
&REST-PAYLOAD\
&itemFilter(0).name=Condition\
&itemFilter(0).value=New\
&itemFilter(1).name=MaxPrice\
&itemFilter(1).value=' + MaxPrice +\
'&itemFilter(1).paramName=Currency\
&itemFilter(1).paramValue=USD\
&keywords=' + search + " " + negative)
    url = url.replace(" ", "%20")
    apiResult = requests.get(url)
    parseddoc = apiResult.json()

for item in (parseddoc["findItemsByKeywordsRespone"][0]["searchResult"][0]["item"]):
    url = item['viewItemURL'][0]
    title = item["title"][0]
    condition = item['condition'][0]['conditionDisplayName'][0]
    price = item['sellingStatus'][0]["convertedCurrentPrice"][0]['__value__']
   if itemid in itemids:
       print("item already alerted")
    else:
        sendemail(url, title, condition, price)
        with open("itemid.txt", "a") as itemfile:
            itemfile.write(itemid + "\n")