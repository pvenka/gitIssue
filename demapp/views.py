from django.shortcuts import render, HttpResponse
import requests
import json
import urllib
from dateutil import parser
import datetime
from collections import OrderedDict
# Create your views here.

def index(request):
	txts = '''Welcome to London transit API example.
		  You can see bus status.
                  Go to ./lineStatus.'''
	return HttpResponse(txts)


def lineStatus(request):
	parsedData = []
	dic = {}
	statd = {}
        if request.method == 'POST':
		busno = str(request.POST.get('busno'))
		url = 'https://api.tfl.gov.uk/Line/' + busno + '/Status?'
        	qstr = urllib.urlencode(OrderedDict([('detail','False'),('app_id','bd8c84b0'),('app_key','1dfcc5142ef4aa70f85a26af9bdd4a2f')]))
		url = url + qstr
		req = requests.get(url)
        	content = req.text
        	jsonl =  json.loads(content)
        	dic = jsonl[0]
		statd['line_no'] = dic['id']
	
		statd['status'] =  dic['lineStatuses'][0]['statusSeverityDescription']
        	parsedData.append(statd)
	return render(request, 'demapp/lineStatus.html', {'data': parsedData})

def gitIssues(request):
	times = []
	alldict = {}
	alldat = []
        global issue
	if request.method == 'POST':
		git_rep = str(request.POST.get('gits'))
		git_repo = str(request.POST.get('repo'))
		url = 'https://api.github.com/repos/' + git_rep +'/'+git_repo+'/issues?'
		qstr = urllib.urlencode({'status':'open'})
		url = url+qstr
		req = requests.get(url)
		r = req.text
		issue = json.loads(r)
		today = datetime.datetime.today()
		for item in issue:
        		diff = today-datetime.datetime.strptime(item["created_at"],'%Y-%m-%dT%H:%M:%SZ')
        		times.append((diff.days))
		ltday = 0
		ltweek = 0
		mtweek = 0
		for i in times:
        		if i < 1:
          			ltday = ltday +1
        		elif (i >= 1 and i <7):
          			ltweek = ltweek + 1
        		else:
          			mtweek = mtweek +1
	        #alldat.append(ltday)
		#alldat.append(ltweek)
		#alldat.append(mtweek)
		alldict["less_than_a_day"] = ltday
		alldict["less_than_a_week"] = ltweek
		alldict["more_than_a_week"] = mtweek
		alldat.append(alldict)
	return render(request,'demapp/gitIssues.html', {'data':alldat})

	