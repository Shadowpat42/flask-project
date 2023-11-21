from app import app, USERS, models
from flask import request, Response
from http import HTTPStatus
import json
import copy


@app.route("/")
def index():
    return "<h1>Hello world</h1>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(id, first_name, last_name, email)

    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "total_reactions": user.total_reactions,
                "posts": user.posts,
            }
        ),
        HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/user/<int:user_id>")
def get_user(user_id):
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    else:
        user = USERS[user_id]
        response = Response(
            json.dumps(
                {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "total_reactions": user.total_reactions,
                    "posts": user.posts,
                }
            ),
            HTTPStatus.CREATED,
            mimetype="application/json",
        )
        return response


@app.post("/post/create")
def post_create():
    data = request.get_json()
    author_id = data["author_id"]

    if author_id < 0 or author_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[int(author_id)]
    text = data["text"]

    post_id = len(user.posts)

    post = models.Post(author_id, text)
    post_to_dict = {
        "post_id": post_id,
        "author_id": post.author_id,
        "text": post.text,
        "reactions": [],
    }

    user.posts.append(post_to_dict)

    response = Response(
        json.dumps(
            {
                "post_id": post_id,
                "author_id": post.author_id,
                "text": post.text,
                "reactions": post.reactions,
            }
        ),
        mimetype="application/json",
        status=HTTPStatus.CREATED,
    )

    return response


@app.get("/post/<int:user_id>/<int:post_id>")
def get_post(user_id, post_id):
    if (user_id < 0 or user_id >= len(USERS)) or (
        post_id < 0 or post_id > len(USERS[user_id].posts)
    ):
        return Response(status=HTTPStatus.NOT_FOUND)
    post = USERS[user_id].posts[post_id]
    response = Response(
        json.dumps(
            {
                "post_id": post["post_id"],
                "author_id": post["author_id"],
                "text": post["text"],
                "reactions": post["reactions"],
            }
        ),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )

    return response


@app.post("/post/<author_id>/<int:post_id>/reaction")
def reaction(author_id, post_id):
    data = request.get_json()
    user_id = int(data["user_id"])
    if user_id < 0 or user_id >= len(USERS):
        return Response(status=HTTPStatus.NOT_FOUND)
    reaction = data["reaction"]
    if reaction not in ["like", "dislike"]:
        return Response(status=HTTPStatus.BAD_REQUEST)
    post = USERS[int(author_id)].posts[post_id]
    reactions_to_dict = {
        "user_id": user_id,
        "reaction": reaction,
    }
    post["reactions"].append(reactions_to_dict)
    USERS[user_id].total_reactions += 1
    return Response(status=HTTPStatus.CREATED)


@app.get("/user/<int:user_id>/posts")
def get_posts(user_id):
    data = request.get_json()
    sort = data["sort"]
    user = USERS[user_id]
    posts = user.posts
    if sort == "asc":
        sorted_posts = sorted(posts, key=lambda x: len(x["reactions"]))
    elif sort == "desc":
        sorted_posts = sorted(posts, key=lambda x: len(x["reactions"]), reverse=True)
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
    response = Response(
        json.dumps({"posts": sorted_posts}),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_users():
    data = request.get_json()
    sort = data["sort"]
    if sort == "asc":
        sorted_users = sorted(USERS, key=lambda x: x.total_reactions)
    elif sort == "desc":
        sorted_users = sorted(USERS, key=lambda x: x.total_reactions, reverse=True)
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

    users_copy = copy.deepcopy(sorted_users)
    for user in users_copy:
        user.__dict__.pop("posts", None)

    response = Response(
        json.dumps(
            {
                "users": users_copy,
            },
            default=lambda x: x.__dict__,
            indent=None,
        ),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )
    return response
