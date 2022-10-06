from unittest.mock import MagicMock
import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(None)

    director_1 = Director(id=1, name='name_1')
    director_2 = Director(id=2, name='name_2')

    director_dao.get_one = MagicMock(return_value=director_1)
    director_dao.get_all = MagicMock(return_value=[director_1, director_2])
    director_dao.create = MagicMock(return_value=director_1)
    director_dao.delete = MagicMock()
    director_dao.update = MagicMock()

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(director_dao)

    def test_get_one(self):
        assert self.director_service.get_one(1) is not None
        assert self.director_service.get_one(1).name == 'name_1'

    def test_get_all(self):
        assert len(self.director_service.get_all()) == 2

    def test_create(self):
        data = {
            "name": "name_1"
        }

        assert self.director_service.create(data).name == data.get('name')

    def test_update(self):
        director = {
            "name": "name_1"
        }
        new_director = self.director_service.create(director)

        assert new_director.name is not None

    def test_delete(self):
        assert self.director_service.delete(2) is None
