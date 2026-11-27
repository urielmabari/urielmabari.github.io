"""Calcule les indicateurs du tableau de bord (contrôle des mesures DAX + images d'aperçu)."""
import json, os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
x = pd.read_excel(os.path.join(HERE, "..", "donnees", "Pharmacie_donnees.xlsx"), sheet_name=None)
P = x["DimProduit"]
v = x["FaitVente"].merge(P[["ProduitID", "Produit", "Categorie", "PrixAchat"]])
v["Marge"] = v.MontantTTC - v.CoutAchat
v["M"] = v.Date.dt.to_period("M")
cur = v[v.Date >= "2025-11-01"]
prv = v[(v.Date >= "2024-11-01") & (v.Date < "2025-11-01")]
k = lambda d: dict(ca=int(d.MontantTTC.sum()), mg=int(d.Marge.sum()), tk=int(d.TicketID.nunique()),
                   pan=float(d.MontantTTC.sum() / d.TicketID.nunique()))
D = {"cur": k(cur), "prv": k(prv)}
mc = cur.groupby(cur.Date.dt.month).MontantTTC.sum(); mp = prv.groupby(prv.Date.dt.month).MontantTTC.sum()
D["mois"] = [[m, int(mc[m]), int(mp[m])] for m in [11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]]
pvn = dict(zip(x["DimPointVente"].PointVenteID, x["DimPointVente"].Arrondissement))
g = cur.groupby("PointVenteID").agg(ca=("MontantTTC", "sum"), mg=("Marge", "sum"))
D["pv"] = [[pvn[i], int(r.ca), float(r.mg / r.ca)] for i, r in g.iterrows()]
t = cur.groupby("TicketID").agg(p=("ModePaiement", "first"), h=("Heure", "first"), d=("Date", "first"))
D["pay"] = t.p.value_counts(normalize=True).to_dict()
tall = v.groupby("TicketID").agg(p=("ModePaiement", "first"), d=("Date", "first"))
q = pd.crosstab(tall.d.dt.to_period("Q").astype(str), tall.p, normalize="index")
D["mmq"] = [[i, float(r["MTN MoMo"] + r["Airtel Money"])] for i, r in q.iterrows()]
hm = pd.crosstab(t.d.dt.dayofweek, t.h) / 52
D["heat"] = hm.round(1).values.tolist(); D["hours"] = [int(h) for h in hm.columns]
tp = cur.groupby("Produit").agg(ca=("MontantTTC", "sum"), mg=("Marge", "sum")).sort_values("ca", ascending=False).head(10)
D["top"] = [[i, int(r.ca), float(r.mg / r.ca)] for i, r in tp.iterrows()]
D["cat"] = [[i, int(s)] for i, s in cur.groupby("Categorie").MontantTTC.sum().sort_values(ascending=False).items()]
D["palu"] = [[str(i), int(s)] for i, s in v[v.Categorie == "Antipaludéens"].groupby("M").MontantTTC.sum().items()]
st = x["FaitStock"].merge(P[["ProduitID", "Produit", "PrixAchat"]]).merge(x["ConsoMoyenne"], on=["PointVenteID", "ProduitID"])
st["jours"] = (st.DatePeremption - st.DateInventaire).dt.days
st["val"] = st.QuantiteStock * st.PrixAchat
st["pv"] = st.PointVenteID.map(pvn)
D["stockval"] = int(st.val.sum()); D["exp90"] = int(st[st.jours <= 90].val.sum()); D["exp30"] = int(st[st.jours <= 30].val.sum())
D["explist"] = [[r.Produit, r.pv, r.Lot, int(r.QuantiteStock), int(r.jours), int(r.val)]
                for r in st[st.jours <= 90].sort_values("jours").head(8).itertuples()]
cov = st.groupby(["pv", "Produit"]).agg(q=("QuantiteStock", "sum"), c=("VenteMoyJour", "first")).reset_index()
cov["couv"] = cov.q / cov.c
low = cov[cov.couv < 10].sort_values("couv")
D["nrupt"] = len(low); D["ruptlist"] = [[r.Produit, r.pv, round(float(r.couv), 1)] for r in low.head(6).itertuples()]
a = v[(v.PointVenteID == "PV3") & (v.ProduitID == "PR004")]
feb = a[(a.Date >= "2025-02-01") & (a.Date < "2025-03-01")].MontantTTC.sum()
mar = a[(a.Date >= "2025-03-01") & (a.Date < "2025-04-01")].MontantTTC.sum()
D["rupt_loss"] = int(feb * 31 / 28 - mar)
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "indicateurs.json")
json.dump(D, open(out, "w"), ensure_ascii=False, indent=1)
print({kk: D[kk] for kk in ["cur", "prv", "stockval", "exp90", "exp30", "nrupt", "rupt_loss"]})
