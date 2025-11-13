# Comment Contribuer à V-Lille-Dash

Merci pour votre intérêt à contribuer au projet V-Lille-Dash ! Votre aide est précieuse.

Que ce soit pour signaler un bug, proposer une amélioration ou écrire du code, nous apprécions votre participation. Pour garantir un processus fluide, veuillez suivre ces quelques directives.

## Signaler un Bug ou Suggérer une Fonctionnalité

La meilleure façon de commencer est d'ouvrir une [**Issue**](https://github.com/Mart1Portfolio/V-Lille-Dash/issues) (un "ticket") sur le dépôt.

* **Pour un bug :** Décrivez le problème le plus précisément possible. Incluez les étapes pour le reproduire, ce que vous attendiez, et ce que vous avez obtenu à la place.
* **Pour une fonctionnalité :** Expliquez votre idée en détail. Pourquoi serait-elle utile pour le projet ?

Cela permet à tout le monde de discuter de l'idée avant que du temps ne soit investi en développement.

## Proposer une Modification (Le "GitHub Flow")

Nous utilisons un flux de travail standard basé sur les *Pull Requests*. Si vous n'êtes pas familier avec ce processus, ne vous inquiétez pas, c'est très simple !

### 1. Créer une Branche (Branch)

N'apportez jamais de modifications directement à la branche `main`.

Commencez par créer une **nouvelle branche** dédiée à vos modifications. Donnez-lui un nom descriptif, par exemple :
`feature/carte-interactive` ou `fix/bug-affichage-velos`.

```bash
# Assurez-vous d'être sur la branche 'main' et à jour
git checkout main
git pull origin main

# Créez votre nouvelle branche
git checkout -b nom-de-votre-branche
```

De cette façon, vos changements, fonctionnalités ou correctifs n'affectent pas la branche principale de travail.

### 2. Faire les Modifications (Commit)

Ensuite, faites vos mises à jour dans la branche que vous venez de créer.

Travaillez sur votre code, votre documentation ou votre correctif. Faites des *commits* atomiques et clairs (un commit par petite étape logique).

```bash
# Ajoutez vos fichiers modifiés
git add .

# Validez vos changements avec un message clair
git commit -m "Ajoute la fonctionnalité X"
```

Si votre flux de travail le supporte, vous pouvez déployer les changements depuis cette branche pour les tester avant de les fusionner.

### 3. Ouvrir une Pull Request (PR)

Une fois vos modifications terminées et testées, poussez votre branche sur GitHub :

```bash
git push -u origin nom-de-votre-branche
```

Maintenant, ouvrez une **Pull Request** (PR) pour inviter à la discussion et commencer la revue de votre code.

Rendez-vous sur la page de votre dépôt GitHub. Vous devriez voir une bannière vous proposant de créer une PR à partir de votre nouvelle branche.

Dans votre PR :
* Donnez-lui un titre clair.
* Rédigez une brève description des changements.
* Si votre PR corrige une *Issue* existante, liez-la en écrivant `Closes #123` (remplacez `123` par le numéro de l'Issue).

### 4. Revue et Fusion

Un mainteneur du projet examinera votre code. Il est possible que l'on vous demande d'apporter des modifications avant que la PR ne soit acceptée.

Une fois approuvée, votre contribution sera fusionnée (merged) dans la branche `main` et fera officiellement partie du projet.

Merci encore pour votre contribution !