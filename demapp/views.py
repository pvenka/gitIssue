from django.shortcuts import render, HttpResponse
import requests
import json
import urllib
import datetime
# Create your views here.

def index(request):
	txts = '''Welcome to  git issue API example.
		  You can see issue status.
                  Go to ./gitIssues.'''
	return HttpResponse(txts)



def gitIssues(request):
	times = []
	alldict = {}
	alldat = []
	errdict = {}
	errs = []
        global issue
	issues = []
	if request.method == 'POST':
		git_rep = str(request.POST.get('gits'))
		git_repo = str(request.POST.get('repo'))
		url = 'https://api.github.com/repos/' + git_rep +'/'+git_repo+'/issues?'
		qstr = urllib.urlencode({'status':'open','per_page':100})
		url = url+qstr
		req = requests.get(url)
		if req.status_code ==200:
	
			r = requests.head(url=url)
			rd = requests.get(url)
			issue = json.loads(rd.text)
			for iss in issue:
        			issues.append(iss)
			while True :
        			if 'next' not in r.links:
                			break

        			urin = r.links['next']['url']
        			r = requests.head(url=urin)
        			rd = requests.get(urin)
        			issue = json.loads(rd.text)
        			for iss in issue:
                			issues.append(iss)


		#req = requests.get(url)
		#if req.status_code==200:
	#		r = req.text
               	#	issue = json.loads(r)
                	today = datetime.datetime.today()
                	for item in issues:
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
                	alldict["less_than_a_day"] = ltday
                	alldict["less_than_a_week"] = ltweek
                	alldict["more_than_a_week"] = mtweek
			alldict["all_total"] = ltday+ltweek+mtweek
                	alldat.append(alldict)
       	      #		return render(request,'demapp/gitIssues.html', {'data':alldat})
		else:
			errdict['err'] = req.status_code
			errs.append(errdict)

	return render(request,'demapp/gitIssues.html', {'data':alldat,'err':errs})
