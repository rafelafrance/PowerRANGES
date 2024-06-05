#!/bin/bash

./ranges/parse_gbif.py \
  --tsv-dir=data/junk \
  --html-dir=data/occurrence_2024-06-05a \
  --csv-dir=data/occurrence_2024-06-05a \
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
  --pass-thru=sex \
  --summary-field=scientificName \
