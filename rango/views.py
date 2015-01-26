from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	context_dict = {'boldmessage':"My picture is in "}
	return render(request, 'rango/index.html',context_dict)
def about(request):
	context_dict = {'boldmessage': "This tutorial has been put together by Laurynas Tamulevicius, 2087510T."}
	return render(request, 'rango/about.html',context_dict)