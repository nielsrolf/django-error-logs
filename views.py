from django.shortcuts import render
from . import core
from django.conf import settings

def all_errors(request):
	if getattr(settings, "LOGGER", {}).get("one_per_group"):
		errors = core.get_one_error_per_group()
	else:
		errors = core.get_all_errors()
	output = []
	for error in errors:
		success, msg = core.run_error(error)()
		output.append({"error":str(error), "success":success, "msg":str(msg), "group": str(error.group), "id": error.id})
	return render(request, 'logger/list.html', {"output":output})