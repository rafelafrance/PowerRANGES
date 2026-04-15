#!/bin/bash

uv run ./ranges/janitor.py \
  --glob=data/Datasets\ for\ Traiter/**/*.csv \
  --glob=data/Datasets\ for\ Traiter/*.csv \
  --glob=data/Datasets\ for\ Traiter/**/*.xlsx \
  --glob=data/Datasets\ for\ Traiter/*.xlsx \
  --csv-dir=data/Datasets\ for\ Traiter/csvs \
  --output-dir=data/Datasets\ for\ Traiter/cleaned
