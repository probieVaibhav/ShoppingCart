from django.shortcuts import render
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
# import checksum.py file from paytm directory
from PayTm import checksum
# paytm marchant key
MERCHANT_KEY = 'Jy8pOnOWwzgTa%vK';

# Create your views here.
from django.http import HttpResponse

def index(request):
    # products = Product.objects.all()
    # print(products)
    # n = len(products)
    # nSlides = n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''return true only if query mathces the item'''
    if query in item.product_desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False
def search(request):
    # return HttpResponse("We are at search")
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0: 
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, 'msg': ""}
    if len(allProds) == 0 or len(query) <= 3:
        params = {'msg': 'Please make sure to enter relavent search query'}
    return render(request, 'shop/search.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    # return HttpResponse("We are at contact")
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        query = request.POST.get('query', '')
        # add contacts
        contact = Contact(name=name, email=email, phone=phone, query=query)
        contact.save()
        thank = True
    return render(request, 'shop/contact.html', {'thank':thank})
def tracker(request):
    # return HttpResponse("We are at tracker")
    if request.method == "POST":
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')
        # return HttpResponse(f'{order_id}, {email}')
        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status': 'success', 'updates': updates, 'itemsJson': order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status": "No item"}')
        except Exception as e:
            # print(f'An exception occured ---> {e}')
            return HttpResponse('{"status": "Error"}')
    return render(request, 'shop/tracker.html')

def prodView(request, prod_id):
    # return HttpResponse("We are at product view")
    # fetch products using id (if we don't have any primary key , then django already done this for us to make an id column with primary key = True)...
    product = Product.objects.filter(id=prod_id)
    print(product)
    return render(request, 'shop/prodView.html', {'product': product[0]})

def checkout(request):
    # return HttpResponse("We are at checkout")
    if request.method == 'POST':
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address_1', '') + " " + request.POST.get('address_2', '')
        phone = request.POST.get('phone', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zipCode', '')
        # add contacts
        order = Order(items_json=items_json, name=name, email=email, phone=phone, city=city, state=state, zip_code=zip_code, address=address, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="the order has been placed")
        update.save()
        thank = True
        id = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # request paytm to transfer the amount to your account after payment by user
        param_dict = {
            'MID':'lOxfNS33424500768376',
            'ORDER_ID':str(order.order_id),
            'TXN_AMOUNT':str(amount),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
	        'CALLBACK_URL':'http://127.0.0.1:8000/shop/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')

# handle request via paytm
@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checkout = form[i]
    verify = checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successfull...')
        else:
            print('order was not sucessfull, because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})