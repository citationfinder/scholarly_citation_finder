run:
	python manage.py runserver
	
tests:
	python manage.py test

test_main:
	python manage.py test search_for_citations.test
	
clear:
	python manage.py flush