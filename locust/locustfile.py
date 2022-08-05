from locust import HttpUser, task, between
import json

class WebsiteUser(HttpUser):
    wait_time = between(5,15)
    @task
    def index(self):
        self.client.get("/api/v1/books")
