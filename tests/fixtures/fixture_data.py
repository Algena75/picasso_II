import pytest


@pytest.fixture
def bicycle():
    from bicycles.models import Bicycle
    return Bicycle.objects.create(number=12345)


@pytest.fixture
def bicycle_2():
    from bicycles.models import Bicycle
    return Bicycle.objects.create(number=54321)
