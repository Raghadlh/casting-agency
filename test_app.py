import datetime
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app

from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_TEST


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""

        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
            DB_USER, DB_PASSWORD, DB_HOST, DB_TEST)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client

        self.new_movie = {
            'title': 'The Canterville Ghost',
            'release_date': datetime.date(2023, 10, 20),
        }
        self.new_actor = {
            'name': 'johnny depp',
            'age': 60,
            'gender': 'Male',
            'movie_id': 1
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_movies(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_get_movies(self):
        res = self.client().get("/moviesss")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_get_actors(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_404_get_actors(self):
        res = self.client().get("/actorsssssss")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_new_movie(self):

        res = self.client().post("/movies", json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_new_actor(self):

        res = self.client().post("/actors", json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_actor(self):
        res = self.client().delete("/actors/2")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_movie(self):
        res = self.client().delete("/movies/3")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_actor_fails(self):
        res = self.client().delete("/actors/50000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_movies_fails(self):
        res = self.client().delete("/movies/50000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_patch_movie(self):
        response = self.client().patch('/movies/4', json=self.new_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_movie_fail(self):
        response = self.client().patch('/movies/2000', json=self.new_movie)
        self.assertEqual(response.status_code, 404)

    def test_patch_actor(self):
        response = self.client().patch('/actors/3', json=self.new_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_actor_fail(self):
        response = self.client().patch('/actors/patch/2000', json=self.new_actor)
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
