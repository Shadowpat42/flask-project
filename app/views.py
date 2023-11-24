from app import app, USERS, models
from flask import request, Response, url_for
from http import HTTPStatus
import matplotlib.pyplot as plt
import json
import copy


@app.route("/")
def index():
    return "<h1>Hello world</h1>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not models.User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = models.User(user_id, first_name, last_name, email)

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
    if models.User.is_valid_id(user_id) is False:
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

    if models.User.is_valid_id(author_id) is False:
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[int(author_id)]
    text = data["text"]
    post_id = len(user.posts)
    post = models.Post(post_id, author_id, text)
    user.add_post(post)

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
    if models.Post.is_valid_id(user_id, post_id) is False:
        return Response(status=HTTPStatus.NOT_FOUND)

    post = USERS[user_id].posts[post_id]
    response = Response(
        json.dumps(
            {
                "post_id": post_id,
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
    if models.User.is_valid_id(user_id) is False:
        return Response(status=HTTPStatus.NOT_FOUND)

    user_reaction = data["reaction"]
    if models.Reaction.is_valid_reaction(user_reaction) is False:
        return Response(status=HTTPStatus.BAD_REQUEST)

    reaction_obj = models.Reaction(post_id, user_id, user_reaction)
    USERS[int(author_id)].add_reaction(reaction_obj)

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
    leaderboard_type = data["type"]
    if leaderboard_type == "list":
        sort = data["sort"]
        if sort == "asc":
            sorted_users = sorted(USERS, key=lambda x: x.total_reactions)
        elif sort == "desc":
            sorted_users = sorted(USERS, key=lambda x: x.total_reactions, reverse=True)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)

        leaderboard = copy.deepcopy(sorted_users)
        for user in leaderboard:
            user.__dict__.pop("posts", None)

        response = Response(
            json.dumps(
                {
                    "users": leaderboard,
                },
                default=lambda x: x.__dict__,
                indent=None,
            ),
            status=HTTPStatus.CREATED,
            mimetype="application/json",
        )
        return response

    elif leaderboard_type == "graph":
        sorted_users = sorted(USERS, key=lambda x: x.total_reactions)
        leaderboard = copy.deepcopy(sorted_users)
        fig, ax = plt.subplots()

        user_names = [f"{user.first_name} {user.last_name} ({user.id})" for user in leaderboard]
        user_total_reactions = [user.total_reactions for user in leaderboard]

        ax.bar(user_names, user_total_reactions)
        ax.set_ylabel("User total reactions")
        ax.set_title("User leaderboard by total reactions")

        plt.savefig("app/static/users_leaderboard.png")
        return Response(
            f"""<img src= "{url_for('static', filename='users_leaderboard.png')}">""",
            status=HTTPStatus.CREATED,
            mimetype="text/html",
        )
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)
