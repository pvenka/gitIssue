from django.shortcuts import render, HttpResponse
import requests
import json
# Create your views here.

def index(request):
	return HttpResponse('Welcome to London transit API example!')


def lineStatus(request):
        req = requests.get('https://api.tfl.gov.uk/Line/411/Status?detail=False&app_id=a56ee583&app_key=2ca63239341edd711a21a3a28234bcd4')
        content = req.text
	statd = {}
	parsedData = []
        jsonl =  json.loads(content)
        dic = jsonl[0]
        statd['line_no'] = dic['id']
	
	statd['status'] =  dic['lineStatuses'][0]['statusSeverityDescription']
        parsedData.append(statd)
	return HttpResponse(parsedData)
