from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import os
import sys

username     = "_404humor"
password     = "Capybara1234"
proxy        = "http://squid:3128"
session_id   = "74992480540%3AjTEcpSmbWbx3pA%3A17%3AAYe3uKPjiekT3umQswWH1MKnBKQ8yGjths2OYfwdpA"
session_dir  = "sessions"
session_file = os.path.join(session_dir, f"{username}_session.json")

os.makedirs(session_dir, exist_ok=True)

cl = Client()
cl.set_proxy(proxy)

# Load any previously saved session
if os.path.exists(session_file):
    cl.load_settings(session_file)
    print(f"Loaded session from {session_file}")

# 1) Try session-ID login
try:
    if cl.login_by_sessionid(session_id):
        print("Authenticated via session_id")
    else:
        raise Exception("session_id login returned False")
except Exception:
    print("session_id login failed; falling back to password login")
    if not cl.login(username, password):
        print("Password login failed; check credentials or 2FA.")
        sys.exit(1)
    print("Authenticated via username/password")

# 2) Verify that we’re actually logged in
try:
    cl.account_info()
except LoginRequired:
    print("Session invalid; performing a full relogin")
    # clear stale cookies and do the normal flow
    cl.relogin()
    print("Relogin successful")

# 3) Save fresh cookies
cl.dump_settings(session_file)
print(f"Logged in and saved session to {session_file}")

# audience is who can see the note:
# 0 - followers you follow back 
# 1 - close friends
def create_note(client, text, audience=0):
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

