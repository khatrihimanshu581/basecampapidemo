from django.shortcuts import render, redirect
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import requests
import json
from django.http import HttpResponse

#-----------------------------------------------------Home Page--------------------------------------------------------------------------------------
    
def home(request):
    global url_get_token
    global basecamp_url
    basecamp_url='https://3.basecampapi.com/3472788/'
    url_get_token='https://launchpad.37signals.com/authorization/token?type=refresh&refresh_token=BAhbB0kiAbB7ImNsaWVudF9pZCI6IjRmN2JmMzk1ZDI2N2QxNTVlYzIzMjkwMWFiMDFjOWYzNzA3ZTdjOGQiLCJleHBpcmVzX2F0IjoiMjAyNy0xMC0wNlQwODozNDozMFoiLCJ1c2VyX2lkcyI6WzMzNzI3MjU3XSwidmVyc2lvbiI6MSwiYXBpX2RlYWRib2x0IjoiMzJmNTBiYzM3MjBjNmZhMmQ3YmZjNTNmZjgxY2E5YTkifQY6BkVUSXU6CVRpbWUNyOQfwOMQ7okJOg1uYW5vX251bWkCtgI6DW5hbm9fZGVuaQY6DXN1Ym1pY3JvIgdpQDoJem9uZUkiCFVUQwY7AEY=--c16902993207ec5061e4e34219838451c8a6043d&client_id=4f7bf395d267d155ec232901ab01c9f3707e7c8d&redirect_uri=http://localhost:8000/&client_secret=41705073e60b79e94f5cca0c284103a8d6b102c8'

    return render(request, 'core/home.html')

#--------------------------------------------------------------Create A ToDolist--------------------------------------------------------------------------
def Create_ToDo(request):
    template = loader.get_template('core/Create_ToDo.html')
    Name=request.POST['name']
    descriptions=request.POST['descriptions']
    url= ''+url_get_token+''
    r = requests.post(''+url+'')
    access_token=json.loads(r.text)['access_token']
    url = ''+basecamp_url+'buckets/1190341/todosets/177952765/todolists.json'
    todo_list_header = {'Authorization': 'Bearer '+access_token+'',
                'Content-Type' :'application/json'}
    data = {"name": Name , "description": "<div><em>"+descriptions+"</em></div>"}
    response = requests.post(url, json=data, headers=todo_list_header)
    #return HttpResponse(response)
    return HttpResponse(template.render(request))
#------------------------------------------------------Upload File---------------------------------------------------------------------------------------------
def Upload_Files(request):
    url= ''+url_get_token+''
    r = requests.post(''+url+'')
    access_token=json.loads(r.text)['access_token']
    template = loader.get_template('core/Upload_Files.html')
    myfile = request.FILES['myfile']
    File_name=myfile.name
    File_size=myfile.size
    #if(File_size<10485760):
    content_type=myfile.content_type
    title=request.POST['title']
    url = ''+basecamp_url+'attachments.json?name='+File_name+''
    attechments_header = {
             'Authorization': 'Bearer '+access_token+'',
            'Content-Type': content_type , 'Content-Length': '999999' }
    r = requests.post(url, data=myfile, headers=attechments_header)
    attachable_sgid=json.loads(r.text)['attachable_sgid']
    url= ''+url_get_token+''
    r = requests.post(''+url+'')
    access_token=json.loads(r.text)['access_token']
    urls = ''+basecamp_url+'buckets/1190341/vaults/177952772/uploads.json'
    file_upload_header = {'Authorization': 'Bearer '+access_token+'',
                 'Content-Type' :'application/json'}
    data = {"attachable_sgid":attachable_sgid,"description":"<div><strong>"+title+"</strong></div>","base_name":""+title+""}
    responses = requests.post(urls, json=data, headers=file_upload_header)
    return HttpResponse(template.render(request))