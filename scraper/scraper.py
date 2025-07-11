import scrapy
import requests
from datetime import date, timedelta
import random

BACKEND_URL = 'http://localhost:8000'

class CharterSpider(scrapy.Spider):
    name = 'charter_spider'
    start_urls = ['http://example.com/fake-dashboard']

    def parse(self, response):
        # Simulate scraping 3 departments, 2 services each, 5 requests each
        departments = [
            {'name': 'Health', 'region': 'North'},
            {'name': 'Education', 'region': 'South'},
            {'name': 'Transport', 'region': 'East'},
        ]
        for dep in departments:
            dep_resp = requests.post(f'{BACKEND_URL}/departments/', json=dep)
            dep_id = dep_resp.json()['id']
            for svc_idx in range(2):
                service = {
                    'name': f"Service {svc_idx+1} of {dep['name']}",
                    'mandated_days': random.choice([5, 7, 10]),
                    'department_id': dep_id
                }
                svc_resp = requests.post(f'{BACKEND_URL}/services/', json=service)
                svc_id = svc_resp.json()['id']
                for req_idx in range(5):
                    req_date = date.today() - timedelta(days=random.randint(1, 15))
                    request = {
                        'citizen_name': f"Citizen {req_idx+1}",
                        'request_date': req_date.isoformat(),
                        'service_id': svc_id
                    }
                    req_resp = requests.post(f'{BACKEND_URL}/requests/', json=request)
                    req_id = req_resp.json()['id']
                    # Simulate delivery
                    delivered_date = req_date + timedelta(days=random.randint(3, 14))
                    delivery = {
                        'delivered_date': delivered_date.isoformat(),
                        'request_id': req_id
                    }
                    requests.post(f'{BACKEND_URL}/deliveries/', json=delivery)
