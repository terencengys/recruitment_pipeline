# Recruitment Pipeline

This project implements a recruitment pipeline for hiring. 

The recruitment pipeline implemented in this project follows the flowchart as below:

![Recruitment Pipeline](flowchart.jpg?raw=true "Recruitment Pipeline")

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

