from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Dailycheckins

# Create your views here.
def index(request):
	user_list = Dailycheckins.objects.order_by('user').values('user').distinct()
	output = Dailycheckins.objects.all().order_by('-cleaned_timestamp')
	paginator = Paginator(output, 25) # Show 25 contacts per page
	
	page = request.GET.get('page')
	output = paginator.get_page(page)
	template = loader.get_template('viewcheckins/index.html')
	context = {
        'output': output,
        'user_list': user_list,
    }
	return HttpResponse(template.render(context, request))

def filter_by_user(request, user):
	user_list = Dailycheckins.objects.order_by('user').values('user').distinct()
	output = Dailycheckins.objects.filter(user=user)
	paginator = Paginator(output, 25) # Show 25 contacts per page
	page = request.GET.get('page')
	output = paginator.get_page(page)
	template = loader.get_template('viewcheckins/index.html')
	context = {
		'output': output,
		'user_list': user_list,
		'current_user' : user,
	}
	return HttpResponse(template.render(context, request))