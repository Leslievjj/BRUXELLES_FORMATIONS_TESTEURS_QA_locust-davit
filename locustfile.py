from locust import HttpUser, task, between, constant
import random


class Visiteur(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(1,3)

    def on_start(self):

        response = self.client.get("/api/events", name="/api/events [init]")
        events_list = response.json()

        self.events_city = [event["city"] for event in events_list]
        
        return super().on_start()
    
    @task(2)
    def recherche_ev_city(self):
       city_hasard = random.choice([self.events_city])
       self.client.get(f"/api/events", params={"city": city_hasard})

    
    @task(0)
    def consulter_catalogue(self):
        self.client.get("/api/events")

##consulter details user de un event aleatoire
    @task(0)
    def consulter_detail(self):
        event_id = random.choice([1, 2, 3, 4])
        self.client.get(f"/api/events/{event_id}", name="/api/events/[id]")
#le name ayuda acategorizar en locust pongo 10-10

    @task(0)
    def rechercher_mot(self):
        liste_mots=["jazz", "electro", "QA", "cloud"]
        mot = random.choice([liste_mots])
        self.client.get(f"/api/events", params={"q": mot},
            name="/api/events?=mot")
        


class Veilleur(HttpUser):
    host = "http://localhost:8000"
    wait_time = constant(5)

    @task
    def consulter_api(self):
        self.client.get("/api/health")

#exo2


