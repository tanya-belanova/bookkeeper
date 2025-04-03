import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget


@pytest.fixture
def repo():
    return MemoryRepository()


def test_create_with_full_args_list():
    b = Budget(amount=100, time='Day', budget=1000, pk=1)
    assert b.amount == 100
    assert b.time == 'Day'
    assert b.budget == 1000


def test_create_brief():
    b = Budget("Week", 100)
    assert b.amount == 100
    assert b.time == "Week"


def test_can_add_to_repo(repo):
    b = Budget("Month", 3000)
    pk = repo.add(b)
    assert b.pk == pk