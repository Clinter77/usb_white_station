# run.py
from flaskr import create_app

app = create_app()

if __name__ == "__main__":
    # en local
    # app.run(host="0.0.0.0", port=5000, debug=True)
    # sur le Rapsberry PI
    # app.run(host="10.10.2.89", port=5000)
    app.run(host="0.0.0.0", port=5000) 
