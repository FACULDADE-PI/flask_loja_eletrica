from datetime import datetime, timedelta


def expiration_time(**kwargs)->datetime:
    return current_time()+timedelta(**kwargs)

def current_time()->datetime:
    return datetime.utcnow() - timedelta(hours=+3)


def current_midnight():
    return current_time().replace(hour=0, minute=0, second=0, microsecond=0)


def midnight_timezone():
    return current_time().replace(hour=0, minute=0, second=0, microsecond=0)


def current_timestamp():
    return current_time().timestamp()
