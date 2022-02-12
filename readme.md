# Not Wordle
Ce projet python a pour but de recréer (plus ou moins) le jeu [wordle](https://www.nytimes.com/games/wordle/index.html).

Le but est de deviner le mot mystère en un nombre d'essai limité  
Pour vous aider il y a plusieurs indicateurs: 
- Cases rouges: elles vous indiquent que la lettre n'est pas dans le mot
- Cases jaunes: la lettre est dans le mot mais pas au bon endroit
- Cases vertes: La lettre est bien placée
  
Ce jeu utilise un fichier de plus de 15 000 mots ['français'](#Problèmes)

---
## Détails techniques
Pour fonctionner le jeu a besoin de ces modules python:
- pygame (version 2.1.2)
- pygame_gui (version 0.6.4)

La version de python conseillée est la 3.8.5  

---
## Problèmes
Malgré les multiples triages, il reste beaucoup de mots peu connus ou même des mots anglais dans la liste.
