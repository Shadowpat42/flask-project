from http import HTTPStatus
import requests
from uuid import uuid4
import random

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Vladimir" + str(uuid4()),
        "last_name": "Jonson" + str(uuid4()),
        "email": "test@test.ru",
        "status": "created",
    }


def test_reaction_create():
    user_payload = create_user_payload()
    create_user = requests.post(f"{ENDPOINT}/user/create", json=user_payload)
    user_id = create_user.json()["id"]
    assert create_user.status_code == HTTPStatus.OK
    assert create_user.json()["total_reactions"] == 0

    post_payload = {
        "author_id": user_id,
        "text": "Example text for testing post",
    }

    create_post = requests.post(f"{ENDPOINT}/post/create", json=post_payload)
    post_id = create_post.json()["post_id"]
    assert create_post.status_code == HTTPStatus.OK

    reaction_payload = {
        "user_id": user_id,
        "reaction": random.choice(["like", "dislike"]),
    }

    for _ in range(5):
        # При создании реакции возвращается только статус запроса!
        create_reaction = requests.post(
            f"{ENDPOINT}/post/{user_id}/{post_id}/reaction", json=reaction_payload
        )
        assert create_reaction.status_code == HTTPStatus.OK

    user_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert user_response.status_code == HTTPStatus.OK
    assert user_response.json()["total_reactions"] == 5

    delete_user_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_user_response.status_code == HTTPStatus.OK

    delete_post_response = requests.delete(f"{ENDPOINT}/post/{user_id}/{post_id}")
    assert delete_post_response.status_code == HTTPStatus.OK
