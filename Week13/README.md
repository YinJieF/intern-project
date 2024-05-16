# Vietnamese NER with ELECTRA Base and BigQuery

## Data Generation ()

The first step involves using a new method of Named Entity Recognition (NER) with the ELECTRA base model for Vietnamese. This model generates entities into three categories: Person, Location, and Organization. The generated data is then uploaded to BigQuery for storage and further processing.

## Model Training (ner-electra-base-vn.ipynb)

The second step involves training the NER model with the new data generated in the first step. During this process, we discovered that the volume of data significantly increases when using original PDF files. However, this led to an imbalance in the data, which adversely affected the performance of the model.
