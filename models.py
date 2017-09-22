from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User

class ErrorGroup(models.Model):
	endpoint = models.CharField(max_length=100)
	method = models.CharField(max_length=10)
	content_type = models.CharField(max_length=30)

	def __str__(self): return self.method + " " + self.endpoint

	@staticmethod
	def get(endpoint, method, content_type):
		try:
			group = ErrorGroup.objects.filter(endpoint=endpoint, method=method, content_type=content_type).first()
			assert(isinstance(group, ErrorGroup))
		except:
			group = ErrorGroup.objects.create(endpoint=endpoint, method=method, content_type=content_type)
		return group

# Create your models here.
class Error(models.Model):
	time = models.DateTimeField(auto_now_add=True, null=True)
	resolved = models.BooleanField(default=False)

	group = models.ForeignKey(ErrorGroup)
	auth = models.CharField(max_length=1000, null=True)
	user = models.ForeignKey(User, null=True)
	body = JSONField(null=True)
	error_msg = models.TextField(default="")

	def __str__(self): return self.error_msg

def new_error(endpoint, method, content_type, auth, user, body, error_msg):
	group = ErrorGroup.get(endpoint=endpoint, method=method, content_type=content_type)
	error = Error.objects.create(group=group, auth=auth, user=user, body=body, error_msg=error_msg)
	return error

