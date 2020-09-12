from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup 
import pandas as pd
import requests
from django.templatetags.static import static
headers  = { 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36' }



def home(request):
 
    context={}
    return render(request,'index.html', context)





def listGenerator(request):
    searchData = [] 
    if request.method == "POST":
        make   = request.POST.get('make')
        model   = request.POST.get('model')
        autoscoutResult = autoscoutScrapper(make,model)
        print(autoscoutResult)
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
    qwe =   []
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
        
    return qwe
    





