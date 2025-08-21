from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
def apidemo(request):
    return JsonResponse({"message":"Demooooo"})