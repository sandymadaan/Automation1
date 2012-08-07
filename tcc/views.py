# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
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
from django import template

register = template.Library()

@register.inclusion_tag("field_test_select.html")
def field_test_select(request):
    field_list = Field.objects.all()
    

    return render_to_response('field_test_select.html', {'field_list' : field_list}, context_instance=RequestContext(request))

def index1(request):
	title = get_object_or_404(Department, pk='1')
	address = get_object_or_404(Organisation, pk='1')
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	#name = Organisation.objects.get('name')
	template = {'address':address,'title':title,'maxid':maxid,}
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
	lab = Lab.objects.all().order_by('code')
	return render_to_response('tcc/catalog.html', {'lab':lab,}, context_instance=RequestContext(request))

def field(request):
	lab = Lab.objects.all().order_by('code')
	lab = Lab.objects.get(id=request.GET['id'])
	#lab_id = request.lab
	field = Field.objects.filter(lab_id = lab)	
	return render_to_response('tcc/field.html', {'lab':lab,'field':field,'lab_id': lab.id}, context_instance=RequestContext(request))

def rate(request):
	lab = Lab.objects.all().order_by('code')
	field = Field.objects.get(id=request.GET['id'])
	test = Test.objects.filter(field_id = field)	
	return render_to_response('tcc/test.html', {'lab':lab,'test':test,'field':field}, context_instance=RequestContext(request))

def all_tcc_fields(request, lab):
    lab = Lab.objects.get(id=lab)
    field = field.objects.all().filter(lab_id=field)
    tcc_fields = serializers.serialize("tcc", fields)
    return HttpResponse(tcc_fields, mimetype="application/javascript")


def add_job(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	
	if request.method == 'POST':
		form = ClientJobForm()
		form.filter_features(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			field =cd['field']
			date =cd ['date']
			site =cd ['site']
			type_of_work =cd ['type_of_work']
			letter_no =cd ['letter_no']
			letter_date =cd ['letter_date']
			form.save()
			p = Auto_number(job_no = maxid)
			p.save()

			#data = {'field':field,'date':date, 'site': site,'type_of_work':type_of_work,'letter_date':letter_date,'letter_no':letter_no,}
			return HttpResponse("%s" % form['material']) 
		
	else:
		form = ClientJobForm()
		return render_to_response('tcc/clientjob.html', {'form': form,'maxid':maxid,}, context_instance=RequestContext(request))

def tests(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	field = Field.objects.all()
	client = ClientJob.objects.values_list('field_id',flat=True).filter(job_no = maxid)
       
	if request.method == 'POST':
		#hmm = request.POST.getlist['tests']
		#profile_form = form_class(request.POST, instance=profile)
		form = MyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			tests = Test.objects.filter(field_id = client)
			tests =cd['tests']
			#field = cd['field']
			form.save()	
			return render_to_response('tcc/checktest.html', {'tests':tests,'field':field,}, context_instance=RequestContext(request))
	else:
		form = 	MyForm()
		return render_to_response('tcc/checktest.html', {'form': form,'maxid':maxid,}, context_instance=RequestContext(request))

def all_json_tests(request, field):
    fieldID = User.objects.get(fieldID=request.GET['fieldID'])
    testID = Test.objects.filter(field_id = fieldID)

    json_test = serializers.serialize("json", testID)
    return HttpResponse(json_test, mimetype="application/javascript")
