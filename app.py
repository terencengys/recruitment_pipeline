from io import BytesIO
from fastapi import FastAPI, Depends, status, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import uvicorn
import json

import schemas
from database import Base, SessionLocal, engine 
from database import create_application, get_application_from_db, upload_resume_to_db, change_stage, get_all_applications, download_resume_from_db

tags_metadata = [
    {
        "name": "default",
        "description": "Default operations."
    },
    {
        "name": "applications",
        "description": "Operations for managing job applications."
    }
]

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Recruitment Pipeline", openapi_tags=tags_metadata)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", tags=["default"])
def index():
	return {"msg":"API working. Check /docs for more"}

# Post an application
@app.post("/application", response_model=schemas.Application, tags=["applications"], status_code=status.HTTP_201_CREATED)
async def post_application(application: schemas.CreateApplication, db: Session = Depends(get_db)):
    new_application = create_application(db, application)
    return new_application

# Post a resume to an existing application
@app.post("/application/resume/{jobid}", tags=["applications"])
async def upload_resume(jobid: str, file: UploadFile=File(...), db: Session = Depends(get_db)):
    upload_file = upload_resume_to_db(db, file, jobid)
    return upload_file

# Get an uploaded resume of an existing application
@app.get("/application/resume/{jobid}", tags=["applications"])
async def download_resume(jobid: str, db: Session = Depends(get_db)):
    output, output_filename = download_resume_from_db(db, jobid)
    headers = {
        'Access-Control-Expose-Headers': 'Content-Length, Content-Disposition',
        'Content-Disposition': f'attachment; filename="{output_filename}"'
    }
    file_output = BytesIO(output)
    return StreamingResponse(file_output, media_type='application/pdf', headers=headers)

# Modify stage of application
@app.patch("/application/update_stage/{jobid}", tags=["applications"])
async def update_stage(jobid: str, update_action: str, db: Session = Depends(get_db)):
    changed_stage = change_stage(db, jobid, update_action)
    return changed_stage

# Get one application
@app.get("/application/{jobid}", response_model=schemas.Application, tags=["applications"])
async def get_application(jobid: str, db: Session = Depends(get_db)):
    retrieved_application = get_application_from_db(db, jobid)
    if retrieved_application is not None:
        return retrieved_application
    else:
        raise HTTPException(status_code=404, detail="Item not found")

# Get all applications
@app.get("/applications", response_model=schemas.ListApplications, tags=["applications"])
async def get_applications(db: Session = Depends(get_db)):
    all_applications = get_all_applications(db)
    if all_applications is not None:
        return all_applications
    else:
        raise HTTPException(status_code=404, detail="Item not found")



if __name__ == "__main__":
    config = {
        "host": "0.0.0.0",
        "port": 8000,
    }
    uvicorn.run(app, **config)