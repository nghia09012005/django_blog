from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Member

def members(request):
    mymembers = Member.objects.all().values() #take a data value in modes (data in sql)
    template = loader.get_template('all_members.html') #load a html 
    context = {
        'mymembers': mymembers, 
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
    template = loader.get_template('myfirsthtml.html')
    mymembersssss = Member.objects.all().values()
    context = {
        'mymember':mymembersssss # mymember la ten bien con mymemberssssss la gia tri duoc load ra o tren 
    }
    return HttpResponse(template.render(context,request))