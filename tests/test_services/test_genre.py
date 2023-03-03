from unittest.mock import MagicMock
import pytest as pytest

from dao.genre import GenreDAO
from setup_db import db
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture
def genre_dao_func():
    gd = GenreDAO(db.session)
    g1 = Genre(id=1, name='test_genre1')
    g2 = Genre(id=2, name='test_genre2')
    g3 = Genre(id=3, name='test_genre3')

    gd.get_one = MagicMock(return_value=g1)
    gd.get_all = MagicMock(return_value=[g1, g2, g3])
    gd.create = MagicMock()
    gd.update = MagicMock()
    gd.delete = MagicMock(return_value=Genre(id=3))
    return gd


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao_func):
        self.genre_service = GenreService(dao=genre_dao_func)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)

        assert genre is not None
        assert genre.id is not None

    def test_get_all(self):
        genres = self.genre_service.get_all()

        assert len(genres) > 0

    def test_create(self):
        genre_data = {"name": "new_genre_test"}
        genre = self.genre_service.create(genre_data)

        assert genre.id is not None

    def test_update(self):
        genre_data = {"id": 4, "name": "новый_жанр_тест"}
        self.genre_service.update(genre_data)

    def test_delete(self):
        self.genre_service.delete(1)
