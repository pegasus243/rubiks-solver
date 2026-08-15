# Solveur de Rubik's Cube 🧩

Un solveur de Rubik's Cube en **deux versions** :

- 🌐 **Version web** — une page interactive : on peint les 6 faces, on clique « Résoudre ».
- 💻 **Version terminal** — un script Python en ligne de commande.

Les deux utilisent l'**algorithme en deux phases de Herbert Kociemba** (résolution en une vingtaine de mouvements maximum).

---

## 🌐 Version web (`index.html`)

Ouvre simplement `index.html` dans un navigateur, ou héberge le dossier
(par exemple avec **GitHub Pages**).

**Utilisation :**
1. Choisis une couleur dans la palette.
2. Peins les cases du patron pour reproduire ton cube (clic ou glisser). Les centres sont fixes.
3. Clique **Résoudre**. La séquence s'affiche, avec l'explication de chaque mouvement en français.

Boutons pratiques :
- **Mélanger** — charge un mélange aléatoire (utile pour tester).
- **Réinitialiser** — remet le cube à l'état résolu.

La résolution se fait **entièrement dans le navigateur** — aucune donnée n'est envoyée.
Avant de résoudre, la page **vérifie que le cube est physiquement possible**
(comptage des couleurs + parités des coins et des arêtes) et signale toute erreur de saisie.

### Correspondance couleurs / faces

| Couleur | Face | Lettre |
|--------|-----------|:---:|
| blanc  | Haut      | U |
| rouge  | Droite    | R |
| vert   | Avant     | F |
| jaune  | Bas       | D |
| orange | Gauche    | L |
| bleu   | Derrière  | B |

---

## 💻 Version terminal (`main.py`)

```bash
pip install -r requirements.txt        # installe kociemba
python3 main.py                        # mode interactif
python3 main.py <54-caractères>        # mode direct (non interactif)
```

En mode interactif, on saisit 9 lettres par face avec le schéma
`b`=blanc, `r`=rouge, `v`=vert, `j`=jaune, `o`=orange, `x`=bleu,
dans l'ordre : Haut, Droite, Avant, Bas, Gauche, Derrière.

En mode direct, l'argument est soit 54 lettres de couleur (`b r v j o x`),
soit 54 lettres kociemba (`U R F D L B`) ; les espaces sont ignorés. Exemple :

```bash
python3 main.py "bbbbbbbbbrrrrrrrrrvvvvvvvvvjjjjjjjjjooooooooo xxxxxxxxx"
```

La saisie est validée (chaque couleur doit apparaître exactement 9 fois) et
un cube déjà résolu est détecté et signalé.

---

## Crédits

- Version terminal : bibliothèque Python [`kociemba`](https://github.com/muodov/kociemba) (GPL).
- Version web : bibliothèque JavaScript [`cubejs`](https://github.com/ldez/cubejs) (MIT) — fichiers `cube.js` et `solve.js`, inclus tels quels.
