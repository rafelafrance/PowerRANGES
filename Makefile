.PHONY: test clean install dev
.ONESHELL:

test:
	uv run -m unittest discover

install:
	uv sync
	uv pip install "git+https://github.com/rafelafrance/traiter.git@master#egg=traiter"
	uv run -- spacy download en_core_web_md

dev:
	uv sync
	uv pip install -e ../traiter
	uv run -- spacy download en_core_web_md

clean:
	rm -rf .venv
	rm -rf build
	find -iname "*.pyc" -delete
