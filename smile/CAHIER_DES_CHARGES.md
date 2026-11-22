# Cahier des charges — SMILE
**Système de Mesure et d'Indicateurs pour L'Enseignement**
Porteur du projet : **Mabari Uriel**, analyste stratégique et expert Power BI

---

## 1. Contexte
L'Université Marien Ngouabi regroupe plusieurs facultés, écoles et instituts répartis sur différents sites.
Chaque établissement produit chaque année des données (inscriptions, notes, décisions de jury), mais elles sont
dispersées entre registres papier et fichiers Excel, et peu exploitées. Il n'existe pas de vue d'ensemble.

## 2. Problématique
> Comment centraliser et analyser les données académiques des établissements de l'Université Marien Ngouabi,
> afin de suivre l'évolution des résultats de chaque parcours et d'aider les responsables à décider ?

## 3. Objectifs
**Général :** concevoir un tableau de bord décisionnel unifié, sous Power BI, couvrant toute l'université.

**Spécifiques :**
1. Centraliser les données de tous les établissements dans un modèle unique.
2. Suivre dans le temps les taux de réussite, d'échec, de redoublement et d'abandon par parcours.
3. Comparer établissements, parcours et niveaux (L1 → M2).
4. Repérer les UE et les parcours en difficulté.
5. Analyser les profils (sexe, série du bac, département d'origine).
6. Anticiper les effectifs et repérer tôt les étudiants à risque.

## 4. Utilisateurs
| Utilisateur | Besoin |
|---|---|
| Rectorat | Vision globale, comparaison des établissements |
| Doyens et directeurs | Pilotage de leur établissement |
| Chefs de parcours, enseignants | UE à risque, suivi des cohortes |
| Étudiants, futurs bacheliers | Orientation (version publique simplifiée, données agrégées uniquement) |

## 5. Indicateurs
| Indicateur | Définition |
|---|---|
| Taux de réussite | Admis ÷ Inscrits |
| Taux de redoublement | Redoublements ÷ Inscrits |
| Taux d'abandon | Abandons ÷ Inscrits |
| Taux d'échec | (Redoublements + Abandons) ÷ Inscrits |
| Taux de validation d'UE | Notes ≥ 10 ÷ Notes saisies |
| Moyenne générale | Moyenne des moyennes annuelles |
| Évolution N-1 | Écart en points avec l'année précédente |

## 6. Données nécessaires (à demander à l'université)
Fichiers **anonymisés** (aucun nom, matricule remplacé par un code) :
- Inscriptions : code étudiant, année, établissement, parcours, niveau, redoublant (oui/non), décision du jury
- Notes : code étudiant, année, UE, note, session
- Profil : sexe, série du bac, année du bac, département d'origine, année de naissance
- Référentiels : liste des établissements, parcours, UE (crédits, semestre)

Le prototype utilise **exactement** cette structure : il suffira de remplacer le fichier fictif par les vraies données.

## 7. Confidentialité
- Données anonymisées avant transmission ; engagement de confidentialité signé.
- Aucune donnée individuelle dans la version publique.
- Sécurité au niveau des lignes (RLS) : chaque doyen ne voit que son établissement.

## 8. Outils
Power BI Desktop (gratuit), Power BI Service (publication), Excel, Power Query, DAX, Python (prévisions).

## 9. Planning indicatif (12 semaines)
| Semaines | Livrable |
|---|---|
| 1–2 | Prototype sur données fictives ✅ (en cours), rencontre avec le doyen de la FST |
| 3–4 | Collecte et nettoyage des données réelles (pilote FST) |
| 5–6 | Modèle de données et mesures validés |
| 7–9 | Rapport complet (6 pages) |
| 10–11 | Module de prévision, tests utilisateurs |
| 12 | Présentation officielle et rapport écrit |
