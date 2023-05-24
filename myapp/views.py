from django.http import HttpResponse
import datetime
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
from django.utils import timezone
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from urllib.parse import quote

# relative import of forms
# Create your views here.


def index(request):
    try:
        user = User_rgp.objects.get(email=request.session['email'])

        if user.usertype == "manager":
            request.session['email'] = user.email
            request.session['fname'] = user.fname
            request.session['dname'] = user.department

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
            if user.usertype == "manager" or user.usertype == "verifier":
                request.session['email'] = user.email
                request.session['fname'] = user.fname
                request.session['dname'] = user.department
            # request.session['profile_pic']=user.profile_pic.url
                return render(request, 'in.html')
            elif user.usertype == "admin":
                return render(request, 'admin_page.html')
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
    user = User_rgp.objects.get(email=request.session['email'])
    if request.method == "POST":
        descript = request.POST.getlist('desc')
        quantity = request.POST.getlist('qty')
        unit = request.POST.getlist('unit')
        for i in range(0, len(descript)):
            series = serial_generate(request)
            Rgp_entry.objects.create(
                rgp_serial=series,
                rgp_created=user,
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


@csrf_exempt
def nrgp_signup(request):
    user = User_rgp.objects.get(email=request.session['email'])
    if request.method == "POST":
        main_series = main_series_generate(request)
        descript = request.POST.getlist('desc')
        quantity = request.POST.getlist('qty')
        unit = request.POST.getlist('unit')
        for i in range(0, len(descript)):
            series = serial_generate_nrgp(request)
            Nrgp_entry.objects.create(
                nrgp_main_serial=main_series,
                nrgp_serial=series,
                nrgp_created=user,
                cpname=request.POST['cpname'],
                spname=request.POST['spname'],
                dpname=request.POST['dpname'],
                desc=descript[i],
                qty=quantity[i],
                unit=unit[i],
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
        user = User_rgp.objects.get(email=request.session['email'])
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
    rgp_entrys = Rgp_entry.objects.filter(
        rgp_created__department=request.session['dname'], current_status="Entry")
    return render(request, 'rgp_view.html', {'rgp_entrys': rgp_entrys})


def rgp_view_operator(request):
    rgp_entrys = Rgp_entry.objects.filter(
        current_status="Entry", approve_status=True)
    return render(request, 'rgp_view_operator.html', {'rgp_entrys': rgp_entrys})


def rgp_exit(request, pk):
    all_in_user = Rgp_entry.objects.filter(
        current_status="Entry", rgp_created__department=request.session['dname'])
    if request.method == "POST":
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        rgp_entrys.current_status = "Exit"
        rgp_entrys.made_on = datetime.datetime.now()
        rgp_entrys.save()
        msg = "Exit Successfully"
        return render(request, 'rgp_view.html', {'msg': msg, 'rgp_entrys': all_in_user})
    else:
        return render(request, 'rgp_view.html', {'rgp_entrys': all_in_user})


def nrgp_exit(request, pk):
    all_in_user = Nrgp_entry.objects.filter(
        current_status="Entry", nrgp_created__department=request.session['dname'])
    if request.method == "POST":
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        nrgp_entrys.current_status = "Exit"
        nrgp_entrys.made_on = datetime.datetime.now()
        nrgp_entrys.save()
        msg = "Exit Successfully"
        return render(request, 'nrgp_view.html', {'msg': msg, 'nrgp_entrys': all_in_user})
    else:
        return render(request, 'nrgp_view.html', {'nrgp_entrys': all_in_user})


def rgp_print(request, pk):
    user_detail = Rgp_entry.objects.get(id=pk)
    return render(request, 'rgp_print.html', {'user_detail': user_detail})


def nrgp_view(request):
    # if request.method=="POST":
    nrgp_entrys = Nrgp_entry.objects.filter(
        nrgp_created__department=request.session['dname'], current_status="Entry")
    return render(request, 'nrgp_view.html', {'nrgp_entrys': nrgp_entrys})


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
    form = Rgp_entryForm, Nrgp_entry(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/"+id)

    # add form dictionary to context
    context["form"] = form

    return render(request, "update_view.html", context)


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


def nrgp_send_email(request, pk):
    if request.method == "POST":
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        subject = 'RGP Details'
        message = f"Concern Person Name :- {nrgp_entrys.cpname}\n Department Name :- {nrgp_entrys.dpname}\n Service Provide Name:-{nrgp_entrys.spname}\n Description :- {nrgp_entrys.desc}\n Unit :- {nrgp_entrys.unit}\n Quantity  :- {nrgp_entrys.qty}\n Remarks  :- {nrgp_entrys.remarks}"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        send_mail(subject, message, email_from, recipient_list)
        msg = "E-Mail Sent Successfully"
        return render(request, 'nrgp_send_email.html', {'nrgp_entrys': nrgp_entrys, 'msg': msg})
    else:
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        return render(request, 'nrgp_send_email.html', {'nrgp_entrys': nrgp_entrys})


def verify_link(request, ver, pk, status):
    rgp_data = Rgp_entry.objects.get(id=pk)
    verifier_per = User_rgp.objects.get(id=ver)
    rgp_data.verify_status = bool(status)
    if status == 1:
        rgp_data.rgp_verify_time = timezone.now()
        rgp_data.verifier = verifier_per
        rgp_data.save()
    elif status == 0:
        rgp_data.rgp_verify_time = None
        rgp_data.verifier = None
        rgp_data.save()
    return render(request, "index.html")


def nrgp_verify_link(request, ver, pk, status):
    rgp_data = Nrgp_entry.objects.get(id=pk)
    verifier_per = User_rgp.objects.get(id=ver)
    rgp_data.nrgp_verify_status = bool(status)
    if status == 1:
        rgp_data.nrgp_verify_time = timezone.now()
        rgp_data.nrgp_verifier = verifier_per
        rgp_data.save()
    elif status == 0:
        rgp_data.nrgp_verify_time = None
        rgp_data.nrgp_verifier = None
        rgp_data.save()
    return render(request, "index.html")


def nrgp_verify_link_all(request, ver, pk, status):
    all_data = Nrgp_entry.objects.filter(nrgp_main_serial=pk)
    verifier_per = User_rgp.objects.get(id=ver)
    for rgp_data in all_data:
        rgp_data.nrgp_verify_status = bool(status)
        if status == 1:
            rgp_data.nrgp_verify_time = timezone.now()
            rgp_data.nrgp_verifier = verifier_per
            rgp_data.save()
        elif status == 0:
            rgp_data.nrgp_verify_time = None
            rgp_data.nrgp_verifier = None
            rgp_data.save()
    return render(request, "index.html")


def send_email_verify(request, pk):
    user_data = User_rgp.objects.filter(
        usertype="verifier", department=request.session['dname'])
    # user_data = User_rgp.objects.all()
    if request.method == "POST":

        rgp_entrys = Rgp_entry.objects.get(id=pk)
        subject = 'RGP VERIFY'
        sel = User_rgp.objects.get(email=request.POST['email'])
        ver = sel.id
        verify = f"{request.get_host()}/verify_link/{ver}/{pk}/1"
        notverify = f"{request.get_host()}/verify_link/{ver}/{pk}/0"
        content = {
            "verify": verify,
            "notverify": notverify,
            "pname": rgp_entrys.cpname,
            "dname": rgp_entrys.dpname,
            "sname": rgp_entrys.spname,
            "desc": rgp_entrys.desc,
            "unit": rgp_entrys.unit,
            "qty": rgp_entrys.qty,
            "remarks": rgp_entrys.remarks,
            "va": "VERIFY",
            "va1": "NOT VERIFY"
        }

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        html_content = render_to_string(
            "rgp_verify.html", content)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject, text_content, email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()

        msg = "E-Mail Sent Successfully"
        return render(request, 'send_email_verify.html', {'rgp_entrys': rgp_entrys, 'msg': msg, 'user_data': user_data})
    else:
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        return render(request, 'send_email_verify.html', {'rgp_entrys': rgp_entrys, 'user_data': user_data})


def nrgp_send_email_verify(request, pk, vid):
    user_data = User_rgp.objects.filter(
        usertype="verifier", department=request.session['dname'])
    if request.method == "POST":
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        id_data = Nrgp_entry.objects.filter(nrgp_main_serial=vid)
        subject = 'NRGP VERIFY'
        sel = User_rgp.objects.get(email=request.POST['email'])
        ver = sel.id
        content = {}
        for i in id_data:
            verify = f"{request.get_host()}/nrgp_verify_link/{ver}/{i.id}/1"
            notverify = f"{request.get_host()}/nrgp_verify_link/{ver}/{i.id}/0"
            verify_all = f"{request.get_host()}/nrgp_verify_link_all/{ver}/{vid}/1"
            content.update({i.id: {"id": i.id,
                                   "verify": verify,
                                   "notverify": notverify,
                                   "verify_all": verify_all,
                                   "pname": i.cpname,
                                   "dname": i.dpname,
                                   "sname": i.spname,
                                   "desc": i.desc,
                                   "unit": i.unit,
                                   "qty": i.qty,
                                   "remarks": i.remarks,
                                   "va": "VERIFY",
                                   "va1": "NOT VERIFY"}
                            })
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        html_content = render_to_string(
            "nrgp_verify.html", {"content": content})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject, text_content, email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        msg = "E-Mail Sent Successfully"
        return render(request, 'nrgp_send_email_verify.html', {'nrgp_entrys': nrgp_entrys, 'msg': msg, 'user_data': user_data, "id_data": id_data})
    else:
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        return render(request, 'nrgp_send_email_verify.html', {'nrgp_entrys': nrgp_entrys, 'user_data': user_data})


def approve_link(request, apr, pk, status):
    rgp_data = Rgp_entry.objects.get(id=pk)
    apr_per = User_rgp.objects.get(id=apr)
    rgp_data.approve_status = bool(status)
    if status == 1:
        rgp_data.rgp_approve_time = timezone.now()
        rgp_data.approver = apr_per
        rgp_data.save()
    elif status == 0:
        rgp_data.rgp_approve_time = None
        rgp_data.approver = None
        rgp_data.save()
    return render(request, "index.html")


def nrgp_approve_link(request, apr, pk, status):
    rgp_data = Nrgp_entry.objects.get(id=pk)
    apr_per = User_rgp.objects.get(id=apr)
    rgp_data.nrgp_approve_status = bool(status)
    if status == 1:
        rgp_data.nrgp_approve_time = timezone.now()
        rgp_data.nrgp_approver = apr_per
        rgp_data.save()
    elif status == 0:
        rgp_data.nrgp_approve_time = None
        rgp_data.nrgp_approver = None
        rgp_data.save()
    return render(request, "index.html")


def nrgp_approve_link_all(request, apr, pk, status):
    all_data = Nrgp_entry.objects.filter(nrgp_main_serial=pk)
    apr_per = User_rgp.objects.get(id=apr)
    for rgp_data in all_data:
        rgp_data.nrgp_approve_status = bool(status)
        if status == 1:
            rgp_data.nrgp_approve_time = timezone.now()
            rgp_data.nrgp_approver = apr_per
            rgp_data.save()
        elif status == 0:
            rgp_data.nrgp_approve_time = None
            rgp_data.nrgp_approver = None
            rgp_data.save()
    return render(request, "index.html")


def send_email_approve(request, pk):
    user_data = User_rgp.objects.filter(
        usertype="approver")
    if request.method == "POST":
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        subject = 'RGP APPROVE'
        sel = User_rgp.objects.get(email=request.POST['email'])
        apr = sel.id
        verify = f"{request.get_host()}/approve_link/{apr}/{pk}/1"
        notverify = f"{request.get_host()}/approve_link/{apr}/{pk}/0"
        content = {
            "verify": verify,
            "notverify": notverify,
            "pname": rgp_entrys.cpname,
            "dname": rgp_entrys.dpname,
            "sname": rgp_entrys.spname,
            "desc": rgp_entrys.desc,
            "unit": rgp_entrys.unit,
            "qty": rgp_entrys.qty,
            "remarks": rgp_entrys.remarks,
            "va": "APPROVE",
            "va1": "NOT APPROVE"
        }

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        html_content = render_to_string(
            "rgp_verify.html", content)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject, text_content, email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        msg = "E-Mail Sent Successfully"
        return render(request, 'send_email_approve.html', {'rgp_entrys': rgp_entrys, 'msg': msg, 'user_data': user_data})
    else:
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        return render(request, 'send_email_approve.html', {'rgp_entrys': rgp_entrys, 'user_data': user_data})


def nrgp_send_email_approve(request, pk, vid):
    # user_data = User_rgp.objects.get(usertype="approver")
    # user_data = User_rgp.objects.all()
    user_data = User_rgp.objects.filter(
        usertype="approver")
    if request.method == "POST":
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        id_data = Nrgp_entry.objects.filter(nrgp_main_serial=vid)
        subject = 'NRGP APPROVE'
        sel = User_rgp.objects.get(email=request.POST['email'])
        apr = sel.id
        content = {}
        for i in id_data:
            verify = f"{request.get_host()}/nrgp_approve_link/{apr}/{i.id}/1"
            notverify = f"{request.get_host()}/nrgp_approve_link/{apr}/{i.id}/0"
            verify_all = f"{request.get_host()}/nrgp_approve_link_all/{apr}/{vid}/1"
            content.update({i.id: {
                "id": i.id,
                "verify": verify,
                "notverify": notverify,
                "verify_all": verify_all,
                "pname": i.cpname,
                "dname": i.dpname,
                "sname": i.spname,
                "desc": i.desc,
                "unit": i.unit,
                "qty": i.qty,
                "remarks": i.remarks,
                "va": "APPROVE",
                "va1": "NOT APPROVE"
            }})
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [request.POST['email']]
        html_content = render_to_string(
            "nrgp_approve.html", {"content": content})
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject, text_content, email_from, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()
        msg = "E-Mail Sent Successfully"
        approver_email = User_rgp.objects.get(email=request.POST['email'])
        nrgp_entrys.nrgp_approver = approver_email
        nrgp_entrys.save()
        return render(request, 'nrgp_send_email_approve.html', {'nrgp_entrys': nrgp_entrys, 'msg': msg, 'user_data': user_data})
    else:
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        return render(request, 'nrgp_send_email_approve.html', {'nrgp_entrys': nrgp_entrys, 'user_data': user_data})


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
    log_data = Rgp_entry.objects.filter(
        rgp_created__department=request.session['dname'])  # .order_by('-id')[:3]
    return render(request, 'rgp_all.html', {'log_data': log_data})


def nrgp_all(request):
    log_data = Nrgp_entry.objects.filter(
        nrgp_created__department=request.session['dname'])  # .order_by('-id')[:3]
    return render(request, 'nrgp_all.html', {'log_data': log_data})


def nrgp_print(request, pk):
    user_detail = Nrgp_entry.objects.filter(nrgp_main_serial=pk)
    single_data = Nrgp_entry.objects.filter(nrgp_main_serial=pk).last()

    return render(request, 'nrgp_print.html', {'user_detail': user_detail, "single_data": single_data})


def rgp_outward(request, pk):
    if request.method == "POST":
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        user = User_rgp.objects.get(email=request.session['email'])
        rgp_entrys.outward_sender = user
        rgp_entrys.outward_status = True
        rgp_entrys.outward_mode = request.POST['tmode']
        rgp_entrys.outward_reciever_name = request.POST['rname']
        rgp_entrys.rgp_outward_time = timezone.now()
        rgp_entrys.save()
        msg = "RGP product Outward successfully"
        return render(request, 'rgp_outward.html', {'rgp_entrys': rgp_entrys, 'msg': msg})
    else:
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        return render(request, 'rgp_outward.html', {'rgp_entrys': rgp_entrys})


def nrgp_outward(request, pk):
    if request.method == "POST":
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        user = User_rgp.objects.get(email=request.session['email'])
        nrgp_entrys.nrgp_outward_sender = user
        nrgp_entrys.nrgp_outward_status = True
        nrgp_entrys.nrgp_outward_mode = request.POST['tmode']
        nrgp_entrys.nrgp_outward_reciever_name = request.POST['rname']
        nrgp_entrys.nrgp_outward_time = timezone.now()
        nrgp_entrys.save()
        msg = "NRGP product Outward successfully"
        return render(request, 'nrgp_outward.html', {'nrgp_entrys': nrgp_entrys, 'msg': msg})
    else:
        nrgp_entrys = Nrgp_entry.objects.get(id=pk)
        return render(request, 'nrgp_outward.html', {'nrgp_entrys': nrgp_entrys})


def rgp_inward(request, pk):
    if request.method == "POST":
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        user = User_rgp.objects.get(email=request.session['email'])
        rgp_entrys.inward_receiver = user
        rgp_entrys.inward_status = True
        rgp_entrys.outward_status = False
        rgp_entrys.inward_party_challan = request.POST['pcnumber']
        rgp_entrys.inward_mode = request.POST['vnumber']
        rgp_entrys.rgp_inward_time = timezone.now()
        rgp_entrys.save()
        msg = "RGP product Inward successfully"
        return render(request, 'rgp_inward.html', {'rgp_entrys': rgp_entrys, 'msg': msg})
    else:
        rgp_entrys = Rgp_entry.objects.get(id=pk)
        return render(request, 'rgp_inward.html', {'rgp_entrys': rgp_entrys})


def nrgp_view_operator(request):
    nrgp_entrys = Nrgp_entry.objects.filter(
        current_status="Entry", nrgp_approve_status=True)
    return render(request, 'nrgp_view_operator.html', {'nrgp_entrys': nrgp_entrys})


def serial_generate(request):
    now = datetime.datetime.now()
    try:
        latest = Rgp_entry.objects.last()
        var3 = latest.rgp_serial
        var4 = int(var3[:-5])+1
        return str(var4)+"-"+str(now.year)
    except:
        var3 = "1"+"-"+str(now.year)
        return var3


def main_series_generate(request):
    now = datetime.datetime.now()
    try:
        latest = Nrgp_entry.objects.last()
        var3 = latest.nrgp_main_serial
        var4 = int(var3)+1
        return str(var4)
    except:
        var3 = "1"
        return var3


def serial_generate_nrgp(request):
    now = datetime.datetime.now()
    try:
        latest = Nrgp_entry.objects.last()
        var3 = latest.nrgp_serial
        var4 = int(var3[:-5])+1
        return str(var4)+"-"+str(now.year)
    except:
        var3 = "1"+"-"+str(now.year)
        return var3
