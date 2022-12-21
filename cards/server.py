from flask_app import app
from flask_app.controllers import control_card
from flask_app.controllers import control_user

if __name__=="__main__":
    app.run(debug=True)