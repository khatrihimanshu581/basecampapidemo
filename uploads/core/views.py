from django.shortcuts import render, redirect
from django.template import loader
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import requests
import json
from django.core import APISetting
from django.http import HttpResponse

#-----------------------------------------------------Home Page--------------------------------------------------------------------------------------

def home(request):
    return render(request, 'core/home.html')

#--------------------------------------------------------------Create A ToDolist--------------------------------------------------------------------------
def Create_ToDo(request):
    template = loader.get_template('core/Create_ToDo.html')
    Name=request.POST['name']
    descriptions=request.POST['descriptions']
    mysetting=APISetting()
    url=mysetting.authURL
    r = requests.post(''+url+'')
    access_token=json.loads(r.text)['access_token']
    url=mysetting.baseURl
    url = ""+url+"buckets/1190341/todosets/177952765/todolists.json"
    headers = {'Authorization': 'Bearer '+access_token+'',
                'Content-Type' :'application/json'}
    data = {"name": Name , "description": "<div><em>"+descriptions+"</em></div>"}
    response = requests.post(url, json=data, headers=headers)
    #return HttpResponse(response)
    return HttpResponse(template.render(request))
#------------------------------------------------------Upload File---------------------------------------------------------------------------------------------
def Upload_Files(request):
    mysetting=APISetting()
    authURL=mysetting.authURL
    baseURl=mysetting.baseURl
    r = requests.post(''+authURL+'')
    access_token=json.loads(r.text)['access_token']
    template = loader.get_template('core/Upload_Files.html')
    myfile = request.FILES['myfile']
    File_name=myfile.name
    File_size=myfile.size
    #if(File_size<10485760):
    content_type=myfile.content_type
    title=request.POST['title']
    url = ""+baseURl+"attachments.json?name="+File_name+""
    headers1 = {
             'Authorization': 'Bearer '+access_token+'',
            'Content-Type': content_type , 'Content-Length': '999999' }
    r = requests.post(url, data=myfile, headers=headers1)
    attachable_sgid=json.loads(r.text)['attachable_sgid']
    url= ''+authURL+''
    r = requests.post(''+authURL+'')
    access_token=json.loads(r.text)['access_token']
    urls = ""+baseURl+"/buckets/1190341/vaults/177952772/uploads.json"
    headers = {'Authorization': 'Bearer '+access_token+'',
                 'Content-Type' :'application/json'}
    data = {"attachable_sgid":attachable_sgid,"description":"<div><strong>"+title+"</strong></div>","base_name":""+title+""}
    responses = requests.post(urls, json=data, headers=headers)
    return HttpResponse(template.render(request))