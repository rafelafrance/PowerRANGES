#!/bin/bash

uv run ./ranges/parse_gbif.py \
  --csv-in=data/datasets_for_traiter/csvs/*.csv \
  --json-dir=data/occurrence_json2 \
  --output-dir=data/occurrence_2026-04-01a \
  --csv-institution \
  --id-field=occurrenceID \
  --parse-field=dynamicProperties \
  --parse-field=occurrenceRemarks \
  --parse-field=fieldNotes \
  --info-field=institutionCode \
  --info-field=collectionCode \
  --info-field=catalogNumber \
  --info-field=scientificName \
  --info-field=order \
  --info-field=family \
  --info-field=genus \
  --info-field=specificEpithet \
  --info-field=day \
  --info-field=month \
  --info-field=year \
  --info-field=countryCode \
  --info-field=stateProvince \
  --info-field=decimalLatitude \
  --info-field=decimalLongitude \
  --overwrite-field=sex \
  --cpus=16 \
  --debug \
  --summary-field=scientificName
