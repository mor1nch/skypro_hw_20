from unittest.mock import MagicMock
import pytest as pytest

from dao.director import DirectorDAO
from setup_db import db
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture
def director_dao_func():
    dd = DirectorDAO(db.session)
    d1 = Director(id=1, name='Иван Иванович')
    d2 = Director(id=2, name='Петр Петрович')
    d3 = Director(id=3, name='Тест Тестович')

    dd.get_one = MagicMock(return_value=d1)
    dd.get_all = MagicMock(return_value=[d1, d2, d3])
    dd.create = MagicMock()
    dd.update = MagicMock()
    dd.delete = MagicMock(return_value=Director(id=3))
    return dd


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao_func):
        self.director_service = DirectorService(dao=director_dao_func)

    def test_get_one(self):
        director = self.director_service.get_one(1)

        assert director is not None
        assert director.id is not None

    def test_get_all(self):
        directors = self.director_service.get_all()

        assert len(directors) > 0

    def test_create(self):
        director_data = {"name": "Vanyaaa123"}
        director = self.director_service.create(director_data)

        assert director.id is not None

    def test_update(self):
        director_data = {"id": 4, "name": "Ваня321"}
        self.director_service.update(director_data)

    def test_delete(self):
        self.director_service.delete(1)
