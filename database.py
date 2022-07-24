import uuid
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy import Boolean, Column, Integer, String, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

import schemas

valid_actions = {
    "Pending": ["Reviewed and shortlisted", "Reviewed and not shortlisted"],
    "Reviewing": ["Reject"],
    "Shortlisted": ["Interview"],
    "Interviewing": ["Advance interview required", "Offer", "Reject"],
    "Advanced Interviewing": ["Offer", "Reject"],
    "Offered": ["Accept", "Reject"],
    "Hired": [],
    "Rejected": []
}

stage_changes = {
    "Reviewed and shortlisted": ["Pending", "Shortlisted"],
    "Reviewed and not shortlisted": ["Pending", "Reviewing"],
    "Interview": ["Shortlisted", "Interviewing"],
    "Advance interview required": ["Interviewing", "Advanced Interviewing"],
    "Accept": ["Offered", "Hired"],
    "Offer": ["Offered"],
    "Reject": ["Rejected"]
}

# Pipeline logic
def get_valid_action(stage):
    # Get the valid action values of stage
    return valid_actions[stage]

# Changes status
def stage_change(stage, action):
    if action == "Offer" or action == "Reject":
        return stage_changes[action][0]
    else:
        if stage == stage_changes[action][0]:
            return stage_changes[action][1]
        else:
            raise HTTPException(status_code=400, detail="Invalid stage change")

SQLALCHEMY_DATABASE_URL = "sqlite:///./applications.db"

def generate_uuid():
    return str(uuid.uuid4())

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Applications(Base):
    __tablename__ = "applications"

    jobid = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, nullable=False)
    resume_filename = Column(String)
    resume = Column(LargeBinary)
    stage = Column(String)

def _parse_application(application, has_resume, valid_actions):
    retrieved_application = {
        "jobid": application.jobid,
        "email": application.email,
        "stage": application.stage,
        "has_resume": has_resume,
        "actions": valid_actions
    }
    return retrieved_application

def create_application(db: Session, application: schemas.CreateApplication):
    db_application = Applications(email = application.email, stage = "Pending")
    db.add(db_application)
    db.commit()
    return _parse_application(db_application, False, ["Reviewed and shortlisted", "Reviewed and not shortlisted"])

def upload_resume_to_db(db: Session, file, jobid):
    try:
        application = db.query(Applications).get(jobid)
        application.resume = file.file.read()
        application.resume_filename = file.filename
        db.commit()
        return {
            "status": "Upload successful",
            }
    except:
        raise HTTPException(status_code=400, detail="Upload unsuccessful")

def download_resume_from_db(db: Session, jobid):
    application = db.query(Applications).get(jobid)
    if application.resume is not None:
        return application.resume, application.resume_filename
    else:
        raise HTTPException(status_code=400, detail="Resume not present. Please upload one.")

def get_application_from_db(db: Session, jobid):
    application = db.query(Applications).get(jobid)
    if application is not None:
        valid_actions = get_valid_action(application.stage)
        has_resume = False
        if application.resume is not None:
            has_resume = True
        db.close()
        return _parse_application(application, has_resume, valid_actions)
    else:
        db.close()
        return None

def get_all_applications(db: Session):
    all_applications = db.query(Applications).all()
    if all_applications is not None:
        parsed_application_list = []
        for application in all_applications:
            valid_actions = get_valid_action(application.stage)
            has_resume = False
            if application.resume is not None:
                has_resume = True
            parsed_application = _parse_application(application, has_resume, valid_actions)
            parsed_application_list.append(parsed_application)
        all_parsed_applications = {
            "count": len(all_applications),
            "applications": parsed_application_list
        }
        db.close()
        return all_parsed_applications
    else:
        db.close()
        return None

def change_stage(db: Session, jobid, action):
    application = db.query(Applications).get(jobid) 
    if action not in stage_changes.keys():
        raise HTTPException(status_code=400, detail="Invalid action")
    new_stage = stage_change(application.stage, action)
    application.stage = new_stage
    db.commit()

    valid_actions_for_stage = get_valid_action(application.stage)
    has_resume = False
    if application.resume is not None:
        has_resume = True
    return _parse_application(application, has_resume, valid_actions_for_stage)
