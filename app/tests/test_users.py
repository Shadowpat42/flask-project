from http import HTTPStatus
import requests
import random
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
    assert post_create.status_code == HTTPStatus.OK
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


def test_get_users_leaderboard_list():
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


def test_get_users_leaderboard_graph():
    payload_user_1 = create_user_payload()
    payload_user_2 = create_user_payload()
    user_create_1 = requests.post(f"{ENDPOINT}/user/create", json=payload_user_1)
    assert user_create_1.status_code == HTTPStatus.OK
    user_id_1 = user_create_1.json()["id"]
    user_create_2 = requests.post(f"{ENDPOINT}/user/create", json=payload_user_2)
    assert user_create_2.status_code == HTTPStatus.OK
    user_id_2 = user_create_2.json()["id"]

    post_payload = {
        "author_id": user_id_1,
        "text": "Example text for testing",
    }

    create_post = requests.post(f"{ENDPOINT}/post/create", json=post_payload)
    post_id = create_post.json()["post_id"]
    assert create_post.status_code == HTTPStatus.OK

    reaction_payload_1 = {
        "user_id": user_id_1,
        "reaction": random.choice(["like", "dislike"]),
    }

    reaction_payload_2 = {
        "user_id": user_id_2,
        "reaction": random.choice(["like", "dislike"]),
    }

    for _ in range(5):
        create_reaction_user_1 = requests.post(
            f"{ENDPOINT}/post/{user_id_1}/{post_id}/reaction", json=reaction_payload_1
        )
        assert create_reaction_user_1.status_code == HTTPStatus.OK

    for _ in range(3):
        create_reaction_user_2 = requests.post(
            f"{ENDPOINT}/post/{user_id_1}/{post_id}/reaction", json=reaction_payload_2
        )
        assert create_reaction_user_2.status_code == HTTPStatus.OK

    leaderboard_graph_payload = {
        "type": "graph",
        "sort": "asc",
    }

    get_leaderboard = requests.get(
        f"{ENDPOINT}/users/leaderboard", json=leaderboard_graph_payload
    )
    assert get_leaderboard.status_code == HTTPStatus.OK
    assert get_leaderboard.text == '<img src= "/static/users_leaderboard.png">'

    graph = requests.get(f"{ENDPOINT}/static/users_leaderboard.png")
    assert graph.status_code == HTTPStatus.OK

    delete_user_1 = requests.delete(f"{ENDPOINT}/user/{user_id_1}")
    assert delete_user_1.status_code == HTTPStatus.OK

    delete_user_2 = requests.delete(f"{ENDPOINT}/user/{user_id_2}")
    assert delete_user_2.status_code == HTTPStatus.OK

    delete_post_response = requests.delete(f"{ENDPOINT}/post/{user_id_1}/{post_id}")
    assert delete_post_response.status_code == HTTPStatus.OK
