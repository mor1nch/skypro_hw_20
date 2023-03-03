from unittest.mock import MagicMock
import pytest as pytest

from dao.movie import MovieDAO
from setup_db import db
from dao.model.movie import Movie
from service.movie import MovieService


@pytest.fixture
def movie_dao_func():
    md = MovieDAO(db.session)
    d1 = Movie(id=1, title='movie1', description='like description test1', trailer='www.trailer_link_test1.com',
               year=1234,
               rating=2.4, genre_id=1, director_id=2)
    d2 = Movie(id=2, title='movie2', description='like description test2', trailer='www.trailer_link_test2.com',
               year=1456,
               rating=5.5, genre_id=1, director_id=2)
    d3 = Movie(id=3, title='movie3', description='like description test3', trailer='www.trailer_link_test3.com',
               year=9999,
               rating=10.0, genre_id=1, director_id=2)

    md.get_one = MagicMock(return_value=d1)
    md.get_all = MagicMock(return_value=[d1, d2, d3])
    md.create = MagicMock()
    md.update = MagicMock()
    md.delete = MagicMock(return_value=Movie(id=3))
    return md


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_dao(self, movie_dao_func):
        self.movie_dao = MovieService(movie_dao_func)

    def test_get_one(self):
        movie = self.movie_dao.get_one(1)

        assert movie is not None
        assert movie.id is not None

    def test_get_all(self):
        movies = self.movie_dao.get_all()

        assert len(movies) > 0

    def test_create(self):
        movie_data = {
            "title": 'movie4',
            "description": 'like description test4',
            "trailer": 'www.trailer_link_test4',
            "year": 4444,
            "rating": 9.9,
            'genre_id': 1,
            "director_id": 2
        }
        movie = self.movie_dao.create(movie_data)

        assert movie.id is not None

    def test_update(self):
        movie_data = {
            "id": 3,
            "title": 'new_movie3',
            "description": 'updated_description',
            "trailer": 'www.new_link.com',
            "year": 2023,
            "rating": 1.1,
            'genre_id': 1,
            "director_id": 2
        }
        self.movie_dao.update(movie_data)

    def test_delete(self):
        self.movie_dao.delete(1)
