run:
	python src/manage.py runserver
	
clear:
	python src/manage.py flush

tests:
	python src/manage.py test

test_main:
	python src/manage.py test core.tests
	
test_lib:
	python src/manage.py test lib.extractor.grobid
	
run_citeseerx:
	python lib/CiteSeerExtractor/src/service.py 8081