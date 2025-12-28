from flask import Flask, render_template

app = Flask(__name__)

# Page administrateur
@app.route("/administrateur")
def administrateur():
    return render_template("administrateur.html")

# Génération automatique EDT (simulation)
@app.route("/generer_edt")
def generer_edt():
    return """
    <h2>Génération automatique de l'EDT</h2>
    <p>Les emplois du temps ont été générés avec succès.</p>
    <ul>
        <li>BD – 10/06 – Amphi A</li>
        <li>Réseaux – 11/06 – Salle B2</li>
        <li>IA – 12/06 – Amphi C</li>
    </ul>
    <a href="/administrateur">Retour</a>
    """

# Détection de conflits (simulation)
@app.route("/conflits")
def conflits():
    return """
    <h2>Conflits détectés</h2>
    <ul>
        <li>Étudiant ID 120 : 2 examens le même jour</li>
        <li>Salle B2 utilisée deux fois à 10h</li>
        <li>Professeur Dr. Karim : 4 examens le même jour</li>
    </ul>
    <a href="/administrateur">Retour</a>
    """

# Optimisation des ressources (simulation)
@app.route("/optimisation")
def optimisation():
    return """
    <h2>Optimisation des ressources</h2>
    <ul>
        <li>Utilisation des amphis : 92%</li>
        <li>Salles optimisées : 18</li>
        <li>Répartition équitable des surveillances</li>
    </ul>
    <a href="/administrateur">Retour</a>
    """

if __name__ == "__main__":
    app.run(debug=True)
