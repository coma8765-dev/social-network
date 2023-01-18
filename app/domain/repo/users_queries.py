CREATE = """
INSERT INTO users 
          (email, password_hash, name) 
   VALUES ($1, $2, $3) 
RETURNING id
"""

UPDATE = """
UPDATE users SET 
   "name" = CASE WHEN $2::varchar IS NOT NULL THEN $2 ELSE "name" END,
   password_hash = CASE WHEN $3::varchar IS NOT NULL THEN $3 
                        ELSE password_hash END
WHERE id = $1
RETURNING id
"""

DELETE = "DELETE FROM users WHERE id = $1 RETURNING id"

GET = "SELECT * FROM users WHERE id = $1"

GET_WITH_PWD = "SELECT * FROM users WHERE email = $1"

EXISTS = "SELECT id FROM users WHERE email = $1"
