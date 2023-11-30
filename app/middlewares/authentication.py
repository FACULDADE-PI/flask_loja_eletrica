from flask_login import current_user, UserMixin
from flask import render_template, url_for, redirect
from functools import wraps
from app.models import TypeUsers
from sqlalchemy import func as _func


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
            return redirect("/")
        return func(*args,**kwargs)
        
    return wrapper

def hasPrivileges(slugs_privileges: list):
    """ Avalia se o usuário possui privilégios """
    def decoratorType(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for slug in slugs_privileges:
                # Utilize ilike para comparação case insensitive do slug
                typeUser = TypeUsers.query.filter(_func.lower(TypeUsers.slug) == _func.lower(slug)).first()
                if typeUser and typeUser.Id == current_user.type_user:
                    return func(*args, **kwargs)
            return render_template("errors/insuficient_privileges.html")
        return wrapper
    return decoratorType
