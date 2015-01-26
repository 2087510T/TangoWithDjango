from django.shortcuts import render
from django.http import HttpResponse

def index(request):
<<<<<<< HEAD
	context_dict = {'boldmessage':"My picture is in "}
	return render(request, 'rango/index.html',context_dict)
def about(request):
	context_dict = {'boldmessage': "This tutorial has been put together by Laurynas Tamulevicius, 2087510T."}
	return render(request, 'rango/about.html',context_dict)
=======
	return HttpResponse('Laurynas says hello world!<br/> <a href="/rango/about">About</a> ')
def about(request):
	return HttpResponse('This tutorial has been put together by Laurynas Tamulevicius, 2087510T. <a href="/rango/">Index</a>')
>>>>>>> abdf291b10d8f97959b4fea6b2b49787baffccdc
