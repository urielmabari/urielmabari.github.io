# 💊 Analyse Power BI d'une pharmacie à Brazzaville (cas d'étude)

**Auteur :** Mabari Uriel, analyste stratégique et expert Power BI

> ⚠️ **Pharmacie et données fictives.** Ce cas d'étude a été généré par `scripts/generer_donnees.py`
> pour démontrer une démarche d'analyse. Aucune donnée réelle d'entreprise n'est utilisée.

## Le cas
Une pharmacie avec **3 points de vente** (Poto-Poto, Moungali, Bacongo), **30 produits** répartis en 9 catégories,
et **24 mois de ventes** (novembre 2024 → octobre 2026) : environ 163 000 tickets et 310 000 lignes de vente.

## Fichiers
| Fichier | Contenu |
|---|---|
| `donnees/Pharmacie_donnees.xlsx` | DimProduit, DimPointVente, DimCalendrier, FaitVente, FaitStock (lots et dates de péremption), ConsoMoyenne |
| `powerbi/mesures.dax` | Mesures DAX : CA, marge, panier moyen, comparaison N-1, Mobile Money, péremption, couverture de stock |
| `scripts/generer_donnees.py` | Génération des données |
| `scripts/analyse.py` | Calcul des indicateurs (contrôle des résultats DAX) |

## Modèle
`FaitVente` → DimProduit (ProduitID), DimPointVente (PointVenteID), DimCalendrier (Date)
`FaitStock` → DimProduit, DimPointVente · `ConsoMoyenne` → DimProduit, DimPointVente
Marquer `DimCalendrier` comme **table de dates**.

## Les 3 pages du rapport
1. **Performance commerciale** : CA, marge, tickets, panier moyen (vs N-1), CA mensuel N / N-1, modes de paiement, CA et marge par point de vente
2. **Produits & saisonnalité** : top 10 des produits, CA par catégorie, saisonnalité des antipaludéens, carte de chaleur de l'affluence par jour et par heure
3. **Stock & péremption** : valeur du stock, stock à périmer (30 / 90 jours), lots prioritaires, risques de rupture

## Ce que révèle l'analyse (12 derniers mois)
| Constat | Chiffre | Recommandation |
|---|---|---|
| Croissance | CA 539,2 M FCFA, **+10,8 %** ; panier moyen stable (6 302 F) | La croissance vient du nombre de clients |
| Antipaludéens | **30 % du CA**, ventes ×1,8 en saison des pluies | Constituer le stock dès septembre |
| Bacongo | Marge **26,7 %** contre ~29,8 % ailleurs | Revoir la politique de remises |
| Mobile Money | **23 % → 41 %** des paiements en 2 ans | Promouvoir MoMo et Airtel Money aux caisses |
| Péremption | **9,5 M FCFA** de stock périme sous 90 jours (23,8 %) | Transferts entre points de vente, promotions ciblées |
| Rupture | Antipaludéen à Bacongo en mars 2025 : **~1,2 M FCFA** de ventes perdues | Seuil d'alerte de réapprovisionnement |
| Affluence | Pics 9 h – 11 h et 17 h – 19 h, samedi | Renforcer le personnel à ces heures |
