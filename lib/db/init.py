import sqlite3
from textwrap import dedent
from lib.db.db import insert_user, insert_post, insert_comment, insert_category, insert_tag, insert_post_tags

def create(db: sqlite3.Connection):
    create_users_sql = dedent(f"""
        --sql
        CREATE TABLE User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255),
            bio TEXT,
            profile_picture VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    create_posts_sql = dedent(f"""
        --sql
        CREATE TABLE Post (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT NOT NULL,
            category_id INTEGER,
            published_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES User(id),
            FOREIGN KEY (category_id) REFERENCES Category(id)
        );
    """)
    create_comments_sql = dedent(f"""
        --sql
        CREATE TABLE Comment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES Post(id),
            FOREIGN KEY (user_id) REFERENCES User(id)
        );
    """)
    create_categories_sql = dedent(f"""
        --sql
        CREATE TABLE Category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    create_tags_sql = dedent(f"""
        --sql
        CREATE TABLE Tag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    create_post_tags = dedent("""
        --sql
        CREATE TABLE PostTags (
            post_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            PRIMARY KEY (post_id, tag_id),
            FOREIGN KEY (post_id) REFERENCES Post(post_id),
            FOREIGN KEY (tag_id) REFERENCES Tag(id)
        );
    """)

    db.executescript("\n".join((
        create_users_sql,
        create_posts_sql,
        create_post_tags,
        create_tags_sql,
        create_comments_sql,
        create_categories_sql
    )))

    db.commit()

def populate(db: sqlite3.Connection):
    # Sample data for users
    users = [
        {"username": "d3vr10", "password": "tomatedivino", "email": "d3vr10@gmail.com"},
        {"username": "johndoe", "password": "password123", "email": "johndoe@example.com"},
        {"username": "janedoe", "password": "password456", "email": "janedoe@example.com"},
    ]
    for user in users:
        insert_user(db, user)

    # Sample data for posts
    posts = [
        {"user_id": 1, "title": "First Post", "content": "This is the first post."},
        {"user_id": 2, "title": "Second Post", "content": "This is the second post."},
        {"user_id": 3, "title": "Third Post", "content": "This is the third post."},
    ]
    for post in posts:
        insert_post(db, post)

    # Sample data for comments
    comments = [
        {"user_id": 1, "post_id": 1, "content": "Great post!"},
        {"user_id": 2, "post_id": 1, "content": "Thanks for sharing."},
        {"user_id": 3, "post_id": 2, "content": "Interesting read."},
    ]
    for comment in comments:
        insert_comment(db, comment)

    # Sample data for categories
    categories = [
        {"name": "Technology"},
        {"name": "Lifestyle"},
        {"name": "Education"},
    ]
    for category in categories:
        insert_category(db, category)

    # Sample data for tags
    tags = [
        {"name": "Python"},
        {"name": "Programming"},
        {"name": "Tutorial"},
    ]
    for tag in tags:
        insert_tag(db, tag)

    # Sample data for post tags
    post_tags = [
        {"post_id": 1, "tag_id": 1},
        {"post_id": 1, "tag_id": 2},
        {"post_id": 2, "tag_id": 2},
        {"post_id": 3, "tag_id": 3},
    ]
    for post_tag in post_tags:
        insert_post_tags(db, post_tag)


def check_init(db: sqlite3.Connection):
    #Creation
    tables = ["User", "Post", "Tag", "PostTags", "Category", "Comment"]
    cursor = db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    rows = list(map(
        lambda x: x[0], 
        cursor.fetchall(),
    ))

    for table in tables:
        if table not in rows:
            raise sqlite3.Error(f'Table "{table}" does not exist')


def init():
    with sqlite3.connect(":memory:") as db:
        try: 
            check_init(db)
        except sqlite3.Error as err:
            create(db)
            populate(db)