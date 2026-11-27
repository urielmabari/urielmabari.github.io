"""
SMILE — Générateur de données FICTIVES pour le prototype Power BI.

Simule le parcours d'étudiants dans plusieurs établissements d'une université
sur 7 années universitaires (2018-2019 → 2024-2025) :
inscriptions, notes par UE, décisions de fin d'année (Admis / Redouble / Abandon).

Toutes les données sont inventées. Aucune donnée réelle d'étudiant n'est utilisée.

Usage :  python generer_donnees.py            (écrit ../donnees/SMILE_donnees.xlsx)
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(2025)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "donnees")
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------
# 1. Dimensions de référence
# ----------------------------------------------------------------------------
ANNEES = list(range(2018, 2025))  # année de début : 2018 => "2018-2019"
NIVEAUX = [("L1", "Licence", 1), ("L2", "Licence", 2), ("L3", "Licence", 3),
           ("M1", "Master", 4), ("M2", "Master", 5)]

# (code, nom, site)  — structure illustrative, à valider avec l'université
ETABS = [
    ("FST",   "Faculté des Sciences et Techniques",            "Campus principal"),
    ("FD",    "Faculté de Droit",                               "Campus principal"),
    ("FSE",   "Faculté des Sciences Économiques",               "Campus principal"),
    ("FLSH",  "Faculté des Lettres et Sciences Humaines",       "Campus principal"),
    ("FSSA",  "Faculté des Sciences de la Santé",               "Site de la Santé"),
    ("ENS",   "École Normale Supérieure",                       "Site ENS"),
    ("ENSP",  "École Nationale Supérieure Polytechnique",       "Site ENSP"),
]

# (code_etab, parcours, difficulté [0..1], effectif L1 de base, a_un_master)
PARCOURS = [
    ("FST", "Génie Informatique", .55, 160, True),
    ("FST", "Mathématiques", .75, 120, True),
    ("FST", "Physique", .70, 90, True),
    ("FST", "Chimie", .65, 85, False),
    ("FST", "Biologie", .50, 150, True),
    ("FD", "Droit Privé", .45, 320, True),
    ("FD", "Droit Public", .45, 260, True),
    ("FSE", "Économie", .50, 280, True),
    ("FSE", "Gestion", .40, 300, True),
    ("FLSH", "Lettres Modernes", .35, 180, True),
    ("FLSH", "Histoire", .35, 140, False),
    ("FLSH", "Anglais", .30, 170, True),
    ("FSSA", "Médecine (tronc commun)", .80, 200, False),
    ("ENS", "Sciences de l'Éducation", .30, 110, True),
    ("ENSP", "Génie Civil", .60, 70, True),
    ("ENSP", "Génie Électrique", .65, 60, True),
]

UE_PAR_NIVEAU = {
    "Génie Informatique": ["Algorithmique", "Programmation", "Bases de données", "Réseaux", "Systèmes d'exploitation", "Génie logiciel", "Intelligence artificielle", "Sécurité informatique"],
    "Mathématiques": ["Analyse", "Algèbre linéaire", "Probabilités", "Statistiques", "Topologie", "Analyse numérique", "Équations différentielles", "Recherche opérationnelle"],
    "Physique": ["Mécanique", "Électromagnétisme", "Thermodynamique", "Optique", "Physique quantique", "Mathématiques pour la physique", "Électronique", "Physique statistique"],
    "Chimie": ["Chimie générale", "Chimie organique", "Chimie minérale", "Chimie analytique", "Thermochimie", "Spectroscopie", "Biochimie", "Mathématiques"],
    "Biologie": ["Biologie cellulaire", "Génétique", "Physiologie", "Écologie", "Microbiologie", "Biochimie", "Botanique", "Statistiques"],
    "Droit Privé": ["Droit civil", "Droit pénal", "Droit des affaires", "Droit du travail", "Procédure civile", "Droit OHADA", "Introduction au droit", "Histoire du droit"],
    "Droit Public": ["Droit constitutionnel", "Droit administratif", "Finances publiques", "Relations internationales", "Libertés fondamentales", "Droit fiscal", "Introduction au droit", "Science politique"],
    "Économie": ["Microéconomie", "Macroéconomie", "Statistiques", "Mathématiques économiques", "Économétrie", "Économie du développement", "Monnaie et banque", "Comptabilité"],
    "Gestion": ["Comptabilité générale", "Marketing", "Gestion financière", "Management", "Contrôle de gestion", "Fiscalité", "Statistiques", "Droit des sociétés"],
    "Lettres Modernes": ["Littérature française", "Littérature africaine", "Linguistique", "Grammaire", "Stylistique", "Littérature comparée", "Méthodologie", "Expression écrite"],
    "Histoire": ["Histoire ancienne", "Histoire médiévale", "Histoire moderne", "Histoire contemporaine", "Histoire de l'Afrique", "Géographie", "Méthodologie", "Archéologie"],
    "Anglais": ["Grammaire anglaise", "Phonétique", "Civilisation britannique", "Civilisation américaine", "Traduction", "Littérature anglophone", "Linguistique", "Expression orale"],
    "Médecine (tronc commun)": ["Anatomie", "Physiologie", "Biochimie", "Histologie", "Biophysique", "Biostatistiques", "Sémiologie", "Santé publique"],
    "Sciences de l'Éducation": ["Psychologie de l'enfant", "Didactique", "Pédagogie", "Sociologie de l'éducation", "Évaluation", "Philosophie de l'éducation", "Statistiques", "Stage pratique"],
    "Génie Civil": ["Résistance des matériaux", "Mécanique des sols", "Béton armé", "Topographie", "Hydraulique", "Dessin technique", "Mathématiques", "Gestion de chantier"],
    "Génie Électrique": ["Électrotechnique", "Électronique de puissance", "Automatique", "Machines électriques", "Réseaux électriques", "Mathématiques", "Énergies renouvelables", "Informatique industrielle"],
}
NB_UE = 6  # UE par niveau

SERIES_BAC = {"C": .20, "D": .32, "A": .30, "G": .10, "E/F": .08}
DEPARTEMENTS = {"Brazzaville": .45, "Pointe-Noire": .18, "Bouenza": .07, "Pool": .07, "Niari": .05,
                "Plateaux": .05, "Cuvette": .05, "Lékoumou": .03, "Sangha": .03, "Likouala": .02}
# affinité série du bac / domaine (bonus de niveau)
AFFINITE = {
    "FST": {"C": .9, "D": .6, "E/F": .7, "A": -.6, "G": -.4},
    "ENSP": {"C": .9, "D": .4, "E/F": 1.0, "A": -.7, "G": -.5},
    "FSSA": {"C": .6, "D": .8, "E/F": .2, "A": -.7, "G": -.5},
    "FD": {"C": .2, "D": .1, "E/F": 0, "A": .4, "G": .2},
    "FSE": {"C": .5, "D": .2, "E/F": .2, "A": -.1, "G": .6},
    "FLSH": {"C": 0, "D": 0, "E/F": -.2, "A": .6, "G": 0},
    "ENS": {"C": .2, "D": .2, "E/F": 0, "A": .3, "G": .1},
}

# --- Tables de dimension -----------------------------------------------------
dim_etab = pd.DataFrame(ETABS, columns=["EtablissementID", "Etablissement", "Site"])
dim_etab["Type"] = np.where(dim_etab.EtablissementID.str.startswith("F"), "Faculté", "École")

dim_parcours = pd.DataFrame(
    [(f"P{i+1:02d}", e, p, round(d, 2), "Oui" if m else "Non") for i, (e, p, d, _, m) in enumerate(PARCOURS)],
    columns=["ParcoursID", "EtablissementID", "Parcours", "IndiceDifficulte", "MasterDisponible"])
P_ID = dict(zip(dim_parcours.Parcours, dim_parcours.ParcoursID))

dim_niveau = pd.DataFrame(NIVEAUX, columns=["NiveauID", "Cycle", "OrdreNiveau"])
dim_niveau["Niveau"] = dim_niveau.NiveauID.map({"L1": "Licence 1", "L2": "Licence 2", "L3": "Licence 3", "M1": "Master 1", "M2": "Master 2"})

dim_annee = pd.DataFrame({"AnneeID": ANNEES})
dim_annee["AnneeUniversitaire"] = dim_annee.AnneeID.astype(str) + "-" + (dim_annee.AnneeID + 1).astype(str)
dim_annee["IndexAnnee"] = dim_annee.AnneeID - ANNEES[0] + 1

ue_rows = []
for pid, parc in zip(dim_parcours.ParcoursID, dim_parcours.Parcours):
    noms = UE_PAR_NIVEAU[parc]
    for niv, _, ordre in NIVEAUX:
        for k in range(NB_UE):
            base = noms[(k + ordre - 1) % len(noms)]
            suffix = {1: "I", 2: "II", 3: "III", 4: "avancé(e) I", 5: "avancé(e) II"}[ordre]
            ue_rows.append(dict(UEID=f"{pid}-{niv}-{k+1}", ParcoursID=pid, NiveauID=niv,
                                UE=f"{base} {suffix}", Semestre=(ordre - 1) * 2 + 1 + (k >= NB_UE // 2),
                                Credits=int(rng.choice([4, 5, 6], p=[.3, .4, .3])),
                                Difficulte=round(float(np.clip(rng.normal(0, 1.1), -2, 2.8)), 2)))
dim_ue = pd.DataFrame(ue_rows)
dim_ue["UELibelle"] = dim_ue.UE + " · " + dim_ue.ParcoursID.map(dict(zip(dim_parcours.ParcoursID, dim_parcours.Parcours))) + " " + dim_ue.NiveauID

# ----------------------------------------------------------------------------
# 2. Simulation des parcours étudiants
# ----------------------------------------------------------------------------
students, inscriptions, notes = [], [], []
sid = 0
active = []  # étudiants en cours : dict(id, pid, etab, niv_ordre, redoublements, aptitude)

ue_by = {k: g for k, g in dim_ue.groupby(["ParcoursID", "NiveauID"])}
niv_code = {o: c for c, _, o in NIVEAUX}
parc_info = {P_ID[p]: (e, d, n, m) for e, p, d, n, m in PARCOURS}

WARMUP = 5  # années simulées avant 2018 pour remplir tous les niveaux (non exportées)
for an in range(ANNEES[0] - WARMUP, ANNEES[-1] + 1):
    trend = max(0, an - ANNEES[0]) * 0.06  # légère amélioration au fil des années
    # nouveaux bacheliers en L1 (croissance des effectifs ~4 %/an)
    for pid, (etab, diff, base_n, _) in parc_info.items():
        n_new = int(base_n * (1.04 ** (an - ANNEES[0])) * rng.uniform(.9, 1.1))  # (an < 2018 : préchauffage)
        for _ in range(n_new):
            sid += 1
            sexe = rng.choice(["F", "M"], p=[.44, .56] if etab not in ("FLSH", "ENS", "FSSA") else [.55, .45])
            serie = rng.choice(list(SERIES_BAC), p=list(SERIES_BAC.values()))
            dep = rng.choice(list(DEPARTEMENTS), p=list(DEPARTEMENTS.values()))
            age_bac = int(rng.choice([17, 18, 19, 20, 21, 22], p=[.08, .27, .30, .20, .10, .05]))
            students.append(dict(EtudiantID=f"E{sid:06d}", Sexe=sexe, SerieBac=serie, Departement=dep,
                                 AnneeNaissance=an - age_bac, AnneeBac=an))
            apt = rng.normal(0, 1) + AFFINITE[etab][serie] * .5 + (.12 if sexe == "F" else 0)
            active.append(dict(id=f"E{sid:06d}", pid=pid, etab=etab, ordre=1, red=0, apt=apt))

    survivors = []
    for st in active:
        etab, diff, _, has_master = parc_info[st["pid"]]
        niv = niv_code[st["ordre"]]
        ins_id = f"I{len(inscriptions)+1:07d}"
        # abandon en cours d'année (plus fréquent en L1)
        p_drop = {1: .10, 2: .05, 3: .03, 4: .03, 5: .02}[st["ordre"]] + max(0, -st["apt"]) * .03 - trend * .1
        if rng.random() < max(p_drop, .01):
            inscriptions.append(dict(InscriptionID=ins_id, EtudiantID=st["id"], AnneeID=an, ParcoursID=st["pid"],
                                     NiveauID=niv, Redoublant="Oui" if st["red"] else "Non",
                                     MoyenneAnnuelle=None, CreditsValides=0, Decision="Abandon"))
            continue
        ues = ue_by[(st["pid"], niv)]
        tot, wsum, cred = 0.0, 0, 0
        for _, ue in ues.iterrows():
            mu = 9.0 + st["apt"] * 2.4 - ue.Difficulte * 1.1 - diff * 2.2 + trend + (st["ordre"] - 1) * .45 + st["red"] * .6
            n1 = float(np.clip(rng.normal(mu, 2.6), 0, 20))
            session = 1
            if n1 < 10 and rng.random() < .6:  # rattrapage
                n1 = float(np.clip(max(n1, rng.normal(mu + .6, 2.3)), 0, 20)); session = 2
            n1 = round(n1 * 4) / 4
            ok = n1 >= 10
            notes.append(dict(InscriptionID=ins_id, UEID=ue.UEID, Note=n1, Session=session,
                              Valide="Oui" if ok else "Non"))
            tot += n1 * ue.Credits; wsum += ue.Credits; cred += ue.Credits if ok else 0
        moy = round(tot / wsum, 2)
        if moy >= 10:
            dec = "Admis"
        else:
            p_quit = .25 + .2 * st["red"] + (.1 if st["ordre"] == 1 else 0)
            dec = "Abandon" if (rng.random() < p_quit or st["red"] >= 2) else "Redouble"
        inscriptions.append(dict(InscriptionID=ins_id, EtudiantID=st["id"], AnneeID=an, ParcoursID=st["pid"],
                                 NiveauID=niv, Redoublant="Oui" if st["red"] else "Non",
                                 MoyenneAnnuelle=moy, CreditsValides=cred, Decision=dec))
        if dec == "Redouble":
            st["red"] += 1; survivors.append(st)
        elif dec == "Admis":
            if st["ordre"] == 3 and not (has_master and rng.random() < .45):
                continue  # diplômé de Licence, quitte l'université
            if st["ordre"] == 5:
                continue  # diplômé de Master
            st["ordre"] += 1; st["red"] = 0; survivors.append(st)
    active = survivors

fait_ins = pd.DataFrame(inscriptions)
fait_notes = pd.DataFrame(notes)
fait_ins = fait_ins[fait_ins.AnneeID >= ANNEES[0]].reset_index(drop=True)
fait_notes = fait_notes[fait_notes.InscriptionID.isin(fait_ins.InscriptionID)].reset_index(drop=True)
dim_etudiant = pd.DataFrame(students)
dim_etudiant = dim_etudiant[dim_etudiant.EtudiantID.isin(fait_ins.EtudiantID)].reset_index(drop=True)
fait_notes.insert(0, "NoteID", [f"N{i+1:07d}" for i in range(len(fait_notes))])

# ----------------------------------------------------------------------------
# 3. Export
# ----------------------------------------------------------------------------
path = os.path.join(OUT, "SMILE_donnees.xlsx")
with pd.ExcelWriter(path, engine="openpyxl") as xw:
    pd.DataFrame({"Information": [
        "SMILE — Système de Mesure et d'Indicateurs pour L'Enseignement",
        "Jeu de données FICTIF généré automatiquement pour le prototype Power BI.",
        "Aucune donnée réelle d'étudiant. Structure des établissements à valider avec l'université.",
        "Auteur : Mabari Uriel",
    ]}).to_excel(xw, sheet_name="LISEZ-MOI", index=False)
    dim_etab.to_excel(xw, sheet_name="DimEtablissement", index=False)
    dim_parcours.to_excel(xw, sheet_name="DimParcours", index=False)
    dim_niveau.to_excel(xw, sheet_name="DimNiveau", index=False)
    dim_annee.to_excel(xw, sheet_name="DimAnnee", index=False)
    dim_ue.to_excel(xw, sheet_name="DimUE", index=False)
    dim_etudiant.to_excel(xw, sheet_name="DimEtudiant", index=False)
    fait_ins.to_excel(xw, sheet_name="FaitInscription", index=False)
    fait_notes.to_excel(xw, sheet_name="FaitNoteUE", index=False)

print(f"Écrit : {path}")
for name, df in [("DimEtablissement", dim_etab), ("DimParcours", dim_parcours), ("DimUE", dim_ue),
                 ("DimEtudiant", dim_etudiant), ("FaitInscription", fait_ins), ("FaitNoteUE", fait_notes)]:
    print(f"  {name:18s} {len(df):>8,d} lignes")
