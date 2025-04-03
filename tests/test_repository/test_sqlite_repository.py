import os

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from dataclasses import dataclass
import pytest


@pytest.fixture
def custom_class():
    @dataclass
    class Custom:
        name: str = 'food'
        pk: int = 0

    return Custom


@pytest.fixture
def repo(custom_class):
    return SQLiteRepository('test_db.db', custom_class)


def test_crud(repo, custom_class):
    obj = custom_class()
    pk = repo.add(obj)
    assert obj.pk == pk

    assert repo.get(pk) == obj

    obj2 = custom_class()
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2

    repo.delete(pk)
    assert repo.get(pk) is None


def test_cannot_add_with_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_add_without_pk(repo, custom_class):
    obj = custom_class()
    obj.pk = None
    with pytest.raises(ValueError):
        repo.add(obj)


def test_cannot_delete_unexistent(repo, custom_class):
    obj = custom_class()
    pk1 = repo.add(obj)
    with pytest.raises(KeyError):
        repo.delete(pk1 + 10)
    repo.delete(pk1)


def test_cannot_delete_without_pk(repo, custom_class):
    with pytest.raises(ValueError):
        repo.delete(0)


def test_cannot_update_without_pk(repo, custom_class):
    obj = custom_class()
    with pytest.raises(ValueError):
        repo.update(obj)


def test_get_all(repo, custom_class):
    objects = [custom_class() for _ in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects
    for o in objects:
        repo.delete(o.pk)


def test_get_all_with_condition(repo, custom_class):
    objects = []
    for i in range(5):
        o = custom_class()
        o.name = str(i)
        repo.add(o)
        objects.append(o)
    assert repo.get_all({'name': '0'}) == [objects[0]]