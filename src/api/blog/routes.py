from src import app, db
from src.models.db_models import user, posts
from src.utils.helper import validate_title_and_description
from src.utils.const import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import jsonify, request, abort


@app.route('/api/v1/get-profile', methods=['GET'])
@jwt_required()
def get_profile():
    '''
    This route deals for with getting the details of current user.
    '''

    # Gets the current user's user id
    user_id = get_jwt_identity()
    current_user = user.query.filter_by(id=user_id).one_or_none()

    # If current user is empty
    if not current_user:
        return jsonify(current_user_error_message)
    else:
        # Articles of the current user logged in
        articles = {"Title": article.title for article in current_user.articles}

        # return's the response
        return jsonify({
            "Name": current_user.name,
            "Email": current_user.email,
            "posts": articles
        })


@app.route('/api/v1/create-post', methods=['POST'])
@jwt_required()
def create_post():
    '''
    This route deals with the creating and inserting posts in DB
    '''

    # Gets the request data
    title = request.json.get("title", None)
    description = request.json.get("description", None)
    title_and_description = validate_title_and_description(title, description)

    # Gets current user
    user_id = get_jwt_identity()
    current_user = user.query.filter_by(id=user_id).one_or_none()

    # Validates the title and description
    if title_and_description:
        post = posts(title=title, description=description,
                     author=current_user.id)

        # Insert into database
        db.session.add(post)
        db.session.commit()

        # Response
        return jsonify(post_added_sucessfully_message)

    # Response
    return jsonify(post_added_failed_message)


@app.route('/api/v1/get-posts', methods=["GET"])
def get_posts():
    '''
    This route deals with the getting posts from the DB
    '''
    # Gets all the posts
    all_posts = posts.query.all()

    # check if posts are avaliable or not
    if len(all_posts):
        all_posts_dict = {
            post.title: {
                "description": post.description,
                "Author": (user.query.filter_by(id=post.author).one_or_none()).name} for post in all_posts
        }
        response = jsonify(all_posts_dict)
    else:
        response = jsonify(posts_error_message)

    # Returns response.
    return response


@app.route('/api/v1/<int:post_id>/get-post', methods=["GET"])
def get_post(post_id):
    '''
    This route deals with getting a single post.
    '''
    # Gets the post for corresponding post id
    post = posts.query.filter_by(id=post_id).one_or_none()

    # Validation of post
    if post:
        response = jsonify({
            post.title: {
                "description": post.description,
                "Author": (user.query.filter_by(id=post.author).one_or_none()).name
            }
        })
    else:
        response = jsonify(posts_not_found_message)

    # Response
    return response


@app.route('/api/v1/<int:post_id>/update-post', methods=["GET", "POST"])
@jwt_required()
def update_post(post_id):
    '''
    This route deals with update of the post for corresponding post id.
    '''

    # Validation of post with corresponding post id
    post = posts.query.filter_by(id=post_id).one_or_none()

    # checks if post is valid.
    if post:
        author_id = (user.query.filter_by(id=post.author).one_or_none()).id
        current_user_id = get_jwt_identity()

        # Check if the current is the Author of the post.
        if current_user_id != author_id:
            return jsonify(unauthorized_update), 403
    else:
        return jsonify(posts_not_found_message)

    if request.method == 'GET':
        # Makes changes in DB
        if post:
            response = jsonify({
                post.title: {
                    "description": post.description,
                    "Author": (user.query.filter_by(id=post.author).one_or_none()).name
                }
            })
        else:
            response = jsonify(posts_not_found_message)

        # Response
        return response

    elif request.method == 'POST':
        new_title = request.json.get("title", None)
        new_description = request.json.get("description", None)

        # Validation of title and description.
        if validate_title_and_description(new_title, new_description):
            post.title = new_title
            post.description = new_description
            # Makes changes in DB
            db.session.commit()

            return jsonify(posts_updated_sucessfully)

        return jsonify(post_added_failed_message)


@app.route('/api/v1/<int:post_id>/delete-post', methods=["GET", "POST"])
@jwt_required()
def delete_post(post_id):
    '''
    This route deals with the deletion of the post
    '''

    post = posts.query.filter_by(id=post_id).one_or_none()

    # Checks if post is valid.
    if post:
        author_id = (user.query.filter_by(id=post.author).one_or_none()).id
        current_user_id = get_jwt_identity()

        # Check if the current is the Author of the post.
        if current_user_id != author_id:
            return jsonify(unauthorized_delete), 403
    else:
        return jsonify(posts_not_found_message)

    # Makes changes in DB
    db.session.delete(post)
    db.session.commit()

    return jsonify(post_deleted_message)
