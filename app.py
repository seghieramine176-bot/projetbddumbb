from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Configuration MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '5aminouhockey',
    'database': 'edt_faculte'
}

@app.route('/')
def liste_examens():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT 
    Examen.id_examen,
    Module.nom_module,
    Departement.nom AS nom_departement,
    Examen.date_exam,
    Examen.duree,
    Salle.nom_salle,
    Salle.capacite,
    Examen.nb_etudiants,
    Professeur.nom AS nom_prof,
    Professeur.prenom AS prenom_prof,
    CASE 
        WHEN Examen.nb_etudiants > Salle.capacite 
        THEN 'CONFLIT'
        ELSE 'OK'
    END AS statut
FROM Examen
JOIN Module ON Examen.id_module = Module.id_module
JOIN Formation ON Module.id_formation = Formation.id_formation
JOIN Departement ON Formation.id_departement = Departement.id_departement
JOIN Salle ON Examen.id_salle = Salle.id_salle
JOIN Professeur ON Examen.id_prof = Professeur.id_prof
ORDER BY Examen.date_exam
    """

    cursor.execute(query)
    examens = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('examens.html', examens=examens)

if __name__ == '__main__':
    app.run(debug=True)
