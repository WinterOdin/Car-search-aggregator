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
        make    = request.POST.get('make')
        model   = request.POST.get('model')
        #olx     = olxScrapper(make,model)
        auto    = autoscoutScrapper(make,model)
        oto     = otomotoScrapper(make,model)
       # print(olx)
        print()
        print(auto)
        print()
        print(oto)

    context={
        #'olx':olx,
        'auto':auto,
        'oto':oto

    }
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
        carName     = x.find('h2',   class_="cldt-summary-makemodel sc-font-bold sc-ellipsis").get_text()
        carPrice    = x.find('span', class_="cldt-price sc-font-xl sc-font-bold" , attrs={"data-item-name":"price"}).get_text(strip=True)
        shortLink   = x.find('a',    href=True, attrs={'data-item-name':True})
        longLink    = baseUrl+shortLink['href']
        try:
            additionalName   = x.find('h2', class_="cldt-summary-version sc-ellipsis").get_text()
        except:
            additionalName   = "No additiona info provided."
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
    return autoscoutData

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
        carPrice    = x.find('span', class_="offer-price__number ds-price-number" ).get_text(strip=True)
        try:
            additionalName   = x.find('h3', class_="offer-item__subtitle ds-title-complement hidden-xs", attrs={'data-type':"complement"} ).get_text()
        except:
            additionalName   = "No additiona info provided."
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
        olxR = requests.get(f'https://www.olx.pl/motoryzacja/samochody/{make}/')
    else:
        olxR = requests.get(f'https://www.olx.pl/motoryzacja/samochody/{make}/{model}/?search%5Border%5D=created_at%3Adesc')
    soup            = BeautifulSoup(olxR.content, 'lxml')
    carList         = soup.find_all('table', attrs={"summary":"Ogłoszenie"})
    nameList, priceList, linkList, additionalList, pictureList = [],[],[],[],[]
    for x in carList:
        carData    = x.find("img", class_="fleft")
        carPicture = carData["src"]
        carName    = ','.join(carData["alt"].split()[:4]).replace(',',' ')
        secondName = ','.join(carData["alt"].split()[4::]).replace(',',' ')
        carLink    = x.find("a",attrs={"data-cy":"listing-ad-title"})['href']
        carPrice   = x.find("p", class_="price").get_text(strip=True)

        priceList.append(carPrice)
        nameList.append(carName)
        linkList.append(carLink)
        pictureList.append(carPicture)
        additionalList.append(secondName)

    olxData   = list(zip(pictureList,nameList,additionalList,priceList,linkList))

    return  olxData
