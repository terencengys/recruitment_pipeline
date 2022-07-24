# Recruitment Pipeline

This project implements a recruitment pipeline for hiring. 

The recruitment pipeline implemented in this project follows the flowchart as below:

![Recruitment Pipeline](flowchart.jpg?raw=true "Recruitment Pipeline")

This project is coded in Python, and uses the FastAPI library to implement a REST API. Applications are persisted using a SQLite database.

## Installation and Deployment

### Local Deployment

This repository is hosted on https://github.com/terencengys/recruitment-pipeline. 

To deploy locally, simply Git clone into the repository:

`git clone https://github.com/terencengys/recruitment-pipeline`

Install the required prerequisite libraries, then run the `app.py` script

`pip install -r requirements.txt`
`python app.py`

The app will run on `http://localhost:8000`

### Heroku Deployment

To deploy on Heroku, simply login to your Heroku account via Heroku CLI and do the following:

`heroku create -a <app name>`
`git remote -v`
`heroku git:remote -a <app name>`
`git push heroku main`

The included Procfile will be used in the deployment.

## Usage

This is a pure backend application, so there will be no frontend GUI. To use this app, navigate to `http://localhost:8000/docs`.

Alternatively, a cloud version of the app is hosted on `https://recruitment-pipeline.herokuapp.com`. Navigate to `https://recruitment-pipeline.herokuapp.com/docs` to use it.

### Posting an Application

To post an application, click on the POST `/application` endpoint and enter the email address of the applicant.

Upon successful creation of the application, both e unique UUID identifier, `jobid`, will be generated, and the stage of the application will be automatically set to `Pending`.

Resumes have to be attached separately. Use the POST `/application/resume/{jobid}` endpoint and enter the `jobid` of the application the resume is to be attached to.

At the moment, only resumes in PDF format are accepted.

### Advancing through the pipeline

To select an application and find its status, use the GET `/application/{jobid}` endpoint with the application's `jobid`. 

Inside the response, there will be a field labeled `actions`, which is a list of valid actions for the particular stage of the application. 

To advance through the application stages, use the POST `/application/update_stage/{jobid}` and enter both the application's `jobid` and one action in the `actions` list.

If the stage advancement is successful, a response with the application details and new stage will be returned.

The stages and valid actions adhere to the flowchart shown above.

### Resume download

At any moment in the recruitment process, the resume of the applicant can be downloaded using the GET `/application/resume/{jobid}` endpoint.