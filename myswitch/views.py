from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
import logging

# import models
from .models import Rate, Transaction

logger = logging.getLogger(__name__)

# dashboard
@login_required
def dashboard(request):
    #rateList = Rate.objects.all()
    #output = ', '.join([q.rateItems for q in rateList])
    dollar_unit = get_object_or_404(Rate, currency_from="US Dollar")
    peso_unit = get_object_or_404(Rate, currency_from="Peso")
    euro_unit = get_object_or_404(Rate, currency_from="Euro")
    canada_unit = get_object_or_404(Rate, currency_from="Canada Dollar")
    user_transfer = Transaction.objects.all().filter(transfer_by = request.user,
                                                     transfer_Date = timezone.now())
    context = {'dollar':dollar_unit, 'peso':peso_unit,
               'euro':euro_unit, 'canada':canada_unit,
               'transaction':user_transfer}
    return render(request,'transferApp/home.html', context)

# transfer
@login_required
def transfer(request):
    if request.method == 'GET':
        dollar_unit = get_object_or_404(Rate, currency_from="US Dollar")
        peso_unit = get_object_or_404(Rate, currency_from="Peso")
        euro_unit = get_object_or_404(Rate, currency_from="Euro")
        canada_unit = get_object_or_404(Rate, currency_from="Canada Dollar")
        context = {'dollar':dollar_unit, 'peso':peso_unit,
                   'euro':euro_unit, 'canada':canada_unit}
        return render(request, 'transferApp/transaction.html', context)
    elif request.method == 'POST':
        origin = request.POST["origingCurrency"]
        originAmount = request.POST["receiveAmount"]
        givenAmount = request.POST["giveAmount"]
        rate = request.POST["unitRate"]
        givenAmountVerification = float(rate) * float(originAmount)
        if givenAmountVerification != givenAmount:
            givenAmount = round(givenAmountVerification,2)
            logger.critical("amount differ from previous calculated amount")
        comment = request.POST["commentTransfer"]
        transfer_by = request.user
        transaction = Transaction(transfer_origin=origin,transfer_originAmount=originAmount,
                                  transfer_givenAmount=givenAmount, rate=rate,
                                  transfer_comment=comment, transfer_by = transfer_by)
        transaction.save()
        return redirect(dashboard)

# profile
@login_required
def profile(request):
    if request.method == 'POST':
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        user = User.objects.get(username=request.POST["username"])
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.save()
        return redirect(profile)
    elif request.method == 'GET':
        return render(request, 'transferApp/profile.html')


# support
@login_required
def support(request):
    return render(request, 'transferApp/support.html')

# view all transactions
@login_required
def transactions(request):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    transact = Transaction.objects.all()
    context = {'transaction':transact}
    return render(request, 'transferApp/transactions_all.html', context)


# view all users
@login_required
def userInfo(request):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'transferApp/users.html', context)


# edit user
@login_required
def usersProfile(request, user_id):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    user_person = User.objects.get(pk=user_id)
    if request.method == 'GET':
        context = {'person':user_person}
        return render(request, 'transferApp/user_profile.html', context)
    if request.method == 'POST':
        firstName = request.POST["firstName"]
        lastName = request.POST["lastName"]
        email = request.POST["email"]
        username = request.POST["username"]
        if request.POST["is_active"] == "True":
            user_person.is_active = True
        else:
            user_person.is_active = False
            
        if request.POST["is_super"] == "True":
            user_person.is_superuser = True
        else:
            user_person.is_superuser = False
            
        user_person.first_name = firstName
        user_person.last_name = lastName
        user_person.email = email
        user_person.username = username
        
        
        user_person.save()
        return redirect(userInfo)

# add rate
@login_required
def rateManagement(request):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    rate = Rate.objects.all()
    context = {'rates':rate}
    return render(request, 'transferApp/rates.html', context)

# change single rate
@login_required
def rateManagementSingle(request, rate_id):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    rate = get_object_or_404(Rate, pk=rate_id)
    if request.method == 'GET':
        context = {'rate':rate}
        return render(request, 'transferApp/rateModification.html', context)
    if request.method == 'POST':
        rate.unitRate = request.POST['unitRate']
        rate.save()
        return redirect(rateManagement)


    
        
def index(request):
    return HttpResponse("you are in the non tenant page")        
        
        



