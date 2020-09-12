from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup 
import pandas as pd
import requests
from django.templatetags.static import static


def home(request):
 
    context={}
    return render(request,'index.html', context)





def listGenerator(request):
    searchData = [] 
    if request.method == "POST":
        make   = request.POST.get('make')
        model   = request.POST.get('model')
        olxResult = olxScrapper(make,model)
        print(olxResult)
    context={}
    return render(request, 'products.html', context)



def autoscoutScrapper(make,model):
    baseUrl        =  'https://www.autoscout24.pl/'
    if not model:
        autoscoutR = requests.get(f'https://www.autoscout24.pl/lst/{make}?sort=age&desc=1&ustate=N%2CU&size=20&page=1&atype=C&')
    else:
        autoscoutR = requests.get(f'https://www.autoscout24.pl/lst/{make}/{model}?sort=standard&desc=0&ustate=N%2CU&atype=C')
    soup            = BeautifulSoup(autoscoutR.content, 'lxml')
    carList         = soup.find_all('div', class_='cldt-summary-full-item-main')
    nameList, priceList, linkList, additionalList, pictureList = [],[],[],[],[]
    for x in carList:
        carName     = x.find('h2',   class_="cldt-summary-makemodel sc-font-bold sc-ellipsis").text
        carPrice    = x.find('span', class_="cldt-price sc-font-xl sc-font-bold" , attrs={"data-item-name":"price"}).text.strip()
        shortLink   = x.find('a',    href=True, attrs={'data-item-name':True})
        longLink    = baseUrl+shortLink['href']
        try:
            additionalName   = x.find('h2', class_="cldt-summary-version sc-ellipsis").text
        except:
            additionalName   = ""
        try:
            tagPicture  = x.find('img', class_="lazyload")
            carPicture  = tagPicture["data-src"]
        except: 
            carPicture  = static("images/human.jpg")
        nameList.append(carName)
        priceList.append(carPrice)
        linkList.append(longLink)
        additionalList.append(additionalName)
        pictureList.append(carPicture)

    autoscoutData   = list(zip(pictureList,nameList,additionalList,priceList,linkList))
    #return autoscoutData 
    pass

def otomotoScrapper(make,model):
    baseUrl        =  'https://www.otomoto.pl/'
    if not model:
        otomotoR = requests.get(f'https://www.otomoto.pl/osobowe/{make}/?search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=')
    else:
        otomotoR = requests.get(f'https://www.otomoto.pl/osobowe/{make}/{model}/?search%5Border%5D=created_at_first%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=')

    nameList, priceList, linkList, additionalList, pictureList = [],[],[],[],[]
    soup        = BeautifulSoup(otomotoR.content, 'lxml')
    carList     = soup.find_all('article', class_='adListingItem offer-item is-row is-active ds-ad-card-experimental')

    for x in carList:
        carData     = x.find('a',  href=True, class_="offer-title__link")
        longLink    = carData['href']
        carName     = carData['title']
        carPrice    = x.find('span', class_="offer-price__number ds-price-number" ).text.strip().replace('\n','')
        try:
            additionalName   = x.find('h3', class_="offer-item__subtitle ds-title-complement hidden-xs", attrs={'data-type':"complement"} ).text
        except:
            additionalName   = ""
        additionalList.append(additionalName)
        try:
            tagPicture  = x.find('img', class_="lazyload")
            carPicture  = tagPicture["data-srcset"][:-4]
        except: 
            carPicture  = static("images/human.jpg")

        nameList.append(carName)
        priceList.append(carPrice)
        linkList.append(longLink)
        additionalList.append(additionalName)
        pictureList.append(carPicture)

    otomotData   = list(zip(pictureList,nameList,additionalList,priceList,linkList))


    return otomotData
    
def olxScrapper(make,model):
    baseUrl        =  'https://www.olx.pl/motoryzacja/samochody/'
    if not model:
        olxR = requests.get(f'https://www.olx.pl/motoryzacja/samochody/{make}/?search%5Border%5D=created_at%3Adesc')
    else:
        olxR = requests.get(f'https://www.olx.pl/motoryzacja/samochody/{make}/{model}/?search%5Border%5D=created_at%3Adesc')
    soup            = BeautifulSoup(olxR.content, 'lxml')
    carList         = soup.find_all('tr', class_='wrap')
    nameList, priceList, linkList, additionalList, pictureList = [],[],[],[],[]
    for x in carList:
        carData     = x.find('a',  href=True, class_="link linkWithHash detailsLink")
        longLink    = str(carData['href'])
        
    
        #nameList.append(carName)

        #linkList.append(longLink)
      

    #olxData   = list(zip(pictureList,nameList,additionalList,priceList,linkList))

    return longLink

