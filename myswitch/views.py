from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
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
    if not (Rate.objects.all()):
        return initialization(request)
    #rateList = Rate.objects.all()
    #if rateList is None:
    #initialization()
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
    return render(request,'myswitch/home.html', context)


@login_required
def initialization(request):
    if request.method == 'POST':
        Rate.objects.bulk_create([
            # configuration of the US rate side
            Rate(unitRate=request.POST['usRate'], currency_from="US Dollar", rate_description="US to Gourdes"),
            # configuration of the CA rate side
            Rate(unitRate=request.POST['caRate'], currency_from="Canada Dollar", rate_description="CA to Gourdes"),
            # configuration of the EURO rate side
            Rate(unitRate=request.POST['euroRate'], currency_from="Euro", rate_description="EURO to Gourdes"),
            # configuration of the PESO rate side
            Rate(unitRate=request.POST['pesoRate'], currency_from="Peso", rate_description="PESO to Gourdes")
        ])
        return redirect(dashboard)
    if request.method == 'GET':
        return render(request, 'myswitch/rate_configuration.html')


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
        return render(request, 'myswitch/transaction.html', context)
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
        return render(request, 'myswitch/profile.html')


# support
@login_required
def support(request):
    return render(request, 'myswitch/support.html')

# view all transactions
@login_required
def transactions(request):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    transact = Transaction.objects.all()
    context = {'transaction':transact}
    return render(request, 'myswitch/transactions_all.html', context)


# view all users
@login_required
def userInfo(request):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    users = User.objects.all()
    context = {'users':users}
    return render(request, 'myswitch/users.html', context)


# edit user
@login_required
def usersProfile(request, user_id):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    user_person = User.objects.get(pk=user_id)
    if request.method == 'GET':
        context = {'person':user_person}
        return render(request, 'myswitch/user_profile.html', context)
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
    return render(request, 'myswitch/rates.html', context)

# change single rate
@login_required
def rateManagementSingle(request, rate_id):
    if not request.user.is_superuser:
        return "You are not allowed to be in this page"
    rate = get_object_or_404(Rate, pk=rate_id)
    if request.method == 'GET':
        context = {'rate':rate}
        return render(request, 'myswitch/rateModification.html', context)
    if request.method == 'POST':
        rate.unitRate = request.POST['unitRate']
        rate.save()
        return redirect(rateManagement)



# first view
@login_required        
def index(request):
    if not (Rate.objects.all()):
        return initialization(request)
    else:
        return redirect(dashboard)        


# check user credentials
def authenticateUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(dashboard)
        else:
            return HttpResponse("wrong login credentials")
    if request.method == 'GET':
        return render(request, 'registration/login.html')


# log user out
def logout_view(request):
    logout(request)
    return redirect(authenticateUser)
