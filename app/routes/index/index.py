from app import app

@app.route("/")
def route_index():
    return "hello w"