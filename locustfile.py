from locust import HttpUser, constant, task
from locust.exception import ResponseError


class MicroblogUser(HttpUser):

    def on_start(self):
        self.login()

    def login(self):
        response = self.client.post('/auth/login', json={
            'username': 'your_username',
            'password': 'your_password'
        })

        if response.status_code != 200:
            raise ResponseError("Unexpected status code: %s" % response.status_code)

    @task
    def visit_profile_page(self):
        response = self.client.get('/user/your_username')

        if response.status_code != 200:
            raise ResponseError("Unexpected status code: %s" % response.status_code)

    wait_time = constant(1)
