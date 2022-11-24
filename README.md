# assesment

## clone repo

```
git clone https://github.com/Imran-456/assesment.git
```
## Installation of dependencies

```
pip install -r requirements.txt
```

## Run the app
```
flask run
```

## Brief description of API's

'/api/v1/register' -> [POST] -> registers a new user. 

'/api/v1/register' -> [POST] -> logins a user.

'/api/v1/get-profile' -> [GET] -> Gets the profile of current logged-in user

'/api/v1/create-post' -> [POST] -> creates a new post

'/api/v1/get-posts' -> [GET] -> Fetches all the avaliable posts

'/api/v1/<int:post_id>/get-post' -> [GET] -> Fetches the post with particular post id

'/api/v1/<int:post_id>/get-post' -> [GET] -> Fetches posts with a particular post id

'/api/v1/<int:post_id>/update-post' -> [POST, GET] -> lets us to fetch the post and update it with a particular post id

'/api/v1/<int:post_id>/delete-post' -> ['GET'] -> deletes the post with particular post id


