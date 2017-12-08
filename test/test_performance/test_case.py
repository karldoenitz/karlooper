# -*- coding: utf-8 -*-

from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):
    def on_start(self):
        print("start...")

    @task(1)
    def index(self):
        self.client.get("/hello-world")

        # @task(1)
        # def about(self):
        #     self.client.get("/hello")


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    host = "http://127.0.0.1:9988"
    min_wait = 1000
    max_wait = 5000
