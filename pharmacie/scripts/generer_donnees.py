"""
Projet Power BI — Pharmacie (FICTIVE) à Brazzaville.
Génère 24 mois de ventes (nov. 2024 → oct. 2026) pour 3 points de vente,
un catalogue de produits et un état du stock avec dates de péremption.
Toutes les données sont inventées.
"""
import os
import numpy as np
import pandas as pd

rng = np.random.default_rng(242)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "donnees")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- Produits
# (produit, catégorie, prix vente FCFA, taux de marge, ordonnance, popularité, saisonnier_palu)
P = [
 ("Paracétamol 500 mg (boîte 16)", "Antalgiques", 600, .35, "Non", 10, 0),
 ("Doliprane 1000 mg", "Antalgiques", 1500, .30, "Non", 6, 0),
 ("Ibuprofène 400 mg", "Antalgiques", 1200, .33, "Non", 4, 0),
 ("Artéméther-Luméfantrine 80/480", "Antipaludéens", 3500, .28, "Oui", 7, 1),
 ("Artésunate-Amodiaquine", "Antipaludéens", 3000, .28, "Oui", 4, 1),
 ("Quinine 300 mg", "Antipaludéens", 2500, .30, "Oui", 2, 1),
 ("Test de diagnostic rapide paludisme", "Antipaludéens", 1500, .40, "Non", 3, 1),
 ("Amoxicilline 500 mg", "Antibiotiques", 2500, .30, "Oui", 5, 0),
 ("Amoxicilline + Ac. clavulanique", "Antibiotiques", 6500, .25, "Oui", 2, 0),
 ("Ciprofloxacine 500 mg", "Antibiotiques", 3000, .28, "Oui", 2, 0),
 ("Métronidazole 500 mg", "Antibiotiques", 1500, .32, "Oui", 3, 0),
 ("SRO (sels de réhydratation)", "Gastro-entérologie", 300, .45, "Non", 4, 0),
 ("Oméprazole 20 mg", "Gastro-entérologie", 2500, .32, "Non", 2, 0),
 ("Smecta", "Gastro-entérologie", 3500, .30, "Non", 2, 0),
 ("Vitamine C 500 mg", "Vitamines & compléments", 1500, .40, "Non", 5, 0),
 ("Multivitamines adulte", "Vitamines & compléments", 4500, .38, "Non", 2, 0),
 ("Fer + Acide folique", "Vitamines & compléments", 2000, .38, "Non", 3, 0),
 ("Amlodipine 5 mg", "Cardiologie & diabète", 3000, .27, "Oui", 3, 0),
 ("Metformine 850 mg", "Cardiologie & diabète", 2500, .27, "Oui", 3, 0),
 ("Bandelettes glycémie (50)", "Cardiologie & diabète", 12000, .22, "Non", 1, 0),
 ("Sirop contre la toux", "ORL & respiratoire", 2500, .35, "Non", 3, 0),
 ("Salbutamol inhalateur", "ORL & respiratoire", 4000, .28, "Oui", 1, 0),
 ("Crème hydratante", "Parapharmacie", 3500, .45, "Non", 2, 0),
 ("Savon antiseptique", "Parapharmacie", 1000, .45, "Non", 3, 0),
 ("Préservatifs (boîte 3)", "Parapharmacie", 500, .50, "Non", 3, 0),
 ("Couches bébé (paquet)", "Parapharmacie", 6000, .30, "Non", 2, 0),
 ("Lait infantile 1er âge", "Parapharmacie", 8500, .20, "Non", 1, 0),
 ("Seringues 5 ml (10)", "Matériel médical", 1000, .40, "Non", 2, 0),
 ("Compresses stériles", "Matériel médical", 800, .45, "Non", 2, 0),
 ("Tensiomètre électronique", "Matériel médical", 25000, .25, "Non", .2, 0),
]
FOURN = {"Antalgiques": "Grossiste A", "Antipaludéens": "Grossiste B", "Antibiotiques": "Grossiste A",
         "Gastro-entérologie": "Grossiste C", "Vitamines & compléments": "Grossiste C",
         "Cardiologie & diabète": "Grossiste B", "ORL & respiratoire": "Grossiste A",
         "Parapharmacie": "Grossiste D", "Matériel médical": "Grossiste D"}
prod = pd.DataFrame(P, columns=["Produit", "Categorie", "PrixVente", "TauxMarge", "Ordonnance", "Popularite", "Palu"])
prod.insert(0, "ProduitID", [f"PR{i+1:03d}" for i in range(len(prod))])
prod["PrixAchat"] = (prod.PrixVente * (1 - prod.TauxMarge)).round(-1).astype(int)
prod["Fournisseur"] = prod.Categorie.map(FOURN)

# ---------------------------------------------------------------- Points de vente
pv = pd.DataFrame([
    ("PV1", "Point de vente Poto-Poto", "Poto-Poto", 1.25, 2016),
    ("PV2", "Point de vente Moungali", "Moungali", 1.00, 2019),
    ("PV3", "Point de vente Bacongo", "Bacongo", 0.80, 2023),
], columns=["PointVenteID", "PointVente", "Arrondissement", "_poids", "AnneeOuverture"])

# ---------------------------------------------------------------- Ventes
dates = pd.date_range("2024-11-01", "2026-10-31", freq="D")
m = dates.month.values
# saison des pluies (oct.→mai) : pic de paludisme
rain = np.where(np.isin(m, [10, 11, 12, 1, 2, 3, 4, 5]), 1.0, 0.0)
palu_season = 1 + 0.9 * rain * (1 + 0.3 * np.isin(m, [11, 12, 3, 4]))
growth = 1 + 0.12 * np.arange(len(dates)) / 365          # +12 %/an
dow = dates.dayofweek.values
dow_f = np.array([1.05, 1.0, 1.0, 1.0, 1.1, 1.15, 0.65])[dow]  # dimanche plus calme
month_start = np.where(dates.day.values <= 7, 1.12, 1.0)      # après la paie

popw = prod.Popularite.values / prod.Popularite.sum()
rows = []
tid = 0
for _, s in pv.iterrows():
    n_tickets = rng.poisson(58 * s._poids * growth * dow_f * month_start * (1 + 0.15 * rain))
    for di, (d, nt) in enumerate(zip(dates, n_tickets)):
        if nt == 0:
            continue
        # poids produits du jour (paludisme saisonnier)
        w = popw * np.where(prod.Palu.values == 1, palu_season[di], 1.0)
        # rupture d'Artéméther en mars 2025 au PV3
        if s.PointVenteID == "PV3" and d.year == 2025 and d.month == 3 and d.day >= 10:
            w = w * np.where(prod.ProduitID.values == "PR004", 0.0, 1.0)
        w = w / w.sum()
        hours = rng.choice(np.arange(7, 22), size=nt,
                           p=np.array([2, 5, 8, 9, 8, 7, 6, 5, 6, 8, 10, 9, 8, 6, 3]) / 100)
        # part Mobile Money croissante dans le temps
        mm = 0.22 + 0.20 * di / len(dates)
        for k in range(nt):
            tid += 1
            nl = 1 + rng.binomial(3, .3)
            items = rng.choice(len(prod), size=nl, replace=False, p=w)
            pay = rng.choice(["Espèces", "MTN MoMo", "Airtel Money", "Assurance / tiers payant"],
                             p=[1 - mm - .08, mm * .65, mm * .35, .08])
            cli = "Assuré" if pay == "Assurance / tiers payant" else rng.choice(["Particulier", "Client fidèle"], p=[.72, .28])
            for it in items:
                q = 1 + rng.binomial(2, .2)
                pu = int(prod.PrixVente.iat[it])
                rem = 0.05 if cli == "Client fidèle" else 0.0
                rows.append((f"T{tid:07d}", d, int(hours[k]), s.PointVenteID, prod.ProduitID.iat[it], q, pu,
                             rem, pay, cli))

v = pd.DataFrame(rows, columns=["TicketID", "Date", "Heure", "PointVenteID", "ProduitID", "Quantite",
                                "PrixUnitaire", "Remise", "ModePaiement", "TypeClient"])
v = v.merge(prod[["ProduitID", "PrixAchat"]], on="ProduitID")
# Bacongo : remises commerciales plus fortes (nouveau point de vente)
v.loc[v.PointVenteID == "PV3", "Remise"] += 0.04
v["MontantTTC"] = (v.Quantite * v.PrixUnitaire * (1 - v.Remise)).round().astype(int)
v["CoutAchat"] = (v.Quantite * v.PrixAchat).astype(int)
v = v.drop(columns="PrixAchat").sort_values(["Date", "TicketID"]).reset_index(drop=True)
v.insert(0, "LigneID", [f"L{i+1:07d}" for i in range(len(v))])

# ---------------------------------------------------------------- Stock au 31/10/2026 (lots)
ref = pd.Timestamp("2026-10-31")
daily = v[v.Date > ref - pd.Timedelta(days=90)].groupby(["PointVenteID", "ProduitID"]).Quantite.sum() / 90
st = []
for (pid_pv, pid), dq in daily.items():
    cover_days = rng.choice([8, 20, 35, 60, 120], p=[.12, .3, .3, .18, .1])
    qty_total = int(dq * cover_days)
    nlots = rng.integers(1, 4)
    for j in range(nlots):
        q = max(1, qty_total // nlots)
        base = int(rng.choice([25, 60, 80, 150, 300, 500, 700], p=[.07, .08, .08, .17, .25, .2, .15]))
        exp = ref + pd.Timedelta(days=max(5, base + int(rng.integers(-18, 19))))
        st.append((pid_pv, pid, f"LOT{len(st)+1:05d}", q, exp))
stock = pd.DataFrame(st, columns=["PointVenteID", "ProduitID", "Lot", "QuantiteStock", "DatePeremption"])
stock["DateInventaire"] = ref
cons = daily.rename("VenteMoyJour").reset_index()

# ---------------------------------------------------------------- Calendrier
cal = pd.DataFrame({"Date": dates})
cal["Annee"] = cal.Date.dt.year
cal["MoisNum"] = cal.Date.dt.month
cal["Mois"] = cal.Date.dt.strftime("%Y-%m")
mois_fr = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
cal["MoisNom"] = cal.MoisNum.map(lambda k: mois_fr[k - 1])
cal["JourSemaine"] = cal.Date.dt.dayofweek.map(lambda k: ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"][k])
cal["NumJourSemaine"] = cal.Date.dt.dayofweek + 1
cal["Saison"] = np.where(np.isin(cal.MoisNum, [10, 11, 12, 1, 2, 3, 4, 5]), "Saison des pluies", "Saison sèche")

path = os.path.join(OUT, "Pharmacie_donnees.xlsx")
with pd.ExcelWriter(path, engine="openpyxl") as xw:
    pd.DataFrame({"Information": ["Pharmacie fictive — Brazzaville. Données inventées pour un projet Power BI.",
                                  "Auteur : Mabari Uriel"]}).to_excel(xw, sheet_name="LISEZ-MOI", index=False)
    prod.drop(columns=["Popularite", "Palu", "TauxMarge"]).to_excel(xw, sheet_name="DimProduit", index=False)
    pv.drop(columns="_poids").to_excel(xw, sheet_name="DimPointVente", index=False)
    cal.to_excel(xw, sheet_name="DimCalendrier", index=False)
    v.to_excel(xw, sheet_name="FaitVente", index=False)
    stock.to_excel(xw, sheet_name="FaitStock", index=False)
    cons.to_excel(xw, sheet_name="ConsoMoyenne", index=False)
print("Écrit :", path, "|", len(v), "lignes de vente,", v.TicketID.nunique(), "tickets,", len(stock), "lots")
