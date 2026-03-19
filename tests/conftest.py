import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module


BASELINE_ACTIVITIES = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities_state():
    # Arrange
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(BASELINE_ACTIVITIES))

    yield

    # Assert/cleanup
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(BASELINE_ACTIVITIES))