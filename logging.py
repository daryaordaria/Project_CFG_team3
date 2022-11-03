def log_out(session):
    try:
        session.pop('username', None)
        session.pop('id', None)
        return True
    except:
        return False
        