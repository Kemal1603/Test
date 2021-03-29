from rest_framework.parsers import JSONParser

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from main.forms import SeoRequestForm

from main.models import SeoResult
from main.parser import Parser


def get_index_View_input(request):
	if request.method == 'POST':

		form = SeoRequestForm(request.POST)
		if form.is_valid():
			Parser(filters={
				"language_name": "English",
				"location_name": form.cleaned_data.get('location'),
				"keyword": form.cleaned_data.get('keyword'),
				"postback_url": "https://herokudjangoappkemal.herokuapp.com/postbackscript",
				"postback_data": 'advanced'}, search_engine=form.cleaned_data.get("engine").lower())
			return redirect(reverse('output') + f'?keyword={form.cleaned_data.get("keyword").lower()}&'
			                                    f'engine={form.cleaned_data.get("engine").lower()}&'
			                                    f'location={form.cleaned_data.get("location")}&')
	else:
		form = SeoRequestForm()
		return render(request, 'index.html', {'form': form})


def index_View(request):
	return render(request, 'index.html')


def output_View(request):
	query_params = request.GET
	try:
		last_pack_number = SeoResult.objects.filter(keywords=query_params.get('keyword'),
		                                            engine=query_params.get('engine'),
		                                            location=query_params.get('location')).last().parse_number
	except AttributeError:
		return render(request, 'output.html', {'data': None})
	else:
		last_pack = SeoResult.objects.filter(parse_number=last_pack_number)
		return render(request, 'output.html', {'data': last_pack})


@csrf_exempt
def postback(request):
	if request.method == 'POST':
		response_from_DFS = JSONParser().parse(request)

		db_input = []
		last_record = SeoResult.objects.last()
		last_parser_number = SeoResult.objects.last().parse_number if last_record else 1
		new_parser_number = last_parser_number + 1 if last_parser_number else last_parser_number
		data = response_from_DFS['tasks'][0]['data']
		keyword = data.get('keyword')
		engine = data.get('se')
		location = data.get('location_name')

		for item in response_from_DFS['tasks'][0]['result'][0]['items']:
			data_for_front_db_input = {
				'domain': item.get('domain'),
				'title': item.get('title'),
				'description': item.get('description'),
				'url': item.get('url'),
				'parse_number': new_parser_number,
				'keywords': keyword,
				'engine': engine,
				'location': location
			}
			db_input.append(SeoResult(**data_for_front_db_input))

		SeoResult.objects.bulk_create(db_input)
		data = {"Status": "The Data has Been Received! Thanks a lot and have a nice day ;)"}
		return JsonResponse(data=data, status=201)
