# Introduction
This week conclude of training NER model, using Gradio as a UI for Inference
# Training
## requirement
### tensorflow version == 2.15.0
## steps
* ### 1. NER_own.ipynb, *bigquery data
* ### 2. after training, two things will produce
* #### 2.1 vocabulary.pkl (for dictionary lookup)
* #### 2.2 ner_model (model weight for inference)

# Inference
## requirement
* ### same version of tensorflow == 2.15.0
* ### 2.1 vocabulary.pkl (for dictionary lookup)
* ### 2.2 ner_model folder(model weight for inference)
## steps
### run app.py
>gradio server
