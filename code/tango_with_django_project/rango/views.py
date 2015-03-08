from django.contrib.auth import logout
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Page
from rango.models import Category
from rango.forms import CategoryForm
from rango.forms import PageForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.bing_search import run_query

def index(request):
	category_list = Category.objects.order_by('-likes')[:5]
	pages_list = Page.objects.order_by('-views')[:5]
	context_dict = {'categories': category_list,'pages':pages_list}
	visits = request.session.get('visits')
	if not visits:
		visits = 1
	reset_last_visit_time = False
	last_visit = request.session.get('last_vist')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
		if (datetime.now() - last_visit_time).days > 0:
			visits += 1
			reset_last_visit_time = True
	else:
		reset_last_visit_time = True
	if reset_last_visit_time:
		request.session['last_vist'] = str(datetime.now())
		request.session['visits'] = visits
	context_dict['visits'] = visits
	response = render(request, 'rango/index.html',context_dict)
	return render(request, 'rango/index.html', context_dict)

def about(request):
	count = 0
	if request.session.get('visits'):
		count = request.session.get('visits')
	context_dict = {'boldmessage': "This tutorial was put together by Duncan Adamson, 2073411",
					'visited': count}
	return render(request, 'rango/about.html', context_dict)

def category(request, category_name_slug):
	context_dict = {}
	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name'] = category.name
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		pass
	return render(request, 'rango/category.html', context_dict)

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})

@login_required
def add_category(request):
	if request.method == 'POST':
		form = CategoryForm(request.POST)
		if form.is_valid():
			form.save(commit = True)
			return index(request)
		else:
			print form.errors
	else:
		form = CategoryForm()
	return render(request, 'rango/add_category.html',{'form':form})

@login_required
def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
                cat = None
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()
    context_dict = {'form':form, 'category': cat}
    return render(request, 'rango/add_page.html', context_dict)

@login_required
def restricted(request):
	return render(request, 'rango/restricted.html',{})


def some_view(request):
	if not request.user.is_authenticated():
	    return HttpResponse("You are logged in.")
	else:
	    return HttpResponse("You are not logged in.")
