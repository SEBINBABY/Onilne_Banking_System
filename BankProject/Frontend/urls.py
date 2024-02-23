from django.urls import path
from Frontend import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('userloginsignup/', views.userloginsignup, name='userloginsignup'),
    path('UserRegistrationDBsave/', views.UserRegistrationDBsave, name='UserRegistrationDBsave'),
    path('UserLogin/', views.UserLogin, name='UserLogin'),
    # **********************************************************************************
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('recover_password/', views.recover_password, name='recover_password'),
    # ****************************************************************************************
    path('UserLogout/', views.UserLogout, name='UserLogout'),
    path('accounts/', views.accounts, name='accounts'),
    path('accountSingle/<int:accid>/<accname>/', views.accountSingle, name='accountSingle'),
    path('creatACCPage/<accname>/', views.creatACCPage, name='creatACCPage'),
    path('OTPPage/', views.OTPPage, name='OTPPage'),
    path('otpverify/', views.otpverify, name='otpverify'),
    path('accountstatus/', views.accountstatus, name='accountstatus'),
    path('update_profile/<int:userid>/', views.update_profile, name='update_profile'),
    path('accounthistory/<int:accid>/', views.accounthistory, name='accounthistory'),
    path('updatebalance/<int:accid>/', views.updatebalance, name='updatebalance'),
    path('transfermoney/<int:accid>/', views.transfermoney, name='transfermoney'),
    path('updatetransfer/<int:accid>/', views.updatetransfer, name='updatetransfer'),
    path('transactionhistory/', views.transactionhistory, name='transactionhistory'),
    path('rating_review/', views.rating_review, name='rating_review'),
    path('save_rating/', views.save_rating, name='save_rating'),
    path('loans/', views.loans, name='loans'),
    path('loan_application/', views.loan_application, name='loan_application'),
    path('submit_loan_application/', views.submit_loan_application, name='submit_loan_application'),
    path('news_single/<int:news_id>/', views.news_single, name='news_single'),
    path('save_customer_messages/', views.save_customer_messages, name='save_customer_messages'),
    path('transaction_date_fetch/', views.transaction_date_fetch, name='transaction_date_fetch'),
    path('about_page/', views.about_page, name='about_page'),
]