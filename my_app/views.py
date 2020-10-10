from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
import itertools




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

    post_listings=soup.find_all(class_="mpof_ki mqen_m6 mp7g_oh mh36_0 mvrt_0 mg9e_8 mj7a_8 m7er_k4 _1y62o _9c44d_1I1gg")

    post_listings2=soup2.find_all(class_="s-item__image-img")
    post_listing21=soup2.find_all(class_="s-item__link")
    post_listing22=soup2.find_all(class_="s-item__price")




    final_listings=[]
    final_listings1=[]

    for pa in post_listings:
        post_title=pa.find(class_="_w7z6o _uj8z7 meqh_en mpof_z0 mqu1_16 _9c44d_2vTdY").text
        post_url=pa.find('a').get('href')
        post_price=pa.find("span",class_="_1svub _lf05o").text.replace(",", ".").replace(" ","")
        post_price=post_price[:-2]
        post_price=float(post_price)
        post_img=pa.find("img").get('data-src')
        if post_img != None:
            final_listings.append((post_title, post_url, post_price, post_img))



    for (ia,ib,ic) in zip(post_listings2,post_listing21,post_listing22):
        post_title=ia.get('alt')
        post_img = ia.get('src')
        post_url=ib.get('href')
        post_price=ic.find("span",class_="ITALIC").get_text().replace(",", ".")

        post_price = post_price[:-2]
        if len(post_price)>=8:
            post_price=post_price[6:]
        post_price = float(post_price)

        final_listings1.append((post_title, post_url, post_price, post_img))

    final_listings = final_listings + final_listings1












    #shuffle(final_listings)
    final_listings.sort(key = lambda x : x[2])



    front = {'search': search ,
                'page':int(page)+1,
                'prev':int(page)-1,
              'final_listings':final_listings}

    return render(request,'my_app/new_search.html',front)





