from flask import Flask, render_template

app = Flask(__name__)

# Page de connexion (exemple)
@app.route("/")
def interface():
    return render_template("interface.html")

# Page Doyen
@app.route("/doyen")
def doyen():
    return render_template("doyen.html")

# Emploi du temps des étudiants (simulation)
@app.route("/edt_etudiants")
def edt_etudiants():
    return """
    <h2>Emploi du temps des étudiants</h2>
    <ul>
        <li>Module : Bases de données – 10/06 – Amphi A</li>
        <li>Module : Réseaux – 11/06 – Salle B2</li>
        <li>Module : IA – 12/06 – Amphi C</li>
    </ul>
    <a href="/doyen">Retour</a>
    """

# Emploi du temps des enseignants (simulation)
@app.route("/edt_enseignants")
def edt_enseignants():
    return """
    <h2>Emploi du temps des enseignants</h2>
    <ul>
        <li>Dr. Ahmed – Surveillance BD – 10/06</li>
        <li>Dr. Sara – Surveillance Réseaux – 11/06</li>
        <li>Dr. Karim – Surveillance IA – 12/06</li>
    </ul>
    <a href="/doyen">Retour</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
