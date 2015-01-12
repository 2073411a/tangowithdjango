from django.shortcuts import render
from django.http import HttpResponse
def index(reuest):
	return HttpResponse("Hello World")
