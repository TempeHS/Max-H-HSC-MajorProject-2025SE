import threading
from flask import session
import uuid

session_locks = {}

def get_secure_session():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    session_id = session['session_id']
    lock = get_secure(session_id)
    return lock  

def set_secure_session(response):
    session_id = session.get('session_id')
    if session_id not in session_locks:
        session_locks[session_id] = threading.Lock()
    
    lock = session_locks[session_id]
    lock.acquire()
    
    try:
        session['secure_session'] = response.get_json()
        return response
    finally:
        lock.release()  

def get_secure(session_id):
    if session_id not in session_locks:
        session_locks[session_id] = threading.Lock()
    return session_locks[session_id]  # Return the lock for the given session ID