from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	context_dict = {'boldmessage': "Iam bold "}
	return render(request, 'rango/index.html',context_dict)
def about(request):
	context_dict = {'boldmessage': "Iam NOT bold "}
	return render(request, 'rango/about.html',context_dict)