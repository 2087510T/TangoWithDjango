from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import PageForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from rango.bing_search import run_query
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views+1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)
def users (request):
    context_dict = {}
	
    try:
        users_list= User.objects.order_by('username')
        context_dict['users'] = users_list
    except:
	    pass

    return render(request, 'rango/users.html',context_dict)
def user(request,username):
    context_dict = {}
    try:
        print (username)
        user= User.objects.get(username=username)
    except:
	    user =None
    if user: 
        context_dict['user_Profile'] = user
        context_dict['logged'] = False
        if (user == request.user):
            context_dict['logged'] = True 		
        try:
            user_profile = UserProfile.objects.get(user=user)
        except: 
            user_profile = None	
        if user_profile: 
            context_dict['website'] = user_profile.website
            context_dict['picture'] = user_profile.picture 
			
    return render(request, 'rango/user.html', context_dict)

def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

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
                # probably better to use a redirect here.
                return category(request, category_name_slug)
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat}

    return render(request, 'rango/add_page.html', context_dict)


def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to  1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response
def about(request):
    # If the visits session varible exists, take it and use it.
    # If it doesn't, we haven't visited the site so set the count to zero.
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    # remember to include the visit data
    return render(request, 'rango/about.html', {'visits': count,'boldmessage': "This tutorial has been put together by Laurynas Tamulevicius, 2087510T."})

def category(request, category_name_slug):
    context_dict = {}
 
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        try:
            query = request.POST['query'].strip()
            if query:
                # Run our Bing function to get the results list!
                result_list = run_query(query)
                context_dict['result_list'] = result_list
                context_dict['query'] = query
        except:
            pass

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
        if not context_dict['query']:
            context_dict['query'] = category.name

    except Category.DoesNotExist:
        HttpResponseRedirect('/rango/')

    return render(request, 'rango/category.html', context_dict)

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html',{})
	
def edit_profile(request):
    if request.method == 'POST':

        users_profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(request.POST, instance=users_profile)
        if profile_form.is_valid():
            profile_to_edit = profile_form.save(commit=False)
            try:
                profile_to_edit.picture = request.FILES['picture']
            except:
                pass
            profile_to_edit.save()
            return profile(request)
    else:
        form = UserProfileForm(request.GET)
        return render(request, 'rango/profile_edit.html', {'profile_form': form})


@login_required
def register_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            if request.user.is_authenticated():
                profile = profile_form.save(commit=False)
                user = User.objects.get(id=request.user.id)
                profile.user = user
                try:
                    profile.picture = request.FILES['picture']
                except:
				    profile.save()
        return index(request)
    else:
        form = UserProfileForm(request.GET)
    return render(request, 'rango/profile_registration.html', {'profile_form': form})
def profile(request):
    user1 = User.objects.get(username = request.user.username)
    context_dict = {}
    try:
        userProfile = UserProfile.objects.get(user=user1)
    except:
	    userProfile = None
    print(user1)
    context_dict['user'] = user1
    context_dict['userprofile'] = userProfile
    return render(request, 'rango/profile.html',context_dict)
def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})
