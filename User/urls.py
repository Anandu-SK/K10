from django.urls import path
from django.contrib.auth import views as auth_views

from User.views import *

urlpatterns = [

    # path('', userindex, name='userindex'),
    path('', userhome, name='userhome'),
    path('userregister/', userregister, name='userregister'),
    path('userlogin/', userlogin, name='userlogin'),
    path('userlogout/', userlogout, name = 'userlogout'),
    path('usermainpage/', usermainpage, name='usermainpage'),
    path('usercategorywiseproducts/<int:cId>/', usercategorywiseproducts, name='usercategorywiseproducts'),
    path('carticon/<int:pId>/', carticon, name='carticon'),
    path('userhomepage/', userhomepage, name='userhomepage'),
    path('shoppingcartdelete/<int:cId>/', shoppingcartdelete, name='shoppingcartdelete'),
    path('quantityupdate', quantityupdate, name ='quantityupdate'),
    path('carttotal/', carttotal, name='carttotal'),
    path('proceedcheck/', proceedcheck, name='proceedcheck'),
    path('ordercheckout/', ordercheckout, name='ordercheckout'),
    path('paynowsuccesspage/', paynowsuccesspage, name='paynowsuccesspage'),
    path('wishlist/<int:pId>', wishlist, name='wishlist'),
    path('wishlistview/', wishlistview, name='wishlistview'),
    path('wishlistremove/<int:pId>/',wishlistremove, name='wishlistremove'),
    path('resetpassword/', resetpassword, name='resetpassword'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('passwordresetform/', passwordresetform, name='passwordresetform'),
    path('orderhistory/<str:date>/', orderhistory, name='orderhistory'),
    path('uniquedate/', uniquedate, name='uniquedate'),
    path('userprofile/', userprofile, name='userprofile'),
    path('updateuserprofile/', updateuserprofile, name='updateuserprofile'),
    path('userdelete/', userdelete, name='userdelete'),
    path('invoice/<str:date>', invoice, name='invoice'),
    path('userfeedback/', userfeedback, name='userfeedback'),
    path('aboutus/', aboutus, name='aboutus')

    # path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "resetpassword.html"), name='password_reset'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]