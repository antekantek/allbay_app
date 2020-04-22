from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus

#from . import models
#from random import shuffle



def home(request):
    return render(request,'base.html')



def new_search(request):
    page = request.POST.get('page')
    if page==None:
        page=1
    BASE_ALL_URL = 'https://allegro.pl/listing?string={}&p='+str(page)
    BASE_EBA_URL= 'https://www.ebay.pl/sch/i.html?_nkw={}&_pgn='+str(page)



    search=request.POST.get('search')
    final_url=BASE_ALL_URL.format(quote_plus(search))
    final_url2 = BASE_EBA_URL.format(quote_plus(search))
    response=requests.get(final_url)
    response2=requests.get(final_url2)
    soup=BeautifulSoup(response.text,'html.parser')
    soup2=BeautifulSoup(response2.text, 'html.parser')
    post_listings=soup.find_all(class_="_9c44d_1V-js")
    post_listings2=soup2.find_all(class_="sresult lvresult clearfix li")




    final_listings=[]


    for pa in post_listings:
        post_title=pa.find(class_="_9c44d_LUA1k").text
        post_url=pa.find('a').get('href')
        post_price=pa.find("span",class_="_9c44d_1zemI").text.replace(",", ".").replace(" ","")
        post_price=post_price[:-2]
        post_price=float(post_price)
        post_img=pa.find("img").get('data-src')
        if post_img != None:
            final_listings.append((post_title, post_url, post_price, post_img))
    #print(len(final_listings))


    for pb in post_listings2:
        post_title=pb.find("h3",class_="lvtitle").text
        post_url = pb.find('a').get('href')
        post_price = pb.find("span", class_="bold").text.replace(",", ".").replace(" ","")
        post_price = post_price[:-2]
        if len(post_price)>=8:
            post_price=post_price[6:]
        post_price = float(post_price)
        post_img=pb.find("img").get('src')



        final_listings.append((post_title, post_url, post_price, post_img))
    #print(len(final_listings))










    #shuffle(final_listings)
    final_listings.sort(key = lambda x : x[2])



    front = {'search': search ,
                'page':int(page)+1,
                'prev':int(page)-1,
              'final_listings':final_listings}

    return render(request,'my_app/new_search.html',front)





