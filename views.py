from django.shortcuts import render
from . import core



def all_errors(request, ):
	errors = core.get_all_errors()
	output = []
	for error in errors:
		success, msg = core.run_error(error)()
		output.append({"error":str(error), "success":success, "msg":str(msg), "group": str(error.group), "id": error.id})
		print("error", str(error))
	return render(request, 'logger/list.html', {"output":output})