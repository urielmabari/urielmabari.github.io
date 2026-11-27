# 😊 SMILE — Système de Mesure et d'Indicateurs pour L'Enseignement

Plateforme d'analyse décisionnelle **Power BI** pour suivre la réussite des étudiants de l'Université Marien Ngouabi :
établissements, parcours, niveaux, unités d'enseignement (UE), années.

**Auteur :** Mabari Uriel, analyste stratégique et expert Power BI · 06 958 27 35 · urielmabari350@gmail.com

> ⚠️ **Phase prototype.** Les données de `donnees/SMILE_donnees.xlsx` sont **fictives**, générées par
> `scripts/generer_donnees.py`. Elles servent à construire et démontrer le rapport en attendant les
> données réelles et anonymisées de l'université.

---

## 📁 Contenu du dossier

| Fichier | Rôle |
|---|---|
| `donnees/SMILE_donnees.xlsx` | Jeu de données fictif : 7 années (2018-2019 → 2024-2025), 7 établissements, 16 parcours, ~55 000 inscriptions, ~309 000 notes |
| `scripts/generer_donnees.py` | Script Python qui régénère les données (`python generer_donnees.py`) |
| `powerbi/mesures.dax` | Toutes les mesures DAX à copier dans Power BI |
| `powerbi/theme_smile.json` | Thème de couleurs SMILE (bleu nuit, or) |
| `CAHIER_DES_CHARGES.md` | Objectifs, indicateurs, périmètre, planning |

---

## 🧱 Le modèle de données (schéma en étoile)

```
                      DimEtablissement
                             │ 1
                             │
                             ▼ *
DimAnnee ──1───*──┐     DimParcours
                  │          │ 1
DimNiveau ─1───*──┤          │
                  ▼          ▼ *
DimEtudiant ─1─*─► FaitInscription ──1───*──► FaitNoteUE ◄──*───1── DimUE
```

| Table | Une ligne = | Colonnes clés |
|---|---|---|
| **FaitInscription** | un étudiant inscrit une année dans un parcours et un niveau | `Decision` (Admis / Redouble / Abandon), `MoyenneAnnuelle`, `CreditsValides`, `Redoublant` |
| **FaitNoteUE** | une note d'un étudiant dans une UE | `Note` (/20), `Session` (1 ou 2), `Valide` |
| DimEtudiant | un étudiant (anonyme) | `Sexe`, `SerieBac`, `Departement`, `AnneeNaissance` |
| DimParcours | un parcours | `Parcours`, `EtablissementID`, `IndiceDifficulte` |
| DimEtablissement | une faculté ou école | `Etablissement`, `Type`, `Site` |
| DimNiveau | L1 … M2 | `Niveau`, `Cycle`, `OrdreNiveau` |
| DimAnnee | une année universitaire | `AnneeUniversitaire`, `AnneeID` |
| DimUE | une unité d'enseignement | `UELibelle`, `Credits`, `Semestre` |

---

## 🛠️ Construire le rapport pas à pas

### Étape 1 — Importer les données
1. Ouvrir **Power BI Desktop**, puis **Accueil > Obtenir les données > Classeur Excel**.
2. Choisir `SMILE_donnees.xlsx` et cocher **les 8 feuilles** (sauf `LISEZ-MOI`).
3. Cliquer sur **Transformer les données** et vérifier les types dans Power Query :
   - `Note`, `MoyenneAnnuelle` → **Nombre décimal**
   - `AnneeID`, `Credits`, `Session`, `OrdreNiveau`, `CreditsValides` → **Nombre entier**
   - les identifiants (`...ID`) → **Texte**, sauf `AnneeID`
4. **Fermer et appliquer.**

### Étape 2 — Créer les relations (vue Modèle)
Power BI en détecte certaines automatiquement : vérifier qu'elles correspondent **exactement** à cette liste.

| De (côté *) | Vers (côté 1) | Filtrage |
|---|---|---|
| FaitInscription[EtudiantID] | DimEtudiant[EtudiantID] | Unique |
| FaitInscription[AnneeID] | DimAnnee[AnneeID] | Unique |
| FaitInscription[ParcoursID] | DimParcours[ParcoursID] | Unique |
| FaitInscription[NiveauID] | DimNiveau[NiveauID] | Unique |
| DimParcours[EtablissementID] | DimEtablissement[EtablissementID] | Unique |
| FaitNoteUE[InscriptionID] | FaitInscription[InscriptionID] | Unique |
| FaitNoteUE[UEID] | DimUE[UEID] | Unique |

❗ **Ne pas relier** `DimUE` à `DimParcours` ni à `DimNiveau`, sinon le modèle devient ambigu.

### Étape 3 — Tris et formats
- `DimAnnee[AnneeUniversitaire]` → **Outils de colonne > Trier par colonne > AnneeID**
- `DimNiveau[Niveau]` → **Trier par colonne > OrdreNiveau**
- Masquer les colonnes `...ID` dans les tables de faits (clic droit > Masquer dans la vue rapport).

### Étape 4 — Ajouter les mesures
1. **Accueil > Entrer des données**, nommer la table **`_Mesures`** et charger.
2. Ouvrir `powerbi/mesures.dax`, puis pour chaque bloc : clic droit sur `_Mesures` > **Nouvelle mesure** > coller.
3. Mettre au format **Pourcentage (1 décimale)** toutes les mesures « Taux… » et « Part… ».

### Étape 5 — Appliquer le thème
**Affichage > Thèmes > Parcourir les thèmes** > `powerbi/theme_smile.json`.

### Étape 6 — Les pages du rapport

| Page | Visuels conseillés |
|---|---|
| **1. Vue Université** | Segments : Année, Établissement, Niveau · Cartes : Nb Étudiants, Taux de réussite, Taux d'abandon, Moyenne générale, Évolution réussite (texte) · Courbe : Taux de réussite par AnneeUniversitaire · Barres : Taux de réussite par Établissement (couleur = *Couleur réussite*) · Anneau : Nb Inscriptions par Decision |
| **2. Établissements & parcours** | Matrice : lignes Établissement > Parcours, colonnes Niveau, valeur Taux de réussite (fond coloré par *Couleur réussite*) · Barres horizontales : classement des parcours |
| **3. Évolution des parcours** | Courbe : Taux de réussite par AnneeUniversitaire, légende Parcours (ou **petits multiples** par Établissement) · Aires empilées : Nb Inscriptions par Niveau et par année |
| **4. UE à risque** | Tableau : UELibelle, Taux de validation UE, Note moyenne UE, Part en rattrapage, Rang UE, Statut UE · Filtre : Statut UE = « UE critique » · Nuage de points : Note moyenne UE × Taux de validation UE |
| **5. Profils étudiants** | Taux de réussite par Sexe, par SerieBac, par Departement · Carte : Part des femmes · Écart femmes - hommes |
| **6. Prévisions** | Courbe : Nb Inscriptions par AnneeID (axe **continu**) → volet **Analyse > Prévision** sur 2 périodes, intervalle de confiance 95 % |

💡 **Navigation :** ajouter des boutons (Insertion > Boutons > Navigateur de pages) et activer **l'extraction (drill-through)** de la page 2 vers la page 4 sur le champ `Parcours`.

### Étape 7 — Vérifier les chiffres
Avec les données fictives actuelles, les mesures doivent donner :

| Contrôle | Valeur attendue |
|---|---|
| Nb Inscriptions (toutes années) | 54 856 |
| Nb Étudiants | 25 135 |
| Taux de réussite (toutes années) | 54,8 % |
| Taux de redoublement / d'abandon | 22,5 % / 22,8 % |
| Taux de réussite 2024-2025 | 57,7 % (▲ +0,9 pt vs N-1) |
| Taux de validation UE | 58,5 % |
| Moyenne générale | 10,36 |
| Réussite 2024-2025 : ENS / FSSA | 64,1 % / 48,4 % |

Si un chiffre diffère, vérifier d'abord les relations (étape 2) et les types (étape 1).

---

## 🗺️ Feuille de route

- [x] Données fictives et modèle en étoile
- [x] Mesures DAX et thème
- [ ] Rapport Power BI (6 pages) : **à construire dans Power BI Desktop**
- [ ] Démonstration au rectorat ou au doyen de la FST
- [ ] Remplacement par les données réelles anonymisées (même structure de colonnes)
- [ ] Module Python de détection des étudiants à risque
- [ ] Publication sur Power BI Service
