from locust import HttpUser, task, between

class MyProject(HttpUser):
    wait_time = between(1, 3)

    @task
    def my_task(self):
        self.client.get("/forum-api/all_questions")
