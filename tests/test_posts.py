from fastapi import status


def test_create_ok(client, fill_db, bearer_token):
    post = {"content": "This is a test post, hope it works"}
    response = client.post("/posts",
                           json=post,
                           headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("content") == post["content"]


def test_create_unauthorized(client, fill_db):
    post = {"content": "This is a test post, hope it works"}
    response = client.post("/posts", json=post)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Not authenticated"


def test_create_empty_content(client, fill_db, bearer_token):
    post = {"content": ""}
    response = client.post("/posts",
                           json=post,
                           headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get("detail") == "Content is required"


def test_create_banned_content(client, fill_db, bearer_token):
    post = {"content": "I hate you all, you are stupid as fuck"}
    response = client.post("/posts",
                           json=post,
                           headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "Post contains inappropriate content"


def test_update_ok(client, fill_db, bearer_token):
    post_id = 0         # from fill_db
    new_content = {"content": "I've changed this post"}
    response = client.patch(f"/posts/{post_id}",
                            json=new_content,
                            headers={"Authorization": f"Bearer {bearer_token}"})

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("content") == "I've changed this post"
    assert response.json().get("last_modified") is not None


def test_update_empty_content(client, fill_db, bearer_token):
    post_id = 0
    post = {"content": ""}
    response = client.patch(f"/posts/{post_id}",
                           json=post,
                           headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get("detail") == "Content is required"


def test_update_unauthorized(client, fill_db):
    post_id = 0
    post = {"content": "I've changed this post"}
    response = client.patch(f"/posts/{post_id}", json=post)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json().get("detail") == "Not authenticated"


def test_update_inappropriate_content(client, fill_db, bearer_token):
    post_id = 0
    post = {"content": "I hate you all, you are stupid as fuck"}
    response = client.patch(f"/posts/{post_id}",
                            json=post,
                            headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json().get("detail") == "Post contains inappropriate content"


def test_update_not_owner(client, fill_db, bearer_token):
    post_id = 3         # from fill_db
    post = {"content": "Hey there, I was in Lviv yesterday"}

    response = client.patch(f"/posts/{post_id}",
                            json=post,
                            headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You are not the owner of this post"


def test_get_my_posts(client, fill_db, bearer_token):
    response = client.get("/posts/my",
                          headers={"Authorization": f"Bearer {bearer_token}"})
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 2


def test_get_all_posts(client, fill_db):
    response = client.get("/posts")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


def test_get_all_posts_no_page(client, fill_db):
    response = client.get("/posts?page=3")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Page not found"


def test_get_all_posts_page_lt1(client, fill_db):
    response = client.get("/posts?page=0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json().get("detail")[0].get("msg") == "Input should be greater than or equal to 1"


def test_read_post(client, get_test_db, fill_db):
    post_id = 1
    response = client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == post_id
    assert response.json().get("content") == "This is second post I'll use"
    assert response.json().get("created_at") == "2024-09-14T00:00:00"

    owner = response.json().get("owner")
    assert owner.get("id") == 0


def test_read_post_not_exists(client, fill_db):
    post_id = 999
    response = client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Post not found"


def test_get_post_comments_ok(client, fill_db):
    post_id = 1
    response = client.get(f"/posts/{post_id}/comments")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) >= 4


def test_get_post_comments_not_exists(client, get_test_db, fill_db):
    post_id = 999
    response = client.get(f"/posts/{post_id}/comments")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json().get("detail") == "Post not found"


def test_delete_post_ok(client, fill_db, bearer_token):
    post_id = 0
    response = client.delete(f"/posts/{post_id}",
                             headers={"Authorization": f"Bearer {bearer_token}"})

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_not_owner(client, fill_db, bearer_token):
    post_id = 3
    response = client.delete(f"/posts/{post_id}",
                             headers={"Authorization": f"Bearer {bearer_token}"})

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json().get("detail") == "You are not the owner of this post"





