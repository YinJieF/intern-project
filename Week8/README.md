# NER Web Demo
## Overview

NER Web is a web application designed to demonstrate Named Entity Recognition (NER) capabilities for Vietnamese crime data. It allows users to input text data and visualize the extracted named entities [name, birthdate] under a user friendly interface.

## Features
-Adding cuztomize data as new dataset or extend on top of old dataset (developing)
-Conduct NER training with different type of NER model
-Test out your model by predict with a crime data
## Installation

To run the application locally, follow these steps:
1. Clone the repository:
2. Install dependencies:
3. Set up your own credentials on google cloud
4. Modify the project-id, dataset-id, table-id and etc cuztomize info inside files
5. Run the application:

## Usage
1. Open the application in your web browser.
2. Preview your dataset on /data route
3. In /train route, select the dataset and the datasize for training
4. By one click, it's all done, and wait for the result

## Technologies Used
- Python
- Flask
- GCP

## Notes
### This application is under development
#### To Do:
- Cuztomization of the data (create/extend)
- Predict route
- Visual of the web application
