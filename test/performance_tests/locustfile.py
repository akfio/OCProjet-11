from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def home(self):
        self.client.get("/")

    @task
    def login(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def purchase_places(self):
        self.client.post("/purchasePlaces", {'competition': 'Test Event', 'club': 'She Lifts', 'places': 12})

    @task
    def get_points(self):
        self.client.get("/points")

