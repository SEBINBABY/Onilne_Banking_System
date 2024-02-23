from django.db import models


# Create your models here.
class UserRegistrationDb(models.Model):
    NAME = models.CharField(max_length=100, null=True, blank=True)
    EMAIL = models.EmailField(max_length=200, null=True, blank=True)
    MOBILE = models.CharField(max_length=200, null=True, blank=True)
    ADDRESS = models.CharField(max_length=600, null=True, blank=True)
    AADHAR = models.CharField(max_length=200, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    PASSWORD = models.CharField(max_length=100, null=True, blank=True)
    PROFILEMAGE = models.ImageField(upload_to='Images', null=True, blank=True)
    failed_login_attempts = models.IntegerField(default=0)
    is_blocked = models.BooleanField(default=False)


class accountCreationDB(models.Model):
    CUSTOMERID = models.IntegerField(null=True, blank=True)
    USERNAME = models.CharField(max_length=100, null=True, blank=True)
    EMAIL = models.EmailField(max_length=100, null=True, blank=True)
    ACCTYPE = models.CharField(max_length=100, null=True, blank=True)
    ACCNO = models.CharField(max_length=100, null=True, blank=True)
    MINBALANCE = models.IntegerField(null=True, blank=True)
    AADHAR = models.CharField(max_length=100, null=True, blank=True)
    MOBILE = models.CharField(max_length=100, null=True, blank=True)
    DATE = models.DateField(null=True, blank=True)
    ADDRESS = models.TextField(max_length=600, null=True, blank=True)
    CITY = models.CharField(max_length=100, null=True, blank=True)
    STATE = models.CharField(max_length=100, null=True, blank=True)
    COUNTRY = models.CharField(max_length=100, null=True, blank=True)
    IMAGE = models.ImageField(upload_to='Images', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)

class TransactionHistory(models.Model):
    created_at = models.DateField(auto_now_add=True)
    CUSTOMERID = models.IntegerField(null=True, blank=True)
    sender_accno = models.CharField(max_length=100, null=True, blank=True)
    receiver_accno = models.CharField(max_length=100, null=True, blank=True)
    transfertype = models.CharField(max_length=100, null=True, blank=True)
    amount_transferred = models.IntegerField(null=True, blank=True)
    balance_amount = models.IntegerField(null=True, blank=True)


class ReviewRatingDb(models.Model):
    customer = models.ForeignKey(UserRegistrationDb, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class LoanSanctionDb(models.Model):
    CUSTOMERID = models.IntegerField(null=True, blank=True)
    USERNAME = models.CharField(max_length=100, null=True, blank=True)
    EMAIL = models.EmailField(max_length=100, null=True, blank=True)
    LOANTYPE = models.CharField(max_length=100, null=True, blank=True)
    ACCNO = models.CharField(max_length=100, null=True, blank=True)
    BALANCE = models.IntegerField(null=True, blank=True)
    AADHAR = models.CharField(max_length=100, null=True, blank=True)
    MOBILE = models.CharField(max_length=100, null=True, blank=True)
    document = models.FileField(upload_to='pdfs', null=True, blank=True)
    IMAGE2 = models.ImageField(upload_to='Images', null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    loanamount=models.IntegerField(null=True, blank=True)

class CustomerMessages(models.Model):
    customer = models.ForeignKey(UserRegistrationDb, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=100, blank=True, null=True)
    message = models.CharField(max_length=100, blank=True, null=True)




