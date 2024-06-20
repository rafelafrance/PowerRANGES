#!/bin/bash

./ranges/parse_gbif.py \
  --tsv-dir=data/occurrence_todo1 \
  --html-dir=data/occurrence_2024-06-20 \
  --csv-dir=data/occurrence_2024-06-20 \
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
  --summary-field=scientificName \
  --sample=1000
