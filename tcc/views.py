# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Max ,Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from Automation.tcc.choices import *
from django.db.models import F
from django.contrib.auth.forms import AuthenticationForm
from Automation.tcc.models import *
from django import template
from Automation.tcc.functions import *
from Automation.tcc.convert_function import *
from tagging.models import Tag, TaggedItem
#from cart import Cart
from django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_page
from gmapi import maps
from gmapi.forms.widgets import GoogleMap

register = template.Library()

@register.inclusion_tag("field_test_select.html")
def material_test_select(request):
    material_list = Material.objects.all()
    testID = Test.objects.all()

    return render_to_response('field_test_select.html', {'material_list' : material_list,'testID':testID}, context_instance=RequestContext(request))

@login_required
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


@login_required
def profile(request):
	if request.method == 'POST':
		form = UserProfileForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			pro = form.save(commit=False)
			pro.user = request.user
			pro.save()
			form.save()
		return render_to_response('tcc/new_client_ok.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		form = UserProfileForm()
	return render_to_response('tcc/new_client.html', {'form': form}, context_instance=RequestContext(request))

@login_required
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

@login_required
def previous(request):
	title = get_object_or_404(Department, pk='1')
	client = request.user
	job = ClientJob.objects.all().filter(client_id =client)
	return render_to_response('tcc/previous.html', {'job':job,'title':title}, context_instance=RequestContext(request))

@login_required
def catalog(request):
	lab = Lab.objects.all().order_by('code')
	return render_to_response('tcc/catalog.html', {'lab':lab,}, context_instance=RequestContext(request))

@login_required
def material(request):
	#lab = Lab.objects.all().order_by('code')
	#lab = Lab.objects.get(id=request.GET['id'])
	#lab_id = request.lab
	material = Material.objects.all().order_by('name')
	return render_to_response('tcc/field.html', {'material':material}, context_instance=RequestContext(request))

@login_required
def rate(request):
	lab = Lab.objects.all().order_by('code')
        field = Material.objects.all()
	material = Material.objects.get(id=request.GET['id'])
	test = Test.objects.filter(material_id = material)
	return render_to_response('tcc/test.html', {'lab':lab,'test':test,'material':material,'field':field}, context_instance=RequestContext(request))

class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))


def displaymap(request):
    gmap = maps.Map(opts = {
        'center': maps.LatLng(38, -97),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 3,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('tcc/map.html', context)


@login_required
def all_tcc_fields(request, lab):
    lab = Lab.objects.get(id=lab)
    field = field.objects.all().filter(lab_id=field)
    tcc_fields = serializers.serialize("tcc", fields)
    return HttpResponse(tcc_fields, mimetype="application/javascript")

@login_required
def select(request):
	field_list = Material.objects.all()
	return render_to_response('tcc/tags.html',{'field_list':field_list}, context_instance=RequestContext(request))

@login_required
def selectcart(request):
	field_list = Material.objects.all()
	return render_to_response('tcc/tags1.html',{'field_list':field_list}, context_instance=RequestContext(request))

@login_required
def add_job(request):
	field_list = Material.objects.all()
	query =request.GET.get('q', '')
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	report = Report.objects.all()
	work = Govt.objects.all()
	payment = Payment.objects.all()
	material =Material.objects.get(id=request.GET['q'])
	test = Test.objects.all().filter(material_id = query)
	if request.method=='POST':
		form = ClientJobForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			site = cd['site']
			test = request.POST.getlist('test')
			selected_work = get_object_or_404(Govt, pk=request.POST.get('type_of_work'))
			selected_report = get_object_or_404(Report, pk=request.POST.get('report_type'))
			profile = form.save(commit=False)
			#request.session.save()
			profile.job_no = maxid
			mat =Material.objects.get(id=request.GET['q'])
			profile.material = mat
			profile.client = request.user
			profile.type_of_work = selected_work
			profile.report_type = selected_report
			profile.save()
        		form.save_m2m()
			mee = ClientJob.objects.aggregate(Max('id'))
			minid =mee['id__max']
			client = ClientJob.objects.get(id=minid)
			value = ClientJob.objects.values_list('test').filter(id=minid)
			values = Test.objects.values_list('cost',flat=True).filter(id__in = value)
			unit_price = sum(values)
			job_no = client.job_no
			mat = client.material_id
			if mat == 1 or mat == 2 or mat == 3 or mat == 4 or mat == 5 :
				type = "ROUTINE"
			else:
				type = "INSTITUTIONAL"
			p = TestTotal(unit_price=unit_price, job_no=job_no,mat=mat,type=type)
			p.save()
			from Automation.tcc.variable import *
			college_income = round(collegeincome * unit_price / 100.00)
			admin_charge = round(admincharge * unit_price / 100.00)
			temp =  unit_price - college_income - admin_charge
			ratio1 = ratio1(type)
			ratio2 = ratio2(type)
			consultancy_asst = round(ratio1 * temp / 100)
			development_fund = round(ratio2 * temp / 100)
			m = Amount(job_no = job_no ,unit_price=unit_price,development_fund=development_fund, college_income = 	college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst,)
			m.save()
			return render_to_response('tcc/job_submit.html',{'test':test,'site':site}, context_instance=RequestContext(request))
	else:
		form = ClientJobForm()
	return render_to_response('tcc/add_job.html', {"form": form,"test":test,"report":report,'field_list':field_list,'payment':payment,'work':work}, context_instance=RequestContext(request))
	
@login_required
def add_to_cart(request):
	field_list = Material.objects.all()
	query =request.GET.get('q', '')
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	report = Report.objects.all()
	work = Govt.objects.all()
	payment = Payment.objects.all()
	material =Material.objects.get(id=request.GET['q'])
	test = Test.objects.all().filter(material_id = query)
	if request.method=='POST':
		form = ClientJobForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			site = cd['site']
			type_of_work = cd['type_of_work']
			report_type = cd['report_type']
			test = request.POST.getlist('test')
			selected_work = get_object_or_404(Govt, pk=request.POST.get('type_of_work'))
			selected_report = get_object_or_404(Report, pk=request.POST.get('report_type'))
			profile = form.save(commit=False)
			#request.session.save()
			profile.job_no = maxid
			mat =Material.objects.get(id=request.GET['q'])
			profile.material = mat
			profile.client = request.user
			profile.type_of_work = selected_work
			profile.report_type = selected_report
			profile.save()
        		form.save_m2m()
			mee = ClientJob.objects.aggregate(Max('id'))
			minid =mee['id__max']
			client = ClientJob.objects.get(id=minid)
			value = ClientJob.objects.values_list('test').filter(id=minid)
			values = Test.objects.values_list('cost',flat=True).filter(id__in = value)
			unit_price = sum(values)
			job_no = client.job_no
			mat = client.material_id
			if mat == 1 or mat == 2 or mat == 3 or mat == 4 or mat == 5 :
				type = "ROUTINE"
			else:
				type = "INSTITUTIONAL"
			p = TestTotal(unit_price=unit_price, job_no=job_no,mat=mat,type=type)
			p.save()
			from Automation.tcc.variable import *
			college_income = round(collegeincome * unit_price / 100.00)
			admin_charge = round(admincharge * unit_price / 100.00)
			temp =  unit_price - college_income - admin_charge
			ratio1 = ratio1(type)
			ratio2 = ratio2(type)
			consultancy_asst = round(ratio1 * temp / 100)
			development_fund = round(ratio2 * temp / 100)
			m = Amount(job_no = job_no ,unit_price=unit_price,development_fund=development_fund, college_income = 	college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst,)
			m.save()
			return render_to_response('tcc/job_submit.html', context_instance=RequestContext(request))
	else:
  		form = ClientJobForm()
	return render_to_response('tcc/add_job2.html', {"form": form,"test":test,'field_list':field_list,'payment':payment,'work':work,"report":report}, context_instance=RequestContext(request))
	
@login_required
def sessioned(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	s = request.session['amt']

@login_required
def job_ok(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	job_no = maxid
	value = TestTotal.objects.values_list('unit_price',flat=True).filter(job_no=maxid)
	price = sum(value)
	from Automation.tcc.variable import *
	service_tax= round(servicetax *  price)
	education_tax = round(educationtax *  price)
	higher_education_tax = round(highereducationtax *  price)
	net_total =  price + higher_education_tax + education_tax + service_tax
	m = Bill(job_no = job_no, price = price, service_tax=service_tax, higher_education_tax=higher_education_tax,education_tax=education_tax,net_total=net_total)
	m.save()
	'''from Automation.tcc.variable import *
	test = TestTotal.objects.all().values_list('unit_price').filter(job_no =maxid)
	testid = TestTotal.objects.all().values_list('id').filter(job_no =maxid)
	for test in testid:
		if test	 == "ROUTINE":
			rou= TestTotal.objects.all().values_list('unit_price',flat=True).filter(type="ROUTINE").filter(job_no =maxid)
			unit_price == 0
			unit = sum(rou)
			unit_price = unit_price + unit
		else :
 			rou= TestTotal.objects.all().values_list('unit_price',flat=True).filter(type="INSTITUTIONAL").filter(job_no =maxid)
			unit_price == 0
			unit = sum(rou)
			unit_price = unit_price + unit
	college_income = round(collegeincome * unit_price / 100.00)
	admin_charge = round(admincharge * unit_price / 100.00)
	temp =  unit_price - college_income - admin_charge
	ratio1 = ratio1(type)
	ratio2 = ratio2(type)
	consultancy_asst = round(ratio1 * temp / 100)
	development_fund = round(ratio2 * temp / 100)
	n = Amount(job_no = job_no ,unit_price=unit_price,development_fund=development_fund, college_income = college_income, admin_charge=admin_charge, consultancy_asst=consultancy_asst,)
	n.save()'''
	return render_to_response('tcc/job_ok.html', {"maxid":maxid}, context_instance=RequestContext(request))


def test_calculation(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	client = ClientJob.objects.get(job_no=maxid)
	value = ClientJob.objects.values_list('test').filter(job_no=id)
	values = Test.objects.values_list('cost',flat=True).filter(id__in = value)
	amt = sum(values)
	job_no = client.job_no
	p = TestTotal(amt=amt, job_no=job_no)
	p.save()
	return render_to_response('tcc/new_client_ok.html', context_instance=RequestContext(request))
	

def tests(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	material = Material.objects.all()
	client = ClientJob.objects.values_list('material_id',flat=True).filter(job_no = maxid)

	if request.method == 'POST':
		#hmm = request.POST.getlist['tests']
		#profile_form = form_class(request.POST, instance=profile)
		form = MyForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			tests = Test.objects.filter(material_id = client)
			tests =cd['tests']
			#field = cd['field']
			form.save()
			return render_to_response('tcc/checktest.html', {'tests':tests,'material':material,}, context_instance=RequestContext(request))
	else:
		form = 	MyForm()
		return render_to_response('tcc/checktest.html', {'form': form,'maxid':maxid,}, context_instance=RequestContext(request))



def search(request):
    field_list = Material.objects.all()
    return render_to_response('tcc/tags.html',{'field_list':field_list}, context_instance=RequestContext(request))

def save_job(request):
	query =request.GET.get('q', '')
	material =Material.objects.get(id=request.GET['q'])
	test = Test.objects.all().filter(material_id = query)
	if request.method=='POST':
		form = JobForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			place = cd['place']
			test = request.POST.getlist('test')
			#form.save_m2m()
			#id = ClientJob.objects.aggregate(Max('job_no'))
			#maxid =id['job_no__max']
			#profile = form.save(commit=False)
			#request.session.save()
			#profile.material = material.name
			#profile.job_no = maxid
			#profile.client = request.user
			#profile.save()
			form.save()
       			#form.save_m2m()
			return render_to_response('tcc/save_job.html', {'form':form,'place':place,'test':test}, context_instance=RequestContext(request))
		
	else:
		form = JobForm()
	return render_to_response('tcc/search.html', {'form': form,"query": query,"test":test,"material":material,}, context_instance=RequestContext(request)) 


@login_required
def bill(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	job_no = maxid
	client = ClientJob.objects.all().values_list('client_id',flat=True).filter(job_no=job_no)
	clients = UserProfile.objects.all().values_list('name',flat=True).filter(user_id__in = client)
	site = ClientJob.objects.all().values_list('site',flat=True).filter(job_no=maxid)
	mat = ClientJob.objects.all().values_list('material_id',flat=True).filter(job_no=maxid)
	mate = Material.objects.all().values_list('name', flat=True).filter(id__in = mat)
	mates = TestTotal.objects.all().values_list('unit_price', flat=True).filter(job_no=maxid)
	from Automation.tcc.variable import *
	bill = Bill.objects.get(job_no=maxid)
	title = get_object_or_404(Department, pk='1')
	address = get_object_or_404(Organisation, pk='1')
	servicetaxprint = servicetaxprint
	educationtaxprint = educationtaxprint
	highereducationtaxprint = highereducationtaxprint
	net_total1 = bill.net_total
	net_total_eng = num2eng(net_total1)
	template = {'job_no': job_no ,'bill_no':bill.job_no,'net_total_eng':net_total_eng,'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'clients': clients,'bill':bill, 'title':title,
	'address':address,'mate':mate,'site':site,'mates':mates,'net_total1':net_total1}
	return render_to_response('tcc/bill.html', template , context_instance=RequestContext(request))

@login_required
def receipt_report(request):
	"""
	View the Receipt Data In Html format
	"""
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	job_no = maxid
	mates = TestTotal.objects.all().filter(job_no=maxid)
	client = ClientJob.objects.all().values_list('client_id',flat=True).filter(job_no=job_no)
	clients = UserProfile.objects.all().get(user_id__in = client)
	mat = ClientJob.objects.all().values_list('material_id',flat=True).filter(job_no=maxid)
	mate = Material.objects.all().filter(id__in = mat)
	bill = Bill.objects.get(job_no=job_no)
	title = get_object_or_404(Department, pk='1')
	address = get_object_or_404(Organisation, pk='1')
	net_total1 = bill.net_total
	net_total_eng = num2eng(net_total1)
	type = 'CASH'
	template = {'job_no': job_no ,'mate':mate, 'net_total_eng':net_total_eng,'type':type,'mates': mates,'title':title, 'address':address,'clients':clients}
	return render_to_response('tcc/receipt.html', template , context_instance=RequestContext(request))

def gen_report(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	job_no = maxid
	amt = Amount.objects.all().filter(job_no=maxid)
	return render_to_response('tcc/get_report.html', {'job_no':job_no,'amt':amt} , context_instance=RequestContext(request))	
	
@login_required	
def rep(request):
	from Automation.tcc.variable import *
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	job_no = maxid
	query =request.GET.get('id')
	client = TestTotal.objects.all().get(id =query)
	amount = Amount.objects.all().get(id =query)
	#user = ClientJob.objects.all().values_list('client_id',flat=True).filter(job_no=job_no)
	#clients = UserProfile.objects.all().values_list('name',flat=True).filter(user_id__in = user)
	#mat = ClientJob.objects.all().values_list('material_id',flat=True).filter(job_no=maxid)
	#mate = Material.objects.all().values_list('name', flat=True).filter(id__in = mat)
	user = ClientJob.objects.all().get(id=query)
	users = user.client_id
	clients = UserProfile.objects.all().get(user=users )
	cli = clients.name
	mat = user.material_id
	mate = Material.objects.all().get(id = mat)
	lab = mate.lab_id
	staff = Staff.objects.all().filter(lab_id = lab)
	title = get_object_or_404(Department, pk='1')
	address = get_object_or_404(Organisation, pk='1')
	con_type = client.type
	ratio1 = ratio1(con_type)
	ratio2 = ratio2(con_type)
	job_no = amount.job_no
	net_total1 = amount.unit_price
	net_total_eng = num2eng(net_total1)
	#teachers = Teachers.objects.all().filter(lab=lab).order_by('id')
	retrieve()
	template = {'job_no': job_no,'net_total_eng':net_total_eng,'title':title,'address':address, 'servicetaxprint':servicetaxprint,
	'highereducationtaxprint':highereducationtaxprint,'educationtaxprint':educationtaxprint,'client': client,'amount':amount,'con_type':con_type, 'ratio1':ratio1 ,'ratio2':ratio2,'collegeincome':collegeincome,'admincharge' : admincharge,'cli':cli,'mate':mate,'staff':staff, }
	return render_to_response('tcc/report.html', template , context_instance=RequestContext(request))

def remove_from_cart(request, product_id):
 product = Product.objects.get(id=product_id)
 cart = Cart(request)
 cart.remove(product)

def get_cart(request):
 return render_to_response('cart.html', dict(cart=Cart(request)))

@login_required
def tags(request):
	field_list = Material.objects.all()
	return render_to_response('tcc/tags.html',{'field_list':field_list}, context_instance=RequestContext(request))

def with_tag(request, tag, object_id=None, page=1):

    query_tag = Tag.objects.get(name=tag)
    entries = TaggedItem.objects.get_by_model(Material, query_tag)
    entries = entries.order_by('-id')
    return render_to_response('tcc/with_tag.html', dict(tag=tag, entries=entries))


def all_json_tests(request, field):
    fieldID = User.objects.get(fieldID=request.GET['fieldID'])
    testID = Test.objects.filter(field_id = fieldID)

    json_test = serializers.serialize("json", testID)
    return HttpResponse(json_test, mimetype="application/javascript")
def transport(request):
	"""
	View of Transport Bill
	"""
	if request.method == 'POST':
		form = TransportForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			job_no =cd['job_no']
			test_date =cd['test_date']
			kilometer =cd['kilometer']
			date =cd ['date']
			id = Transport.objects.aggregate(Max('id'))
			maxid =id['id__max']
			if maxid== None :
				maxid = 1
			else:
				maxid = maxid + 1
			bill_no = maxid
			#rate = cd ['rate']
			form.save()
			Transport.objects.filter(job_no = job_no).update( bill_no = maxid )
			data = {'job_no':job_no,'rate':rate, 'kilometer': kilometer,'bill_no':bill_no,'test_date':test_date}
			return render_to_response('tcc/trans.html', data,  context_instance=RequestContext(request))
	else:
		form = TransportForm()
	return render_to_response('tcc/client.html', {'form': form}, context_instance=RequestContext(request))
def transport_bill(request):
	"""
	Final Report of Transport Bill
	"""
	transport_old = Transport.objects.get(job_no=request.GET['job_no'])
	client = ClientJob.objects.get(job_no=request.GET['job_no'])
	kilometer = transport_old.kilometer
	temp = [0,0,0,0,0,0,0,0,0,0]
	range = kilometer.split(',')
	i=0
	while i < len(range):
		temp[i] = range[i]
		i+=1
	rate = transport_old.rate
	amount1 = int(temp[0])*rate
	amount2 = int(temp[1])*rate
	amount3 = int(temp[2])*rate
	amount4 = int(temp[3])*rate
	amount5 = int(temp[4])*rate
	amount6 = int(temp[5])*rate
	amount7 = int(temp[6])*rate
	amount8 = int(temp[7])*rate
	amount9 = int(temp[8])*rate
	amount10 = int(temp[9])*rate
	total = amount1 + amount2 + amount3 + amount4 + amount5 + amount6 + amount7 + amount8 + amount9 + amount10
	all_amounts = amount1,amount2,amount3,amount4,amount5,amount6,amount7,amount8,amount9,amount10
	Transport.objects.filter(job_no = transport_old.job_no).update( total = total, amounts = all_amounts )
	transport = Transport.objects.get(job_no=transport_old.job_no)
	title = get_object_or_404(Variable, pk='1')
	sub_title = get_object_or_404(Variable, pk='2')
	sign = get_object_or_404(Variable, pk='3')
	vehical_no = get_object_or_404(Variable, pk='4')
	template ={'transport':transport,'title':title,'sub_title':sub_title, 'vehical_no':vehical_no ,'client':client,'sign':sign}
	return render_to_response('tcc/transportbill.html', template , context_instance=RequestContext(request))



