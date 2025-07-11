from datetime import timedelta
from sqlalchemy.orm import Session
from .models import Request, Delivery, Service

def check_and_update_compliance(db: Session, request: Request):
    service: Service = request.service
    delivery: Delivery = request.delivery
    if not service or not delivery:
        return
    mandated_days = service.mandated_days
    deadline = request.request_date + timedelta(days=mandated_days)
    delivery.is_late = delivery.delivered_date > deadline
    db.commit()
