# Site actuel du Refuge des Trois Ruisseaux

Pièce de démonstration n° 3 du chapitre « Concevoir et construire les interfaces » (Uncode School, S4 Hopper). Version du 05/10/2026.

C'est le site vitrine que le refuge fait tourner depuis 2016 : celui que l'apprenant découvre dans l'existant du dossier, et que les vidéos 7, 10 et 11 auscultent. Il porte volontairement cinq défauts, et seulement ceux-là.

## Les pages

| Page | Contenu |
| --- | --- |
| `index.html` | Vidéo en lecture automatique, carrousel des douze animaux, trois nouvelles, appel aux dons, fenêtre de dons au bout de 3 secondes |
| `animaux.html` et `animaux/<nom>.html` | Les douze animaux du dossier, tous « À adopter », liste « mise à jour le 12 août 2026 » |
| `adopter.html` | Les quatre étapes d'aujourd'hui et les pièces demandées par le questionnaire papier. Le délai de 7 jours n'y figure pas |
| `aider.html`, `don.html` | Façons d'aider. `don.html` dit que la plateforme de dons n'est pas reliée |
| `contact.html` | Formulaire de contact avec la case cochée d'avance. Rien n'est envoyé |
| `mentions-legales.html` | Éditeur, directrice de la publication, hébergeur, données personnelles, mention de fiction |

## Les défauts plantés

| Défaut | Où le montrer | Vidéo |
| --- | --- | --- |
| Liens orange abricot sur fond crème (1,88:1) | Tous les liens du contenu, par exemple « Voir tous nos animaux à l'adoption » sur l'accueil | 7 |
| Bouton « Faire un don » en blanc sur abricot (2,02:1) | En-tête de chaque page, bloc d'appel de l'accueil | 7 |
| Vidéo en lecture automatique et en boucle, sans son et sans bouton pour l'arrêter, 2048 × 1080, 17,3 Mo | Haut de l'accueil | 10 |
| Photos publiées telles quelles, en pleine résolution : de 4160 à 6720 px de large, de 1,5 à 9,4 Mo (4,2 Mo en moyenne), affichées à 940 px de large au plus | Carrousel de l'accueil, catalogue, fiches | 10 |
| Carrousel de douze photos chargées d'un coup alors qu'une seule est visible | Accueil | 10 |
| Fenêtre de dons dont le refus dit « Non merci, je préfère ne pas les aider » | Accueil, 3 secondes après l'arrivée | 11 |
| Case « Je m'inscris à la lettre d'information du refuge » cochée d'avance | `contact.html` | 11 |

Poids de l'accueil : environ 68 Mo (douze photos, 50,5 Mo en tout, et la vidéo, 17,3 Mo).

Le site ne charge aucune ressource tierce : ni police distante, ni outil de mesure, ni module de dons. Ce que les outils d'audit trouvent vient donc des seuls défauts ci-dessus.

Audit axe-core du 05/10, critères WCAG 2.2 A et AA, sur les huit pages types : seules les erreurs de contraste plantées ressortent. La vidéo sans bouton d'arrêt manque aussi au critère 2.2.2 (« Mettre en pause, arrêter, masquer »), que les outils automatiques ne détectent pas : à citer en vidéo 9 si besoin.

Ce qui n'est **pas** un défaut, à dessein : les champs ont leurs étiquettes, les images leur texte de remplacement, la fenêtre de dons se ferme au clavier (Échap) et rend le focus, le carrousel ne défile pas tout seul, le formulaire informe sur l'usage des données.

## Pour les prises

- `index.html?fenetre=non` : l'accueil sans la fenêtre de dons, pour les prises des vidéos 7 et 10.
- La fenêtre revient à chaque visite : le site ne mémorise rien, aucun cookie.

## Garde-fous

- `noindex, nofollow` dans chaque page et `robots.txt` qui interdit tout. Sur le VPS, l'en-tête `X-Robots-Tag` en plus.
- Mention de fiction dans chaque pied de page et dans les mentions légales.
- Téléphone dans la plage 02 61 91 réservée à la fiction par l'Arcep. Aucune adresse e-mail.
- Le formulaire n'a pas de destination : à l'envoi, il affiche qu'aucun message n'est parti.
- Aucun paiement possible : `don.html` le dit.

## Photos et vidéo

Les douze photos viennent d'Unsplash et la vidéo de Pexels, téléchargées le 05/10/2026 dans leur fichier d'origine. Les deux licences autorisent l'usage libre, y compris commercial, sans crédit obligatoire. Les crédits figurent quand même dans les mentions légales, et la liste est dans `build.py` (`CREDITS_PHOTOS`, `CREDIT_VIDEO`).

Les originaux vivent dans `sources/`, hors du dépôt : `docs/photos/` et `docs/video/` en portent une copie. Ils ne sont ni compressés ni redimensionnés : leur poids est le défaut que la vidéo 10 corrige.

`docs/medias-optimises/` contient les versions allégées pour la maquette, que le site actuel n'utilise pas : chaque photo en WebP à 1200 et 600 px de large (de 7 à 215 Ko), et une affiche de la vidéo. Les douze photos en 600 px pèsent environ 0,25 Mo en tout, contre 50,5 Mo pour les originaux.

Pour changer un média : déposer le nouveau fichier dans `sources/photos/<nom>.jpg` ou `sources/video/refuge.mp4`, supprimer sa copie dans `docs/` et ses versions dans `docs/medias-optimises/`, mettre à jour le crédit dans `build.py`, puis relancer la construction. Sans fichier dans `sources/`, le script fabrique un média provisoire.

## Construire

```
python3 build.py                   # mentions légales pour GitHub Pages
python3 build.py --hebergeur vps   # mentions légales pour le VPS (hébergeur à compléter dans build.py)
```

Le résultat est dans `docs/`, le dossier que publie GitHub Pages. Il faut Python 3 avec Pillow, et ffmpeg pour l'affiche de la vidéo. Les médias provisoires demandent aussi NumPy.

## Mettre en ligne

### GitHub Pages (recommandé)

1. Créer un dépôt **public** `refuge-trois-ruisseaux`. Pages n'est gratuit que pour les dépôts publics.
2. Y pousser tout ce dossier, branche `main`. Le dossier `sources/` reste hors du dépôt (`.gitignore`) : `docs/` porte déjà une copie des médias.
3. Dans le dépôt : Settings → Pages → Build and deployment → Deploy from a branch → `main`, dossier `/docs`.
4. Le site répond quelques minutes plus tard à `https://<compte>.github.io/refuge-trois-ruisseaux/`. Tous les liens sont relatifs : le sous-chemin ne gêne pas.

Limites de GitHub Pages : 1 Go par site publié, 100 Go de bande passante par mois en limite souple. À 68 Mo l'accueil, cela laisse environ 1 500 chargements complets par mois.

### VPS

Le dossier `deploiement/vps/` contient un `docker-compose.yml` (nginx derrière Traefik), un `nginx.conf` et un `env.exemple`.

1. Lire les quatre points à vérifier en tête du `docker-compose.yml` (réseau, point d'entrée, résolveur, DNS).
2. Copier le dossier dans `/opt/refuge/`, placer le contenu de `docs/` dans `/opt/refuge/site/`, créer `.env` à partir de `env.exemple`.
3. Construire avec `--hebergeur vps` après avoir renseigné l'hébergeur dans `build.py`.
4. `docker compose up -d` dans `/opt/refuge/`. Retrait : `docker compose down`.

---

Cas fictif créé pour la formation Uncode School. Police Nunito sous licence SIL Open Font License 1.1 (`fonts/OFL.txt`).
