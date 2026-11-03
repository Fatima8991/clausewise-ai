# ClauseWise AI

**Analyse explicable de contrats d’assurance — de la clause à la décision métier.**

ClauseWise AI est un projet personnel de portfolio initié et porté par **Fatima Oumouloud**. Il explore une question métier concrète : *à partir des conditions générales d’un contrat d’assurance habitation, peut-on expliquer si un sinistre semble couvert, identifier les clauses pertinentes et reconnaître les cas où les éléments disponibles ne permettent pas de conclure ?*

Le projet reprend le cas d’usage « Un sinistre et les conditions générales » proposé dans un brief de recrutement. Le nom **ClauseWise AI**, le cadrage du prototype, les choix de conception, l’architecture de démonstration, l’interface et les scénarios de validation constituent le travail de portfolio présenté ici.

> **Transparence sur le développement :** ClauseWise AI est un projet personnel initié et porté par Fatima Oumouloud. Le cadrage fonctionnel, l’orientation produit et les choix de conception sont présentés et assumés par sa porteuse. Une assistance IA a été utilisée comme outil d’accélération pour le code et la rédaction ; le code doit être relu, compris et validé avant toute évolution ou utilisation en conditions réelles.

## Objectif produit

L’outil permet de charger un contrat PDF textuel ou TXT, de poser une question formulée en langage naturel et d’obtenir une première analyse structurée :

- une qualification prudente (`Garantie potentiellement applicable`, `Couverture non établie` ou `Analyse à revoir`) ;
- les passages contractuels retrouvés, avec leur page et leur extrait ;
- une explication du raisonnement et des points de vigilance ;
- une abstention lorsque les éléments retrouvés ne suffisent pas à étayer une conclusion.

**Principe de conception : la preuve contractuelle avant la confiance dans la réponse.** Une absence de clause retrouvée ne prouve pas automatiquement une exclusion. Le prototype distingue donc « non établi » de « exclu ».

## Démonstration actuelle

La version incluse est un prototype fonctionnel local, sans clé API ni service payant obligatoire.

| Fonction | État |
|---|---|
| Import PDF textuel et TXT | Implémenté |
| Extraction du texte PDF et conservation du numéro de page | Implémenté |
| Découpage en passages/clauses | Implémenté, heuristique |
| Recherche lexicale pondérée de type BM25 | Implémenté, version légère |
| Restitution des extraits et pages sources | Implémenté |
| Qualification prudente et abstention | Implémenté, règles déterministes |
| Interface web dédiée | Implémentée |
| Jeu de tests unitaires | 3 tests inclus |
| OCR des PDF scannés | Non implémenté |
| Recherche vectorielle et reranking | Non implémentés |
| Analyse LLM avec validation automatique des citations | Non implémentée |
| Authentification, chiffrement et isolation multi-client | Non implémentés |

Le contrat livré dans `sample-data/` est **entièrement synthétique**. Il sert à lancer la démonstration immédiatement et ne représente aucun assureur.

## Sources documentaires publiques pour les essais

Le brief demande de récupérer des conditions générales accessibles en ligne. Les liens ci-dessous constituent un point de départ pour les tests manuels. Les PDF restent hébergés par leurs éditeurs : le dépôt ne les redistribue pas. Téléchargez le document depuis la source, puis importez-le dans l’application.

1. **MACIF — Conditions générales Macif Habitation, version 06/2025** : [PDF officiel](https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_habitation/CG-Macif-Habitation.pdf).
2. **Direct Assurance — Conditions générales multirisque habitation** : [page d’information et accès au PDF éditeur](https://www.direct-assurance.fr/assurance-habitation/sinistre-garanties-habitation/la-garantie-vol-de-votre-assurance-habitation).
3. **Caisse d’Épargne — Assurance habitation, documents contractuels** : [page officielle des documents](https://www.caisse-epargne.fr/assurer/assurance-habitation/).
4. **Service-Public.fr — Explication générale de la garantie vol** : [fiche officielle](https://www.service-public.gouv.fr/particuliers/vosdroits/F2028). Cette fiche est une source de contexte, pas un contrat d’assurance et ne doit pas être utilisée comme preuve contractuelle.

Voir [`SOURCES.md`](SOURCES.md) pour les précautions de comparaison et les scénarios de test.

## Architecture

```text
clausewise-ai/
├── backend/
│   ├── app/
│   │   ├── main.py        # API, import, extraction et stockage local
│   │   ├── retrieval.py   # recherche lexicale pondérée
│   │   ├── analysis.py    # qualification prudente et abstention
│   │   └── schemas.py     # contrats de données Pydantic
│   └── tests/             # tests unitaires
├── frontend/
│   ├── app/               # application Next.js
│   └── components/        # interface ClauseWise AI
├── sample-data/           # contrat synthétique de démonstration
├── SOURCES.md             # sources publiques et protocole de test
└── docker-compose.yml
```

### Stack

- **Frontend :** Next.js, React, TypeScript, Tailwind CSS.
- **Backend :** Python, FastAPI, Pydantic.
- **Documents :** PyMuPDF pour l’extraction du texte des PDF.
- **Recherche :** scoring lexical local de type BM25, sans dépendance à un LLM.
- **Qualité :** Pytest.
- **Exécution :** Docker Compose ou lancement local.

### Parcours de traitement

1. L’utilisateur sélectionne un contrat et décrit le sinistre.
2. Le backend recherche les passages qui partagent le plus de termes avec la question.
3. Les passages sont classés selon leur rôle lexical apparent : garantie/support, limitation ou contexte.
4. Des règles conservatrices produisent une qualification provisoire ou une abstention.
5. L’interface présente la conclusion, les raisons, les extraits et les numéros de page.

La qualification des rôles et le verdict sont actuellement heuristiques. Ils ne constituent pas une interprétation juridique automatisée.

## Lancer le projet en local

Prérequis : Python 3.11 ou supérieur, Node.js 20 ou supérieur.

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell : .venv\\Scripts\\Activate.ps1
# macOS / Linux : source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Documentation API : http://localhost:8000/docs

### 2. Frontend

Dans un second terminal :

```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://localhost:3000. Par défaut, l’interface appelle l’API sur `http://localhost:8000`. Pour une autre adresse, définir `NEXT_PUBLIC_API_URL`.

### 3. Docker Compose

Depuis la racine du dépôt :

```bash
docker compose up --build
```

Frontend : http://localhost:3000 — API : http://localhost:8000.

## Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

Les tests actuels vérifient la récupération lexicale, l’abstention sur un cas de vol dans un local commun non verrouillé et l’abstention lorsqu’aucune clause pertinente n’est retrouvée. Ils ne remplacent pas une évaluation métier sur un corpus représentatif.

## Limites connues et sécurité

- Les PDF scannés nécessitent un OCR, non inclus dans cette version.
- La segmentation des clauses est heuristique et peut fusionner ou couper incorrectement certains paragraphes.
- La recherche lexicale peut manquer des synonymes, des renvois entre articles et des conditions exprimées indirectement.
- Le moteur ne vérifie pas encore systématiquement les conditions particulières, annexes, définitions, plafonds, franchises et avenants.
- Les résultats sont des aides au repérage, pas des avis juridiques ni des décisions d’indemnisation.
- Le stockage est local et ne fournit pas de garanties de sécurité de niveau production. Ne chargez aucun document confidentiel, contrat client ou donnée personnelle dans une instance publique.

## Pistes d’évolution

1. Constituer un corpus d’évaluation versionné à partir de contrats publics, avec références exactes des pages et clauses.
2. Ajouter un parseur structuré des PDF et OCR pour les documents numérisés.
3. Combiner recherche lexicale et recherche vectorielle, puis mesurer le rappel des clauses pertinentes.
4. Ajouter une étape de reranking et une validation automatique de chaque citation contre le texte source.
5. Modéliser les liens entre garanties, exclusions, définitions, franchises et conditions particulières.
6. Isoler les contrats par espace de travail, ajouter authentification, journalisation et gestion sécurisée des fichiers.
7. Évaluer la qualité avec des métriques documentées : Recall@k, précision des citations, taux d’abstention pertinent et taux de réponses faussement affirmatives.

## À propos

**Projet :** ClauseWise AI  
**Initiatrice et porteuse du projet :** Fatima Oumouloud  
**Domaine :** Generative AI · Document AI · RAG · Explainable AI · Insurance workflows  
**Portfolio :** [fatimaoumouloud-dev.netlify.app](https://fatimaoumouloud-dev.netlify.app/)  
**Contact :** fatima.oumouloud98@gmail.com

---

*ClauseWise AI est un prototype indépendant réalisé à des fins de démonstration technique et d’évaluation de compétences. Il n’est affilié à aucun assureur. Les marques et documents cités restent la propriété de leurs éditeurs respectifs.*
