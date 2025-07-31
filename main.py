from instagrapi import Client
import json
import os

username = "_404humor"
password = "Capybara1234"
session_id = "34209631-04ae-4c8e-9f7d-eeeb25eb1570"
proxy = "http://squid:3128"
session_dir = "/app/sessions"
session_file = f"{session_dir}/{username}_session.json"


cl = Client()
# cl.set_proxy(proxy)
if os.path.exists(session_file):
    cl.load_settings(session_file)
    print(f"Successfully loaded session for {username}")
    try:
        cl.login(username, password)
    except Exception as e:
        print(f"Error logging in with session for {username}: {e}")
else:
    print(f"Error: Session file for {username} does not exist at {session_file}.")

# audience is who can see the note:
# 0 - followers you follow back 
# 1 - close friends
def create_note(client, text, audience = 0):
    # notes should be less than 60 characters
    # 1 request every 2 minutes 
    try:
        if len(text) > 60:
            raise ValueError("Note text must be less than 60 characters.")
        if audience not in [0, 1]:
            raise ValueError("Audience must be 0 (followers you follow back) or 1 (close friends).")
        note = client.create_note(
            text=text,
            audience=audience)
        print(note.dict())
    except ValueError as e:
        print(f"Error creating note: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

# TODO:
def get_notes(client):
    try:
        notes = client.get_notes()
        for note in notes:
            print(note.dict())
        return notes
    except Exception as e:
        print(f"Error retrieving notes: {e}")


# TODO:
def delete_note(client):
    note = get_notes(client)
    if note:
        try:
            client.delete_note(note.id)
            print(f"Note {note.id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting note: {e}")

create_note(cl, "Hello from instaDM!", 0)    

