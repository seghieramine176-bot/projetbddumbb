from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "une_clef_secrete_pour_session"  # obligatoire pour session

# =========================
# CONFIGURATION BDD
# =========================
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '5aminouhockey',
    'database': 'edt_faculte'
}

# =========================
# PAGE DE CONNEXION
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        role = request.form.get("role")

        if not username or not role:
            return render_template("interface.html", error="Veuillez remplir tous les champs")

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        if role == "Étudiant":
            query = "SELECT * FROM etudiant WHERE nom = %s"
        elif role == "Professeur":
            query = "SELECT * FROM professeur WHERE nom = %s"
        elif role == "Doyen":
            query = "SELECT * FROM doyen WHERE nom = %s"
        elif role == "Administrateur":
            query = "SELECT * FROM administrateur WHERE nom = %s"
        elif role == "ChefDeDepartement":
            query = "SELECT * FROM chef_departement WHERE nom = %s"
        else:
            cursor.close()
            conn.close()
            return render_template("interface.html", error="Rôle invalide")

        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if not user:
            return render_template("interface.html", error="Utilisateur non trouvé")

        session.clear()
        session['role'] = role

        if role == "Étudiant":
            session['id_etudiant'] = user['id_etudiant']
            return redirect(url_for("etudiant"))

        if role == "Professeur":
            session['id_prof'] = user['id_prof']
            session['id_departement'] = user['id_departement']
            return redirect(url_for("professeur"))

        if role == "Doyen":
            return redirect(url_for("doyen"))

        if role == "Administrateur":
            return redirect(url_for("administrateur"))

        if role == "ChefDeDepartement":
            session['id_chef'] = user['id_chef']
            session['id_departement'] = user['id_departement']
            return redirect(url_for("chef_departement"))

    return render_template("interface.html", error=error)

# =========================
# PAGES SELON ROLE
# =========================
@app.route("/etudiant")
def etudiant():
    if session.get("role") != "Étudiant":
        return redirect(url_for("login"))
    return render_template("etudiant.html")

@app.route("/professeur")
def professeur():
    if session.get("role") != "Professeur":
        return redirect(url_for("login"))
    return render_template("professeur.html")

@app.route("/doyen")
def doyen():
    if session.get("role") != "Doyen":
        return redirect(url_for("login"))
    return render_template("doyen.html")

@app.route("/administrateur")
def administrateur():
    if session.get("role") != "Administrateur":
        return redirect(url_for("login"))
    return render_template("Administrateur.html")



# =========================
# PLANNING ETUDIANT (uniquement pour l'étudiant connecté)
# =========================
@app.route("/planning_etudiant")
def planning_etudiant():
    if session.get("role") != "Étudiant":
        return redirect(url_for("login"))

    id_etudiant = session.get('id_etudiant')
    if not id_etudiant:
        return "ID étudiant manquant dans la session", 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT m.nom_module AS module,
               ex.date_exam AS date,
               ex.duree AS duree,
               s.nom_salle AS salle
        FROM inscription i
        JOIN module m ON i.id_module = m.id_module
        JOIN examen ex ON ex.id_module = m.id_module
        JOIN salle s ON ex.id_salle = s.id_salle
        WHERE i.id_etudiant = %s
        ORDER BY ex.date_exam
    """
    cursor.execute(query, (id_etudiant,))
    planning = cursor.fetchall()
    cursor.close()
    conn.close()

    # Formatage durée
    for exam in planning:
        exam['duree'] = f"{exam['duree']}:00" if exam['duree'] else "Non défini"

    return render_template("planning_etudiant.html", planning=planning)



# =========================
# PLANNING PROFESSEUR (uniquement pour le professeur connecté)
# =========================
@app.route("/planning_professeur")
def planning_professeur():
    if session.get("role") != "Professeur":
        return redirect(url_for("login"))

    id_prof = session.get('id_prof')
    if not id_prof:
        return "ID professeur manquant dans la session", 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
        m.nom_module AS module,
        ex.date_exam AS date,
        ex.heure_debut AS heure,  -- ajouter l'heure de début
        ex.duree AS duree,
        s.nom_salle AS salle
    FROM surveillance sv
    JOIN examen ex ON sv.id_examen = ex.id_examen
    JOIN module m ON ex.id_module = m.id_module
    JOIN salle s ON ex.id_salle = s.id_salle
    WHERE sv.id_prof = %s
    ORDER BY ex.date_exam
    """
    cursor.execute(query, (id_prof,))
    planning = cursor.fetchall()
    cursor.close()
    conn.close()

    # Formatage durée
    for exam in planning:
        exam['duree'] = f"{exam['duree']}:00" if exam['duree'] else "Non défini"

    return render_template("planning_professeur.html", planning=planning)






# =========================
# =========================
# =========================
# EDT DES ETUDIANTS (CHEF DE DEPARTEMENT)
# =========================

@app.route("/edt_etudiants")
def edt_etudiants():
    if session.get("role") != "ChefDeDepartement":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Seulement les étudiants du département du chef
    query = """
        SELECT 
            e.nom AS etudiant_nom,
            e.prenom AS etudiant_prenom,
            f.nom AS formation,
            m.nom_module AS module,
            ex.date_exam AS date_exam,
            ex.duree AS duree,
            s.nom_salle AS salle
        FROM etudiant e
        JOIN formation f ON e.id_formation = f.id_formation
        JOIN inscription i ON e.id_etudiant = i.id_etudiant
        JOIN module m ON i.id_module = m.id_module
        LEFT JOIN examen ex ON ex.id_module = m.id_module
        LEFT JOIN salle s ON ex.id_salle = s.id_salle
        WHERE f.id_departement = %s
        ORDER BY e.nom, ex.date_exam
    """
    cursor.execute(query, (session['id_departement'],))

    edt = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template("edt_etudiants.html", edt=edt)







# =========================
# EDT ENSEIGNANTS (CHEF DE DEPARTEMENT)
# =========================
@app.route("/edt_enseignants")
def edt_enseignants():
    if session.get("role") != "ChefDeDepartement":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Récupérer uniquement les professeurs du département et leurs surveillances
    query = """
        SELECT 
            p.nom AS nom_prof,
            p.prenom AS prenom_prof,
            m.nom_module AS module,
            ex.date_exam AS date_exam,
            ex.duree AS duree,
            s.nom_salle AS salle
        FROM professeur p
        JOIN surveillance sv ON sv.id_prof = p.id_prof
        JOIN examen ex ON sv.id_examen = ex.id_examen
        JOIN module m ON ex.id_module = m.id_module
        JOIN salle s ON ex.id_salle = s.id_salle
        WHERE p.id_departement = %s
        ORDER BY p.nom, ex.date_exam
    """
    cursor.execute(query, (session['id_departement'],))

    edt = cursor.fetchall()
    cursor.close()
    conn.close()

    # Formatage durée et valeurs manquantes
    for ex in edt:
        ex['duree'] = f"{ex['duree']}:00" if ex.get('duree') else "Non défini"
        if not ex['date_exam']:
            ex['date_exam'] = "Non défini"
        if not ex['salle']:
            ex['salle'] = "Non défini"

    return render_template("edt_enseignants.html", edt=edt)




# =========================
# CHEF DE DÉPARTEMENT - STATISTIQUES
# =========================

@app.route("/chef_departement")
def chef_departement():
    if session.get("role") != "ChefDeDepartement":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Nombre total d'étudiants
    cursor.execute("""
        SELECT COUNT(*) AS total_etudiants
        FROM etudiant e
        JOIN formation f ON e.id_formation = f.id_formation
        WHERE f.id_departement = %s
    """, (session['id_departement'],))
    total_etudiants = cursor.fetchone()['total_etudiants']

    # Nombre total de professeurs
    cursor.execute("""
        SELECT COUNT(*) AS total_professeurs
        FROM professeur
        WHERE id_departement = %s
    """, (session['id_departement'],))
    total_professeurs = cursor.fetchone()['total_professeurs']

    # Nombre total de modules
    cursor.execute("""
       SELECT COUNT(*) AS total_modules
        FROM module m
        JOIN formation f ON m.id_formation = f.id_formation
        WHERE f.id_departement = %s
    """, (session['id_departement'],))
    total_modules = cursor.fetchone()['total_modules']

    # Nombre total de formations
    cursor.execute("""
        SELECT COUNT(*) AS total_formations
        FROM formation
        WHERE id_departement = %s
    """, (session['id_departement'],))
    total_formations = cursor.fetchone()['total_formations']

    # Fermeture du curseur et de la connexion après toutes les requêtes
    cursor.close()
    conn.close()

    return render_template(
        "chef_departement.html",
        total_etudiants=total_etudiants,
        total_professeurs=total_professeurs,
        total_modules=total_modules,
        total_formations=total_formations
    )





# =========================
# ADMINISTRATEUR - FONCTIONNALITÉS
# =========================



# =========================
# generer_edt
# =========================

from datetime import datetime, timedelta



@app.route("/generer_edt", methods=["GET", "POST"])
def generer_edt():
    if session.get("role") != "Administrateur":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    message = None
    planning = []

    if request.method == "POST":
        try:
            # 1️⃣ Modules sans examen
            cursor.execute("""
                SELECT m.id_module, m.duree
                FROM module m
                LEFT JOIN examen e ON e.id_module = m.id_module
                WHERE e.id_examen IS NULL
            """)
            modules = cursor.fetchall()

            date_depart = datetime.today().date()
            jour = 0

            for m in modules:
                cursor.execute("""
                    INSERT INTO examen (id_module, date_exam, duree, id_salle, id_prof)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    m['id_module'],
                    date_depart + timedelta(days=jour),
                    m['duree'],
                    1,
                    1
                ))
                jour += 1

            conn.commit()
            message = "Génération de l’EDT effectuée avec succès ✅"

        except Exception as e:
            conn.rollback()
            message = f"Erreur : {e}"

    # 2️⃣ Récupération de l’EDT
    cursor.execute("""
        SELECT 
        d.nom AS departement,
        f.nom AS formation,
        m.nom_module,
        e.date_exam,
        e.duree,
        s.nom_salle,
        CONCAT(p.nom, ' ', p.prenom) AS professeur
    FROM examen e
    JOIN module m ON e.id_module = m.id_module
    JOIN formation f ON m.id_formation = f.id_formation
    JOIN departement d ON f.id_departement = d.id_departement
    JOIN salle s ON e.id_salle = s.id_salle
    JOIN professeur p ON e.id_prof = p.id_prof
    ORDER BY f.nom, e.date_exam
    """)
    planning = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "generer_edt.html",
        message=message,
        planning=planning
    )

# =========================
# detecter_conflits
# =========================

# Page de détection
@app.route("/detecter_conflits")
def detecter_conflits():
    if session.get("role") != "Administrateur":
        return redirect(url_for("login"))
    # Page ouverte mais pas encore lancé : aucun résultat
    return render_template("detecter_conflits.html",
                           conflits_etudiants=None,
                           conflits_salles=None,
                           detection_lancee=False)
    
    

# Lancer la détection
@app.route("/detecter_conflits/lancer")
def lancer_detection_conflits():
    if session.get("role") != "Administrateur":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Conflits étudiants : même date et heure
    cursor.execute("""
        SELECT pe.id_etudiant, e.date_exam, e.heure_debut, COUNT(*) as nb_examens
        FROM passage_examen pe
        JOIN examen e ON pe.id_examen = e.id_examen
        GROUP BY pe.id_etudiant, e.date_exam, e.heure_debut
        HAVING COUNT(*) > 1
    """)
    conflits_etudiants = cursor.fetchall()

    # Conflits salle : nb étudiants > capacité
    cursor.execute("""
        SELECT e.id_examen, s.nom_salle, s.capacite, COUNT(pe.id_etudiant) AS nb_etudiants
        FROM examen e
        JOIN salle s ON e.id_salle = s.id_salle
        JOIN passage_examen pe ON e.id_examen = pe.id_examen
        GROUP BY e.id_examen
        HAVING nb_etudiants > s.capacite
    """)
    conflits_salles = cursor.fetchall()
    
    # Conflits professeurs : plus de 3 examens par jour
    cursor.execute("""
        SELECT e.id_prof, p.nom AS nom_prof, e.date_exam, COUNT(*) AS nb_examens
        FROM examen e
        JOIN professeur p ON e.id_prof = p.id_prof
        GROUP BY e.id_prof, e.date_exam
        HAVING COUNT(*) > 3
    """)
    conflits_profs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("detecter_conflits.html",
                       conflits_etudiants=conflits_etudiants,
                       conflits_salles=conflits_salles,
                       conflits_profs=conflits_profs,
                       detection_lancee=True)



# =========================
# optimiser_ressources
# =========================

# Page optimisation
@app.route("/optimiser_ressources")
def optimiser_ressources():
    if session.get("role") != "Administrateur":
        return redirect(url_for("login"))

    return render_template("optimiser_ressources.html",
                           detection_lancee=False,
                           conflits_etudiants=None,
                           conflits_profs=None,
                           conflits_salles=None)

# Lancer l’optimisation automatique
@app.route("/optimiser_ressources/lancer")
def lancer_optimisation():
    if session.get("role") != "Administrateur":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Conflits étudiants
    cursor.execute("""
        SELECT pe.id_etudiant, e.date_exam, e.heure_debut, COUNT(*) as nb_examens
        FROM passage_examen pe
        JOIN examen e ON pe.id_examen = e.id_examen
        GROUP BY pe.id_etudiant, e.date_exam, e.heure_debut
        HAVING COUNT(*) > 1
    """)
    conflits_etudiants = cursor.fetchall()

    # Conflits professeurs
    cursor.execute("""
        SELECT e.id_prof, e.date_exam, e.heure_debut, COUNT(*) as nb_examens
        FROM examen e
        GROUP BY e.id_prof, e.date_exam, e.heure_debut
        HAVING COUNT(*) > 1
    """)
    conflits_profs = cursor.fetchall()

    # Conflits salles : nb étudiants > capacité
    cursor.execute("""
        SELECT e.id_examen, s.nom_salle, s.capacite, COUNT(pe.id_etudiant) AS nb_etudiants
        FROM examen e
        JOIN salle s ON e.id_salle = s.id_salle
        JOIN passage_examen pe ON e.id_examen = pe.id_examen
        GROUP BY e.id_examen
        HAVING nb_etudiants > s.capacite
    """)
    conflits_salles = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("optimiser_ressources.html",
                           detection_lancee=True,
                           conflits_etudiants=conflits_etudiants,
                           conflits_profs=conflits_profs,
                           conflits_salles=conflits_salles)






# =========================
# Doyen - Emploi du temps des étudiants
# =========================
@app.route("/doyen_etudiants")
def doyen_etudiants():
    if session.get("role") != "Doyen":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            e.nom AS etudiant_nom,
            e.prenom AS etudiant_prenom,
            f.nom AS formation,
            d.nom AS departement,
            m.nom_module AS module,
            ex.date_exam,
            ex.duree,
            s.nom_salle AS salle
        FROM etudiant e
        JOIN formation f ON e.id_formation = f.id_formation
        JOIN departement d ON f.id_departement = d.id_departement
        JOIN inscription i ON e.id_etudiant = i.id_etudiant
        JOIN module m ON i.id_module = m.id_module
        LEFT JOIN examen ex ON ex.id_module = m.id_module
        LEFT JOIN salle s ON ex.id_salle = s.id_salle
        ORDER BY d.nom, f.nom, e.nom, ex.date_exam
    """
    cursor.execute(query)
    edt = cursor.fetchall()

    cursor.close()
    conn.close()

    # Formatage des valeurs nulles
    for e in edt:
        e['duree'] = f"{e['duree']}:00" if e.get('duree') else "Non défini"
        e['date_exam'] = e['date_exam'] if e['date_exam'] else "Non défini"
        e['salle'] = e['salle'] if e['salle'] else "Non défini"

    return render_template("doyen_etudiants.html", edt=edt)




# =========================
# Doyen - Emploi du temps des enseignants
# =========================
@app.route("/doyen_enseignants")
def doyen_enseignants():
    if session.get("role") != "Doyen":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT
            p.nom AS professeur_nom,
            p.prenom AS professeur_prenom,
            d.nom AS departement,
            m.nom_module AS module,
            ex.date_exam,
            ex.heure_debut,
            ex.duree,
            s.nom_salle AS salle
        FROM professeur p
        JOIN examen ex ON ex.id_prof = p.id_prof
        JOIN module m ON ex.id_module = m.id_module
        JOIN formation f ON m.id_formation = f.id_formation
        JOIN departement d ON f.id_departement = d.id_departement
        LEFT JOIN salle s ON ex.id_salle = s.id_salle
        ORDER BY d.nom, p.nom, ex.date_exam
    """

    cursor.execute(query)
    edt_enseignants = cursor.fetchall()

    cursor.close()
    conn.close()

    # Sécurisation affichage
    for e in edt_enseignants:
        e["date_exam"] = e["date_exam"] if e["date_exam"] else "Non défini"
        e["heure_debut"] = e["heure_debut"] if e["heure_debut"] else "Non défini"
        e["duree"] = f"{e['duree']}h" if e["duree"] else "Non défini"
        e["salle"] = e["salle"] if e["salle"] else "Non définie"

    return render_template("doyen_enseignants.html", edt_enseignants=edt_enseignants)




# =========================
# DOYEN DASHBOARD
# =========================


@app.route("/doyen_dashboard")
def doyen_dashboard():
    if session.get("role") != "Doyen":
        return redirect(url_for("login"))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # KPI 1 : total examens
    cursor.execute("SELECT COUNT(*) AS total FROM examen")
    total_examens = cursor.fetchone()['total']

    # KPI 2 : taux d'utilisation des salles
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT e.id_salle) * 100 / (SELECT COUNT(*) FROM salle) AS taux
        FROM examen e
    """)
    taux_salles = round(cursor.fetchone()['taux'] or 0, 2)

    # KPI 3 : heures profs
    cursor.execute("SELECT SUM(duree) AS heures FROM examen")
    heures_profs = cursor.fetchone()['heures'] or 0

    # Occupation des salles
    cursor.execute("""
        SELECT s.nom_salle, s.capacite, COUNT(e.id_examen) AS nb_examens
        FROM salle s
        LEFT JOIN examen e ON s.id_salle = e.id_salle
        GROUP BY s.id_salle
    """)
    occupation_salles = cursor.fetchall()

    # ✅ KPI 4 : conflits étudiants (1 examen max / jour)
    cursor.execute("""
        SELECT COUNT(*) AS nb FROM (
            SELECT pe.id_etudiant
            FROM passage_examen pe
            JOIN examen e ON pe.id_examen = e.id_examen
            GROUP BY pe.id_etudiant, e.date_exam
            HAVING COUNT(*) > 1
        ) t
    """)
    conflits_etudiants = cursor.fetchone()['nb']

    cursor.close()
    conn.close()

    kpi = {
        "total_examens": total_examens,
        "taux_salles": taux_salles,
        "heures_profs": heures_profs,
        "total_conflits": conflits_etudiants   # ✅ VRAI conflit
    }

    return render_template(
        "doyen_dashboard.html",
        kpi=kpi,
        occupation_salles=occupation_salles
    )

# ========================
# VALIDER EDT (DOYEN)
# =========================

@app.route("/valider_edt")
def valider_edt():
    if session.get("role") != "Doyen":
        return redirect(url_for("login"))

    return render_template("valider_edt.html")


@app.route("/valider_edt/confirmer", methods=["POST"])
def confirmer_validation_edt():
    if session.get("role") != "Doyen":
        return redirect(url_for("login"))

    now = datetime.now()
    date_validation = now.date()
    heure_validation = now.time()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO validation_edt (date_validation, heure_validation, valide_par)
        VALUES (%s, %s, %s)
    """, (date_validation, heure_validation, "Doyen"))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("doyen_dashboard"))




# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================
# LANCEMENT
# =========================
if __name__ == "__main__":
    app.run(debug=True)







