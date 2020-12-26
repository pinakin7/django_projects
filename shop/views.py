from django.shortcuts import render
from django.http import HttpResponse
from .models import product
from .models import Contact
from .models import Order
from .models import OrderUpdate
from .models import SiteData
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
import sys 
import os
sys.path.append(os.path.abspath("D:/Programs/python/django_projects/ecomm/shop/"))
from PayTm import Checksum
MERCHANT_KEY = 'kbzk1DSbJiV_O3p5'

def index(request):
    # products = product.objects.all()
    # n = len(products)
    # nslides = n//4 + ceil((n/4) - (n//4))
    allproducts =[]

    product_category = product.objects.values('category','id')

    cats = {item['category'] for item in product_category}
    for cat in cats:
        products = product.objects.filter(category=cat)
        n = len(products)
        nslides = n//4 + ceil((n/4) - (n//4))
        allproducts.append([products,range(1,nslides),nslides])
    
    # params = {'no_of_slides': nslides,'range':range(nslides),'product':products}
    
    # allproducts = [[products,range(1,nslides),nslides],
    #                 [products,range(1,nslides),nslides]]
    params = {'allproducts':allproducts}
    return render(request, 'shop/index.html',params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        user_contact = Contact(name=name, email=email, phone=phone, desc=desc)
        user_contact.save()
        
    return render(request, 'shop/contact.html')

def track(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            orr = Order.objects.filter(order_id=orderId, email=email)
            if len(orr)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, orr[0].item_json],default=str)

                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/track.html')

def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query.lower() in item.description.lower() or query.lower() in item.product_name.lower() or query.lower() in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    # print(query)
    udata = SiteData(product_name=query,action='Search')
    udata.save()
    allproducts = []
    catprods = product.objects.values('category', 'id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    print(cats)
    for cat in cats:
        prodtemp = product.objects.filter(category=cat)
        print(prodtemp)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allproducts.append([prod, range(1, nSlides), nSlides])
    params = {'allproducts': allproducts, "msg": ""}
    if len(allproducts) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    print(params)
    return render(request, 'shop/search.html', params)


def productview(request,myid):
    my_product = product.objects.filter(id=myid)
    for items in my_product:
        udata = SiteData(product_name=items.product_name,action='View Product')
        udata.save()
        print(items.product_name)
    

    return render(request, 'shop/productview.html',{'product':my_product[0]})

def checkout(request):
    if request.method=='POST':
        item_json = request.POST.get('itemJson', '')
        amount = request.POST.get('amount', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1','') + " " + request.POST.get('address2','')
        city = request.POST.get('city','')
        state = request.POST.get('state','')
        zipcode = request.POST.get('zip', '')
        phone = request.POST.get('phone', '')
        orr = Order(item_json=item_json,amount=amount,name=name, email=email, address=address, city=city, state=state,zip_code=zipcode, phone=phone)
        orr.save()
        # update= OrderUpdate(order_id= orr.order_id, update_desc="The order has been placed")
        # update.save()
        thank = True
        _id = orr.order_id
        # print(json.loads(item_json))
        for key in json.loads(item_json):
            udata = SiteData(product_name=json.loads(item_json)[key][1],action='Purchase')
            udata.save()
            # print(json.loads(item_json)[key][1])
        # for item in item_json:
        #     print(item)
            # udata = SiteData(product_name = item["product_name"],action='Purchase')
            # udata.save()
        return render(request, 'shop/checkout.html',{'thank': thank,'id':_id})
        #request Paytm to transfer amount
        # param_dict = {

        #         'MID': 'WorldP64425807474247',
        #         'ORDER_ID': "or"+str(_id),
        #         'TXN_AMOUNT': str(amount),
        #         'CUST_ID': email,
        #         'INDUSTRY_TYPE_ID': 'Retail',
        #         'WEBSITE': 'WEBSTAGING',
        #         'CHANNEL_ID': 'WEB',
        #         'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlepayment/',

        # }
        # param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        # print(param_dict)
        # return render(request, 'shop/paytm.html', {'param_dict': param_dict})

    return render(request, 'shop/checkout.html')




# Paytm Integration
# @csrf_exempt
# def handle_payment(request):
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
    
#     print(response_dict)
    
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#         else:
#             print('order was not successful because ' + response_dict['RESPMSG'])
#     return render(request, 'shop/paymentstatus.html', {'response': response_dict})