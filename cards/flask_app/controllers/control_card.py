from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.card import Card
from flask_app.models.user import User

@app.route('/newcard')
def add():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id":session['user_id']
    }
    return render_template ("newcard.html", user=User.get_by_id(data))

@app.route("/create", methods=['POST'])
def create():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Card.validate_card(request.form):
        return redirect('/newcard')
    data={
        "title": request.form["title"],
        "graded": request.form["graded"],
        "price":request.form["price"],
        "date_of_print": request.form["date_of_print"],
        "league": request.form["league"],
        "user_id": session["user_id"],
    }
    Card.create(data)
    return redirect("/account/<int:id>")

@app.route('/account/<int:id>')
def account(id):
    data= {
        "id":id
    }
    userdata ={
        'id': session['user_id']
    }
    if 'user_id' not in session:
        return redirect('/logout')
    user=User.get_by_id(userdata)
    cards=Card.get_all_from_one(data)
    return render_template("account.html", user=user, cards=cards)

@app.route("/edit/card/<int:id>")
def editcard(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        "id":id
    }
    userdata={
        "id":session['user_id']
    }
    return render_template("edit.html", card=Card.get_all_from_one(data), user=User.get_by_id(userdata))

@app.route("/update/card", methods=['POST'])
def update():
        if not Card.validate_card(request.form):
            return redirect('/addform')
        data={
            "title": request.form["title"],
            "graded": request.form["graded"],
            "price":request.form["price"],
            "date_of_print": request.form["date_of_print"],
            "league": request.form["league"],
            "id": request.form["id"],
        }
        Card.update(data)
        return redirect('/account/<int:id>')

@app.route("/delete/<int:id>")
def destroy(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
    }
    Card.destroy(data)
    return redirect('/account/<int:id>')

@app.route("/view/<int:id>")
def view_card(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":id
        }
    userdata={
        "id":session['user_id']
    }
    return render_template("show.html", card=Card.get_one(data), user=User.get_by_id(userdata))

@app.route('/allcards')
def allcards():
    if 'user_id' not in session:
        return redirect('/logout')
    data= {
        "id":id
    }
    user=User.get_by_id(data)
    cards=Card.get_all()
    return render_template("allcards.html", user=user, cards=cards)

