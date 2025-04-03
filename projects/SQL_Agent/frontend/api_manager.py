import requests

class APIServer:
    def __init__(self, service_name):
        self.url = "http://127.0.0.1:8000"
        self.service_name = service_name
    
    def make_request(self, payload=None):
        response = requests.post(
            f"{self.url}/{self.service_name}",
            json=payload
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {'status_code': response.status_code}
