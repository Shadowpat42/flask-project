from http import HTTPStatus
import requests
from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Vladimir" + str(uuid4()),
        "last_name": "Jonson" + str(uuid4()),
        "email": "test@test.ru"
    }


def test_post_create():
    user_payload = create_user_payload()
    user_create = requests.post(f"{ENDPOINT}/user/create", json=user_payload)
    user_id = user_create.json()["id"]
    assert user_create.status_code == HTTPStatus.OK

    post_payload = {
        "author_id": user_id,
        "text": "Example text for testing post",
    }

    create_post = requests.post(f"{ENDPOINT}/post/create", json=post_payload)
    post_id = create_post.json()["post_id"]
    assert (create_post.status_code ==
            HTTPStatus.OK)
    assert create_post.json()["author_id"] == post_payload["author_id"]
    assert create_post.json()["text"] == post_payload["text"]

    create_post_response = requests.get(f"{ENDPOINT}/post/{user_id}/{post_id}")
    assert create_post_response.status_code == HTTPStatus.OK
    assert create_post_response.json()["author_id"] == post_payload["author_id"]
    assert create_post_response.json()["text"] == post_payload["text"]

    delete_post_response = requests.delete(f"{ENDPOINT}/post/{user_id}/{post_id}")
    assert delete_post_response.status_code == HTTPStatus.OK
    assert (
        delete_post_response.json()["post_id"] == create_post_response.json()["post_id"]
    )
    assert (
        delete_post_response.json()["author_id"]
        == create_post_response.json()["author_id"]
    )
    assert delete_post_response.json()["text"] == create_post_response.json()["text"]
    assert (
        delete_post_response.json()["reactions"]
        == create_post_response.json()["reactions"]
    )

    delete_user_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert (delete_user_response.status_code ==
            HTTPStatus.OK)
    assert delete_user_response.json()["first_name"] == user_payload["first_name"]
    assert delete_user_response.json()["last_name"] == user_payload["last_name"]
    assert delete_user_response.json()["email"] == user_payload["email"]
