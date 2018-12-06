from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def pg_records(request, list, num):
	paginator = Paginator(list, num)

	page = request.GET.get('page')

	try:
		page_obj = paginator.page(page)
	except PageNotAnInteger:
		page_obj = paginator.page(1)
	except EmptyPage:
		page_obj = paginator.page(paginator.num_pages)

	return page_obj