# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Max ,Q, Sum
from django.contrib.auth.models import User
#from Automation.tcc.convert_function import *
#from Automation.tcc.functions import *
from django.contrib.auth import authenticate, login
#from Automation.tcc.forms import *
#from Automation.tcc.variable import *
from Automation.tcc.choices import *
from django.db.models import F
from django.contrib.auth.forms import AuthenticationForm
from Automation.tcc.models import *


def index1(request):
	title = get_object_or_404(Department, pk='1')
	address = get_object_or_404(Organisation, pk='1')
	#name = Organisation.objects.get('name')
	template = {'address':address,'title':title}
	if request.user.is_staff == 1 and request.user.is_active == 1 and request.user.is_superuser == 1:
		return render_to_response('index1.html',template,context_instance=RequestContext(request))
	elif request.user.is_staff == 1 and request.user.is_active == 1 and request.user.is_superuser == 0 :
		return render_to_response('index2.html', context_instance=RequestContext(request))
	else:
		return render_to_response('index3.html', context_instance=RequestContext(request))


def profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
		return render_to_response('tcc/new_client_ok.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		form = UserProfileForm()
	return render_to_response('tcc/new_client.html', {'form': form}, context_instance=RequestContext(request))

def performa(request):
	"""
	Detail Veiw of data
	"""
	user = User.objects.get(id=request.GET['id'])
	performa = UserProfile.objects.filter(user_id = user)	
     #   x
       # while(fulldetail=fulldetail)
        #    y=x++
	return render_to_response("tcc/detail.html", {'performa' : performa, 'user':user} )

def previous(request):
	if request.method == 'POST':
		form = PreviousForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
		return render_to_response('tcc/performa.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		form = ClientForm()
	return render_to_response('tcc/profile.html', {'form': form}, context_instance=RequestContext(request))

def catalog(request):
	from Automation.tcc.models import Lab
	lab = Lab.objects.all().order_by('code')
	return render_to_response('tcc/catalog.html', {'lab':lab,}, context_instance=RequestContext(request))

def field(request):
	from Automation.tcc.models import *
	lab = Lab.objects.get(id=request.GET['id'])
	#lab_id = request.lab
	field = Field.objects.filter(lab_id = lab)	
	return render_to_response('tcc/field.html', {'lab':lab,'field':field,'lab_id': lab.id}, context_instance=RequestContext(request))

def rate(request):
	from Automation.tcc.models import *
	field = Field.objects.get(id=request.GET['id'])
	test = Test.objects.filter(field_id = field)	
	return render_to_response('tcc/test.html', {'test':test,'field':field}, context_instance=RequestContext(request))




def add_job(request):
	from Automation.tcc.models import *
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	if request.method == 'POST':
		form = ClientJobForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			form.save()
			p = Auto_number(job_no = maxid)
			p.save()
		
		return render_to_response('tcc/clientjob_ok.html', {'form': form,'maxid':maxid,'test':test,'field':field}, context_instance=RequestContext(request))
	else:
		form = ClientJobForm()
		return render_to_response('tcc/clientjob.html', {'form': form,'maxid':maxid,}, context_instance=RequestContext(request))



