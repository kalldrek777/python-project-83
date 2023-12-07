install:
	poetry install

dev:
	poetry run flask --app page_analyzer/app run

PORT ?= 8000
#start:
#	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:8000 page.analyzer.app:app

build:
	./build.sh
