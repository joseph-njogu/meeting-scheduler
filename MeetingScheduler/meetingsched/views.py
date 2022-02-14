# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from faunadb import query as q
# import pytz
# from faunadb.objects import Ref
# from faunadb.client import FaunaClient
import hashlib
import datetime



# client = FaunaClient(secret="")
# indexes = client.query(q.paginate(q.indexes()))


def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        try:
            user = client.query(q.get(q.match(q.index("users_index"), username)))
            if hashlib.sha512(password.encode()).hexdigest() == user["data"]["password"]:
                request.session["user"] = {
                    "id": user["ref"].id(),
                    "username": user["data"]["username"]
                }
                return redirect("meetingsched:dashboard")
            else:
                raise Exception()
        except:
            messages.add_message(request, messages.INFO,"You have supplied invalid login credentials, please try again!", "danger")
            return redirect("meetingsched:login")
    return render(request,"login.html")

def create_meeting(request):
    if "user" in request.session:
        if request.method=="POST":
            name=request.POST.get("name")
            agenda=request.POST.get("description")
            time=request.POST.get("time")
            date=request.POST.get("date")
            try:
                user = client.query(q.get(q.match(q.index("events_index"), date,time)))
                messages.add_message(request, messages.INFO, 'An Event is already scheduled for the specified time.')
                return redirect("meetingsched:create-meeting")
            except:
                user = client.query(q.create(q.collection("Events"), {
                    "data": {
                        "name": name,
                        "agenda": agenda,
                        "time": time,
                        "date": date,
                        "user": request.session["user"]["username"],
                        "status": 'False',
                    }
                }))
                messages.add_message(request, messages.INFO, 'Meeting Scheduled Successfully.')
                return redirect("meetingsched:create-meeting")
        return render(request,"meet/create-meeting.html")
    else:
        return HttpResponseNotFound("Page not found")


def dashboard(request):
    if "user" in request.session:
        user=request.session["user"]["username"]
        context={"user":user}
        return render(request,"index.html",context)
    else:
        return HttpResponseNotFound("Page not found")

def today_meeting(request):
    if "user" in request.session:
        meetings=client.query(q.paginate(q.match(q.index("events_today_paginate"), request.session["user"]["username"],str(datetime.date.today()))))["data"]
        meetings_count=len(meetings)
        page_number = int(request.GET.get('page', 1))
        meeting = client.query(q.get(q.ref(q.collection("Events"), meetings[page_number-1].id())))["data"]
        if request.GET.get("complete"):
            client.query(q.update(q.ref(q.collection("Events"), meetings[page_number-1].id()),{"data": {"status": "True"}}))["data"]
            return redirect("meetingsched:today-meeting")
        if request.GET.get("delete"):
            client.query(q.delete(q.ref(q.collection("Events"), meetings[page_number-1].id())))
            return redirect("meetingsched:today-meeting")
        context={"count":meetings_count,"meeting":meeting,"page_num":page_number, "next_page": min(meetings_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request,"today-meeting.html",context)
    else:
        return HttpResponseNotFound("Page not found")


def all_meeting(request):
    if "user" in request.session:
        meetings=client.query(q.paginate(q.match(q.index("events_index_paginate"), request.session["user"]["username"])))["data"]
        meetings_count=len(meetings)
        page_number = int(request.GET.get('page', 1))
        meeting = client.query(q.get(q.ref(q.collection("Events"), meetings[page_number-1].id())))["data"]
        if request.GET.get("delete"):
            client.query(q.delete(q.ref(q.collection("Events"), meetings[page_number-1].id())))
            return redirect("meetingsched:all-meeting")
        context={"count":meetings_count,"meeting":meeting, "next_page": min(meetings_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request,"all-meetings.html",context)
    else:
        return HttpResponseNotFound("Page not found")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            user = client.query(q.get(q.match(q.index("users_index"), username)))
            messages.add_message(request, messages.INFO, 'User already exists with that username.')
            return redirect("meetingsched:register")
        except:
            user = client.query(q.create(q.collection("users"), {
                "data": {
                    "username": username,
                    "email": email,
                    "password": hashlib.sha512(password.encode()).hexdigest(),
                    "date": datetime.datetime.now(pytz.UTC)
                }
            }))
            messages.add_message(request, messages.INFO, 'Registration successful.')
            return redirect("meetingsched:login")
    return render(request,"user_register.html")
