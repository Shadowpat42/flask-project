from app import app
from models import User, Post, Reaction
from sqlalchemy import exc
from app.forms import CreateUserForm, CreatePostForm, CreateReactionForm
from flask import request, Response, url_for, render_template
from http import HTTPStatus
import matplotlib.pyplot as plt
import json
import requests


@app.route("/")
def index():
    return render_template("index.html", USERS=User.all())


@app.post("/user/create")
def user_create():
    data = request.get_json()
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data["email"]

    if not User.is_valid_email(email):
        return Response(status=HTTPStatus.BAD_REQUEST)

    user = User(
        first_name=first_name, 
        last_name=last_name, 
        email=email
    )
    user.save()  # .save() method also can be used in 26 line after constructor call

    response = Response(
        json.dumps(user.json()),  # Flask.jsonify is good alternative
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/user/<int:user_id>")
def get_user(user_id):
    user = User.get_by_id(user_id)
    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)
    else:
        response = Response(
            json.dumps(user.json()),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response


@app.post("/post/create")
def post_create():
    data = request.get_json()
    author_id = data["author_id"]
    user = User.get_by_id(author_id)

    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    text = data["text"]

    try:
        post = Post(
            author_id=author_id, 
            text=text
        )
        post.save()

        response = Response(
            json.dumps(post.json()),
            mimetype="application/json",
            status=HTTPStatus.OK,
        )
        return response
    # exc.IntegrityError raised when the foreign key (author_id) refers to a non-existent user
    except exc.IntegrityError:
        return Response(status=HTTPStatus.BAD_REQUEST)        


@app.get("/post/<int:user_id>/<int:post_id>")
def get_post(user_id, post_id):
    post = Post.get_by_id(post_id)

    if post is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    response = Response(
        json.dumps(post.json()),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.delete("/post/<int:user_id>/<int:post_id>")
def delete_post(user_id, post_id):
    post = Post.get_by_id(post_id)

    if post is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    post_json = post.json()
    post.delete()

    response = Response(
        json.dumps(post_json),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )

    return response


@app.post("/post/<int:author_id>/<int:post_id>/reaction")
def reaction(author_id, post_id):
    data = request.get_json()

    user = User.get_by_id(data["user_id"])

    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    user_reaction = data["reaction"]
    if Reaction.is_valid_reaction(user_reaction) is False:
        return Response(status=HTTPStatus.BAD_REQUEST)

    try:
        reaction = Reaction(
            user_id=user.id,
            post_id=post_id, 
            reaction=user_reaction
        )
        reaction.save()
        return Response(status=HTTPStatus.OK)
    
    except exc.IntegrityError:
        return Response(status=HTTPStatus.BAD_REQUEST)


@app.get("/user/<int:user_id>/posts")
def get_user_posts(user_id):
    data = request.get_json()
    sort = data["sort"]
    user = User.get_by_id(user_id)

    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)
    
    if sort == "asc":
        posts = Post.get_by_user_id(user.id)
    elif sort == "desc":
        posts = Post.get_by_user_id(user.id, desc=True)
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)

    response = Response(
        json.dumps({"posts": [post.json() for post in posts]}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/leaderboard")
def get_users_leaderboard():
    data = request.get_json()
    leaderboard_type = data["type"]
    if leaderboard_type == "list":
        sort = data["sort"]
        if sort == "asc":
            users = User.get_by_reactions()
        elif sort == "desc":
            users = User.get_by_reactions(desc=True)
        else:
            return Response(status=HTTPStatus.BAD_REQUEST)

        leaderboard = [user.json() for user in users]

        response = Response(
            json.dumps(
                {
                    "users": leaderboard,
                }
            ),
            status=HTTPStatus.OK,
            mimetype="application/json",
        )
        return response

    elif leaderboard_type == "graph":
        users = User.get_by_reactions()
        fig, ax = plt.subplots()

        user_names = [
            f"{user.first_name} {user.last_name} ({user.id})" for user in users
        ]
        user_total_reactions = [user.total_reactions for user in users]

        ax.bar(user_names, user_total_reactions)
        ax.set_ylabel("User total reactions")
        ax.set_title("User leaderboard by total reactions")

        plt.savefig("app/static/users_leaderboard.png")
        return Response(
            f"""<img src= "{url_for('static', filename='users_leaderboard.png')}">""",
            status=HTTPStatus.OK,
            mimetype="text/html",
        )
    else:
        return Response(status=HTTPStatus.BAD_REQUEST)


@app.delete("/user/<int:user_id>")
def delete_user(user_id):
    user = User.get_by_id(user_id)
    
    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)
    else:
        user_json = user.json()
        user.delete()
        response = Response(
            json.dumps(user_json),
            HTTPStatus.OK,
            mimetype="application/json",
        )
        return response


@app.get("/front/user/<int:user_id>")
def front_get_user(user_id):
    user = User.get_by_id(user_id)

    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)

    posts = Post.get_by_user_id(user.id)

    return render_template("get_user.html", user=user, user_posts=posts, USERS=User.all())


@app.route("/front/user/create", methods=["GET", "POST"])
def front_user_create():
    user_data = None
    form = CreateUserForm()
    if form.validate_on_submit():
        user_data = dict()
        user_data["first_name"] = form.first_name.data
        user_data["last_name"] = form.last_name.data
        user_data["email"] = form.email.data
        response = requests.post(f"http://127.0.0.1:5000/user/create", json=user_data)
        if response.status_code not in {HTTPStatus.OK, HTTPStatus.CREATED}:
            return "Invalid email"
    return render_template(
        "create_user_form.html", form=form, user_data=user_data, USERS=User.all()
    )


@app.get("/front/post/<int:user_id>/<int:post_id>")
def front_get_post(user_id, post_id):
    user = User.get_by_id(user_id)

    if user is None:
        return Response(status=HTTPStatus.NOT_FOUND)
    
    post = Post.get_by_id(post_id)

    if post is None:
        return Response(status=HTTPStatus.NOT_FOUND)
    
    return render_template("get_post.html", post=post, user=user, USERS=User.all())


@app.route("/front/post/create", methods=["GET", "POST"])
def front_post_create():
    post_data = None
    form = CreatePostForm()
    if form.validate_on_submit():
        post_data = dict()
        post_data["author_id"] = int(form.author_id.data)
        post_data["text"] = form.text.data
        response = requests.post(f"http://127.0.0.1:5000/post/create", json=post_data)
        if response.status_code not in {HTTPStatus.OK, HTTPStatus.CREATED}:
            return "Invalid author_id"
    return render_template(
        "create_post_form.html", form=form, post_data=post_data, USERS=User.all()
    )


@app.route("/front/post/<int:user_id>/<int:post_id>/reaction", methods=["GET", "POST"])
def front_reaction_create(user_id, post_id):
    user = User.get_by_id(user_id)
    post = Post.get_by_id(post_id)
    reaction_data = None
    form = CreateReactionForm()

    if form.validate_on_submit():
        reaction_data = dict()
        reaction_data["user_id"] = int(form.user_id.data)
        reaction_data["reaction"] = form.reaction.data
        response = requests.post(                                        # what for sync http request?   
            f"http://127.0.0.1:5000/post/{user_id}/{post_id}/reaction",  # you can call your function
            json=reaction_data,
        )
        if response.status_code not in {HTTPStatus.OK, HTTPStatus.CREATED}:
            return "Invalid reaction or user_id"

    return render_template(
        "create_reaction_form.html",
        form=form,
        reaction_data=reaction_data,
        USERS=User.all(),
        user=user,
        post=post,
    )
