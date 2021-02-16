# Préparer son code
Avant de se lancer sur des tests il faut s'assurer que le projet est assez flexible pour intégrer un mécanisme de test, en termes d'architecture et séparation de code. Sinon, l'effort de mettre en place des tests devient trop important, voir contre productif.

Il est donc essentiel de partir sur des bases solides. Dans cette partie un rappel sur le principe des fonctions pures.

Une fonction pure est une fonction dont la sortie dépend uniquement de ses paramètres en entrées, et n’a pas d’effets de bord en dehors de la fonction elle-même. C-à-d que la fonction pure ne fait pas appel à des configurations, ne va pas chercher des valeurs dans des services, n’utilise pas de variable globales, etc…

- `len(s)` est pure
- `random()` n’est pas pure, car elle ne dépend pas des paramètres en entrée.

La fonction pure ne résout généralement qu’un problème à la fois. Répondant à une seule problématique, la fonction est généralement de taille réduite. En pratique, ce fait se traduit par une fonction ne dépendant que de ses entrées, écrire un test unitaire dessus est simple.

Les fonctions pures sont la base du Test Driven Développement. Elles sont "étanches", et peuvent se traiter de manière isolée du reste du programme, sans risque d’effet de bord. On peut les déplacer et les refactorer simplement.

Pensez aussi à bien choisir les paramètres en entrée de la fonction. Les paramètres doivent correspondre à ce sur quoi la fonction va travailler.

Prenons un exemple d’une fonction dont le but est de formater la date d’un article pour l’affichage :

- `formatDate(article)` => bad ! inutile de passer tout l’article
- `formatDate(date)` => better ! notre fonction est universelle et facilement testable
