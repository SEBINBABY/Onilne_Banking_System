from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from Backend.models import CustomUser, AccountDB, AccountTypeDB, LoanDb, BankNews
from Frontend.models import accountCreationDB, UserRegistrationDb, LoanSanctionDb, TransactionHistory, ReviewRatingDb, CustomerMessages
from Backend.forms import UserAdminCreationForm
from django.utils.datastructures import MultiValueDictKeyError
from django.core.files.storage import FileSystemStorage
import random
from django.core.mail import send_mail
from django.conf import settings
from axes.decorators import axes_dispatch
from django.views.decorators.cache import cache_page
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView


# Create your views here.

def indexpage(request):
    return render(request, 'index.html')

def register(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('AdminLoginPage')
        else:
            for fields, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
            return redirect(register)
    return render(request, 'register.html', {'form': form})

def AdminLoginPage(request):
    return render(request, 'AdminLoginPage.html')

@axes_dispatch
def AdminLogin(request):
    if request.method == 'POST':
        eml = request.POST.get('Email')
        pwd = request.POST.get('password')
        if CustomUser.objects.filter(email=eml).exists():
            user = authenticate(request, email=eml, password=pwd)
            if user is not None:
                login(request, user)
                request.session['email'] = eml
                request.session['password'] = pwd
                otp = random.randint(1000, 9999)
                request.session['otp'] = otp
                message = "Your OTP to Login into Apex Bank"
                send_mail(otp, message, settings.EMAIL_HOST_USER, [eml], fail_silently=False)
                return render(request, 'otp.html', {'email': eml})
            else:
                messages.error(request, "Invalid Email or Password")
                return redirect(AdminLoginPage)
        else:
            messages.error(request, "Invalid Email or Password")
            return redirect(AdminLoginPage)

def otp_verification(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otp1 = request.session.get('otp')
        if str(otp) == str(otp1):
            messages.success(request, "Logged In Successfully")
            return redirect(indexpage)
        else:
            messages.error(request, "Invalid OTP")
            return redirect(AdminLoginPage)
    return render(request, 'AdminLoginPage.html')

def AdminLogout(request):
    del request.session['email']
    del request.session['password']
    messages.success(request, "You have successfully Logged Out")
    return redirect('AdminLoginPage')

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_message = "We have emailed you instructions for setting your password," \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you donot receive an email, " \
                      "please make sure you have entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('AdminLoginPage')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'  # Set your custom template name
    # Override success_url attribute
    success_url = reverse_lazy('password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'  # Set your custom template name
    # Override success_url attribute
    success_url = reverse_lazy('AdminLoginPage')


@cache_page(60*10)
def AddAccounts(request):
    return render(request, 'AddAccounts.html')

def accountssave(request):
    if request.method == 'POST':
        nm = request.POST.get('AccName')
        desc = request.POST.get('AccDesc')
        desc1 = request.POST.get('AccDesc1')
        img = request.FILES['AccImage']
        obj = AccountDB(ACCNAME=nm, ACCDESC=desc, ACCFULLDESC=desc1, ACCIMAGE=img)
        obj.save()
        messages.success(request, "Account Saved Successfully")
        return redirect(AddAccounts)

def displayAccount(request):
    account = AccountDB.objects.all()
    return render(request, 'AccountsDisplay.html', {'account':account})

def editaccount(request, accid):
    account = AccountDB.objects.get(id=accid)
    return render(request, 'EditAccount.html', {'account':account})

def updateaccount(request, accid):
    if request.method == 'POST':
        nm = request.POST.get('AccName')
        desc = request.POST.get('AccDesc')
        desc1 = request.POST.get('AccDesc1')
        try:
            img = request.FILES['AccImage']
            fs = FileSystemStorage()
            file = fs.save(img.name, img)
        except MultiValueDictKeyError:
            file = AccountDB.objects.get(id=accid).ACCIMAGE
        AccountDB.objects.filter(id=accid).update(ACCNAME=nm, ACCDESC=desc, ACCFULLDESC=desc1, ACCIMAGE=file)
        messages.success(request, "Account Updated Successfully")
        return redirect(displayAccount)

def deleteaccount(request, accid):
    account = AccountDB.objects.filter(id=accid)
    account.delete()
    messages.error(request, "Account is Deleted")
    return redirect(displayAccount)

def addaccounttype(request):
    account = AccountDB.objects.all()
    return render(request, 'AddAccountType.html', {'account':account})

def typesave(request):
    if request.method == 'POST':
        accnm = request.POST.get('AccName')
        tynm = request.POST.get('TypeName')
        tydesc1 = request.POST.get('TypeDesc1')
        tydesc2 = request.POST.get('TypeDesc2')
        typeimg = request.FILES['TypeImage']
        obj = AccountTypeDB(ACCOUNT=accnm, ACCOUNTTYPE=tynm, SHORTDESC=tydesc1, FULLDESC=tydesc2, TYPEIMAGE=typeimg)
        obj.save()
        messages.success(request, "Account Type Saved Successfully")
        return redirect(addaccounttype)


def displayaccounttype(request):
    accounttype = AccountTypeDB.objects.all()
    return render(request, 'DisplayAccountType.html', {'accounttype':accounttype})

def editaccounttype(request, typeid):
    accounttype = AccountTypeDB.objects.get(id=typeid)
    account = AccountDB.objects.all()
    return render(request, 'EditAccountType.html', {'accounttype':accounttype,'account':account})

def typeupdate(request, typeid):
    if request.method == 'POST':
        accnm = request.POST.get('AccName')
        tynm = request.POST.get('TypeName')
        tydesc1 = request.POST.get('TypeDesc1')
        tydesc2 = request.POST.get('TypeDesc2')
        try:
            typeimg = request.FILES['TypeImage']
            fs = FileSystemStorage()
            file = fs.save(typeimg.name, typeimg)
        except:
            file = AccountTypeDB.objects.get(id=typeid).TYPEIMAGE
        AccountTypeDB.objects.filter(id=typeid).update(ACCOUNT=accnm, ACCOUNTTYPE=tynm, SHORTDESC=tydesc1, FULLDESC=tydesc2,
                                 TYPEIMAGE=file)
        messages.success(request, "Account Type Updated Successfully")
        return redirect(displayaccounttype)

def deleteaccounttype(request, typeid):
    accounttype = AccountTypeDB.objects.filter(id=typeid)
    accounttype.delete()
    messages.error(request, "Product is Deleted")
    return redirect(displayaccounttype)

def approved_accounts(request):
    status = accountCreationDB.objects.values_list('status', flat=True)
    for i in status:
        if i == "Approved":
            approved_account = accountCreationDB.objects.filter(status=i)
            return render(request, "approved_accounts.html", {'approved_account': approved_account})
    else:
        messages.info(request, "You have No Approved Accounts")
        return redirect(indexpage)

def PendingAccountDisplay(request):
    status = accountCreationDB.objects.values_list('status', flat=True)
    for i in status:
        if i == "Pending":
            pending_acc = accountCreationDB.objects.filter(status=i)
            return render(request,"PendingAccountDetails.html", {'pending_acc':pending_acc})
    else:
        messages.info(request, "You have No Pending Accounts")
        return redirect(indexpage)

def deletecustomeraccount(request, accid):
    url = request.META.get("HTTP_REFERER")
    account = accountCreationDB.objects.filter(id=accid)
    account.delete()
    messages.error(request, "Customer Account Info Deleted")
    return redirect(url)

def approvecustomer(request, accid):
    account = accountCreationDB.objects.get(id=accid)
    return render(request, 'EditCustomerAccount.html', {'account': account})

def approve_account(request, accid):
        if request.method == 'POST':
            minimum_balance = request.POST.get('minimum_balance')
            account_numbers = accountCreationDB.objects.values_list('ACCNO', flat=True)
            accno = str(random.randint(10000000000, 99999999999))
            while accno in account_numbers:
                accno = str(random.randint(10000000000, 99999999999))
            accountCreationDB.objects.filter(id=accid).update(ACCNO=accno, MINBALANCE=minimum_balance, status='Approved')
            subject = "APEX BANK - Hello Customer.."
            message = "We are pleased to inform that Your Account has been activated. Kindly Check your Profile."
            email = accountCreationDB.objects.get(id=accid).EMAIL
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            return redirect(PendingAccountDisplay)

def blocked_accounts(request):
    blocked = UserRegistrationDb.objects.values_list('is_blocked', flat=True)
    for i in blocked:
        if i == True:
            blocked_ = UserRegistrationDb.objects.filter(is_blocked=i)
            return render(request,"blockedContactsDisplay.html", {'blocked_':blocked_})
    else:
        messages.info(request, "You have No Blocked Accounts")
        return redirect(indexpage)

def unblock(request):
    blocked = UserRegistrationDb.objects.values_list('is_blocked', flat=True)
    for i in blocked:
        if i == True:
            UserRegistrationDb.objects.filter(is_blocked=i).update(is_blocked=False, failed_login_attempts=0)
            messages.success(request, "You have Successfully Unblocked the Account")
            return redirect(blocked_accounts)

def add_loan(request):
    return render(request, 'AddLoans.html')

def save_loan(request):
    if request.method == "POST":
        loan_type = request.POST.get("loan_type")
        loan_desc = request.POST.get("loan_desc")
        loan_image = request.FILES["loan_image"]
        obj = LoanDb(type=loan_type, description=loan_desc, image=loan_image)
        obj.save()
        messages.success(request, "Your Loan is added successfully")
        return redirect(add_loan)


def loan_display(request):
    loan = LoanDb.objects.all()
    return render(request, 'LoanDisplay.html', {'loan':loan})

def loan_edit(request, loan_id):
    loan = LoanDb.objects.get(id=loan_id)
    return render(request, 'EditLoan.html',{'loan':loan})

def update_loan(request, loan_id):
    if request.method == "POST":
        loan_type = request.POST.get("loan_type")
        loan_desc = request.POST.get("loan_desc")
        try:
            loan_image = request.FILES["loan_image"]
            fs = FileSystemStorage()
            file = fs.save(loan_image.name, loan_image)
        except:
            file = LoanDb.objects.get(id=loan_id).image
        LoanDb.objects.filter(id=loan_id).update(type=loan_type, description=loan_desc, image=file)
        messages.success(request, "Your Loan is updated successfully")
        return redirect(loan_display)
    messages.info(request, "Your Loan is failed to update")
    return redirect(loan_display)

def delete_loan(request, loan_id):
    loan = LoanDb.objects.filter(id=loan_id)
    loan.delete()
    return redirect(loan_display)

def approved_loans(request):
    status = LoanSanctionDb.objects.values_list('status', flat=True)
    for i in status:
        if i == "Approved":
            approved_loan = LoanSanctionDb.objects.filter(status=i)
            return render(request, "Approved_LoansDisplay.html", {'approved_loan': approved_loan})
    else:
        messages.info(request, "You have No Approved Loans")
        return redirect(indexpage)

def pending_loans(request):
    status = LoanSanctionDb.objects.values_list('status', flat=True)
    for i in status:
        if i == "Pending":
            pending_loan = LoanSanctionDb.objects.filter(status=i)
            return render(request, "Pending_LoansDisplay.html", {'pending_loan': pending_loan})
    else:
        messages.info(request, "You have No Pending Loans")
        return redirect(indexpage)

def delete_userloan(request, loanid):
    url = request.META.get("HTTP_REFERER")
    loan = LoanSanctionDb.objects.filter(id=loanid)
    loan.delete()
    messages.error(request, "Customer Loan Info Deleted")
    return redirect(url)

def loan_sanction(request, loanid):
    loan = LoanSanctionDb.objects.get(id=loanid)
    return render(request, 'ApproveCustomerLoan.html', {'loan':loan})

def approve_loan(request, loanid):
    if request.method == 'POST':
        customer_id = request.session['id']
        balance = LoanSanctionDb.objects.get(id=loanid).BALANCE
        account = LoanSanctionDb.objects.get(id=loanid).ACCNO
        loan_amount = request.POST.get('amount')
        new_balance = int(balance) + int(loan_amount)
        accountCreationDB.objects.filter(ACCNO=account).update(MINBALANCE=new_balance)
        LoanSanctionDb.objects.filter(id=loanid).update(loanamount=loan_amount, BALANCE=new_balance,
                                                        status='Approved')
        obj = TransactionHistory(CUSTOMERID=customer_id, sender_accno='BANK ADMIN',
                                 receiver_accno=account, transfertype='Credit',
                                 amount_transferred=loan_amount, balance_amount=new_balance)
        obj.save()
        subject = "APEX BANK - Hello Customer.."
        message = "We are pleased to inform that Your Loan Amount has been credited to yourAccount. Kindly Check your Profile."
        email = LoanSanctionDb.objects.get(id=loanid).EMAIL
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        return redirect(pending_loans)
    else:
        return redirect(pending_loans)

def customer_review_display(request):
    review = ReviewRatingDb.objects.all()
    return render(request, 'review_display.html', {'review': review})

def delete_review(request, review_id):
    review = ReviewRatingDb.objects.get(id=review_id)
    review.delete()
    messages.success(request, "Review is Deleted successfully")
    return redirect(customer_review_display)

def addnews(request):
    return render(request, 'AddNews.html')

def save_news(request):
    if request.method == "POST":
        title_ = request.POST.get('title')
        short_desc = request.POST.get('short_desc')
        full_desc = request.POST.get('full_desc')
        image = request.FILES['image']
        obj = BankNews(title=title_, short_description=short_desc, full_description=full_desc, news_image=image)
        obj.save()
        messages.success(request, "News item is saved successfully")
        return redirect(addnews)
    else:
        messages.error(request, "Sorry, News item cannot be saved")
        return redirect(addnews)

def display_news(request):
    news = BankNews.objects.all()
    return render(request, 'DisplayNews.html', {'news': news})

def edit_news(request, news_id):
    news = BankNews.objects.get(id=news_id)
    return render(request, 'EditNews.html', {'news': news})

def update_news(request, news_id):
    if request.method == "POST":
        title_ = request.POST.get('title')
        short_desc = request.POST.get('short_desc')
        full_desc = request.POST.get('full_desc')
        try:
            image = request.FILES['image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
        except:
            file = BankNews.objects.get(id=news_id).news_image
        BankNews.objects.filter(id=news_id).update(title=title_, short_description=short_desc,
                                                   full_description=full_desc, news_image=file)
        messages.success(request, "News item is updated successfully")
        return redirect(display_news)
    return redirect(display_news)

def delete_news(request, news_id):
    news = BankNews.objects.filter(id=news_id)
    news.delete()
    messages.success(request, "News item is Deleted successfully")
    return redirect(display_news)

def customer_messages_display(request):
    message = CustomerMessages.objects.all()
    return render(request, 'customer_messages_display.html', {'message': message})


def delete_messages(request, message_id):
    message = CustomerMessages.objects.get(id=message_id)
    message.delete()
    messages.success(request, "Message is Deleted successfully")
    return redirect(customer_messages_display)





















