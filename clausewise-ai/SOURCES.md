# Sources publiques & protocole d’évaluation

Ce fichier référence des documents publics à utiliser pour tester ClauseWise AI. Les documents contractuels sont hébergés par leurs éditeurs ; ce dépôt conserve les liens et non des copies des PDF.

## Corpus de départ

| Source | Nature | Utilisation prévue | Précaution |
|---|---|---|---|
| [MACIF — Conditions générales Macif Habitation, 06/2025](https://www.macif.fr/files/live/sites/maciffr/files/conditions_generales_habitation/CG-Macif-Habitation.pdf) | Conditions générales d’un assureur | Tester garanties vol, exclusions, mesures de prévention et conditions | Vérifier la version et la formule avant chaque test |
| [Direct Assurance — garantie vol et PDF des conditions générales](https://www.direct-assurance.fr/assurance-habitation/sinistre-garanties-habitation/la-garantie-vol-de-votre-assurance-habitation) | Page éditeur donnant accès à ses informations contractuelles | Tester les exigences de protection et les conséquences de leur non-respect | Importer le PDF contractuel exact ; la page web seule n’est pas le contrat |
| [Caisse d’Épargne — documents assurance habitation](https://www.caisse-epargne.fr/assurer/assurance-habitation/) | Page éditeur référençant les documents contractuels | Ajouter un troisième contrat après sélection de la formule adaptée | Conserver le nom, la date et la formule du document téléchargé |
| [Service-Public.fr — assurance habitation et vol](https://www.service-public.gouv.fr/particuliers/vosdroits/F2028) | Information publique institutionnelle | Contexte général pour préparer les questions | Ne pas traiter cette page comme une clause contractuelle ni comme une preuve de couverture |

## Protocole conseillé

Pour chaque contrat importé, consigner :

- l’assureur et le nom exact du produit ;
- la formule concernée (si le document en distingue plusieurs) ;
- le titre et la date/version du document ;
- l’URL officielle d’origine et la date de consultation ;
- les pages des garanties, exclusions, définitions, franchises et conditions de prévention.

Ne pas comparer deux contrats sans vérifier que les garanties et les formules sont comparables. Les conditions particulières, les avenants et la situation individuelle de l’assuré peuvent modifier l’analyse.

## Scénarios métier à tester

1. **Vélo volé dans le local commun non verrouillé.** Vérifier si les biens situés dans les locaux communs sont garantis, si le vélo est un bien assuré, si le local est une dépendance ou une partie commune, et si une exclusion spécifique s’applique.
2. **Bougie laissée sur une table de jardin pendant les vacances, endommagée par la chaleur.** Identifier la garantie susceptible de s’appliquer, la définition des biens extérieurs, les exclusions liées à la chaleur, à l’absence ou à la négligence, ainsi que les conditions particulières.
3. **Vol dans le logement après effraction.** Vérifier la garantie vol, la définition de l’effraction, les conditions de preuve, les mesures de prévention et les éventuelles franchises.

## Format de fiche d’évaluation

Pour chaque couple (contrat, question), créer une fiche manuelle contenant :

- `contract_id` et version du contrat ;
- question utilisateur et faits connus ;
- clauses attendues et pages exactes ;
- clauses contraires ou conditions à vérifier ;
- verdict métier de référence : `potentiellement couvert`, `non établi` ou `à examiner` ;
- justification du verdict et informations manquantes ;
- résultat du système et statut de validation humaine.

Ne publier aucun score de performance avant d’avoir constitué un jeu d’évaluation suffisamment documenté et vérifié manuellement.
