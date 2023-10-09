from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from Admin.models import *
from User.models import*



def admindashboard(request):
    customercount = Userregister.objects.all().count()
    feddbackcount = Userfeedback.objects.all().count()
    productscount = Productregister.objects.all().count()
    orderconfirmedcount = Order.objects.filter(status = 1).count()
    orderdeliveredcount = Order.objects.filter(status = 2).count()
    context = {
        'customercount':customercount, 'feddbackcount':feddbackcount, 'productscount':productscount,
        'orderconfirmedcount':orderconfirmedcount, 'orderdeliveredcount':orderdeliveredcount
    }
    return render(request, 'admindashboard.html', context)

def adminlogin(request):
    if request.method == 'POST':
        aUsername = request.POST['aUsername']
        aPassword = request.POST['aPassword']
        user = authenticate(request, username = aUsername, password = aPassword)
        
        if user is not None:
            login(request, user)
            return redirect('admindashboard')
        else:
            return redirect('adminlogin')
    return render(request, 'admin_login.html')

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')

@login_required(login_url='adminlogin')
def productregister(request):
    category = Productcategory.objects.all()
    if request.method == 'POST':
        pname = request.POST['pname']
        pimage = request.FILES['pimage']
        pprice = request.POST['pprice']
        pcategory = request.POST['pcategory']
        pcategoryInstance = Productcategory.objects.get(id = pcategory)
        pquantity = request.POST['pquantity']
        Productregister.objects.create(pName = pname, pImage = pimage, pPrice = pprice, pCategory = pcategoryInstance, pQuantity = pquantity)
        return redirect(admindashboard)
    return render(request, 'productregister.html', {'category':category})

@login_required(login_url='adminlogin')
def productviews(request):
    productall = Productregister.objects.all()
    return render(request, 'productviewall.html', {'productall':productall})

@login_required(login_url='adminlogin')
def productviewindividual(request, pId):
    individualproduct = Productregister.objects.filter(id = pId)
    category = Productcategory.objects.all()
    return render(request, 'productindividual.html', {'individualproduct':individualproduct, 'category':category} )

@login_required(login_url='adminlogin')
def productupdate(request, pId):
    if request.method == 'POST':
        pname = request.POST['pname']
        try:
            pimage = request.FILES['pimage']
            fs = FileSystemStorage()
            files = fs.save(pimage.name, pimage)
        except MultiValueDictKeyError:
            files = Productregister.objects.get(id = pId).pImage
        pprice = request.POST['pprice']
        pcategory = request.POST['pcategory']
        pquantity = request.POST['pquantity']
        Productregister.objects.filter(id = pId).update(pName = pname, pImage = files, pPrice = pprice, pCategory = pcategory, pQuantity = pquantity)
        return redirect('admindashboard')

@login_required(login_url='adminlogin')   
def productdelete(request, pId):
    Productregister.objects.filter(id = pId).delete()
    return redirect('productviews')

@login_required(login_url='adminlogin')   
def productcategory(request):
    if request.method == 'POST':
        cname = request.POST['cname']
        cimage = request.FILES['cimage']
        Productcategory.objects.create(cName = cname, cImage = cimage)
        return redirect('admindashboard')
    return render(request, 'productcategory.html')

@login_required(login_url='adminlogin')
def categoryviewall(request):
    categorydata = Productcategory.objects.all()
    return render(request, 'viewcategory.html', {'categorydata':categorydata})

@login_required(login_url='adminlogin')
def categoryindividual(request, cId):
    categoryindividualview = Productcategory.objects.filter(id = cId)
    return render(request, 'categoryindividualview.html', {'categoryindividualview':categoryindividualview})

@login_required(login_url='adminlogin')
def categoryupdate(request, cId):
    if request.method == 'POST':
        cname = request.POST['cname']
        try:
            cimage = request.FILES['cimage']
            fs = FileSystemStorage()
            files = fs.save(cimage.name, cimage)
        except:
            files = Productcategory.objects.get(id = cId).cImage
        Productcategory.objects.filter(id = cId).update(cName = cname, cImage = files)
        return redirect('categoryviewall')

@login_required(login_url='adminlogin')    
def categorydelete(request, cId):
    Productcategory.objects.filter(id = cId).delete()
    return redirect('categoryviewall')

@login_required(login_url='adminlogin')
def orderrequests(request):
    orderdata = Order.objects.filter( status__in = [0,1]).order_by('orderdate')
    return render(request, 'orderrequests.html', {'orderdata':orderdata})

@login_required(login_url='adminlogin')
def orderrequestsapprove(request, oId):
    Order.objects.filter(id = oId).update(status = 1)
    user_id = Order.objects.get(id = oId).userid.id
    user_name = Userregister.objects.get(id = user_id).uname
    user_email = Userregister.objects.get(id = user_id).uemail
    order_date = Order.objects.get(id = oId).orderdate
    product_name = Order.objects.get(id = oId).productid.pName

    context = {
        'user_name':user_name, 'order_date':order_date, 'product_name':product_name
    }

    template = render_to_string('orderrequestapproveemail.html', context)
    email = EmailMessage(
        'Greetings',
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )
    email.fail_silently = False
    email.send()
    return redirect('orderrequests')

@login_required(login_url='adminlogin')
def orderrequestsdelivered(request, oId):
    Order.objects.filter(id = oId).update(status = 2)
    user_id = Order.objects.get(id = oId).userid.id
    user_name = Userregister.objects.get(id = user_id).uname
    user_email = Userregister.objects.get(id = user_id).uemail
    order_date = Order.objects.get(id = oId).orderdate
    product_name = Order.objects.get(id = oId).productid.pName
    context = {
        'user_name':user_name, 'order_date':order_date, 'product_name':product_name
    }

    template = render_to_string('orderdeliveryconfirmemail.html', context)
    email = EmailMessage(
        'Greetings',
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )
    email.fail_silently = False
    email.send()
    return redirect('orderrequests')

@login_required(login_url='adminlogin')
def orderhistoryadmin(request):
    orderhistory = Order.objects.filter(status = 2).order_by('orderdate')
    return render(request, 'orderhistoryadmin.html', {'orderhistory':orderhistory})

@login_required(login_url='adminlogin')
def registeredusers(request):
    userlist = Userregister.objects.all()
    return render(request, 'registeredusers.html',{'userlist':userlist})

@login_required(login_url='adminlogin')
def userfeedbacklist(request):
    feedbacklist = Userfeedback.objects.all()
    return render(request, 'userfeedbackadmin.html', {'feedbacklist':feedbacklist})
