from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import LoginForm,RegisterForm
from .forms import ContactForm

def home_page(request):
    #print(request.session.get("cart_id","Unknown"))
    context = {
    "title":"Zambezistore.com",
    "content":"Welcome to Zambezistore"
    }
    return render(request,"home_page.html",context)

def about_page(request):
    context = {
    "title":"Zambezistore.com",
    "content": "About Zambezistore"

    }
    return render(request,"about_page.html",context)

def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context={
    "title":"Zambezistore",
    "content": "Contact us",
    "form":contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    """if request.method == "POST":
        print(request.POST.get('fullname'))
        print(request.POST.get('email'))
        print(request.POST.get('content'))"""
    return render(request,"contact/view.html",context)
