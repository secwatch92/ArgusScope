from locust import HttpUser, task, between

class ScanPerformanceTest(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_scan_endpoint(self):
        self.client.post("/scan", json={"target": "example.com"})
        
    @task(3)
    def test_report_endpoint(self):
        self.client.get("/reports/latest")
