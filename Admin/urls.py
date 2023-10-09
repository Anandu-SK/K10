from django.urls import path
from Admin.views import *

urlpatterns = [
    path('adminlogin/', adminlogin, name ='adminlogin'),
    path('adminlogout/', adminlogout, name ='adminlogout'),
    path('admindashboard/', admindashboard, name='admindashboard'),
    path('productregister/', productregister, name='productregister'),
    path('productviews/', productviews, name='productviews'),
    path('productviewindividual/<int:pId>/', productviewindividual, name='productviewindividual'),
    path('productupdate/<int:pId>', productupdate, name='productupdate'),
    path('productdelete/<int:pId>/', productdelete, name= 'productdelete'),
    path('productcategory/', productcategory, name='productcategory'),
    path('categoryviewall/', categoryviewall, name='categoryviewall'),
    path('categoryindividual/<int:cId>/', categoryindividual, name='categoryindividual'),
    path('categoryupdate/<int:cId>/', categoryupdate, name='categoryupdate'),
    path('categorydelete/<int:cId>/', categorydelete, name='categorydelete'),
    path('orderrequests/', orderrequests, name='orderrequests'),
    path('orderrequestsapprove/<int:oId>/', orderrequestsapprove, name='orderrequestsapprove'),
    path('orderrequestsdelivered/<int:oId>/', orderrequestsdelivered, name='orderrequestsdelivered'),
    path('orderhistoryadmin/', orderhistoryadmin, name='orderhistoryadmin'),
    path('registeredusers/', registeredusers, name='registeredusers'),
    path('userfeedbacklist/', userfeedbacklist, name='userfeedbacklist')
]


