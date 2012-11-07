# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.db.models import Max ,Q, Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from Automation.tcc.choices import *
from django.db.models import F
from django.contrib.auth.forms import AuthenticationForm
from Automation.tcc.models import *
from django import template
from tagging.models import Tag, TaggedItem
from cart import Cart
from django.contrib.sessions.models import Session
from django.views.decorators.cache import cache_page

register = template.Library()

@register.inclusion_tag("field_test_select.html")
def material_test_select(request):
    material_list = Material.objects.all()
    testID = Test.objects.all()

    return render_to_response('field_test_select.html', {'material_list' : material_list,'testID':testID}, context_instance=RequestContext(request))

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

def material(request):
	#lab = Lab.objects.all().order_by('code')
	#lab = Lab.objects.get(id=request.GET['id'])
	#lab_id = request.lab
	material = Material.objects.all().order_by('name')	
	return render_to_response('tcc/field.html', {'material':material}, context_instance=RequestContext(request))

def rate(request):
	lab = Lab.objects.all().order_by('code')
        field = Material.objects.all()
	material = Material.objects.get(id=request.GET['id'])
	test = Test.objects.filter(material_id = material)	
	return render_to_response('tcc/test.html', {'lab':lab,'test':test,'material':material,'field':field}, context_instance=RequestContext(request))

def all_tcc_fields(request, lab):
    lab = Lab.objects.get(id=lab)
    field = field.objects.all().filter(lab_id=field)
    tcc_fields = serializers.serialize("tcc", fields)
    return HttpResponse(tcc_fields, mimetype="application/javascript")

@cache_page(60 * 15)
def add_job(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	if maxid== None :
		maxid = 1
	else:
		maxid = maxid + 1
	
	if request.method=='POST':
		form = ClientJobForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			type_of_work = cd['type_of_work']
			profile = form.save(commit=False)
			#request.session.save()
		        profile.client = request.user
			if not request.session.exists(request.session.session_key):
    				request.session.create() 
			profile.sess = Session.objects.get(session_key=request.session.session_key)
            		profile.save()
        		form.save_m2m()
			client = ClientJob.objects.get(job_no=maxid)
			value = ClientJob.objects.values_list('test').filter(job_no=maxid)
			values = Test.objects.values_list('cost',flat=True).filter(id__in = value)
			unit_price = sum(values)
			job_no = client.job_no
			mat = client.material_id
			p = TestTotal(unit_price=unit_price, job_no=job_no,mat=mat)
			p.save()
			return render_to_response('tcc/new_client_ok.html', context_instance=RequestContext(request))
	else:
  		form = ClientJobForm()
	return render_to_response('tcc/add_job.html', {"form": form}, context_instance=RequestContext(request))
	
def sessioned(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	s = request.session['amt']
	
	
	
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
	'''if request.method=='POST':
		form = TestTotalForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			value = ClientJob.objects.values_list('test').filter(job_no=id)
			values = Test.objects.values_list('cost',flat=True).filter(id__in = value)
			amt = sum(values)
			form.save()
		return render_to_response('tcc/new_client_ok.html', {'form': form,}, context_instance=RequestContext(request))
	else:
  		form = TestTotalForm()
	return render_to_response('tcc/add_job.html', {"form": form}, context_instance=RequestContext(request))'''
		
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
    query =request.GET.get('q', '')
    field_list = Material.objects.all()
    if query:
	material =Material.objects.get(id=request.GET['q'])
        test = Test.objects.all().filter(material_id = query )
	if request.method=='POST':
		form = ClientJobForm(request.POST)
  		if form.is_valid():
			cd = form.cleaned_data
			test =cd['test']
			site =cd['site']
			#material =material.name
			form.save()
        	return render_to_response('tcc/new_client_ok.html', {'form': form,}, context_instance=RequestContext(request))
	else:
		form = ClientJobForm()
	return render_to_response('tcc/search.html', {'form': form,"query": query,"test":test,"material":material,"field_list":field_list}, context_instance=RequestContext(request))
    else:                                                                                                                                               
        results = Material.objects.all()
	return render_to_response('tcc/tags.html',{'field_list':field_list}, context_instance=RequestContext(request))
 
def add_to_cart(request):
	id = ClientJob.objects.aggregate(Max('job_no'))
	maxid =id['job_no__max']
	product = TestTotal.objects.get(job_no=maxid)
	#unit = TestTotal.objects.values_list('unit_price',flat=True).filter(job_no=maxid)
	#unit_price = unit
	cart = Cart(request)
	cart.add(product, product.unit_price)

def remove_from_cart(request, product_id):
 product = Product.objects.get(id=product_id)
 cart = Cart(request)
 cart.remove(product)

def get_cart(request):
 return render_to_response('cart.html', dict(cart=Cart(request)))
    

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

