# API Endpoints

## Users

### Create User
- **HTTP Method:** POST
- **URL:** `/users/`

### Retrieve User
- **HTTP Method:** GET
- **URL:** `/users/{user_id}/`

### Update User
- **HTTP Method:** PUT
- **URL:** `/users/{user_id}/`

### Delete User
- **HTTP Method:** DELETE
- **URL:** `/users/{user_id}/`

### Find User
- **HTTP Method:** GET
- **URL:** `/users/find_user/?username={username}`

## Posts

### List all posts
- **HTTP Method:** GET
- **URL:** `/posts/`

### Create a new post
- **HTTP Method:** POST
- **URL:** `/posts/`

### Retrieve a specific post
- **HTTP Method:** GET
- **URL:** `/posts/{post_id}/`

### Update a specific post
- **HTTP Method:** PUT
- **URL:** `/posts/{post_id}/`

### Partially update a specific post
- **HTTP Method:** PATCH
- **URL:** `/posts/{post_id}/`

### Delete a specific post
- **HTTP Method:** DELETE
- **URL:** `/posts/{post_id}/`

## Comments

### Create Comment
- **HTTP Method:** POST
- **URL:** `/comments/`
- **Action Method:** create

### Retrieve Comment by ID or Author's Username
- **HTTP Method:** GET
- **URL (by Comment ID):** `/comments/{comment_id}/`
- **URL (by Author's Username):** `/comments/{author_username}/`
- **Action Method:** retrieve

### Update Comment by ID
- **HTTP Method:** PUT or PATCH
- **URL:** `/comments/{comment_id}/`
- **Action Method:** update

### Delete Comment by ID
- **HTTP Method:** DELETE
- **URL:** `/comments/{comment_id}/`
- **Action Method:** destroy

### List Comments (All Comments)
- **HTTP Method:** GET
- **URL:** `/comments/`


# Friend Request API Endpoints

Here are the API endpoints for managing friend requests:

- **List all friend requests**:
  - HTTP Method: `GET`
  - Endpoint: `/api/friend-requests/`

- **Create a new friend request**:
  - HTTP Method: `POST`
  - Endpoint: `/api/friend-requests/`

- **Retrieve a specific friend request**:
  - HTTP Method: `GET`
  - Endpoint: `/api/friend-requests/{request_id}/`
  - Replace `{request_id}` with the actual request ID to retrieve a specific friend request.

- **Update a specific friend request**:
  - HTTP Method: `PUT`
  - Endpoint: `/api/friend-requests/{request_id}/`
  - Replace `{request_id}` with the actual request ID to update a specific friend request.

- **Partial update of a specific friend request**:
  - HTTP Method: `PATCH`
  - Endpoint: `/api/friend-requests/{request_id}/`
  - Replace `{request_id}` with the actual request ID to partially update a specific friend request.

- **Delete a specific friend request**:
  - HTTP Method: `DELETE`
  - Endpoint: `/api/friend-requests/{request_id}/`
  - Replace `{request_id}` with the actual request ID to delete a specific friend request.


### Retrieve Comments on a Particular Post
- **HTTP Method:** GET
- **URL:** `/comments/comments_on_post/{post_id}/`
- **Action Method:** comments_on_post

