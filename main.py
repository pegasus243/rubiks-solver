#!/usr/bin/env python3
"""
Solveur de Rubik's Cube - Version Terminal
Algorithme : Kociemba (résolution en ~20 mouvements max)
"""

import sys

import kociemba

# --- Correspondance couleur (initiale française) -> lettre kociemba ---
COULEURS = {
    'b': 'U',  # blanc  -> Haut     (Up)
    'r': 'R',  # rouge  -> Droite   (Right)
    'v': 'F',  # vert   -> Avant    (Front)
    'j': 'D',  # jaune  -> Bas      (Down)
    'o': 'L',  # orange -> Gauche   (Left)
    'x': 'B',  # bleu   -> Derrière (Back)  [x pour éviter confusion avec b=blanc]
}

# Informations sur chaque face : (nom, couleur du centre, lettre kociemba)
FACES = [
    ('Haut',      'blanc',   'U'),
    ('Droite',    'rouge',   'R'),
    ('Avant',     'vert',    'F'),
    ('Bas',       'jaune',   'D'),
    ('Gauche',    'orange',  'L'),
    ('Derrière',  'bleu',    'B'),
]

# Chaîne kociemba d'un cube déjà résolu (UUUUUUUUURRRRRRRRR...).
# Sert à détecter ce cas : kociemba renvoie une séquence inutile pour un
# cube résolu, on court-circuite donc pour afficher « déjà résolu ».
CUBE_RESOLU = "".join(lettre * 9 for _, _, lettre in FACES)

# Codes ANSI pour les couleurs de fond (fond coloré + texte noir)
ANSI = {
    'U': '\033[47m\033[30m',       # blanc
    'R': '\033[41m\033[30m',       # rouge
    'F': '\033[42m\033[30m',       # vert
    'D': '\033[43m\033[30m',       # jaune
    'L': '\033[48;5;208m\033[30m', # orange (256 couleurs)
    'B': '\033[44m\033[37m',       # bleu (texte blanc pour lisibilité)
}
RESET = '\033[0m'

# Explication des mouvements
EXPLICATION = {
    'U':  "Tourne la face du Haut dans le sens horaire",
    "U'": "Tourne la face du Haut dans le sens anti-horaire",
    'U2': "Tourne la face du Haut de 180°",
    'D':  "Tourne la face du Bas dans le sens horaire",
    "D'": "Tourne la face du Bas dans le sens anti-horaire",
    'D2': "Tourne la face du Bas de 180°",
    'R':  "Tourne la face Droite dans le sens horaire",
    "R'": "Tourne la face Droite dans le sens anti-horaire",
    'R2': "Tourne la face Droite de 180°",
    'L':  "Tourne la face Gauche dans le sens horaire",
    "L'": "Tourne la face Gauche dans le sens anti-horaire",
    'L2': "Tourne la face Gauche de 180°",
    'F':  "Tourne la face Avant dans le sens horaire",
    "F'": "Tourne la face Avant dans le sens anti-horaire",
    'F2': "Tourne la face Avant de 180°",
    'B':  "Tourne la face Derrière dans le sens horaire",
    "B'": "Tourne la face Derrière dans le sens anti-horaire",
    'B2': "Tourne la face Derrière de 180°",
}


# ─────────────────────────────────────────────────────────────
#  Affichage du cube en 2D (croix en couleurs ANSI)
# ─────────────────────────────────────────────────────────────

def cellule(c):
    """Retourne une case colorée de 3 caractères visibles."""
    return f"{ANSI[c]} {c} {RESET}"

def ligne_face(face, row):
    """Retourne une ligne d'une face (3 cases côte à côte)."""
    return cellule(face[row * 3]) + cellule(face[row * 3 + 1]) + cellule(face[row * 3 + 2])

def afficher_cube(cube_string):
    """
    Affiche le cube en vue 2D "croix" :

               [Haut]
    [Gauche] [Avant] [Droite] [Derrière]
               [Bas]
    """
    U = cube_string[0:9]
    R = cube_string[9:18]
    F = cube_string[18:27]
    D = cube_string[27:36]
    L = cube_string[36:45]
    B = cube_string[45:54]

    # Largeur d'une face = 3 cases * 3 chars visibles = 9 chars
    # + codes ANSI invisibles
    # L'indentation pour U et D doit aligner avec F :
    # largeur(L) + séparateur = 9 + 1 = 10 chars visibles
    vide  = "          "  # 10 espaces (aligne avec F)
    sep   = " "

    print()
    print("  ┌─ Vue du cube ──────────────────────────────────────────┐")

    # Face Haut
    for row in range(3):
        print("  │  " + vide + ligne_face(U, row) + RESET)

    print("  │")

    # Faces Gauche / Avant / Droite / Derrière
    for row in range(3):
        print("  │  " +
              ligne_face(L, row) + sep +
              ligne_face(F, row) + sep +
              ligne_face(R, row) + sep +
              ligne_face(B, row) + RESET)

    print("  │")

    # Face Bas
    for row in range(3):
        print("  │  " + vide + ligne_face(D, row) + RESET)

    print("  │")
    print("  │  Légende : b=blanc  r=rouge  v=vert  j=jaune  o=orange  x=bleu")
    print("  └────────────────────────────────────────────────────────┘")
    print()


# ─────────────────────────────────────────────────────────────
#  Saisie
# ─────────────────────────────────────────────────────────────

def afficher_intro():
    print()
    print("╔══════════════════════════════════════════╗")
    print("║      SOLVEUR DE RUBIK'S CUBE             ║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Couleurs à utiliser pour la saisie :")
    print("  b = blanc   (centre de la face Haut)")
    print("  r = rouge   (centre de la face Droite)")
    print("  v = vert    (centre de la face Avant)")
    print("  j = jaune   (centre de la face Bas)")
    print("  o = orange  (centre de la face Gauche)")
    print("  x = bleu    (centre de la face Derrière)")
    print()
    print("Pour chaque face, entre 9 lettres dans cet ordre :")
    print()
    print("  [1][2][3]  ← ligne haute")
    print("  [4][5][6]  ← ligne milieu  (5 = case centrale, fixe)")
    print("  [7][8][9]  ← ligne basse")
    print()
    print("Orientation standard :")
    print("  Face Avant = face que tu regardes")
    print("  Face Haut  = au-dessus")
    print()


def saisir_face(nom, couleur_centre, lettre_kociemba):
    print(f"─── Face {nom} (centre = {couleur_centre}) ───")

    while True:
        entree = input(f"  9 couleurs : ").strip().lower()

        if len(entree) != 9:
            print(f"  ✗ Il faut exactement 9 caractères (tu en as entré {len(entree)})\n")
            continue

        valide = True
        face_kociemba = ""
        for i, c in enumerate(entree):
            if c not in COULEURS:
                print(f"  ✗ Caractère '{c}' invalide en position {i + 1}. "
                      f"Utilise : b r v j o x\n")
                valide = False
                break
            face_kociemba += COULEURS[c]

        if not valide:
            continue

        if face_kociemba[4] != lettre_kociemba:
            print(f"  ✗ Le centre (position 5) doit être {couleur_centre}.\n")
            continue

        print(f"  ✓ Face {nom} enregistrée\n")
        return face_kociemba


# ─────────────────────────────────────────────────────────────
#  Affichage de la solution
# ─────────────────────────────────────────────────────────────

def afficher_solution(solution):
    mouvements = solution.strip().split()
    nb = len(mouvements)

    print()
    print("╔══════════════════════════════════════════╗")
    print(f"║  SOLUTION : {nb} mouvements{' ' * (27 - len(str(nb)))}║")
    print("╚══════════════════════════════════════════╝")
    print()
    print("Séquence complète :")
    print("  " + "  ".join(mouvements))
    print()
    print("Détail pas à pas :")
    for i, m in enumerate(mouvements, 1):
        explication = EXPLICATION.get(m, m)
        print(f"  {i:2}. {m:<3}  →  {explication}")
    print()


# ─────────────────────────────────────────────────────────────
#  Validation & résolution
# ─────────────────────────────────────────────────────────────

def valider_cube(cube_string):
    """Vérifie que la chaîne représente un cube plausible.

    Contrôle la longueur (54) et le fait que chaque couleur apparaisse
    exactement 9 fois. Retourne (True, "") si OK, sinon (False, message).
    """
    if len(cube_string) != 54:
        return False, f"le cube doit contenir 54 cases (il en a {len(cube_string)})."
    for nom, couleur, lettre in FACES:
        n = cube_string.count(lettre)
        if n != 9:
            return False, (f"la couleur {couleur} apparaît {n} fois au lieu de 9 "
                           f"(vérifie ta saisie).")
    return True, ""


def cube_depuis_argument(arg):
    """Convertit un argument ligne de commande en chaîne kociemba.

    Accepte soit les lettres couleurs (b r v j o x), soit directement les
    lettres kociemba (U R F D L B). Les espaces sont ignorés.
    Retourne (chaine_kociemba, "") ou (None, message d'erreur).
    """
    arg = "".join(arg.split())
    if len(arg) != 54:
        return None, f"l'argument doit contenir 54 caractères (il en a {len(arg)})."

    bas = arg.lower()
    if all(c in COULEURS for c in bas):
        return "".join(COULEURS[c] for c in bas), ""

    haut = arg.upper()
    if all(c in "URFDLB" for c in haut):
        return haut, ""

    return None, "caractères non reconnus. Utilise b r v j o x (ou U R F D L B)."


def resoudre(cube_string, montrer_cube=True):
    """Valide, détecte le cube résolu, puis résout et affiche la solution."""
    ok, msg = valider_cube(cube_string)
    if not ok:
        print(f"\n✗ Cube invalide : {msg}")
        return

    if montrer_cube:
        print("\nVoici le cube :")
        afficher_cube(cube_string)

    if cube_string == CUBE_RESOLU:
        print("✓ Le cube est déjà résolu — aucun mouvement nécessaire !\n")
        return

    print("Résolution en cours...")
    try:
        solution = kociemba.solve(cube_string)
    except Exception as e:
        print()
        print("✗ Erreur : l'état du cube n'est pas valide (mélange impossible).")
        print("  Vérifie que tu as bien entré chaque face depuis la bonne orientation.")
        print(f"  Détail technique : {e}")
        return

    afficher_solution(solution)


# ─────────────────────────────────────────────────────────────
#  Programme principal
# ─────────────────────────────────────────────────────────────

def saisir_cube_interactif():
    """Saisie des 6 faces avec relecture et possibilité de recommencer."""
    while True:
        cube_string = ""
        for nom, couleur, lettre in FACES:
            cube_string += saisir_face(nom, couleur, lettre)

        print("\nVoici le cube que tu as entré :")
        afficher_cube(cube_string)

        rep = input("  Est-ce correct ? (o/n) ").strip().lower()
        if rep in ("", "o", "oui", "y", "yes"):
            return cube_string
        print("\nOn recommence la saisie.\n")


def main():
    # Mode non-interactif : chaîne du cube passée en argument
    #   python3 main.py brvjox...   (54 lettres couleurs ou U R F D L B)
    if len(sys.argv) > 1:
        cube_string, msg = cube_depuis_argument(sys.argv[1])
        if cube_string is None:
            print(f"✗ {msg}")
            sys.exit(1)
        resoudre(cube_string)
        return

    afficher_intro()
    try:
        cube_string = saisir_cube_interactif()
    except EOFError:
        print("\nSaisie interrompue.")
        return
    except KeyboardInterrupt:
        print("\nAbandon.")
        return

    # Le cube a déjà été affiché lors de la relecture.
    resoudre(cube_string, montrer_cube=False)


if __name__ == "__main__":
    main()
