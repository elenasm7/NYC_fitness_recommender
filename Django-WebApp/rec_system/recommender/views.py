from django.shortcuts import render_to_response,render
from recommender.models import Company
from django.http import HttpResponse
from django.template import RequestContext, Context
from .recommender import *
from django.db.models import Q

# Create your views here.


def search(request):

	show_results = False

	if request.method == 'GET':
		query_1 = request.GET.get('query-1')
		query_2 = request.GET.get('query-2')
		query_3 = request.GET.get('query-3')
		query_4 = request.GET.get('query-4')
		results = Company.objects.filter(categories__contains = query_2).filter(rating__gt = query_3)
		results_list = list(results)

		recommended = recomend_places(query_1,query_4,results_list)

		show_results = True

	context = {
		'type': query_2,
		'recommended': list(recommended),
		'results':results_list,
		'show_results': show_results
	}
	return render(request, 'search.html', context)
	# return render_to_response('search.html',variables, request)