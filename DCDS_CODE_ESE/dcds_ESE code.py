import mysql.connector
import tkinter as tk
from tkinter import messagebox, Listbox, simpledialog

# MySQL connection
conn = mysql.connector.connect(host='localhost', user='root', password='123456', database='project_data')
cursor = conn.cursor()

# Color scheme
bg_color = "#FFF7D1"
button_color = "#FFB0B0"
text_color = "black"

# Offset for opening windows in new positions
window_offset = 30
window_count = 0


# Helper function to center windows with offset
def center_window(window):
    global window_count
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2) + (window_offset * window_count)
    y = (window.winfo_screenheight() // 2) - (height // 2) + (window_offset * window_count)
    window.geometry(f"{width}x{height}+{x}+{y}")
    window_count += 1


def home_page():
    global window_count
    window_count = 0

    home = tk.Tk()
    home.title("Social Media App")
    home.geometry("400x400")
    home.configure(bg=bg_color)

    tk.Label(home, text="Social Media CRUD App", font=("Arial", 16), bg=bg_color, fg=text_color).pack(pady=20)

    # Buttons to navigate to each table's CRUD page
    for page_name, page_func in [
        ("Users", users_page),
        ("Photos", photos_page),
        ("Tags", tags_page),
        ("Follows", follows_page),
        ("Comments", comments_page)
    ]:
        tk.Button(home, text=page_name, command=page_func, width=20, bg=button_color).pack(pady=10)

    center_window(home)
    home.mainloop()


def comments_page():
    def add_comment():
        comment_text = comment_text_entry.get()
        user_id = user_id_entry.get()
        photo_id = photo_id_entry.get()

        if comment_text and user_id and photo_id:
            try:
                cursor.execute(
                    "INSERT INTO comments (comment_text, user_id, photo_id, comment_created_at) VALUES (%s, %s, %s, NOW())",
                    (comment_text, user_id, photo_id)
                )
                conn.commit()
                messagebox.showinfo("Success", "Comment added successfully.")
                refresh_comments()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Input Error", "Comment text, User ID, and Photo ID are required.")

    def delete_comment():
        selected_items = comments_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a comment to delete.")
            return

        selected = comments_listbox.get(selected_items[0])
        comment_id = int(selected.split(",")[0].split(": ")[1])

        try:
            cursor.execute("DELETE FROM comments WHERE id = %s", (comment_id,))
            conn.commit()
            messagebox.showinfo("Success", "Comment deleted successfully.")
            refresh_comments()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_comments():
        comments_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, comment_text, user_id, photo_id, comment_created_at FROM comments")
        for comment in cursor.fetchall():
            comments_listbox.insert(tk.END, f"ID: {comment[0]}, Text: {comment[1]}, User ID: {comment[2]}, "
                                            f"Photo ID: {comment[3]}, Created At: {comment[4]}")

    # Window for Comments Page
    comments_window = tk.Toplevel()
    comments_window.title("Comments Page")
    comments_window.geometry("500x500")
    comments_window.configure(bg=bg_color)

    # Input fields for Comment Text, User ID, and Photo ID
    tk.Label(comments_window, text="Comment Text:", bg=bg_color, fg=text_color).pack(pady=5)
    comment_text_entry = tk.Entry(comments_window, bg="white")
    comment_text_entry.pack(pady=5)

    tk.Label(comments_window, text="User ID:", bg=bg_color, fg=text_color).pack(pady=5)
    user_id_entry = tk.Entry(comments_window, bg="white")
    user_id_entry.pack(pady=5)

    tk.Label(comments_window, text="Photo ID:", bg=bg_color, fg=text_color).pack(pady=5)
    photo_id_entry = tk.Entry(comments_window, bg="white")
    photo_id_entry.pack(pady=5)

    # CRUD buttons
    tk.Button(comments_window, text="Add Comment", command=add_comment, bg=button_color).pack(pady=5)
    tk.Button(comments_window, text="Delete Comment", command=delete_comment, bg=button_color).pack(pady=5)

    # Listbox to display comments
    comments_listbox = tk.Listbox(comments_window)
    comments_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
    refresh_comments()

    # Back button
    tk.Button(comments_window, text="Back to Home", command=comments_window.destroy, bg=button_color).pack(pady=10)
    center_window(comments_window)


# Remember to replace bg_color, text_color, button_color, and center_window function with your own configurations


def follows_page():
    def add_follow():
        follower_id = follower_id_entry.get()
        followee_id = followee_id_entry.get()

        if follower_id and followee_id:
            try:
                cursor.execute("INSERT INTO follows (follower_id, followee_id) VALUES (%s, %s)",
                               (follower_id, followee_id))
                conn.commit()
                messagebox.showinfo("Success", "Follow relationship added successfully.")
                refresh_follows()
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            messagebox.showerror("Input Error", "Both follower ID and followee ID are required.")

    def delete_follow():
        selected_items = follows_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a follow relationship to delete.")
            return

        selected = follows_listbox.get(selected_items[0])
        follower_id, followee_id = [int(part.split(": ")[1]) for part in selected.split(",")]

        try:
            cursor.execute("DELETE FROM follows WHERE follower_id = %s AND followee_id = %s",
                           (follower_id, followee_id))
            conn.commit()
            messagebox.showinfo("Success", "Follow relationship deleted successfully.")
            refresh_follows()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_follows():
        follows_listbox.delete(0, tk.END)
        cursor.execute("SELECT follower_id, followee_id FROM follows")
        for follow in cursor.fetchall():
            follows_listbox.insert(tk.END, f"Follower ID: {follow[0]}, Followee ID: {follow[1]}")

    # Window for Follows Page
    follows_window = tk.Toplevel()
    follows_window.title("Follows Page")
    follows_window.geometry("500x500")
    follows_window.configure(bg=bg_color)

    # Input fields for Follower ID and Followee ID
    tk.Label(follows_window, text="Follower ID:", bg=bg_color, fg=text_color).pack(pady=5)
    follower_id_entry = tk.Entry(follows_window, bg="white")
    follower_id_entry.pack(pady=5)

    tk.Label(follows_window, text="Followee ID:", bg=bg_color, fg=text_color).pack(pady=5)
    followee_id_entry = tk.Entry(follows_window, bg="white")
    followee_id_entry.pack(pady=5)

    # CRUD buttons
    tk.Button(follows_window, text="Add Follow", command=add_follow, bg=button_color).pack(pady=5)
    tk.Button(follows_window, text="Delete Follow", command=delete_follow, bg=button_color).pack(pady=5)

    # Listbox to display follow relationships
    follows_listbox = tk.Listbox(follows_window)
    follows_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
    refresh_follows()

    # Back button
    tk.Button(follows_window, text="Back to Home", command=follows_window.destroy, bg=button_color).pack(pady=10)
    center_window(follows_window)


def users_page():
    def add_user():
        username = username_entry.get()

        if username:
            cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
            conn.commit()
            messagebox.showinfo("Success", "User added successfully.")
            refresh_users()
        else:
            messagebox.showerror("Input Error", "Username cannot be empty.")

    def delete_user():
        selected_items = users_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a user to delete.")
            return

        selected = users_listbox.get(selected_items[0])
        user_id = int(selected.split(",")[0].split(": ")[1])
        try:
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            messagebox.showinfo("Success", "User deleted successfully.")
            refresh_users()
        except mysql.connector.IntegrityError as err:
            messagebox.showerror("Error", f"Cannot delete user due to foreign key constraint: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_user():
        selected_items = users_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a user to update.")
            return

        selected = users_listbox.get(selected_items[0])
        user_id = int(selected.split(",")[0].split(": ")[1])
        new_username = username_entry.get()

        if new_username:
            cursor.execute("UPDATE users SET username = %s WHERE id = %s", (new_username, user_id))
            conn.commit()
            messagebox.showinfo("Success", "User updated successfully.")
            refresh_users()
        else:
            messagebox.showerror("Input Error", "Username cannot be empty.")

    def refresh_users():
        users_listbox.delete(0, tk.END)
        cursor.execute("SELECT id, username, user_created_at FROM users")
        for user in cursor.fetchall():
            users_listbox.insert(tk.END, f"ID: {user[0]}, Username: {user[1]}, Created At: {user[2]}")

    # Window for Users Page
    try:
        users_window = tk.Toplevel()
        users_window.title("Users Page")
        users_window.geometry("500x500")
        users_window.configure(bg=bg_color)

        # User input fields
        tk.Label(users_window, text="Username:", bg=bg_color, fg=text_color).pack(pady=5)
        username_entry = tk.Entry(users_window, bg="white")
        username_entry.pack(pady=5)

        # CRUD buttons
        tk.Button(users_window, text="Add User", command=add_user, bg=button_color).pack(pady=5)
        tk.Button(users_window, text="Update User", command=update_user, bg=button_color).pack(pady=5)
        tk.Button(users_window, text="Delete User", command=delete_user, bg=button_color).pack(pady=5)

        # Listbox to display users
        users_listbox = tk.Listbox(users_window)
        users_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        refresh_users()

        # Back button
        tk.Button(users_window, text="Back to Home", command=users_window.destroy, bg=button_color).pack(pady=10)
        center_window(users_window)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening users page: {e}")


# Photos Page
def photos_page():
    def add_photo():
        image_url = image_url_entry.get()
        username = username_entry.get()
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user_id = cursor.fetchone()
        if image_url and user_id:
            cursor.execute("INSERT INTO photos (image_url, user_id) VALUES (%s, %s)", (image_url, user_id[0]))
            conn.commit()
            messagebox.showinfo("Success", "Photo added successfully.")
            refresh_photos()
        else:
            messagebox.showerror("Input Error", "Both fields must be filled with valid data.")

    def delete_photo():
        selected_items = photos_listbox.curselection()
        if not selected_items:
            messagebox.showerror("Selection Error", "Please select a photo to delete.")
            return

        selected = photos_listbox.get(selected_items[0])
        photo_id = int(selected.split(",")[0].split(": ")[1])
        try:
            cursor.execute("DELETE FROM photos WHERE id = %s", (photo_id,))
            conn.commit()
            messagebox.showinfo("Success", "Photo deleted successfully.")
            refresh_photos()
        except mysql.connector.IntegrityError as err:
            messagebox.showerror("Error", f"Cannot delete photo due to foreign key constraint: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_photos():
        photos_listbox.delete(0, tk.END)
        cursor.execute(
            "SELECT photos.id, photos.image_url, users.username FROM photos JOIN users ON photos.user_id = users.id"
        )
        for photo in cursor.fetchall():
            photos_listbox.insert(tk.END, f"ID: {photo[0]}, URL: {photo[1]}, User: {photo[2]}")

    # Window for Photos Page
    try:
        photos_window = tk.Toplevel()
        photos_window.title("Photos Page")
        photos_window.geometry("500x500")
        photos_window.configure(bg=bg_color)

        tk.Label(photos_window, text="Image URL:", bg=bg_color, fg=text_color).pack(pady=5)
        image_url_entry = tk.Entry(photos_window, bg="white")
        image_url_entry.pack(pady=5)

        tk.Label(photos_window, text="Username:", bg=bg_color, fg=text_color).pack(pady=5)
        username_entry = tk.Entry(photos_window, bg="white")
        username_entry.pack(pady=5)

        tk.Button(photos_window, text="Add Photo", command=add_photo, bg=button_color).pack(pady=5)
        tk.Button(photos_window, text="Delete Photo", command=delete_photo, bg=button_color).pack(pady=5)

        photos_listbox = Listbox(photos_window)
        photos_listbox.pack(pady=5, fill=tk.BOTH, expand=True)
        refresh_photos()

        tk.Button(photos_window, text="Back to Home", command=photos_window.destroy, bg=button_color).pack(pady=10)
        center_window(photos_window)
    except Exception as e:
        messagebox.showerror("Error", f"Error opening photos page: {e}")


# Tags Page (Tagging and Tags Management)
def tags_page():
    def add_tag_to_photo():
        photo_id = simpledialog.askinteger("Photo ID", "Enter the Photo ID:")
        tag_name = simpledialog.askstring("Tag Name", "Enter the Tag Name:")

        if photo_id and tag_name:
            # Check if the tag exists; if not, create it
            cursor.execute("SELECT id FROM tags WHERE tag_name = %s", (tag_name,))
            tag = cursor.fetchone()

            if tag:
                tag_id = tag[0]
            else:
                cursor.execute("INSERT INTO tags (tag_name) VALUES (%s)", (tag_name,))
                conn.commit()
                tag_id = cursor.lastrowid  # Get the ID of the new tag

            # Add the tag to the photo
            try:
                cursor.execute("INSERT INTO photo_tags (photo_id, tag_id) VALUES (%s, %s)", (photo_id, tag_id))
                conn.commit()
                messagebox.showinfo("Success", f"Tag '{tag_name}' added to Photo ID {photo_id}.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Could not add tag: {err}")
        else:
            messagebox.showwarning("Input Error", "Both Photo ID and Tag Name are required.")

    def view_tags_for_photo():
        photo_id = simpledialog.askinteger("Photo ID", "Enter the Photo ID to view tags:")
        if photo_id:
            cursor.execute("""
                SELECT tags.tag_name 
                FROM tags 
                JOIN photo_tags ON tags.id = photo_tags.tag_id 
                WHERE photo_tags.photo_id = %s
            """, (photo_id,))
            tags = cursor.fetchall()
            tags_text = "\n".join(tag[0] for tag in tags)
            messagebox.showinfo("Tags for Photo", f"Tags for Photo ID {photo_id}:\n{tags_text}")

    def update_tag():
        old_tag_name = simpledialog.askstring("Old Tag Name", "Enter the existing Tag Name to update:")
        new_tag_name = simpledialog.askstring("New Tag Name", "Enter the new Tag Name:")

        if old_tag_name and new_tag_name:
            try:
                cursor.execute("UPDATE tags SET tag_name = %s WHERE tag_name = %s", (new_tag_name, old_tag_name))
                conn.commit()
                messagebox.showinfo("Success", f"Tag '{old_tag_name}' updated to '{new_tag_name}'.")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Could not update tag: {err}")
        else:
            messagebox.showwarning("Input Error", "Both old and new tag names are required.")

    def delete_tag_from_photo():
        photo_id = simpledialog.askinteger("Photo ID", "Enter the Photo ID:")
        tag_name = simpledialog.askstring("Tag Name", "Enter the Tag Name to remove from photo:")

        if photo_id and tag_name:
            cursor.execute("SELECT id FROM tags WHERE tag_name = %s", (tag_name,))
            tag = cursor.fetchone()
            if tag:
                tag_id = tag[0]
                cursor.execute("DELETE FROM photo_tags WHERE photo_id = %s AND tag_id = %s", (photo_id, tag_id))
                conn.commit()
                messagebox.showinfo("Success", f"Tag '{tag_name}' removed from Photo ID {photo_id}.")
            else:
                messagebox.showerror("Error", "Tag not found.")
        else:
            messagebox.showwarning("Input Error", "Both Photo ID and Tag Name are required.")

    # Window for Tags Page
    tags_window = tk.Toplevel()
    tags_window.title("Tags Management")
    tags_window.geometry("400x400")
    tags_window.configure(bg=bg_color)

    tk.Button(tags_window, text="Add Tag to Photo", command=add_tag_to_photo, bg=button_color).pack(pady=5)
    tk.Button(tags_window, text="View Tags for Photo", command=view_tags_for_photo, bg=button_color).pack(pady=5)
    tk.Button(tags_window, text="Update Tag", command=update_tag, bg=button_color).pack(pady=5)
    tk.Button(tags_window, text="Delete Tag from Photo", command=delete_tag_from_photo, bg=button_color).pack(pady=5)

    tk.Button(tags_window, text="Back to Home", command=tags_window.destroy, bg=button_color).pack(pady=10)
    center_window(tags_window)


# Run the app
if __name__ == "__main__":
    home_page()

conn.close()