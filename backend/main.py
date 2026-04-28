from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- DATABASE ----------------
engine = create_engine(
    "sqlite:///./grievance.db",
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# ---------------- TABLES ----------------
class ComplaintDB(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    category = Column(String)
    priority = Column(String)
    status = Column(String)


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)


# create tables
Base.metadata.create_all(bind=engine)

# ---------------- REQUEST MODELS ----------------
class Complaint(BaseModel):
    text: str


class LoginData(BaseModel):
    username: str
    password: str


# ---------------- AI LOGIC ----------------
def analyze(text: str):
    text = text.lower()

    if "water" in text:
        return {"category": "Water", "priority": "High"}
    elif "electricity" in text:
        return {"category": "Electricity", "priority": "Medium"}
    elif "road" in text:
        return {"category": "Road", "priority": "High"}
    else:
        return {"category": "General", "priority": "Low"}


# ---------------- REGISTER API ----------------
@app.post("/register")
def register(data: LoginData):
    db = SessionLocal()

    existing = db.query(UserDB).filter(UserDB.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = UserDB(username=data.username, password=data.password)
    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}


# ---------------- LOGIN API ----------------
@app.post("/login")
def login(data: LoginData):
    db = SessionLocal()

    user = db.query(UserDB).filter(UserDB.username == data.username).first()

    if not user or user.password != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}


# ---------------- POST COMPLAINT ----------------
@app.post("/complaint")
def create_complaint(data: Complaint):
    db = SessionLocal()

    ai = analyze(data.text)

    new_complaint = ComplaintDB(
        text=data.text,
        category=ai["category"],
        priority=ai["priority"],
        status="Pending"
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)

    return {
        "id": new_complaint.id,
        "text": new_complaint.text,
        "category": new_complaint.category,
        "priority": new_complaint.priority,
        "status": new_complaint.status
    }


# ---------------- GET COMPLAINTS ----------------
@app.get("/complaints")
def get_complaints():
    db = SessionLocal()
    items = db.query(ComplaintDB).all()

    return [
        {
            "id": i.id,
            "text": i.text,
            "category": i.category,
            "priority": i.priority,
            "status": i.status
        }
        for i in items
    ]


# ---------------- UPDATE STATUS ----------------
@app.put("/complaint/{complaint_id}")
def update_status(complaint_id: int, status: str):
    db = SessionLocal()

    complaint = db.query(ComplaintDB).filter(ComplaintDB.id == complaint_id).first()

    if not complaint:
        raise HTTPException(status_code=404, detail="Not found")

    complaint.status = status
    db.commit()

    return {"message": "updated", "status": status}
