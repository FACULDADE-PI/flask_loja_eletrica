from app import app, db

if __name__ == "__main__":
    app.run(
        port=7000,
        debug=False,
    )