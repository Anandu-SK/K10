from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.aggregates import Sum
from django.conf import settings
from django.contrib import messages
from datetime import date
from django.core.mail import send_mail
import random as r
from datetime import datetime, timedelta
from django.utils import timezone
import hashlib
from django.db.models import DateField
from django.db.models.functions import Cast
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import stripe


from User.models import *
from Admin.models import *


def userindex(request):
    if 'u_id' in request.session:
        userid = request.session.get('u_id')
        cart_count = Cart.objects.filter(userid = userid, status = 0).count()
        cart_total = Cart.objects.filter(userid = userid, status = 0).aggregate(Sum('total'))
        categorydata = Productcategory.objects.all()
        return render(request, 'userindex.html', {'cart_count':cart_count, 'cart_total':cart_total, 'categorydata':categorydata})
    else:
        return redirect('userlogin')



def userhome(request):
    if 'u_id' in request.session:
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id=usersession)
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        cart_total = Cart.objects.filter(userid = usersession, status = 0).aggregate(Sum('total'))
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        categorydata = Productcategory.objects.all()
        return render(request, 'userhome.html', {'cart_count':cart_count, 'cart_total':cart_total, 'wishlist_count':wishlist_count, 'categorydata':categorydata})
    else:
        return('userlogin')

def userhomepage(request):
    return render(request, 'userhome.html')

def userregister(request):
    if request.method=='POST':
        uName = request.POST['uName']
        uEmail = request.POST['uEmail']
        uPassword = request.POST['uPassword']
        uAddress = request.POST['uAddress']
        uPhone = request.POST['uPhone']
        if Userregister.objects.filter(uemail = uEmail).exists():
            messages.warning(request, 'This Email Address already exists')
            return redirect(userlogin)
        else:
            Userregister.objects.create(uname = uName, uemail = uEmail, upassword = uPassword, uaddress = uAddress, uphonenumber = uPhone)
            context = {
                'uName':uName, 'uEmail':uEmail
            }
            template = render_to_string('newregistereduseremail.html', context)
            email = EmailMessage(
            'Subject: Welcome to Our Coffee and Snack Shop!',
            template,
            settings.EMAIL_HOST_USER,
            [uEmail],
            )
            email.fail_silently = False
            email.send()
            return redirect('userlogin')
    
def userlogin(request):
    if 'u_id' in request.session:
        return redirect('userhome')
    else:
        if request.method == 'POST':
            uEmail = request.POST['uEmail']
            uPassword = request.POST['uPassword']
            if Userregister.objects.filter(uemail = uEmail, upassword = uPassword).exists():
                data = Userregister.objects.filter(uemail = uEmail, upassword = uPassword).values('uname', 'uphonenumber', 'uaddress', 'id').first()
                request.session['u_id'] = data['id']
                request.session['username'] = data['uname']
                request.session['userphonenumber'] = data['uphonenumber']
                request.session['useraddress'] = data['uaddress']
                request.session['useremail'] = uEmail
                request.session['userpassword'] = uPassword
                return redirect('userhome')
            else:
                messages.error(request, 'Invalid Credentials')
                return redirect('userlogin')
        return render(request, 'userloginandregister.html')
        
def userlogout(request):
    if 'u_id' in request.session:
        del request.session['u_id']
        del request.session['username']
        del request.session['userphonenumber']
        del request.session['useraddress']
        del request.session['useremail']
        del request.session['userpassword']
        return redirect('userhomepage')
    else:
        return redirect('userlogin')

def usermainpage(request):
    if 'u_id' in request.session:
        data = Productcategory.objects.all()
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id=usersession)
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        categorydata = Productcategory.objects.all()
        return render(request, 'usermainpage.html', {'data':data, 'cart_count':cart_count, 'wishlist_count':wishlist_count, 'cart_total':cart_total, 'categorydata':categorydata})
    else:
        return redirect('userlogin')

def usercategorywiseproducts(request, cId):
    if 'u_id' in request.session:
        category_id = Productcategory.objects.get(id = cId).id
        categorywise = Productregister.objects.filter(pCategory__id=category_id)
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id=usersession)
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        categorydata = Productcategory.objects.all()
        return render(request, 'usercategorywiseproducts.html', {'categorywise':categorywise, 'cart_count':cart_count, 'cart_total':cart_total, 'wishlist_count':wishlist_count, 'categorydata':categorydata})
    else:
        return redirect('userlogin')

def carticon(request, pId):
    if 'u_id' in request.session:
        usersession = request.session.get('u_id')
        request.session['pid'] = pId
        cart_count = Cart.objects.filter(status = 0).count()
        if request.method == 'POST':
            cart_item = Cart.objects.filter(userid=usersession, productid = pId, status=0).first()
            if cart_item:
                user_id = Userregister.objects.get(id = usersession)
                product_id = Productregister.objects.get(id=pId)
                product_quantity = Productregister.objects.get(id=pId).pQuantity
                productprice = Productregister.objects.get(id=pId).pPrice
                if cart_item.quantity < product_quantity:
                    cart_quantity = min(cart_item.quantity + 1, 15, product_quantity)
                else:
                    cart_quantity = min(15, product_quantity)
                cart_sum = int(cart_quantity)*int(productprice)
                cart_total = request.POST['cart_total']
                Cart.objects.filter(userid = user_id, productid = product_id).update(quantity = cart_quantity, total = cart_sum)
                Wishlist.objects.filter(userid = usersession, productid = pId ,status = 0).update(status = 1)
                return redirect('carttotal')
            else:
                user_id = Userregister.objects.get(id = usersession)
                product_id = Productregister.objects.get(id=pId)
                cart_quantity = 1
                cart_total = request.POST['cart_total']
                Cart.objects.create(userid = user_id, productid = product_id, quantity = cart_quantity, total = cart_total)
                Wishlist.objects.filter(userid = usersession, productid = pId ,status = 0).update(status = 1)
                return redirect('carttotal')
        return render(request, 'usermainpage.html', {'cart_count':cart_count})
    else:
        return redirect('userlogin')


def shoppingcartdelete(request, cId):
    Cart.objects.filter(id=cId).delete()
    return redirect('carttotal')

@csrf_exempt
def quantityupdate(request):
    if 'u_id' in request.session:
        if request.method == 'POST':
            cart_quantity = request.POST['qty']
            cart_price = request.POST['price']
            cart_id = request.POST['cid']
            cart_total = int(cart_price) * int(cart_quantity)
            Cart.objects.filter(id = cart_id).update(total = cart_total, quantity = cart_quantity)
            return JsonResponse({'success':True})
    else:
        return redirect('userlogin')
        

def carttotal(request):
    if 'u_id' in request.session:
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id=usersession)
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        cartdata = Cart.objects.filter(userid = user_id, status = 0)
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id=usersession)
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        categorydata = Productcategory.objects.all()
        cartlist = []     
        for i in cartdata:
            cartlist.append(i.total)
        cartlist.sort(reverse=True)
        cartlist_length = len(cartlist)
        if cartlist_length == 0:
            highestprice = 0
            request.session['highest_price'] = highestprice
        else:
            highestprice = cartlist[0]
            request.session['highest_price'] = highestprice
        return render(request, 'shoppingcart.html', {'cart_total':cart_total, 'cartdata':cartdata, 'cart_count':cart_count, 'cart_total':cart_total, 'wishlist_count':wishlist_count, 'categorydata':categorydata})
    else:
        return redirect('userlogin')
    

def proceedcheck(request):
    if 'u_id' in request.session:
        usersession = request.session.get('u_id')
        highestprice = request.session.get('highest_price')
        user_id = Userregister.objects.get(id = usersession)
        user_name = Userregister.objects.get(id = usersession).uname
        user_address = Userregister.objects.get(id = usersession).uaddress
        user_phone = Userregister.objects.get(id = usersession).uphonenumber
        user_email = Userregister.objects.get(id = usersession).uemail
        cartdata = Cart.objects.filter(userid = user_id, status = 0)
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id=usersession)
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        cartlist = []
        for i in cartdata:
            pQuantity_update = i.productid.pQuantity-i.quantity
            if pQuantity_update <= 0 :
                messages.warning(request, f"Only {i.productid.pQuantity} more {i.productid.pName} left.")
        for i in cartdata:
            cartlist.append(i.total)
        cartlist_length = len(cartlist)
        first_matching_item = True
        for item in cartdata:
            if cartlist_length == 1:
                item.is_first_matching = False
            else:
                if item.total == highestprice and first_matching_item:
                    item.is_first_matching = True
                    first_matching_item = False
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        if cartlist_length == 0:
            total_sum = 0
        else:
            total_sum = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))['total__sum']
        if cartlist_length == 1:
            tax = int((8/100)*total_sum)
            total_bill = (total_sum + tax)
        else:
            tax = int((8/100)*total_sum)
            total_bill = (total_sum + tax) - highestprice
        request.session['totalbill'] = total_bill
        request.session['utax'] = tax
        categorydata = Productcategory.objects.all()
        context = {
            'cartdata':cartdata, 'cart_total':cart_total, 'tax':tax,
            'highestprice':highestprice, 'total_bill':total_bill, 'user_name':user_name,
            'user_address':user_address, 'user_phone':user_phone, 'user_email':user_email,
            'cart_count':cart_count, 'wishlist_count':wishlist_count, 'categorydata':categorydata
        }
        return render(request, 'checkout.html', context)
    else:
        return redirect('userlogin')
    
stripe.api_key = settings.STRIPE_SECRET_KEY
def ordercheckout(request):
    if 'u_id' in request.session:
        if request.method == 'POST':
            user_id = request.session.get('u_id')
            uName = request.POST['uName']
            uAddress = request.POST['uAddress']
            uTown = request.POST['uTown']
            uPostcode = request.POST['uPostcode']
            uPhone = request.POST['uPhone']
            uEmail = request.POST['uEmail']
            request.session['uName1'] = uName
            request.session['uAddress1'] = uAddress
            request.session['uTown1'] = uTown
            request.session['uPostcode1'] = uPostcode
            request.session['uPhone1'] = uPhone
            request.session['uEmail1'] = uEmail
            current_date = date.today()
            cdata = Cart.objects.filter(userid = user_id, status = 0)
            cartlist = []
            for i in cdata:
                cartlist.append(i.total)
            cartlist_length = len(cartlist)
            if Order.objects.filter(orderdate = current_date).exists():
                messages.warning(request,"You cannot order more than once a day. Comeback again tomorrow. Thank you")
                return redirect('proceedcheck')
            else:
                if cartlist_length == 0:
                    messages.warning(request,"Add atleast one item first before you proceed")
                    return redirect('proceedcheck')
                else:
                    for i in cdata:
                        cartid = i.id
            total_bill = request.session.get('totalbill')
            session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                line_items=[{
                        'price_data':{
                            'currency': 'inr',
                            'product_data':{
                                'name': 'totalbill',
                            },
                            'unit_amount': int(total_bill)*100,
                        
                        },
                        'quantity':1,
                }],
                mode='payment',
                success_url = "http://127.0.0.1:8000/paynowsuccesspage?session_id={CHECKOUT_SESSION_ID}",
                cancel_url = "http://127.0.0.1:8000/pay_cancel",
                client_reference_id=cartid,
                )
            return redirect(session.url, code=303)
    else:
        return redirect('userlogin')
        
def paynowsuccesspage(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    cartid = session.client_reference_id
    if 'u_id' in request.session:
        usersession = request.session.get('u_id')
        user_id = Userregister.objects.get(id = usersession)
        uName = request.session.get('uName1')
        uAddress = request.session.get('uAddress1')
        uTown = request.session.get('uTown1')
        uPostcode = request.session.get('uPostcode1')
        uPhone = request.session.get('uPhone1')
        uEmail = request.session.get('uEmail1')
        highestprice = request.session.get('highest_price')
        tax = request.session.get('utax')
        cdata = Cart.objects.filter(userid = usersession,status=0)
        total_bill = request.session.get('totalbill')
        Shippingaddress.objects.create(userid = user_id, username = uName, address = uAddress, town = uTown, postcode = uPostcode, phone = uPhone, email = uEmail)
        for items in cdata:
            if Order.objects.filter(userid = usersession, cartid = items.id).exists():
                pass
            else:
                for i in cdata:
                    if (i.productid.pQuantity-i.quantity) <= 0:
                        each_product_total = i.quantity * int(i.productid.pPrice)
                        print(each_product_total)
                        print("++++++++++++++++++++++++++++++++++++++++++++")
                        order_quantity = min(i.productid.pQuantity, i.quantity)
                        pQuantity_update = i.productid.pQuantity - order_quantity
                        Order.objects.create(userid = i.userid, productid = i.productid, cartid = Cart.objects.get(id = i.id), orderquantity = order_quantity , total = i.total, total_bill = total_bill, discount = highestprice, tax = tax, each_product_total = each_product_total)
                        product_id = i.productid.id
                        Productregister.objects.filter(id = product_id).update(pQuantity = pQuantity_update)
                    else:
                        each_product_total = i.quantity * i.productid.pPrice
                        print(each_product_total)
                        print("++++++++++++++++++++++++++++++++++++++++++++")
                        Order.objects.create(userid = i.userid, productid = i.productid, cartid = Cart.objects.get(id = i.id), orderquantity = i.quantity , total = i.total, total_bill = total_bill, discount = highestprice, tax = tax, each_product_total = each_product_total)
                        pQuantity_update = i.productid.pQuantity-i.quantity
                        product_id = i.productid.id
                        Productregister.objects.filter(id = product_id).update(pQuantity = pQuantity_update)
        Cart.objects.filter(userid = user_id, status = 0).update(status=1)
        if 'uName' in request.session:
            del request.session['uName']
        if 'uAddress' in request.session:
            del request.session['uAddress']
        if 'uTown' in request.session:
            del request.session['uTown']
        if 'uPostcode' in request.session:
            del request.session['uPostcode']
        if 'uEmail' in request.session:
            del request.session['uEmail']
        if 'uPhone' in request.session:
            del request.session['uPhone']
        if 'total_bill' in request.session:
            del request.session['total_bill']
        if 'highestprice' in request.session:
            del request.session['highestprice']
        if 'tax' in request.session:
            del request.session['tax']
        return render(request, 'paysuccess.html')
    else:
        return redirect('userlogin')

def wishlist(request, pId):
    if 'u_id' in request.session:
        user_session = request.session.get('u_id')
        user_id = Userregister.objects.get(id= user_session)
        if Wishlist.objects.filter(userid = user_id, productid__id = pId, status=0).exists():
            messages.warning(request, "This item is already in the wishlist")
            return redirect('wishlistview')
        else:
            user_session = request.session.get('u_id')
            user_id = Userregister.objects.get(id = user_session)
            product_id = Productregister.objects.get(id = pId)
            Wishlist.objects.create(userid = user_id, productid = product_id)
            return redirect('wishlistview')
    else:
        return redirect('userlogin')
    
def wishlistview(request):
    if 'u_id' in request.session:
        user_session = request.session.get('u_id')
        user_id = Userregister.objects.get(id = user_session)
        cart_count = Cart.objects.filter(userid = user_id, status=0).count()
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        wishlistdata = Wishlist.objects.filter(userid = user_session, status = 0)
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        categorydata = Productcategory.objects.all()
        return render(request, 'wishlist.html', {'wishlistdata':wishlistdata, 'wishlist_count':wishlist_count, 'cart_count':cart_count, 'cart_total':cart_total, 'categorydata':categorydata})
    else:
        return redirect('userlogin')

def wishlistremove(request, pId):
    if 'u_id' in request.session:
        user_session = request.session.get('u_id')
        user_id = Userregister.objects.get(id = user_session)
        Wishlist.objects.filter(userid = user_id, productid = pId ,status = 0).update(status = 2)
        return redirect('wishlistview')
    else:
        return redirect('userlogin')

# OTP GENERATION AND VALIDATION
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    
def generate_otp():
    otp = ''.join(r.choice('1234567890') for _ in range(6))
    return otp

def send_otp_email(request, uEmail, otp):
    email_hash = hashlib.sha256(uEmail.encode()).hexdigest()
    user_key = f'last_otp_sent_time{email_hash}'
    # print(user_key)
    # print(request.session.get(user_key))
    # print("[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    last_otp_sent_time_str = request.session.get(user_key)
    if last_otp_sent_time_str:
        last_otp_sent_time = datetime.strptime(last_otp_sent_time_str, '%Y-%m-%d %H:%M:%S.%f%z')
        elapsed_time = timezone.now() - last_otp_sent_time
        if  elapsed_time < timedelta(seconds=20):
        # Inform the user that they need to wait before requesting another OTP
            messages.success(request,'Please wait before requesting for a new OTP')
            return redirect('resetpassword')
        else:
            subject = 'Your OTP to reset password'
            message = f"Your verification code to reset the password is {otp}"
            from_email = 'falcon952698@gmail.com'
            recipient_list = [uEmail]
            send_mail(subject, message, from_email, recipient_list)
    request.session[user_key] = str(timezone.now()) 
            
    
def resetpassword(request):
    if request.method == 'POST':
        uEmail = request.POST['uEmail'] 
        email_hash_form = hashlib.sha256(uEmail.encode()).hexdigest()
        if Userregister.objects.filter(uemail = uEmail).exists():
            otp = generate_otp()
            send_otp_email(request,uEmail, otp)
            request.session[f'reset_password_otp_{uEmail}'] = otp
            request.session['Email'] = uEmail
            messages.success(request, 'The OTP has sent successfully')
            request.session[email_hash_form] = True
            return redirect('verify_otp')
          
        else:
            messages.warning(request, 'This email does not exists')
    return render(request, 'resetpassword.html')


def verify_otp(request):
    uEmail1 = request.session.get('Email')
    stored_otp = request.session.get(f'reset_password_otp_{uEmail1}')
    # print("{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}")
    # print(stored_otp)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if stored_otp == entered_otp:
            if 'uEmail1' in request.session:
                del request.session['uEmail1']
            if 'stored_otp' in request.session:
                del request.session['stored_otp']     
            return redirect('passwordresetform')
            
        else:
            messages.warning(request, 'Invalid OTP')

    return render(request, 'otp.html')

def resend_otp(request):
    
    uEmail = request.session.get('Email')
    email_hash = hashlib.sha256(uEmail.encode()).hexdigest()
    user_key = f'last_otp_sent_time{email_hash}'
    last_otp_sent_time_str = request.session.get(user_key)
    if last_otp_sent_time_str:
        last_otp_sent_time = datetime.strptime(last_otp_sent_time_str, '%Y-%m-%d %H:%M:%S.%f%z')
        elapsed_time = timezone.now() - last_otp_sent_time
        if  elapsed_time < timedelta(seconds=20):
        # Inform the user that they need to wait before requesting another OTP
            messages.success(request,'Please wait before requesting for a new OTP')
            return redirect('verify_otp')
        else:
            otp = generate_otp()
            if 'stored_otp' in request.session:
                del request.session['stored_otp']
            request.session[f'reset_password_otp_{uEmail}'] = otp
            subject = 'Your OTP to reset password'
            message = f"Your verification code to reset the password is {otp}"
            from_email = 'falcon952698@gmail.com'
            recipient_list = [uEmail]
            send_mail(subject, message, from_email, recipient_list)
    request.session[user_key] = str(timezone.now()) 
    return redirect('verify_otp')
        
def passwordresetform(request):
    uEmailreset = request.session.get('Email')
    email_hash_form = hashlib.sha256(uEmailreset.encode()).hexdigest()
    if request.session.get(email_hash_form):
        if request.method == 'POST':
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            if password1!=password2:
                messages.error(request, 'The password does not match')
            else:
                uEmailreset = request.session.get('Email')
                Userregister.objects.filter(uemail = uEmailreset).update(upassword = password2)
                messages.success(request, 'Password Changed Successfully')
                del request.session[email_hash_form]
                return redirect('userlogin')
        return render(request, 'passwordresetform.html')
    else:
        messages.warning(request, 'Invalid request. Please go through the proper steps.')
        return redirect('userlogin')
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def orderhistory(request, date):
    if 'u_id' in request.session:
        user_id = request.session.get('u_id')
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        categorydata = Productcategory.objects.all()
        order_history = Order.objects.filter(userid = user_id, orderdate =date)
        context = {
            'order_history':order_history, 'cart_count':cart_count, 'cart_total':cart_total,
            'wishlist_count':wishlist_count, 'categorydata':categorydata
        }
        return render(request, 'orderhistory.html', context)
    else:
        return redirect('userlogin')
    
def uniquedate(request):
    if 'u_id' in request.session:
        user_id = request.session.get('u_id')
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        categorydata = Productcategory.objects.all()
        unique_dates = Order.objects.filter(userid=user_id).annotate(order_date=Cast('orderdate', DateField())).values_list('order_date', flat=True).distinct()
        context = {
            'unique_dates':unique_dates, 'cart_count':cart_count, 'cart_total':cart_total,
            'wishlist_count':wishlist_count, 'categorydata':categorydata
        }
        return render(request, 'orderdates.html', context)
    else:
        return redirect('userlogin')

def userprofile(request):
    if 'u_id' in request.session:
        user_id = request.session.get('u_id')
        cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
        cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
        wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
        categorydata = Productcategory.objects.all()
        userprofiledetails = Userregister.objects.filter(id = user_id)
        context = {
            'userprofiledetails':userprofiledetails, 'cart_count':cart_count, 'cart_total':cart_total,
            'wishlist_count':wishlist_count, 'categorydata':categorydata
        }
        return render(request, 'userprofile.html', context)
    else:
        return redirect('userlogin')
    
def updateuserprofile(request):
    if 'u_id' in request.session:
        user_id = request.session.get('u_id')
        if request.method == 'POST':
            uName = request.POST['uName']
            uPhone = request.POST['uPhone']
            uAddress = request.POST['uAddress']
            uEmail = request.POST['uEmail']
            Userregister.objects.filter(id = user_id).update(uname = uName, uphonenumber = uPhone, uaddress = uAddress, uemail = uEmail)
            messages.success(request, 'The profile has been updated successfully')
            return redirect('userprofile')
    else:
        return redirect('userlogin')

def userdelete(request): 
    if 'u_id' in request.session:
        user_id = request.session.get('u_id')
        Userregister.objects.filter(id = user_id).delete()
        del request.session['u_id']
        messages.success(request, 'Profile Deleted successfully')
        return redirect('userlogin')
    else:
        return redirect('userlogin')

def invoice(request, date):

    if 'u_id' in request.session:

         user_id = request.session.get('u_id')
         highestprice = request.session.get('highest_price')
         orderdata_invoice = Order.objects.filter(userid = user_id, orderdate = date)
         cart_count = Cart.objects.filter(userid = user_id, status = 0).count()
         cart_total = Cart.objects.filter(userid = user_id, status = 0).aggregate(Sum('total'))
         wishlist_count = Wishlist.objects.filter(userid = user_id, status=0).count()
         categorydata = Productcategory.objects.all()
         totalbill1 = orderdata_invoice.first()
         totalbill = totalbill1.total_bill
         tax = totalbill1.tax
         discount = totalbill1.discount
         context = {
            'highestprice':highestprice, 'orderdata_invoice':orderdata_invoice, 'cart_count':cart_count,
            'cart_total':cart_total, 'wishlist_count':wishlist_count, 'categorydata':categorydata, 'date':date,
            'totalbill':totalbill, 'tax':tax, 'discount':discount
         }
         return render(request, 'invoice.html', context)
    else:
        return redirect('userlogin')

def userfeedback(request):

    if request.method == 'POST':
        uName = request.POST['uName']
        uEmail = request.POST['uEmail']
        uMessage = request.POST['uMessage']
        Userfeedback.objects.create(uname = uName, uemail = uEmail, umessage = uMessage)
    return render(request, 'userfeedback.html')

def aboutus(request):
    return render(request, 'aboutus.html')