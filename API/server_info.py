import psycopg2
from psycopg2 import sql
import pandas as pd

def send_server(df_posts, df_users, df_comments, df_freq):
    dbname = "InstagramDB"
    user = "postgres"
    password = "admin"
    host = "localhost"
    port = "5432"

    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cursor = connection.cursor()

        # Post Info
        existing_posts = set()
        cursor.execute("SELECT post_link FROM post_info_table")
        rows = cursor.fetchall()
        for row in rows:
            existing_posts.add(row[0])

        for index, row in df_posts.iterrows():
            if row['post_link'] not in existing_posts:
                insert_query = sql.SQL("""
                    INSERT INTO post_info_table (post_link, post_owner_name, post_owner_link, post_num_like, post_num_comment, post_datetime, pos, neg)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """)
                try:
                    cursor.execute(insert_query, (row['post_link'], row['post_owner_name'], row['post_owner_link'], row['post_num_like'], row['post_num_comment'], row['post_datetime'], row['pos'], row['neg']))
                except Exception as e:
                    print("Error inserting post info:", e)
                    continue
            else:
                print(f"Post URL {row['post_link']} already exists in the table.")

        # User Info
        existing_users = set()
        cursor.execute("SELECT user_name FROM users_info_table")
        rows = cursor.fetchall()
        for row in rows:
            existing_users.add(row[0])

        for index, row in df_users.iterrows():
            if row['user_name'] not in existing_users:
                insert_query = sql.SQL("""
                    INSERT INTO users_info_table (user_name, user_profile_link)
                    VALUES (%s, %s)
                """)
                try:
                    cursor.execute(insert_query, (row['user_name'], row['user_profile_link']))
                except Exception as e:
                    print("Error inserting user info:", e)
                    continue
            else:
                print(f"User {row['user_name']} already exists in the table.")

        # Comment Info
        for index, row in df_comments.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO post_comments_table (user_name, user_comment, comment_datetime, comment_pred, post_link, comment_pred_cat, user_comment_pre, comment_pos, comment_neg)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """)
            try:
                cursor.execute(insert_query, (row['user_name'], row['user_comment'], row['comment_datetime'], row['comment_pred'], row['post_link'], row['comment_pred_cat'], row['user_comment_pre'], row['comment_pos'], row['comment_neg']))
            except Exception as e:
                print("Error inserting comment info:", e)
                continue

        # Frequency Info
        for index, row in df_freq.iterrows():
            insert_query = sql.SQL("""
                INSERT INTO freq_pre_table (word, pos_freq, neg_freq, total_freq, post_link)
                VALUES (%s, %s, %s, %s, %s)
            """)

            try:
                cursor.execute(insert_query, (row['word'], row['pos_freq'], row['neg_freq'], row['total_freq'], row['post_link']))
            except Exception as e:
                print("Error inserting frequency info:", e)
                continue

        connection.commit()
        print("Data inserted successfully")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

