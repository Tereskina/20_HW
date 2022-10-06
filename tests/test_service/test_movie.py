from unittest.mock import MagicMock
import pytest
from flask import jsonify

from dao.movie import MovieDAO
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(None)

    movie_1 = Movie(id=1,
                    title='title_1',
                    description='description_1',
                    trailer='trailer_1',
                    year=2021,
                    rating=10.0,
                    genre_id=1,
                    director_id=1)

    movie_2 = Movie(id=2,
                    title='title_2',
                    description='description_2',
                    trailer='trailer_2',
                    year=2022,
                    rating=9.0,
                    genre_id=2,
                    director_id=2)

    movie_dao.get_one = MagicMock(return_value=movie_1)
    movie_dao.get_all = MagicMock(return_value=[movie_1, movie_2])
    movie_dao.create = MagicMock(return_value=movie_1)
    movie_dao.delete = MagicMock()
    movie_dao.update = MagicMock()

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(movie_dao)

    def test_get_one(self):
        assert self.movie_service.get_one(1) is not None
        assert self.movie_service.get_one(1).title == 'title_1'

    def test_get_all(self):
        assert len(self.movie_service.get_all()) == 2

    def test_create(self):
        data = {
            "id": 1,
            "title": "title_1",
            "description": "description_1",
            "trailer": "trailer_1",
            "year": 2021,
            "rating": 10.0,
            "genre_id": 1,
            "director_id": 1
        }

        assert self.movie_service.create(data).title == data.get('title')

    def test_update(self):
        movie = {
            "id": 3,
            "title": "title_3",
            "description": "description_3",
            "trailer": "trailer_3",
            "year": 2023,
            "rating": 3.0,
            "genre_id": 3,
            "director_id": 3
        }

        new_movie = self.movie_service.create(movie)

        assert new_movie.title is not None


    def test_partially_update(self):
        movie = self.movie_service.get_one(1)
        new_movie_year = 2011
        movie.year = new_movie_year
        assert movie.year == 2011


    def test_delete(self):
        assert self.movie_service.delete(2) is None
