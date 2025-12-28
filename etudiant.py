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

        if role == "Étudiant":
            return redirect(url_for("etudiant"))
        elif role == "Professeur":
            return redirect(url_for("professeur"))

    return render_template("interface.html", error=None)

# Page Étudiant
@app.route("/etudiant")
def etudiant():
    return render_template("etudiant.html")

# Page Professeur (exemple minimal)
@app.route("/professeur")
def professeur():
    return "<h1>Page Professeur - à compléter</h1>"

if __name__ == "__main__":
    app.run(debug=True)
