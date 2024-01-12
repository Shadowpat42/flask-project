from http import HTTPStatus
import requests
from uuid import uuid4

ENDPOINT = "http://127.0.0.1:5000"


def create_user_payload():
    return {
        "first_name": "Vladimir" + str(uuid4()),
        "last_name": "Jonson" + str(uuid4()),
        "email": "test@test.ru",
    }


def test_user_create():
    payload = create_user_payload()
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.OK
    user_data = create_response.json()
    user_id = user_data["id"]
    assert user_data["first_name"] == payload["first_name"]
    assert user_data["last_name"] == payload["last_name"]
    assert user_data["email"] == payload["email"]

    get_response = requests.get(f"{ENDPOINT}/user/{user_id}")
    assert get_response.json()["first_name"] == payload["first_name"]
    assert get_response.json()["last_name"] == payload["last_name"]
    assert get_response.json()["email"] == payload["email"]

    delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_response.status_code == HTTPStatus.OK
    assert delete_response.json()["first_name"] == payload["first_name"]
    assert delete_response.json()["last_name"] == payload["last_name"]
    assert delete_response.json()["email"] == payload["email"]
    assert delete_response.json()["status"] == "deleted"


def test_user_create_wrong_data():
    payload = create_user_payload()
    payload["email"] = "testtest.ru"  # wrong email
    create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
    assert create_response.status_code == HTTPStatus.BAD_REQUEST


def test_get_user_posts():
    user_payload = create_user_payload()
    user_create = requests.post(f"{ENDPOINT}/user/create", json=user_payload)
    user_id = user_create.json()["id"]
    assert user_create.status_code == HTTPStatus.OK

    post_payload = {"author_id": user_id, "text": "Example text for testing post"}

    post_create = requests.post(f"{ENDPOINT}/post/create", json=post_payload)
    post_id = post_create.json()["post_id"]
    assert (post_create.status_code ==
            HTTPStatus.OK)
    assert post_create.json()["author_id"] == post_payload["author_id"]
    assert post_create.json()["text"] == post_payload["text"]

    get_user_posts = requests.get(
        f"{ENDPOINT}/user/{user_id}/posts", json={"sort": "asc"}
    )
    assert get_user_posts.status_code == HTTPStatus.OK
    assert isinstance(get_user_posts.json()["posts"], list)
    assert len(get_user_posts.json()["posts"]) == 1

    delete_user_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
    assert delete_user_response.status_code == HTTPStatus.OK

    delete_post_response = requests.delete(f"{ENDPOINT}/post/{user_id}/{post_id}")
    assert delete_post_response.status_code == HTTPStatus.OK


def test_get_users_leaderboard():
    n = 3
    test_users = []
    for _ in range(n):
        payload = create_user_payload()
        create_response = requests.post(f"{ENDPOINT}/user/create", json=payload)
        assert create_response.status_code == HTTPStatus.OK
        test_users.append(create_response.json()["id"])

    payload_leaderboard = {
        "type": "list",
        "sort": "asc",
    }

    get_response = requests.get(
        f"{ENDPOINT}/users/leaderboard", json=payload_leaderboard
    )

    leaderboard = get_response.json()["users"]
    assert isinstance(leaderboard, list)
    assert len(leaderboard) == n

    for user_id in test_users:
        delete_response = requests.delete(f"{ENDPOINT}/user/{user_id}")
        assert delete_response.status_code == HTTPStatus.OK
