#Run NER model
##Training
### tensorflow == 2.15.0
1. NER_own.ipynb, *bigquery data
2. after training, one file and one folder will produce
>vocabulary.pkl (for dictionary lookup)
>ner_model (model weight for inference)
##Inference
1. ner.py
>preprocess data and load model
2. app.py
>gradio server
