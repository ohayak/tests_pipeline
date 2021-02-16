# Tester en développement

Un fois le pipeline/composant est prêt (ou vous vous sentez prêt à l'essayer), la création d'un test de référence passe par les étapes suivantes:
1. Capturer les inputs (ou un subset utile)
2. Capturer les outputs correspondants aux inputs choisis. Ces outputs serons la référence du test.
3. Définir une procédure de comparaison des futurs outputs avec la référence.

La librairies [TDDA](https://tdda.readthedocs.io/en/tdda-1.0.13/overview.html) nous permet de créer facilement des tests de références.

## Exemple
Le dossier [demo](../demo) contient un pipeline qu'on souhaite tester. Il se résume dans le code suivant:
```python
df = load.load(input_dataset)
df = clean.clean(df)
df = filter.filter(df)
save(df, output_dataset)
```

Les tests de référence sont une extension des tests unitaires. Ils sont là pour tester notre code, donc il est recommandé de les inclure dans la batteries des tests juste avant le packaging est la livraison.

Dans la suite de ce premier hands-on on va tester le module `load`.

### Environnement de dev
On aura besoin de `pytest` et `tdda`. Il suffit de lancer la commade `make install` pour installer les dépendances,  et `source .venv/bin/activate` pour activer l'environnement virtuelle.

*Pour réinstialiser la demo: `make resetdemo`*

### Écrire le test

la fonction `load` charge un CSV est retourne le dataframe correspondant. Une fonction de test peut se présenter comme ceci:
```python
def test_load(ref):
    resultframe = load.load('tests/data/input/embauche_sample.csv')
    ref.assertDataFrameCorrect(resultframe, 'tests/data/references/embauche_loaded.csv', csv_read_fn=pd.read_csv, infer_datetime_format=False)
```
1. Dans ce test on va fournir l'input uniquement: un subset du dataset original: `tests/data/input/embauche_sample.csv`.
2. On suppose que l'output de référence se trouve dans: `tests/data/references/embauche_loaded.csv` (à cette étape la référence n'existe pas). Dans ce cas le DataFrame de référence est sauvegardé sous la forme d'un CSV.
3. pour comparer les résultats on utilise [assertDataFrameCorrect](https://tdda.readthedocs.io/en/tdda-1.0.13/referencetest.html?highlight=assertDataFrameCorrect#tdda.referencetest.referencetest.ReferenceTest.assertDataFrameCorrect) fournie par TDDA. (la méthode est accessible à travers la fixture pytest `ref`) cette méthode compare un `Pandas.DataFrame` à un deuxième DataFrame de référence.

### Exécuter le test

La commande pytest pour executer ce test est:
```bash
pytest tests/test_component.py::test_load
```
la commande échoue avec l'erreur suivante:
```
E   FileNotFoundError: [Errno 2] File b'tests/data/references/embauche_loaded.csv' does not exist: b'tests/data/references/embauche_loaded.csv'
```

### Générer la référence
Pour corriger l'erreur on doit créer le fichier `tests/data/references/embauche_loaded.csv`. C'est possible de le faire manuellement, mais `tdda` est capable de le faire pour nous:
```bash
pytest --write-all tests/test_component.py::test_load
```
Ce fichier servira comme référence à toutes les exécutions de ce test dans le future. Donc si vous utilisez des nombres aléatoires pensez au `seed`.

Plus généralement, `tdda` gère des références aux formats: CSV, text, string, Pandas DataFrame.

À cette étape, la commande `pytest tests/test_component.py::test_load` doit s'exécuter sans erreurs.

*Si le code reste inchangé, comment ce test peut échouer ?*
- modification des inputs
-	Une MaJ python, système, package
-	L’utilisation des nombres aléatoires
-	Quelqu’un peut effectuer des changements sur le code source sans prévenir

### Exécuter tous les tests

Les fichier de `test_component.py` et `test_pipeline.py` contient plusieurs tests de références. Pour générer toutes les références:
```bash
pytest -s --write-all
```
Il y a des dépendances entre les tests: par exemple le test de `clean` utilise la référence de `load` comme input, afin d'éviter de faire appel à la fonction load dans le test de clean.
Cette pratique permet d'isoler le code qu'on souhaite tester, c'est l'intérêt principale des tests de composants. Par contre, le `test_pipeline` permet de tester le pipeline dans sa globalité sur un échantillon de données, sans se préoccuper des inputs/outputs de chaque composant.
