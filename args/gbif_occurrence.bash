#!/bin/bash

./ranges/parse_gbif.py \
  --tsv-dir=data/occurrence \
  --html-dir=data/occurrence_sample_500_2024-05-15_html \
  --id-field=occurrenceID \
  --parse-field=dynamicProperties \
  --parse-field=occurrenceRemarks \
  --parse-field=fieldNotes \
  --info-field=order \
  --info-field=family \
  --info-field=scientificName \
  --info-field=eventDate \
  --info-field=countryCode \
  --info-field=stateProvince \
  --info-field=scientificName \
  --info-field=decimalLatitude \
  --info-field=decimalLongitude \
  --sample=500
