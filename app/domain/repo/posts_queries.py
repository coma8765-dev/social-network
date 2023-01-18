CREATE = """
INSERT INTO posts (created_by, title, body) 
           VALUES ($1, $2, $3) 
RETURNING id, create_date
"""

DELETE = "DELETE FROM posts WHERE id = $1 RETURNING id"

UPDATE = """
UPDATE posts SET (
    title,
    body
) = (
    COALESCE($2, title),
    COALESCE($3, body)
)
WHERE id = $1
RETURNING id
"""

GET = """
SELECT p.*, pe."like" as liked 
FROM posts p 
LEFT JOIN post_estimates pe on p.id = pe.post_id AND pe.user_id = $2
WHERE p.id = $1
"""

LIST = """
SELECT posts.*, pe."like" AS liked
FROM posts 
LEFT JOIN post_estimates pe on posts.id = pe.post_id AND pe.user_id = $3
LIMIT $2 + 1
OFFSET $1::INTEGER * $2::INTEGER
"""

REMOVE_ESTIMATE = """
DELETE FROM post_estimates WHERE post_id = $1 AND  user_id = $2
"""

ESTIMATE = """
with s as (DELETE FROM post_estimates WHERE post_id = $1 AND user_id = $2)
INSERT
INTO post_estimates (post_id, user_id, "like")
VALUES ($1, $2, $3);
"""
