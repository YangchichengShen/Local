import sqlite3
import json

# create the users table if it doesn't exist
def initialize_db():
    conn = sqlite3.connect("reddit.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userID TEXT PRIMARY KEY,
            subreddits TEXT,
            posts TEXT,
            comments TEXT,
            interest_score REAL,
            sorted_interests TEXT
        )
    """)

    conn.commit()
    conn.close()


# updates only changed fields for given userID. if userID doesn't exist, it inserts the entire scrape
def upsert_user_data_if_changed(user_data):
    conn = sqlite3.connect("reddit.db")
    cursor = conn.cursor()

    userID = user_data["userID"]

    # convert new data to JSON for comparison
    new_data = {
        "subreddits": json.dumps(user_data["subreddits"]),
        "posts": json.dumps(user_data["posts"]),
        "comments": json.dumps(user_data["comments"]),
        "interest_score": user_data["interest_score"],
        "sorted_interests": json.dumps(user_data["sorted_interests"])
    }

    # fetch current row if exists
    cursor.execute("SELECT * FROM users WHERE userID = ?", (userID,))
    row = cursor.fetchone()

    # if user doesn't exist, insert everything
    if row is None:
        print(f"Inserting new user: {userID}")
        cursor.execute("""
            INSERT INTO users (userID, subreddits, posts, comments, interest_score, sorted_interests)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            userID,
            new_data["subreddits"],
            new_data["posts"],
            new_data["comments"],
            new_data["interest_score"],
            new_data["sorted_interests"]
        ))
    else:
        # column order: userID, subreddits, posts, comments, interest_score, sorted_interests
        existing_data = {
            "subreddits": row[1],
            "posts": row[2],
            "comments": row[3],
            "interest_score": row[4],
            "sorted_interests": row[5]
        }

        # determine which fields have changed in new scrape
        changed_fields = {}
        for key in new_data:
            if new_data[key] != existing_data[key]:
                changed_fields[key] = new_data[key]

        # if anything changed, build and run an UPDATE statement
        if changed_fields:
            print(f"Updating fields for user {userID}: {list(changed_fields.keys())}")
            set_clause = ", ".join(f"{field} = ?" for field in changed_fields)
            values = list(changed_fields.values())
            values.append(userID)

            cursor.execute(f"""
                UPDATE users
                SET {set_clause}
                WHERE userID = ?
            """, values)
        else:
            print(f"No changes detected for user {userID}")

    conn.commit()
    conn.close()
