from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from .forms import Rgp_entryForm
from .forms import Nrgp_entryForm
from .models import Rgp_entry
from .models import Nrgp_entry
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)
import datetime
from django.http import JsonResponse
import random
from django.conf import settings
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from mysite import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import User_rgp, Rgp_entry


# relative import of forms
# Create your views here.


def index(request):
    try:
        user = User_rgp.objects.get(email=request.session['email'])

        if user.usertype == "manager":
            request.session['email'] = user.email
            request.session['fname'] = user.fname
    # request.session['profile_pic']=user.profile_pic.url
            return render(request, 'in.html')
        else:
            request.session['email'] = user.email
            request.session['fname'] = user.fname
            # request.session['profile_pic']=user.profile_pic.url
            return render(request, 'in_operator.html')
    except:
        return render(request, 'index.html')


def validate_email(request):
    email = request.GET.get('email')
    data = {
        'is_taken': User_rgp.objects.filter(email__iexact=email).exists()
    }
    return JsonResponse(data)


def login(request):
    if request.method == "POST":
        try:
            user = User_rgp.objects.get(email=request.POST['email'])
            user = User_rgp.objects.get(
                email=request.POST['email'],
                password=request.POST['password']

            )
            if user.usertype == "manager":
                request.session['email'] = user.email
                request.session['fname'] = user.fname
            # request.session['profile_pic']=user.profile_pic.url
                return render(request, 'in.html')
            else:
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                # request.session['profile_pic']=user.profile_pic.url
                return render(request, 'in_operator.html')
        except:
            msg = "Email or Password is Incorrect"
            return render(request, 'login.html', {'msg': msg})
    else:
        return render(request, 'login.html')

# def visitor_login(request):
    # if request.method=="POST":
        # try:
        # user=User.objects.get(
        # email=request.POST['email'],
        # password=request.POST['password']

        # )
        # request.session['email']=user.email
        # request.session['fname']=user.fname
        # request.session['profile_pic']=user.profile_pic.url
        # return render(request,'visitor_in.html')
        # except:
        # msg="Email or Password is correct"
        # return render(request,'visitor_in.html',{'msg':msg})
    # else:
        # return render(request,'login.html')


def logout(request):
    try:
        del request.session['email']
        del request.session['fname']
        # del request.session['profile_pic']
        return render(request, 'login.html')
    except:
        return render(request, 'login.html')


@csrf_exempt
def rgp_signup(request):
    user=User_rgp.objects.get(email=request.session['email'])
    if request.method == "POST":
        descript=request.POST.getlist('desc')
        quantity=request.POST.getlist('qty')
        unit=request.POST.getlist('unit')
        for i in range(0,len(descript)):
            Rgp_entry.objects.create(
                    cpname=request.POST['cpname'],
                    spname=request.POST['spname'],
                    dpname=request.POST['dpname'],
                    desc=descript[i],
                    qty=quantity[i],
                    unit=unit[i],
                    remarks=request.POST['remarks'],
                )
            
        msg = "RGP Enrollment Successfully"
        return render(request, 'rgp_entry.html', {'msg': msg})

    else:
        msg = ""
        return render(request, 'rgp_entry.html', {'msg': msg})
    
def nrgp_signup(request):
    user=User_rgp.objects.get(email=request.session['email'])
    if request.method == "POST":
        descript = request.POST.getlist('desc')
        quantity = request.POST.getlist('qty')
        unit = request.POST.getlist('unit')
        for i in range(0, len(descript)):
            Nrgp_entry.objects.create(
                    cpname=request.POST['cpname'],
                    spname=request.POST['spname'],
                    desc=request.POST['desc'],
                    dpname=request.POST['dpname'],
                    unit=request.POST['unit'],
                    qty=request.POST['qty'],
                    remarks=request.POST['remarks'],
                )
            
        msg = "NRGP Enrollment Successfully"
        return render(request, 'nrgp_entry.html', {'msg': msg})

    else:
        msg = ""
        return render(request, 'nrgp_entry.html', {'msg': msg})


def back(request):
    user = User_rgp.objects.get(email=request.session['email'])
    if user.usertype == "manager":
        request.session['email'] = user.email
        request.session['fname'] = user.fname
        # request.session['profile_pic']=user.profile_pic.url
        return render(request, 'in.html')
    else:
        request.session['email'] = user.email
        request.session['fname'] = user.fname
        # request.session['profile_pic']=user.profile_pic.url
        return render(request, 'in_operator.html')
        # except:
        # msg="Email or Password is Incorrect"
        # return render(request,'in.html',{'msg':msg})

    # else:
        # return render(request,'visitor_in.html')
    # return render(request,'in.html')


def change_password(request):
    if request.method == "POST":
        user = User.objects.get(email=request.session['email'])
        if user.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['cnew_password']:
                user.password = request.POST['new_password']
                user.save()
                return redirect('logout')
            else:
                msg = "New password & Confirm New Password Does Not matched"
                return render(request, 'change_password.html', {'msg': msg})
        else:
            msg = "Old Password does Not Matched"
            return render(request, 'change_password.html', {'msg': msg})

    else:
        return render(request, 'change_password.html')


def new_password(request):
    email = request.POST['email']
    np = request.POST['new_password']
    cnp = request.POST['cnew_password']

    if np == cnp:
        user = User.objects.get(email=email)
        user.password = np
        user.save()
        msg = "Password Updated Successfully"
        return render(request, 'login.html', {'msg': msg})
    else:
        msg = "New Password & Confirm New Password Does Not Matched"
        return render(request, 'new_password.html', {'email': email, 'msg': msg})
    
def rgp_view(request):
    # if request.method=="POST":
    rgp_entrys=Rgp_entry.objects.filter(current_status="Entry")
    return render(request,'rgp_view.html' ,{'rgp_entrys':rgp_entrys})
    # else:
	# 	rgp_entrys=Rgp_entry.objects.all()#.order_by('-id')[:3]
	#     return render(request,'visitor_view.html' ,{'rgp_entrys':rgp_entrys})

def rgp_view_operator(request):
    # if request.method=="POST":
    rgp_entrys=Rgp_entry.objects.filter(current_status="Entry")
    return render(request,'rgp_view_operator.html' ,{'rgp_entrys':rgp_entrys})

def rgp_exit(request, pk):
    all_in_user = Rgp_entry.objects.filter(current_status="Entry")
    if request.method == "POST":
            rgp_entrys = Rgp_entry.objects.get(id=pk)
            rgp_entrys.current_status = "Exit"
            rgp_entrys.made_on = datetime.datetime.now()
            rgp_entrys.save()
            msg = "Exit Successfully"
            return render(request, 'rgp_view.html', {'msg': msg, 'rgp_entrys': all_in_user})
    else:
        return render(request, 'rgp_view.html', {'rgp_entrys': all_in_user})
    
def rgp_print(request, pk):
    user_detail = Rgp_entry.objects.get(id=pk)
    return render(request, 'rgp_print.html', {'user_det': user_detail})

def nrgp_view(request):
    # if request.method=="POST":
    nrgp_entrys=Nrgp_entry.objects.filter(current_status="Entry")
    return render(request,'nrgp_view.html' ,{'nrgp_entrys':nrgp_entrys})





def log_print(request, pk):
    user_detail = Rgp_entry.objects.get(id=pk)
    return render(request, 'log_print.html', {'user_det': user_detail})





def update_view(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Rgp_entry, Nrgp_entry, id=id)
    

    # pass the object as instance in form
    form = Rgp_entryForm , Nrgp_entry (request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+id)

    # add form dictionary to context
    context["form"] = form

    return render(request, "update_view.html", context)

# def update_view_nrgp(request, id):
#     # dictionary for initial data with
#     # field names as keys
#     context = {}

#     # fetch the object related to passed id
#     obj = get_object_or_404(Nrgp_entry, id=id)

#     # pass the object as instance in form
#     form = Nrgp_entryForm(request.POST or None, instance=obj)

#     # save the data from the form and
#     # redirect to detail_view
#     if form.is_valid():
#         form.save()
#         return HttpResponseRedirect("/"+id)

#     # add form dictionary to context
#     context["form"] = form

#     return render(request, "update_view_nrgp.html", context)





def send_email(request, pk):
    if request.method == "POST":
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        subject = 'RGP Details'
        message = f"Concern Person Name :- {rgp_entrys.cpname}\n Department Name :- {rgp_entrys.dpname}\n Service Provide Name:-{rgp_entrys.spname}\n Description :- {rgp_entrys.desc}\n Unit :- {rgp_entrys.unit}\n Quantity  :- {rgp_entrys.qty}\n Remarks  :- {rgp_entrys.remarks}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        send_mail(subject, message, email_from, recipient_list)
        msg = "E-Mail Sent Successfully"
        return render(request, 'send_email.html', {'rgp_entrys': rgp_entrys, 'msg': msg})
    else:
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        return render(request, 'send_email.html', {'rgp_entrys': rgp_entrys})


def rgp_search(request):
    if request.method == "POST":
        # try:
            # user_detail = Rgp_entry.objects.get(id=pk)
            # signups=Signup.objects.all()
            return render(request, 'register_rgp.html')
        # except:
            # msg = "Invalid RGP Number"
            # return render(request, 'rgp_search.html', {'msg': msg})
    else:
        return render(request, 'rgp_search.html')

def rgp_all(request):
    log_data = Rgp_entry.objects.all()  # .order_by('-id')[:3]
    return render(request, 'rgp_all.html', {'log_data': log_data})

def nrgp_all(request):
    log_data = Nrgp_entry.objects.all()  # .order_by('-id')[:3]
    return render(request, 'nrgp_all.html', {'log_data': log_data})


def nrgp_print(request, pk):
    user_detail = Nrgp_entry.objects.get(id=pk)
    return render(request, 'nrgp_print.html', {'user_det': user_detail})

def rgp_outward(request):
    if request.method=="POST":
       return render(request, 'rgp_outward.html')
    else:
      return render(request, 'rgp_outward.html')
        
def rgp_inward(request):
    if request.method=="POST":
       return render(request, 'rgp_inward.html')
    else:
      return render(request, 'rgp_inward.html')   

def nrgp_outward(request):
    if request.method=="POST":
       return render(request, 'nrgp_outward.html')
    else:
      return render(request, 'nrgp_outward.html')
    
def nrgp_view_operator(request):
    nrgp_entrys=Nrgp_entry.objects.filter(current_status="Entry")
    return render(request,'nrgp_view_operator.html' ,{'nrgp_entrys':nrgp_entrys})