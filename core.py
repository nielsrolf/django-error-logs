from .models import *
from rest_framework.exceptions import ValidationError
from django.http import Http404
import requests
from django.conf import settings
from rest_framework.test import APIClient
from django.test import TestCase

import pprint
pp = pprint.PrettyPrinter(indent=2)
show = pp.pprint


class TestHook(object):
	def __init__(self, get_response):
		self.get_response = get_response
		settings.LOGGING["hook"]=self
	def __call__(self, request): return self.get_response(request)

class LoggingMiddleware(object):
	ignore = (ValidationError, Http404,)

	def __init__(self, get_response): self.get_response = get_response

	def __call__(self, request): return self.get_response(request)

	def process_exception(self, request, exception):
		if isinstance(exception, LoggingMiddleware.ignore): return None
		try:
			if request.META.NO_ERROR_LOG: return None
		except: pass
		log = new_error(
			endpoint = request.path,
			method = request.method,
			content_type = request.__dict__.get("content_type", None),
			auth = request.__dict__.get("auth", None),
			user = request.user,
			body = request.__dict__.get("body", None),
			error_msg = str(exception)
			)
		return None

class run_error():
	def __init__(self, error): self.error = error
	def __call__(self):
		error = self.error
		if error.group.content_type:
			if error.group.content_type != "application/json":
				return True, "Error has unsopprted content type, skipped :/"

		client = APIClient()

		if error.auth:
			client.credentials(HTTP_AUTHORIZATION='Bearer ' + error.auth)
			print("set credentials:"+error.auth)
		elif error.user:
			client.force_authenticate(error.user)

		try:
			if error.group.method == "GET":
				response = client.get(error.group.endpoint, NO_ERROR_LOG=True)
			elif error.group.method == "POST":
				response = client.post(error.group.endpoint, error.body, format="json", NO_ERROR_LOG=True)
			elif error.group.method == "PUT":
				response = client.put(error.group.endpoint, error.body, format="json", NO_ERROR_LOG=True)
			elif error.group.method == "DELETE":
				response = client.delete(error.group.endpoint, NO_ERROR_LOG=True)
		except Exception as e:
			if isinstance(e, LoggingMiddleware.ignore):
				error.resolved = True
				error.save()
				return True, str(e)
			error.resolved = False
			error.save()
			return False, str(e)

		if 200 <= response.status_code and response.status_code <= 299:
			error.resolved=True
			error.save()
			return True, None
		if 400 <= response.status_code and response.status_code <= 499:
			error.resolved=True
			error.save()
			return True, str(response)

		return False, str(response)

def get_one_error_per_group():
	groups = ErrorGroup.objects.all()
	errors = []
	for group in groups:
		try: error = Error.objects.first(group=group, resolved=False)
		except Error.DoesNotExist:  Error.objects.first(group=group)
		errors.append(error)
	return errors

def get_all_errors():
	return Error.objects.all()

def get_all_unresolved():
	return Error.objects.filter(resolved=False).all()