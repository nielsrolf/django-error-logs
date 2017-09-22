# Error Logger for Django Rest Framework

Error logging for DRF projects: log occuring errors, group them by endpoint, and reconstruct them without effort.

Catches all Exceptions except django.http.Http404 and rest_framework.exceptions.ValidationError, and logs them. You can then get the requests that caused errors: all, one per group or all not yet resolved ones.

# Installation
1. Clone this project into your Django project
2. Add `logger` to your installed apps in setting.py
3. Add `logger.core.LoggingMiddleware` to your middleware in settings.py
4. `python manage.py migrate`


# Use

## Where to find logs?
You have an overview over all errors in the django admin site, and logger provides a view in its subpath `/list` with overview over all errors.

![preview](preview.png?raw=true "Title")

You can add one of these to your tests:

## Use logged errors as tests
Call one of these in your tests to get errors
```
errors = logger.core.get_one_error_per_group()
errors = logger.core.get_all_errors()
errors = logger.core.get_all_unresolved()
```

And then
```
for error in errors:
	succes, msg = logger.core.run_error(error)
	...	
```

# Missing features
- Requests with files: files are not saved
- Auto generate test cases

