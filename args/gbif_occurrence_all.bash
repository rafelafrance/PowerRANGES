#!/bin/bash

./ranges/parse_gbif.py \
  --tsv-file=data/occurrence/*occurrence.txt \
  --json-dir=data/occurrence_json \
  --csv-file=data/occurrence_2024-07-08.csv \
  --html-file=data/occurrence_2024-07-08.html \
  --id-field=occurrenceID \
  --parse-field=dynamicProperties \
  --parse-field=occurrenceRemarks \
  --parse-field=fieldNotes \
  --info-field=institutionCode \
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
  --sample-size=10000 \
  --skip-parse \
  --summary-field=scientificName
