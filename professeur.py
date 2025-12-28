from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Page de connexion principale
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        role = request.form.get("role")

        if not username or not role:
            return render_template("interface.html", error="Veuillez remplir tous les champs")

        if role == "Professeur":
            return redirect(url_for("professeur"))
        elif role == "Étudiant":
            return redirect(url_for("etudiant"))

    return render_template("interface.html", error=None)

# Page Professeur
@app.route("/professeur")
def professeur():
    return render_template("professeur.html")

# Page Étudiant (exemple minimal)
@app.route("/etudiant")
def etudiant():
    return "<h1>Page Étudiant - à compléter</h1>"

if __name__ == "__main__":
    app.run(debug=True)
