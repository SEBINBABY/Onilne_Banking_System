from Backend.models import LoanDb
from Frontend.models import ReviewRatingDb

def get_loan(request):
    loan = LoanDb.objects.all()
    context = {'loan': loan}
    return context




