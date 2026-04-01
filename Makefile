.PHONY: test clean spacy traiter dev
.ONESHELL:

test:
	uv run -m unittest discover

spacy:
	uv run -- spacy download en_core_web_md

traiter:
	uv pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter

dev:
	uv pip install -e ../../traiter

clean:
	rm -rf .venv
	rm -rf build
	find -iname "*.pyc" -delete
