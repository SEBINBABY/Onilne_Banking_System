from django.shortcuts import render, redirect
from Frontend.models import UserRegistrationDb, accountCreationDB, TransactionHistory, ReviewRatingDb,LoanSanctionDb, CustomerMessages
from django.contrib import messages
from Backend.models import AccountDB, AccountTypeDB, LoanDb, BankNews
import random
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import cache_page


# Create your views here.
def home(request):
    review = ReviewRatingDb.objects.all()
    news = BankNews.objects.all()
    return render(request, "home.html", {'review':review, 'news':news})

def userloginsignup(request):
    return render(request, "userlogin.html")

def UserRegistrationDBsave(request):
    if request.method == "POST":
        nm = request.POST.get('UserName')
        email = request.POST.get('Email')
        mob = request.POST.get('Mobile')
        add = request.POST.get('Address')
        adhr = request.POST.get('Aadhar')
        dob = request.POST.get('DOB')
        pwd = request.POST.get('Password')
        pwd1 = request.POST.get('ConfirmPassword')
        img1 = request.FILES['Image']
        if pwd == pwd1:
            if UserRegistrationDb.objects.filter(EMAIL=email).exists():
                messages.info(request, "Email already exists")
                return redirect(userloginsignup)
            elif UserRegistrationDb.objects.filter(NAME=nm).exists():
                messages.info(request, "Username already exists")
                return redirect(userloginsignup)
            else:
                obj = UserRegistrationDb(NAME=nm, EMAIL=email, MOBILE=mob, ADDRESS=add, AADHAR=adhr,
                                         DOB=dob, PASSWORD=pwd, PROFILEMAGE=img1)
                obj.save()
                messages.success(request, "You have successfully Registered")
                return redirect(userloginsignup)
        else:
            messages.error(request, "Passwords doesnot match, SignUp Again")
            return redirect(userloginsignup)

def UserLogin(request):
    if request.method == "POST":
        unm = request.POST.get("LoginName")
        pwd = request.POST.get("LoginPassword")
        email = request.POST.get("LoginEmail")
        if UserRegistrationDb.objects.filter(EMAIL=email).exists():
            if UserRegistrationDb.objects.get(EMAIL=email).is_blocked:
                return render(request, 'lock_out.html')
            else:
                if UserRegistrationDb.objects.filter(NAME=unm, PASSWORD=pwd).exists():
                    UserRegistrationDb.objects.filter(NAME=unm).update(failed_login_attempts=0)
                    customerid = UserRegistrationDb.objects.get(NAME=unm).id
                    eml = UserRegistrationDb.objects.get(NAME=unm).EMAIL
                    request.session['NAME'] = unm
                    request.session['PASSWORD'] = pwd
                    request.session['id'] = customerid
                    request.session['EMAIL'] = eml
                    subject = "APEX BANK - Hello Customer.."
                    message = "You are logged into your account. If this is not you, please contact the toll-free number provided for assistance."
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [eml], fail_silently=False)
                    return redirect(home)
                else:
                    failed_attempts = UserRegistrationDb.objects.get(EMAIL=email).failed_login_attempts
                    failed_attempts += 1
                    UserRegistrationDb.objects.filter(EMAIL=email).update(failed_login_attempts=failed_attempts)
                    if failed_attempts >= 3:
                        UserRegistrationDb.objects.filter(EMAIL=email).update(is_blocked=True)
                    messages.error(request, "Invalid Username or Password")
                    return redirect(userloginsignup)
        else:
            messages.error(request, "Email doesnot exists")
            return redirect(userloginsignup)
    else:
        return redirect(userloginsignup)


@cache_page(60 * 10)
def forgot_password(request):
    return render(request, "Forgot_Password.html")

def recover_password(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        if UserRegistrationDb.objects.filter(EMAIL=email).exists():
            subject = "APEX BANK - Your Password"
            password = UserRegistrationDb.objects.get(EMAIL=email).PASSWORD
            message = password
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            messages.info(request, "Kindly check your Email for your Password")
            return redirect(userloginsignup)
        else:
            messages.info(request, "Sorry, This email doesnot exists ")
            return redirect(forgot_password)


def UserLogout(request):
    del request.session['NAME']
    del request.session['PASSWORD']
    return redirect(userloginsignup)

def accounts(request):
    account = AccountDB.objects.all()
    status = accountCreationDB.objects.filter(CUSTOMERID=request.session['id'])
    return render(request, 'accounts.html',{'account':account, 'status':status})

def accountSingle(request, accid, accname):
    account = AccountDB.objects.get(id=accid)
    accounttype = AccountTypeDB.objects.filter(ACCOUNT=accname)
    return render(request, 'accountSingle.html',{'account':account, 'accounttype':accounttype})

def creatACCPage(request,accname):
    accounttype = AccountTypeDB.objects.filter(ACCOUNT=accname)
    return render(request, 'creatACCPage.html', {'accounttype':accounttype})


def OTPPage(request):
    if request.method == 'POST':
        customerid = request.session['id']
        nm = request.POST.get('name')
        eml = request.POST.get('email')
        acctype = request.POST.get('accounttype')
        aadhr = request.POST.get('aadhar')
        mob = request.POST.get('mobile')
        dt = request.POST.get('date')
        add = request.POST.get('address')
        cty = request.POST.get('city')
        ste = request.POST.get('state')
        con = request.POST.get('country')
        img = request.FILES['image']
        obj = accountCreationDB(CUSTOMERID=customerid, USERNAME=nm, EMAIL=eml, ACCTYPE=acctype, MINBALANCE=0,
                              ACCNO='XXXXXXXXXXX',
                              AADHAR=aadhr, MOBILE=mob, DATE=dt, ADDRESS=add,CITY=cty, STATE=ste, COUNTRY=con,
                              IMAGE=img, status='Pending')
        obj.save()
        onetimepassword = random.randint(1000, 9999)
        request.session['onetimepassword'] = onetimepassword
        message = "Your OTP to create Account"
        send_mail(onetimepassword, message, settings.EMAIL_HOST_USER, [eml], fail_silently=False)
        return render(request, 'otpPage.html')
    else:
        return redirect(creatACCPage)


def otpverify(request):
    if request.method == 'POST':
        otp1 = request.POST.get('onetimepassword')
        otp2 = request.session.get('onetimepassword')
        if str(otp1) == str(otp2):
            messages.success(request, "Your Account will be activated in 48 hours. Thank You!")
            subject = "APEX BANK - Hello Customer.."
            message = "Thank You for choosing Apex Bank. Your Account will be activated in 48 Hours."
            eml = request.session['EMAIL']
            send_mail(subject, message, settings.EMAIL_HOST_USER, [eml], fail_silently=False)
            return redirect(home)
        else:
            messages.error(request, "Invalid OTP")
            return redirect(OTPPage)
    return redirect(OTPPage)

def accountstatus(request):
    data = UserRegistrationDb.objects.get(id=request.session['id'])
    status = accountCreationDB.objects.filter(CUSTOMERID=request.session['id'])
    return render(request, 'accountstatus.html', {'status': status, 'data':data})

def update_profile(request, userid):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('Email')
        mobile = request.POST.get('Mobile')
        address = request.POST.get('Address')
        oldpwd = request.POST.get('OldPassword')
        newpwd = request.POST.get('NewPassword')
        try:
            image = request.FILES['Image']
            fs = FileSystemStorage()
            file = fs.save(image.name, image)
        except:
            file = UserRegistrationDb.objects.get(id=userid).PROFILEMAGE
        password = UserRegistrationDb.objects.get(id=userid).PASSWORD
        if oldpwd == password:
            UserRegistrationDb.objects.filter(id=userid).update(NAME=name, EMAIL=email, MOBILE=mobile,
                                                                ADDRESS=address, PASSWORD=newpwd, PROFILEMAGE=file)
            messages.success(request,"Your data has been updated successfully")
            return redirect(accountstatus)
        else:
            messages.error(request, 'Entered an Incorrect Old Password')
            return redirect(accountstatus)
    return redirect(accountstatus)

def accounthistory(request, accid):
    accountno = accountCreationDB.objects.filter(id=accid)
    return render(request, 'ACCOUNTHISTORY.html', {'accountno':accountno})

def updatebalance(request, accid):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        customer_id = request.session['id']
        balance = accountCreationDB.objects.get(id=accid).MINBALANCE
        account = accountCreationDB.objects.get(id=accid).ACCNO
        deposit = request.POST.get('deposit')
        type = request.POST.get('transfertype')
        if type == "Deposit":
            if balance >= 1000000:
                messages.info(request, "Please Contact your Homebranch for deposits above Rs.1000000")
                return redirect(url)
            else:
                if int(deposit) > 500000:
                    messages.info(request, "Sorry You have exceeded the limit, Please Contact your Homebranch")
                    return redirect(url)
                else:
                    new_balance = int(balance) + int(deposit)
                    accountCreationDB.objects.filter(id=accid).update(MINBALANCE=new_balance)
                    obj = TransactionHistory(CUSTOMERID=customer_id, sender_accno=account,
                                                       receiver_accno='Self Account', transfertype='Deposit',
                                                       amount_transferred=deposit, balance_amount=new_balance)
                    obj.save()
                    subject = "APEX BANK - Hello Customer.You have deposited this amount."
                    message = deposit
                    email = accountCreationDB.objects.get(id=accid).EMAIL
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                    return redirect(url)
        elif type == "Withdrawal":
            if int(deposit) > balance:
                messages.info(request, "Sorry You have insufficient balance")
                return redirect(url)
            else:
                if int(deposit) > 50000:
                    messages.info(request, "Please Contact your Homebranch for withdrawals above Rs.50000")
                    return redirect(url)
                else:
                    new_balance = int(balance) - int(deposit)
                    accountCreationDB.objects.filter(id=accid).update(MINBALANCE=new_balance)
                    obj = TransactionHistory(CUSTOMERID=customer_id, sender_accno=account,
                                                       receiver_accno='Self Account', transfertype='Withdrawal',
                                                       amount_transferred=deposit, balance_amount=new_balance)
                    obj.save()
                    subject = "APEX BANK - Hello Customer.You have withdrawn this amount."
                    message = deposit
                    email = accountCreationDB.objects.get(id=accid).EMAIL
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                    return redirect(url)
        return redirect(url)

def transfermoney(request, accid):
    accountno = accountCreationDB.objects.filter(id=accid)
    return render(request, 'transfermoney.html', {'accountno':accountno})

def updatetransfer(request, accid):
    url = request.META.get("HTTP_REFERER")
    if request.method == "POST":
        customer_id = request.session['id']
        receiver_accno = request.POST.get('receiver')
        amount = request.POST.get('amount')
        sender_balance = accountCreationDB.objects.get(id=accid).MINBALANCE
        if int(amount) < int(sender_balance):
            try:
                with transaction.atomic():
                    account = accountCreationDB.objects.get(id=accid).ACCNO
                    new_balance = int(sender_balance) - int(amount)
                    accountCreationDB.objects.filter(id=accid).update(MINBALANCE=new_balance)
                    obj = TransactionHistory(CUSTOMERID=customer_id, sender_accno=account,
                                                   receiver_accno=receiver_accno, transfertype='Debit',
                                                   amount_transferred=amount, balance_amount=new_balance)
                    obj.save()
                    subject = "APEX BANK - Hello Customer.Your account has been debited with this amount."
                    message = amount
                    EMAIL1 = accountCreationDB.objects.get(id=accid).EMAIL
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [EMAIL1], fail_silently=False)
                    receiver_balance = accountCreationDB.objects.get(ACCNO=receiver_accno).MINBALANCE
                    receiver_id = accountCreationDB.objects.get(ACCNO=receiver_accno).CUSTOMERID
                    new_balance = int(receiver_balance) + int(amount)
                    accountCreationDB.objects.filter(ACCNO=receiver_accno).update(MINBALANCE=new_balance)
                    messages.success(request, "Your Transaction has been done successfully")
                    obj = TransactionHistory(CUSTOMERID= receiver_id, sender_accno=account,
                                                   receiver_accno=receiver_accno, transfertype='Credit',
                                                   amount_transferred=amount, balance_amount=new_balance)
                    obj.save()
                    subject = "APEX BANK - Hello Customer.Your account has been credited with this amount."
                    message = amount
                    EMAIL2 = accountCreationDB.objects.get(ACCNO=receiver_accno).EMAIL
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [EMAIL2], fail_silently=False)
                    return redirect(url)
            except Exception as e:
                print(e)
                messages.error(request, "Something Went Wrong!Please Check Receivers Account Number")
                return redirect(url)
        else:
            messages.error(request, "Something Went Wrong!Check whether sufficient Balance")
            return redirect(url)


def transactionhistory(request):
    account = TransactionHistory.objects.filter(CUSTOMERID=request.session['id'])
    return render(request, 'transactionhistory.html', {'account':account})

# @cache_page(60*10)
def rating_review(request):
    return render(request, 'rating_review.html')

def save_rating(request):
    if request.method == "POST":
        customer_id = request.session['id']
        customer_rating = request.POST.get('rating')
        customer_subject = request.POST.get('subject')
        customer_review = request.POST.get('review')
        obj_user = UserRegistrationDb.objects.get(id=customer_id)
        obj = ReviewRatingDb(customer=obj_user, rating=customer_rating, subject=customer_subject,
                           review=customer_review)
        obj.save()
        return redirect(rating_review)


def loans(request):
    return render(request, 'loans.html')

def loan_application(request):
    return render(request, 'loan_application.html')

def submit_loan_application(request):
    if request.method == "POST":
        customerid = request.session['id']
        accno = request.POST.get('accno')
        accounts = accountCreationDB.objects.values_list('ACCNO', flat=True)
        print(accounts)
        if accno in accounts:
            balance = accountCreationDB.objects.get(ACCNO=accno).MINBALANCE
            name = request.POST.get('name')
            email = request.POST.get('email')
            loantype = request.POST.get('loantype')
            aadhar = request.POST.get('aadhar')
            mobile = request.POST.get('mobile')
            pdf = request.FILES['pdf_file']
            img = request.FILES['image']
            obj = LoanSanctionDb(CUSTOMERID=customerid, USERNAME=name, EMAIL=email, LOANTYPE=loantype, ACCNO=accno,
                        BALANCE=balance, AADHAR=aadhar, MOBILE=mobile, document=pdf, IMAGE2=img, status='Pending',
                                 loanamount=0)
            obj.save()
            messages.success(request, "Your Loan Application has been submitted successfully.")
            subject = "APEX BANK - Hello Customer.."
            message = "Thank You for choosing Apex Bank. Your Loan Application will be reviewed Soon."
            eml = request.session['EMAIL']
            send_mail(subject, message, settings.EMAIL_HOST_USER, [eml], fail_silently=False)
            return redirect(loans)
        else:
            messages.error(request, "Pleas enter a valid account number")
            return redirect(loans)
    else:
        messages.error(request, "Something Went Wrong. Try Again")
        return redirect(loans)

def news_single(request, news_id):
    news = BankNews.objects.filter(id=news_id)
    return render(request, 'news_single.html', {'news': news})

def save_customer_messages(request):
    if request.method == "POST":
        customer_id = request.session['id']
        obj_user = UserRegistrationDb.objects.get(id=customer_id)
        email_ = request.POST.get('email')
        phone_no_ = request.POST.get('phone_no')
        message_ = request.POST.get('message')
        obj = CustomerMessages(customer=obj_user, email=email_, phone_number=phone_no_, message=message_)
        obj.save()
        messages.success(request, "Your message has been sent successfully")
        return redirect(rating_review)
    else:
        messages.error(request, "Your message is not sent")
        return redirect(rating_review)


def transaction_date_fetch(request):
    if request.method == "POST":
        from_date = request.POST.get('fromdate')
        to_date = request.POST.get('todate')
        try:
            on_date_history = TransactionHistory.objects.filter(CUSTOMERID=request.session['id'],
                                                               created_at__lte=to_date,
                                                      created_at__gte=from_date)
        except:
            on_date_history = None
        return render(request, 'date_filtered_transaction.html', {"on_date_history": on_date_history})
    else:
        messages.error(request, "Something went wrong! Please try again..")
        return redirect(transactionhistory)

def about_page(request):
    return render(request, 'About_Page.html')












