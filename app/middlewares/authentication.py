from flask_login import current_user, UserMixin
from flask import redirect, url_for, render_template
from functools import wraps


def isAuthenticated(func):

    @wraps(func)
    def wrapper(*args,**kwargs):
        user:UserMixin = current_user
        if not user.is_authenticated:
            return redirect(url_for("auth.route_login"))   
        return func(*args,**kwargs)
        
    return wrapper
    

def ifAuthenticatedGoIndex(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        user:UserMixin = current_user
        if user.is_authenticated:
            return render_template("dashboard/index.html")
        return func(*args,**kwargs)
        
    return wrapper


