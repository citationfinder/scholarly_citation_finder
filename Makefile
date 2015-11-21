run:
	python src/manage.py runserver
	
tests:
	python src/manage.py test

test_main:
	python src/manage.py test search_for_citations.tests
	
test_harvester:
	python src/manage.py test harvester.tests

clear:
	python src/manage.py flush
	
test_lib:
	python src/tests.py