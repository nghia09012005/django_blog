from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from home import models
from .import models
from django.conf import settings
from django.http import JsonResponse
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.contrib.auth.decorators import login_required

# api test
API_KEY = settings.YOUTUBE_API_KEY

def search_videos(request):
    # print(request)
    query = request.GET.get('q')  # Lấy từ khóa tìm kiếm từ query params
    try: 
        youtube = build('youtube', 'v3', developerKey=API_KEY)

        # Thực hiện tìm kiếm
        request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        maxResults=5
        )
        response = request.execute() #data

    # items = response.get('items')
    # for it in items:
    #     if it.get("snippet").get('channelTitle') == "Cảm Bóng Đá":
    #         print( True)
    #         break
        return response
    except HttpError as e:
        # print(f"An HTTP error occurred: {e}")
        return JsonResponse({"error": "Failed to connect to YouTube API."}, status=500)
######

# Create your views here.


def home(request):
    # query = request.GET.get('q', '')
    # if request.method == 'GET': 
    #     print(query)

    # valid = request.session.get('islogin', '')
    # print('---',valid)

    name = request.GET.get('name')
    template = loader.get_template('home.html')
    return render(request, 'home.html', {'name': name})
    # return render(request,'home.html')

def about(request):
    name = request.GET.get('name')
    template = loader.get_template('about.html')
    # return HttpResponse(template.render())
    return render(request,'about.html',{'name':name})



def contactme(request):

    if request.method == 'POST':
        # từ form trong contactme lấy ra information
        email = request.POST['email']
        name = request.POST['name']
        phone = request.POST['phone']
        dsr = request.POST['dsr']
        if email != '' and name != '' and phone != '':
            ins = models.contactme(name=name,email=email,phone=phone,dsr=dsr)
            ins.save()
           # print('data has store to db')
        else: 
           # print("fill full info plz")
           pass
    
    data = len(models.contactme.objects.all())

    
    # if request.method == 'GET':
    name = request.GET.get('name')
    # print(request)
    # print(name)

    template = loader.get_template('contactme.html')
    #return HttpResponse(template.render())
    return render(request,'contactme.html',{"data":data,'name':name})

def login(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        users = models.user.objects.all().values()
        for user in users:
            n = user['name']
            e = user['email']
            p = user['password']
            if n == name and e == email and password == p:
                # return render(request,'home.html')
                # request.session['islogin'] = True

                return HttpResponseRedirect(f'/home/?name={name}')
    template = loader.get_template('login.html')
    return render(request,'login.html')


def project(request):

    name = request.GET.get('name')
    # print(name)
    if request.method == 'GET':
        response = search_videos(request)
        #print(response)
        if isinstance(response, JsonResponse):
            return render(request,'project.html',{'name':name})
        
        # print(response)
        
        # print(request)
        find = request.GET.get('q')
        videolink = []
        channellink = []
        channeltitlelist = []
        viddsr = []
        thumb = []

        items = response.get('items')
        for it in items:
            
            channelid = it.get('id').get('channelId')
            channel_url = f'https://www.youtube.com/channel/{channelid}'
            channellink.append(channel_url)
            # print(channelid)

            video_id = it.get('id').get('videoId') 
            if video_id:
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                videolink.append(video_url)
            else:
                videolink.append('None')

            channeltitle = it.get("snippet").get('channelTitle')
            date = it.get("snippet").get('publishedAt')
            dsr =  it.get("snippet").get('description')
            thumbnails = it.get("snippet").get('thumbnails').get('medium').get('url')
            
            thumb.append(thumbnails)
            channeltitlelist.append(channeltitle)
            viddsr.append(dsr)

            # print(it.get("snippet").get('thumbnails'))
    template = loader.get_template('project.html')
    # return HttpResponse(template.render())

    # data = {'thumbnails':thumb,
    #         'channeltitile':channeltitlelist,
    #         'dsr':viddsr,
    #         'vidlink':videolink,
    #         'channellink':channellink
    #         }

    data = [
    (thumb[i], channeltitlelist[i], viddsr[i], videolink[i], channellink[i])
    for i in range(len(thumb))  # giả sử các danh sách có cùng độ dài
    ]

    return render(request,'project.html',{'data':data,'name':name})


def result(request):
    videourl =  []
    # videourl = [{'link': 'https://www.youtube.com/watch?v=link1'}, {'link': 'https://www.youtube.com/watch?v=link2'}]
    if request.method == 'GET':
        response = search_videos(request) 
        for item in response.get('items', []):  
            video_id = item.get('id', {}).get('videoId') 
            if video_id:  # Kiểm tra nếu videoId tồn tại
                video_url = f'https://www.youtube.com/watch?v={video_id}'
                videourl.append(video_url)
    
    template = loader.get_template('result.html')
    return render(request,'result.html',{'videourl':videourl})
    # return render(request,'result.html')