run:
	python src/manage.py runserver
	
tests:
	python src/manage.py test

test_main:
	python src/manage.py test search_for_citations.test
	
clear:
	python src/manage.py flush