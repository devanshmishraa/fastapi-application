from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, DeletePost, PostResponse

app = FastAPI()


text_posts = {
    1: {"title": "New post", "content": "Cool test post about FastAPI."},
    2: {"title": "Learning Python", "content": "Today I learned about dictionaries and functions."},
    3: {"title": "FastAPI Tips", "content": "FastAPI makes building APIs super fast and clean!"},
    4: {"title": "My First API", "content": "Just deployed my first API using Uvicorn and FastAPI."},
    5: {"title": "Async in Python", "content": "Understanding async/await can really improve performance."},
    6: {"title": "SQLAlchemy Intro", "content": "ORMs make database interactions much easier."},
    7: {"title": "Docker for Devs", "content": "Containerizing apps simplifies deployment."},
    8: {"title": "Frontend vs Backend", "content": "Exploring how APIs power modern web apps."},
    9: {"title": "APIs Everywhere", "content": "APIs connect services across the internet — they’re the glue of modern apps."},
    10: {"title": "Deploying to Render", "content": "Quick guide: how to deploy a FastAPI app for free."}
}

@app.get("/posts")
def get_all_posts(limit: int=None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{id}")
def get_a_post(id:int) -> PostResponse:
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)


@app.post("/posts") 
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title":post.title, "content": post.content}
    text_posts[max(text_posts.keys(), default=0)+1] = new_post
    return new_post
    

@app.delete("/posts")
def delete_post(post: DeletePost):
    if post.id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not available to delete")
    deleted_post = text_posts.pop(post.id)
    return {"message": f"Post with id {post.id} deleted successfully", "post": deleted_post}