from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, engine
from .models import Base, Department, Service, Request, Delivery
from .rule_engine import check_and_update_compliance
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Schemas
class DepartmentCreate(BaseModel):
    name: str
    region: Optional[str]

class ServiceCreate(BaseModel):
    name: str
    mandated_days: int
    department_id: int

class RequestCreate(BaseModel):
    citizen_name: str
    request_date: date
    service_id: int

class DeliveryCreate(BaseModel):
    delivered_date: date
    request_id: int

# Endpoints
@app.post('/departments/')
def create_department(dep: DepartmentCreate, db: Session = Depends(get_db)):
    department = Department(name=dep.name, region=dep.region)
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

@app.post('/services/')
def create_service(svc: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(name=svc.name, mandated_days=svc.mandated_days, department_id=svc.department_id)
    db.add(service)
    db.commit()
    db.refresh(service)
    return service

@app.post('/requests/')
def create_request(req: RequestCreate, db: Session = Depends(get_db)):
    request = Request(citizen_name=req.citizen_name, request_date=req.request_date, service_id=req.service_id)
    db.add(request)
    db.commit()
    db.refresh(request)
    return request

@app.post('/deliveries/')
def create_delivery(delivery_in: DeliveryCreate, db: Session = Depends(get_db)):
    request = db.query(Request).filter(Request.id == delivery_in.request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail='Request not found')
    delivery = Delivery(delivered_date=delivery_in.delivered_date)
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    request.delivery_id = delivery.id
    db.commit()
    db.refresh(request)
    check_and_update_compliance(db, request)
    return delivery

@app.get('/compliance/')
def get_compliance(db: Session = Depends(get_db)):
    results = db.query(Department, Service, Request, Delivery).join(Service, Service.department_id == Department.id).join(Request, Request.service_id == Service.id).join(Delivery, Delivery.id == Request.delivery_id).all()
    compliance = []
    for dep, svc, req, deliv in results:
        compliance.append({
            'department': dep.name,
            'region': dep.region,
            'service': svc.name,
            'mandated_days': svc.mandated_days,
            'citizen_name': req.citizen_name,
            'request_date': req.request_date,
            'delivered_date': deliv.delivered_date,
            'is_late': deliv.is_late
        })
    return compliance
