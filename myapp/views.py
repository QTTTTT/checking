# coding=utf8
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from myapp.models import *
# Create your views here.
import datetime


def index(request):
    return render(request, 'index.html')


def signup(request):
    state = ""
    if request.method == "POST":
        name = request.POST.get('name', '')
        identity = request.POST.get('identity', '')
        member = Member.objects.filter(name=name, identity=identity)
        if member.count() == 0:
            state = 'No one'
        elif Record.objects.filter(date=datetime.date.today(), member=member[0]).count() > 0:
            state = 'exist'
        else:
            new_record = Record(
                date=datetime.date.today(),
                first_time=datetime.datetime.now().time(),
                first_result=datetime.datetime.now().time() > datetime.time(9, 0),
                member=member[0],
            )
            new_record.save()
            new_user_object = UserObject(
                date=datetime.date.today(),
                up=True,
                member=member[0],
                record=new_record,
            )
            new_user_object.save()
            if new_record.first_result:
                state = 'late'
            else:
                state = 'normal'
    content = {
        'state': state,
    }
    return render(request, 'signup.html', content)


def signdown(request):
    state = ""
    if request.method == "POST":
        name = request.POST.get('name', '')
        identity = request.POST.get('identity', '')
        member = Member.objects.filter(name=name, identity=identity)
        if member.count() == 0:
            state = 'No one'
        elif Record.objects.filter(member=member[0], date=datetime.datetime.today()).count() == 0:
            state = "Not Signup"
        elif Record.objects.get(member=member[0], date=datetime.datetime.today()).second_time:
            state = "exist"
        else:
            record = Record.objects.get(member=member[0], date=datetime.datetime.today())
            record.second_time = datetime.datetime.now().time()
            record.second_result = datetime.datetime.now().time() < datetime.time(17, 0)
            record.save()
            if record.second_result:
                state = 'early'
            else:
                state = 'normal'
    content = {
        'state': state,
    }
    return render(request, 'signdown.html', content)


def query(request):
    state = ''
    if request.method == "POST":
        name = request.POST.get('name', '')
        identity = request.POST.get('identity', '')
        member = Member.objects.filter(name=name, identity=identity)
        if member.count() == 0:
            state = "No one"
        else:
            return detail(request, member[0])
    content = {
        'state': state,
    }
    return render(request, 'query.html', content)


def detail(request, member):
    day_list = [datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, i) for i in
                range(1, datetime.datetime.now().day + 1)]
    for day in day_list:
        print day
        if UserObject.objects.filter(date=day, member=member).count() == 0:

            new_user_object = UserObject(
                up=False,
                date=day,
                member=member,
            )
            new_user_object.save()

            try:
                record = Record.objects.get(date=day, member=member)
                new_user_object.record = record
                new_user_object.save()
            except:
                pass
    user_objects = UserObject.objects.filter(member=member).order_by('date')

    content = {
        'user_objects': user_objects,
    }
    return render(request, 'user.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse_lazy('all'))
    else:
        state = ""
        if request.method == "POST":
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect(reverse_lazy('all'))
            else:
                state = 'error'
        content = {'state': state}
        return render(request, 'login.html', content)


@login_required(login_url=reverse_lazy('login'))
def all(request):
    month = datetime.date.today().month
    for admin_object in AdminObject.objects.all():
        admin_object.delete()

    member_list = Member.objects.all()
    for member in member_list:
        up_days = Record.objects.filter(member=member, date__month=datetime.datetime.now().month).count()
        down_days = datetime.datetime.now().today().day - up_days
        late_times = Record.objects.filter(first_result=True, member=member).count()
        early_times = Record.objects.filter(second_result=True, member=member).count()
        admin_object = AdminObject(
            up_days=up_days,
            down_days=down_days,
            late_times=late_times,
            early_times=early_times,
            member=member,
        )
        admin_object.save()

    content = {
        'admin_objects': AdminObject.objects.all(),
        'month': month,
    }

    if request.method == "POST":
        identity = request.POST.get('identity')
        if Member.objects.filter(identity=identity).count() == 0:
            return HttpResponse("查无此人")
        AdminObject.objects.get(member__identity=identity).delete()
        up_days = Record.objects.filter(member=Member.objects.get(identity=identity),
                                        date__month=datetime.datetime.now().month).count()
        down_days = datetime.datetime.now().today().day - up_days
        late_times = Record.objects.filter(first_result=True, member=Member.objects.get(identity=identity)).count()
        early_times = Record.objects.filter(second_result=True, member=Member.objects.get(identity=identity)).count()
        admin_object = AdminObject(
            up_days=up_days,
            down_days=down_days,
            late_times=late_times,
            early_times=early_times,
            member=Member.objects.get(identity=identity),
        )
        admin_object.save()
        content = {
            'admin_objects': AdminObject.objects.filter(member=Member.objects.get(identity=identity)),
            'month': month,
        }

    return render(request, 'all.html', content)
