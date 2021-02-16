# Tester en production

Le concept des contraintes est de mettre en place des vérifications de données rapides qui devraient être vrais à différents points, en particulier les jeux de données en entrée et en sortie, et potentiellement à n’importe quel ensemble de données intermédiaires. Et ces contraintes peuvent être presque n'importe quoi.
Ils peuvent s'appliquer à des champs individuels:
- L’âge doit être compris entre 0 et 150 ans
- L'âge devrait être un entier
- CustomerID ne doit pas être NULL
- Le numéro de carte de crédit doit comporter 16 chiffres.

et ils peuvent s'appliquer à des ensembles de données entiers:
- Le jeu de données doit contenir un champ CID
- Le jeu de données doit contenir exactement 118 enregistrements.
- StartDate ≤ EndDate

## Exemple
Il faut rappeler que les tests qu'on a fait dans la première parties s'exécutent uniquement au moment du packaging.
Sur l'exemple de la démo on a rajouté des tests de contraintes. Cette fois les tests de contraintes s'exécutent avec le code de l'application.
Étant en prod les inputs changes d'une exécution à l'autre, il est inutile de mettre des tests de références. Par contre,  les tests de contraintes permettrons de tester dynamiquement les données.

### Générer les contraintes
#### CLI
TDDA est capable de générer les contraintes à partir de plusieurs sources de données:
- CSV
- feather
- PostgreSQL
- MySQL
- SQLite
- MongoDB

Il est également possible d'utiliser l'API TDDA pour développer une extension personnalisée.

On utilisera les CSV de référence qu'on a généré précédemment en ligne de commande:
```bash
tdda discover tests/data/input/embauche_sample.csv data/constraints/embauche_sample.tdda
```
Cette commande génère le fichier `embauche_sample.tdda` au format json résumant les contraintes par champs.
Il est nécessaire de relire ces contraintes et les adapter.
Prenons l'exemple du champs age:
```json
"age": {
    "type": "real",
    "min": 13.0,
    "max": 58.0,
    "sign": "positive",
    "max_nulls": 0
}
```
Les valeurs min et max sont vrais pour l'échantillon de données, il est possible de trouver des bornes plus étendues sur l'input `embauche.csv` original.

Sans modifier le fichier de contraintes lancez la commande suivante:

```bash
tdda verify data/input/embauche.csv data/constraints/embauche_sample.tdda
```

Cette commande va passer toutes les valeurs dans `embauche.csv` au crible des contraintes et génère le rapport suivant:

```
FIELDS:
Unnamed: 0: 3 failures  3 passes  type ✓  min ✗  max ✗  sign ✗  max_nulls ✓  no_duplicates ✓
index: 3 failures  3 passes  type ✓  min ✗  max ✗  sign ✗  max_nulls ✓  no_duplicates ✓
date: 1 failure  2 passes  type ✓  min_length ✗  max_length ✓
cheveux: 0 failures  4 passes  type ✓  min_length ✓  max_length ✓  allowed_values ✓
age: 4 failures  1 pass  type ✓  min ✗  max ✗  sign ✗  max_nulls ✗
exp: 4 failures  1 pass  type ✓  min ✗  max ✗  sign ✗  max_nulls ✗
salaire: 3 failures  2 passes  type ✓  min ✗  max ✗  sign ✓  max_nulls ✗
sexe: 1 failure  4 passes  type ✓  min_length ✓  max_length ✓  max_nulls ✗  allowed_values ✓
diplome: 0 failures  4 passes  type ✓  min_length ✓  max_length ✓  allowed_values ✓
specialite: 1 failure  4 passes  type ✓  min_length ✓  max_length ✓  max_nulls ✗  allowed_values ✓
note: 2 failures  2 passes  type ✓  min ✗  max ✗  sign ✓
dispo: 0 failures  4 passes  type ✓  min_length ✓  max_length ✓  allowed_values ✓
embauche: 0 failures  5 passes  type ✓  min ✓  max ✓  sign ✓  max_nulls ✓
SUMMARY:
Constraints passing: 39
Constraints failing: 22
```

Sur la ligne age, seule la contrainte de type est respecté. Et c'est normal, car `embauche.csv` contient plus de données donc des bornes age plus étendues.

Si vous voulez creuser plus, il y a la commande `tdda detect` qui permet d'extraire les lignes qui ne respectent pas les contraintes dans fichier CSV

```bash
tdda detect data/input/embauche.csv data/constraints/embauche_sample.tdda out.csv
```

Si on modifie les contraintes:
```json
"age": {
    "type": "real",
    "min": -10.0,
    "max": 99.0
}
```
- Élargir les bornes de -10 à 99 (petit piège: il y a des valeurs négatives dans age)
- supprimer la condition `max_nulls` car on sait pas exactement la proportion des valeurs nulls
- supprimer la condition `signe` car les nulls n'ont pas de signe.

C'est contraintes résument le travail de nettoyage à faire, on peut rajouter ces contraintes pour tester la sortie de cette étape.

Le résultat du verify devient:
```
age: 0 failures  3 passes  type ✓  min ✓  max ✓
```
Pour aller plus loin: [Génération des contraintes dans TDDA](http://www.tdda.info/constraint-generation-in-the-presence-of-bad-data)

#### API
Les tests de contraintes sont plus souples et dynamiques, on peut facilement les intégrer dans le code de la pipeline pour contrôler la qualité des entrées/sorties à chaque exécution et bien plus.

##### Cas d'usage 1: un livrable du projet

Un fichier de contraintes concrétise un contrat entre le développeur et sa source de données.
Souvent on est amené à developper des pipelines qui traitent des données biaisées (dumps, extracts, mocks ...), pour des raisons de sécurité ou de disponibilité de données, on peut même passer en prod sans jamais pouvoir manipuler les données "réels". Dans la plus part des cas le basculement sur les données réels est accompagné par une charge de débug, car les nouvelles entrées cachent des surprises non anticipées durant le dev.
Il est judicieux dans ces cas de livrer un projet avec un contrat sur les données acceptées, ainsi c'est une protection pour le développeur si le data provider change le format d'une entrée.

##### Cas d'usage 2: programmation defensive

On peut utiliser les contraintes comme un filtre pour isoler les données de mauvaise qualité, surtout en production:
- éviter l'interruption de la pipeline.
- logger les entrées erronées.
- activer un traitement de correction.

C'est une pratique du [Defensive Programing](https://en.wikipedia.org/wiki/Defensive_programming) qui couvre les contrôles de sécurité et autres mesures de précaution visant à atténuer les problèmes pouvant résulter de situations inattendues.

Plus généralement, les contraintes s'intègrent facilement dans les pipelines de [QA/QC](https://www.usgs.gov/products/data-and-tools/data-management/manage-quality)

### Exécuter la pipeline avec les contraintes TDDA

Pour intégrer les fonctionnalité qu'on a vu ci-dessus, on doit passer par l'[API tdda](https://tdda.readthedocs.io/en/tdda-1.0.22/constraints.html#module-tdda.constraints.baseconstraints)

L'exemple de l'intégration des contrainte en prod ressemble au code dans `run_with_detect.py`
```python
df = load.load(DataPaths.input_dataset)
my_detect_df(df, 'data/constraints/embauche_loaded.tdda', outpath='data/output/embauche_loaded_fails.csv', per_constraint=True)
df = clean.clean(df)
my_detect_df(df, 'data/constraints/embauche_cleaned.tdda', outpath='data/output/embauche_cleaned_fails.csv', per_constraint=True)
df = filter.filter(df)
my_detect_df(df, 'data/constraints/embauche_filtered.tdda', outpath='data/output/embauche_filtered_fails.csv', per_constraint=True)
save(df, DataPaths.output_dataset)
```
On fait appel à la fonction `detect_df` après chaque étape de traitement du pipeline, et selon les résultats du test on peut choisir d'interrompre le flux et lever une exception, ou bien logger l'erreur et lancer une procédure de correction.
Le code ci-dessus sauvegarde les mauvaises données dans des CSV `..._fails.csv`.

Lancer la commande `make tddadiscover` pour créer les fichiers de contraintes nécessaire. Ensuite à l'aide des commandes `make run_verify` ou `make run_detect` vous pouvez lancer la pipeline.
À cette étape les l'exécution échoue car les contraintes sont trop fortes. Essayez de modifier les fichiers `.tdda` pour faire passer les tests.
