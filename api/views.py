#from django.shortcuts import render
import json
from django.http import HttpResponse
from django.core import serializers


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = __import__(module_name, globals(), locals(), class_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


def get_all(request, collection):
    loaded_class = class_for_name('api.models', collection)
    response_data = loaded_class.objects.all()
    return HttpResponse(serializers.serialize('json', response_data), content_type="application/json")


def get(request, collection):
    loaded_class = class_for_name('api.models', collection)
    response_data = loaded_class.objects.distinct('currency1', 'currency2')
    return HttpResponse(serializers.serialize('json', response_data), content_type="application/json")
