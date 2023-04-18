from locust import HttpUser, task, between

user_count = 0


class MyUser(HttpUser):
    wait_time = between(1, 2)
    curr_id = 0

    def on_start(self):
        self.register_user()
        self.login_user()

    @task
    def user_page(self):
        self.client.get(f'/user/testuser{self.curr_id}')

    def register_user(self):
        self.client.post('/')
        global user_count

        data = {
            'username': f'testuser{user_count}',
            'email': f'testuser{user_count}@example.com',
            'password': 'testpassword'
        }
        self.curr_id = user_count
        user_count += 1
        self.client.post('/api/users', json=data)

    def login_user(self):
        data = {'username': f'testuser{self.curr_id}',
                'password': 'testpassword'}
        self.client.post('/api/login', json=data)
