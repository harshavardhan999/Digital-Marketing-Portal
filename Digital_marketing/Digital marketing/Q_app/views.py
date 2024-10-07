
from django.shortcuts import render,redirect
from .models import clientdetails,person,requirements,user_report,logindetails
from django.db.models import Q
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
#from .models import requirements,clientdata,user_report
from django.core import serializers
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
import json
import mysql.connector
import matplotlib.pyplot as plt
import numpy as np
import os
from django.db.models.deletion import CASCADE
from django.db.models.base import Model

from django.contrib.auth.hashers import make_password, check_password
from .models import User
from django.utils import timezone
from datetime import timedelta
import random
import string
from django.core.mail import send_mail
from django.conf import settings
import io
import base64
# Create your views here.
#login super admin ,user and client
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import User
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import urllib.parse
from django.http import HttpResponse
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from django.shortcuts import render


def loginpage(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        global clientname
        clientname = request.POST.get('clientname')
        password = request.POST.get('password')
        if clientname=='superadmin' and password=='super':
            return redirect(homepage)
        
        elif clientname=='user' and password=='user':
            return redirect(userhomepage)
        else:
            try:
                users = User.objects.get(clientname=clientname)
            except User.DoesNotExist:
                messages.error(request, 'Invalid d  etails')
                return render(request, 'login.html')
            if check_password(password, users.password):
                # Passwords match, login successful
                logo=clientdetails.objects.filter(clientname=clientname)
                x=user_report.objects.filter(clientname=clientname)
                campaign_names= user_report.objects.filter(clientname=clientname).values_list('campaign_name').distinct()
                templist=[]
                for k in range(len(campaign_names)):
                    element = campaign_names[k][0]
                    templist.append(element)
                campaign_names = list(campaign_names)
                campaigns=user_report.objects.all()
                context={'x':x,'campaigns':campaigns,'campaign_names':templist,'logo':logo}
                return render(request, 'campaign.html',context)
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'login.html')

       


def campaign_details(request):
    if request.method == 'POST':
        global clientname
        logo = clientdetails.objects.filter(clientname=clientname)
        selected_campaign = request.POST.get('campaign_name')
        campaign = user_report.objects.filter(campaign_name=selected_campaign).order_by('date')
        labels = []
        impressions = []
        clicks = []
        for item in campaign:
            labels.append(item.date)
            impressions.append(item.no_of_impressions)
            clicks.append(item.no_of_clicks)
        x = np.arange(len(labels))
        width = 0.30
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width/2, impressions, width, label='Impressions')
        rects2 = ax.bar(x + width/2, clicks, width, label='Clicks')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        plt.ylabel('Count')
        plt.title('Impressions and Clicks by Date')
        plt.grid()
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        plt.close(fig)
        chart_url = base64.b64encode(buffer.getvalue()).decode('utf-8')
        campaign_names = user_report.objects.filter(clientname=clientname).values_list('campaign_name', flat=True).distinct()
        campaigns = user_report.objects.all()
        context = {'campaign': campaign, 'campaigns': campaigns, 'campaign_names': campaign_names, 'logo': logo, 'chart_url': f"data:image/png;base64,{chart_url}"}
        return render(request, 'campaign.html', context)
    else:
        campaign_names = user_report.objects.filter(clientname=clientname).values_list('campaign_name', flat=True).distinct()
        campaigns = user_report.objects.all()
        logo = clientdetails.objects.filter(clientname=clientname)
        context = {'campaign_names': campaign_names, 'campaigns': campaigns, 'logo': logo}
        return render(request, 'campaign.html', context)













# super admin homepage
def homepage(request):
    return render(request,'SAdmin_homepage.html')



# user home page
def userhomepage(request):
    return render(request,'User_Homepage.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email=request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        user = User(username=username, password=hashed_password,email=email)
        user.save()
        return redirect('login')
    return render(request, 'registration.html')


# client form
def upload_image(request):
    if request.method == 'GET':
        dat = clientdetails.objects.all().values()  # displaying the values that are before saved
        return render(request, 'SAdmin_ClientDetails.html', {'dat': dat})
    elif request.method == 'POST':
        clientname = request.POST['clientname']
        email = request.POST['email']
        password = request.POST['password']
        hashed_password = make_password(password)  # hash the password using make_password
        if User.objects.filter(Q(clientname=clientname) | Q(email=email)).exists():  # it checks client name and email are already registered or not
            messages.error(request, "Client Name or Email already registered !")
            return render(request, 'SAdmin_ClientDetails.html')
        else:
            data = dict()
            if "GET" == request.method:
                return render(request, 'SAdmin_ClientDetails.html', data)
            # process POST request
            files = request.FILES  # multivalued dict
            date = request.POST.get('date')
            image = files.get("image")
            instance_cd = clientdetails()
            instance_cd.clientname = clientname
            instance_cd.userid = request.POST.get('userid')
            instance_cd.password = request.POST.get('password')
            instance_cd.email = request.POST.get('email')
            instance_cd.date = date
            instance_cd.image = image
            instance_cd.save()

            instance_user = User()
            instance_user.clientname = clientname
            instance_user.email = email
            instance_user.password = hashed_password  # save hashed password
            instance_user.save()

            messages.success(request, "Form Submitted Successfully")
            return render(request, 'SAdmin_ClientDetails.html')







# view campaign requriements data
def taskdata(request):
    td=requirements.objects.all()
    return render(request,'SAdmin_Taskdata.html',{'td':td})



# campaign creation form
def taskcreation(request):
    
    if request.method=='GET':
        people = clientdetails.objects.all()
        return render(request,'taskcreation.html',{'people': people})
    
    elif request.method=='POST':
        people=requirements.objects.all().values()
        campaign_name=request.POST['campaign_name']
            
            
        if requirements.objects.filter(campaign_name=campaign_name).exists(): # it checks client name is already registered or not
            messages.error(request,"Campaign Name already registered !")  
            return render(request,'taskcreation.html',{'people': people})
        
   
        else:
            requirements(
                name=request.POST.get('name'),
                campaign_name=request.POST.get('campaign_name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                planned_impressions=request.POST.get('planned_impressions'),
                planned_cpm=request.POST.get('planned_cpm'),
                planned_cpc=request.POST.get('planned_cpc'),
                planned_cost=request.POST.get('planned_cost'),
                deptid_id=request.POST.get('deptid_id')
            ).save()
            messages.success(request,"Form Submitted Successfully")
            people = clientdetails.objects.all()
            return render(request,'taskcreation.html',{'people': people})




def taskcreation_user(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        return render(request,'taskcreation_user.html',{'people': people})
    
    elif request.method=='POST':
        people=requirements.objects.all().values()
        campaign_name=request.POST['campaign_name']
        if requirements.objects.filter(campaign_name=campaign_name).exists(): # it checks client name is already registered or not
            messages.error(request,"Campaign Name already registered !")  
            return render(request,'taskcreation_user.html',{'people': people})
        else:
            requirements(
                name=request.POST.get('name'),
                campaign_name=request.POST.get('campaign_name'),
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                planned_impressions=request.POST.get('planned_impressions'),
                planned_cpm=request.POST.get('planned_cpm'),
                planned_cpc=request.POST.get('planned_cpc'),
                planned_cost=request.POST.get('planned_cost'),
                deptid_id=request.POST.get('deptid_id')
            ).save()
            messages.success(request,"Form Submitted Successfully")
            people = clientdetails.objects.all()
            return render(request,'taskcreation_user.html',{'people': people})



# delete campaign req data 
def delete(request, id):
    td=requirements.objects.get(id=id)
    td.delete()
    return redirect("/taskdata")

# edit campaign req data
def edit(request, id):

    td=requirements.objects.get(id=id)
    return render(request,'edittaskdata.html',{'td':td})

#  campaign req data
def update(request, id):
    
    #people = Person.objects.get(id=id)
    #name=request.POST.get('name'),
    campaign_name=request.POST.get('campaign_name')
    start_date=request.POST.get('start_date')
    end_date=request.POST.get('end_date')
    planned_impressions=request.POST.get('planned_impressions')
    planned_cpm=request.POST.get('planned_cpm')
    planned_cpc=request.POST.get('planned_cpc')
    planned_cost=request.POST.get('planned_cost')
    deptid_id = request.POST.get('deptid_id')
    td=requirements.objects.get(id=id)

    #td.name=name
    
    td.campaign_name=campaign_name
    td.start_date=start_date
    td.end_date=end_date
    td.planned_impressions=planned_impressions
    td.planned_cpm=planned_cpm
    td.planned_cpc=planned_cpc
    td.planned_cost=planned_cost
    td.deptid_id=deptid_id
    td.save()
    return redirect(taskdata)
      

   


def reportdata(request):
    if request.method=="POST":
        datef=request.POST.get("datef")
        datet=request.POST.get("datet")
        queryset = user_report.objects.filter(date__range=[datef, datet])
        #rd=user_report.objects.all()
        return render(request,'searchresult.html',{'queryset':queryset})
    else:
        rd=user_report.objects.all()
        return render(request,'SAdmin_Reportdata.html',{'rd':rd})



def delete_report(request, id):
    rd=user_report.objects.get(id=id)
    rd.delete()
    return redirect("/reportdata")



def edit_report(request, id):    
    rd=user_report.objects.get(id=id)
    return render(request,'editreportdata.html',{'rd':rd})



def update_report(request, id):
    #people = Person.objects.get(id=id)
    #name=request.POST.get('name'),
    date=request.POST.get('date')
    no_of_impressions=request.POST.get('no_of_impressions')
    no_of_clicks=request.POST.get('no_of_clicks')
    cost_per_impressions=request.POST.get('cost_per_impressions')
    cost_per_click=request.POST.get('cost_per_click')
    total_cost_per_impressions=request.POST.get('total_cost_per_impressions')
    total_cost_per_click=request.POST.get('total_cost_per_click')
    cost_per_day=request.POST.get('cost_per_day')
    rd=user_report.objects.get(id=id)

    #td.name=name
    rd.date=date
    rd.no_of_impressions=no_of_impressions
    rd.no_of_clicks=no_of_clicks
    rd.cost_per_impressions=cost_per_impressions
    rd.cost_per_click=cost_per_click
    rd.total_cost_per_impressions=total_cost_per_impressions
    rd.total_cost_per_click=total_cost_per_click
    rd.cost_per_day=cost_per_day

    rd.save()
    return redirect(reportdata) 
    return render({'people': people})




def viewclientdetails(request):
    people=clientdetails.objects.all()
    #image=clientdetails.objects
    return render(request,'SAdmin_ViewClientDetails.html',{'people':people})


def delete_client(request, id):
    people=clientdetails.objects.get(id=id)
    people.delete()
    return redirect("/viewclientdetails")

def edit_client1(request, id):

    people=clientdetails.objects.get(id=id)
    return render(request,'edit3.html',{'people':people})

import os
def update_client(request, id):
    
    people=clientdetails.objects.get(id=id)
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(people.image) > 0:
                os.remove(people.image.path)
            people.image = request.FILES['image']
        people.clientname = request.POST.get('clientname')
        people.userid = request.POST.get('userid')
        people.password = request.POST.get('password')
        people.date=request.POST.get('date')
        people.save()
        #messages.success(request, "Product Updated Successfully")
        return redirect(viewclientdetails)    

    context = {'people':people}
    return render(request, 'SAdmin_ViewClientDetails.html', context)








def u_report(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        return render(request,'user_report.html',context)
    
    elif request.method=='POST':
        date=request.POST['date']
        if user_report.objects.filter(date=date).exists(): # it checks client name is already registered or not
            empcontext = requirements.objects.all()    
            context={'empcontext':empcontext}
            #people = clientdetails.objects.all()
            messages.error(request,"Given Date Already Registered !")  
            return render(request,'user_report.html',context)

    
        
        else:
            user_report(
                clientname=request.POST.get('hiddenclient'),
                campaign_name=request.POST.get('hiddencampaign'),
                date=request.POST.get('date'),
                no_of_impressions=request.POST.get('no_of_impressions'),
                no_of_clicks=request.POST.get('no_of_clicks'),
                cost_per_impressions=request.POST.get('cost_per_impressions'),
                cost_per_click=request.POST.get('cost_per_click'),
                total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
                total_cost_per_click=request.POST.get('total_cost_per_click'),
                cost_per_day=request.POST.get('cost_per_day')
            ).save()
            people = clientdetails.objects.all()
            #deptcontext = clientdetails.objects.all()
            empcontext = requirements.objects.all()    
            context={'people':people,'empcontext':empcontext}
            messages.success(request,'Form Submitted Successfully')
            return render(request,'user_report.html',context)


def report_user(request):
    if request.method=='GET':
        people = clientdetails.objects.all()
        #deptcontext = clientdetails.objects.all()
        empcontext = requirements.objects.all()    
        context={'people':people,'empcontext':empcontext}
        return render(request,'user_report_user.html',context)
    
    elif request.method=='POST':
        date=request.POST['date']
        if user_report.objects.filter(date=date).exists(): # it checks client name is already registered or not
            empcontext = requirements.objects.all()    
            context={'empcontext':empcontext}
            #people = clientdetails.objects.all()
            messages.error(request,"Given Date Already Registered !")  
            return render(request,'user_report_user.html',context)      
        else:
            user_report(
                clientname=request.POST.get('hiddenclient'),
                campaign_name=request.POST.get('hiddencampaign'),
                date=request.POST.get('date'),
                no_of_impressions=request.POST.get('no_of_impressions'),
                no_of_clicks=request.POST.get('no_of_clicks'),
                cost_per_impressions=request.POST.get('cost_per_impressions'),
                cost_per_click=request.POST.get('cost_per_click'),
                total_cost_per_impressions=request.POST.get('total_cost_per_impressions'),
                total_cost_per_click=request.POST.get('total_cost_per_click'),
                cost_per_day=request.POST.get('cost_per_day')
            ).save()
            people = clientdetails.objects.all()
            #deptcontext = clientdetails.objects.all()
            empcontext = requirements.objects.all()    
            context={'people':people,'empcontext':empcontext}
            messages.success(request,'Form Submitted Successfully')
            return render(request,'user_report_user.html',context)

from django.shortcuts import get_object_or_404
from datetime import datetime







def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'forgot_password.html', {'error': 'Email does not exist'})
        token = generate_unique_token()
        user.reset_password_token = token
        user.reset_password_expiration = timezone.now() + timedelta(minutes=15)
        user.save()
        send_reset_password_email(email, token)
        return render(request, 'forgot_password.html', {'success': '* Please check your email for instructions to reset your password.'})
    return render(request, 'forgot_password.html')



def reset_password(request, token):
    try:
        user = User.objects.get(reset_password_token=token, reset_password_expiration__gt=timezone.now())
    except User.DoesNotExist:
        return render(request, 'reset_password.html', {'error': 'Invalid or expired token'})
    if request.method == 'POST':
        password = request.POST.get('password')
        user.password = make_password(password)
        user.reset_password_token = None
        user.reset_password_expiration = None
        user.save()
        return redirect('login')
    return render(request, 'reset_password.html', {'token': token})





def generate_unique_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    while User.objects.filter(reset_password_token=token).exists():
        token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    return token







def send_reset_password_email(email, token):
    subject = 'Reset your password'
    message = f'Click the link below to reset your password:\n\n{settings.BASE_URL}/reset-password/{token}/'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)