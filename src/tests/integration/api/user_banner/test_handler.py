from datetime import timedelta

import pytest
from fastapi.testclient import TestClient

from app.system.loging.auth import create_access_token
from app.system.loging.base import ACCESS_TOKEN_EXPIRE_MINUTES, ADMIN_NAME, USER_NAME


def test_ready(client):
    response = client.get("/healthz/ready")
    assert response.status_code == 200


@pytest.mark.parametrize("tag_id, feature_id, username, use_last_revision, expected, expected_code",
[
    pytest.param(0, 0, ADMIN_NAME, True,
        {'text': 'some_text', 'title': 'some_title', 'url': 'https://www.google.com/'}, 200, id='successful'),
    pytest.param(1, 0, ADMIN_NAME, True,
        {"detail":"The banner was not found"}, 404, id='banner_not_found'),
    pytest.param(0, 0, USER_NAME, True,
        {"detail":"The user does not have access"}, 403, id='user_not_have_access'),
    pytest.param(0, 0, USER_NAME, False,
        {'text': 'some_text', 'title': 'some_title', 'url': 'https://www.google.com/'}, 200, id='redis'),
    pytest.param(0, 0, 'no_name', False,
        {'detail': 'Could not validate credentials'}, 401, id='no_name'),
]
)
def test_user_banner_handler(tag_id, feature_id, username, use_last_revision, expected, expected_code, client: TestClient):
    access_token = create_access_token(
        data_token={'sub': username}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    headers = {"accept": "application/json", "token": access_token, "Content-Type": "application/json"}
    data_params = {
      "tag_ids": [
        0
      ],
      "feature_id": 0,
      "content": {
        "title": "some_title",
        "text": "some_text",
        "url": "https://www.google.com/"
      },
      "is_active": True
    }

    response = client.post("/banner", json=data_params, headers=headers)

    assert response.status_code in (201, 422, 403, 401)

    headers = {"accept": "application/json", "token": access_token}
    data_params = {'tag_id': tag_id, 'feature_id': feature_id, 'use_last_revision': use_last_revision}

    response = client.get('/user_banner',  params=data_params, headers=headers)
    assert response.status_code == expected_code
    assert response.json() == expected
