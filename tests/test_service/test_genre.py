from unittest.mock import MagicMock
import pytest

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(None)

    genre_1 = Genre(id=1, name='name_1')
    genre_2 = Genre(id=2, name='name_2')

    genre_dao.get_one = MagicMock(return_value=genre_1)
    genre_dao.get_all = MagicMock(return_value=[genre_1, genre_2])
    genre_dao.create = MagicMock(return_value=genre_1)
    genre_dao.delete = MagicMock()
    genre_dao.update = MagicMock()

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(genre_dao)

    def test_get_one(self):
        assert self.genre_service.get_one(1) is not None
        assert self.genre_service.get_one(1).name == 'name_1'

    def test_get_all(self):
        assert len(self.genre_service.get_all()) == 2

    def test_create(self):
        data = {
            "name": "name_1"
        }

        assert self.genre_service.create(data).name == data.get('name')

    def test_update(self):
        genre = {
            "name": "name_1"
        }
        new_genre = self.genre_service.create(genre)

        assert new_genre.name is not None

    def test_delete(self):
        assert self.genre_service.delete(2) is None











