#!/usr/bin/env python3
"""Construit le « site actuel » du Refuge des Trois Ruisseaux dans docs/.

Le dossier docs/ est celui que GitHub Pages publie (branche main, dossier /docs).

Cas fictif de la formation Uncode School (chapitre « Concevoir et construire
les interfaces »). Le site porte volontairement les défauts listés dans
LISEZMOI.md. Ne pas les corriger : les vidéos 7, 10 et 11 s'en servent.

Usage :
    python3 build.py                      # hébergement GitHub Pages
    python3 build.py --hebergeur vps      # hébergement sur un VPS

Photos et vidéo :
    sources/photos/<slug>.jpg   photo réelle, publiée telle quelle (c'est le défaut)
    sources/video/refuge.mp4    vidéo réelle
    Sans fichier source, le script fabrique une image ou une vidéo provisoire
    du même poids qu'une photo de téléphone (environ 5 Mo).
"""

import html
import shutil
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
DIST = ICI / "docs"
ASSETS = ICI / "assets"
SOURCES = ICI / "sources"

HEBERGEURS = {
    "github": "GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.",
    "vps": "[Nom, adresse et téléphone de l'hébergeur du VPS, à compléter avant la mise en ligne.]",
}

TELEPHONE = "02 61 91 47 30"  # plage réservée à la fiction par l'Arcep
MISE_A_JOUR = "12 août 2026"

# Les douze animaux du dossier de démonstration (§8.1).
# Le site n'est plus à jour : il montre tout le monde « à adopter »,
# y compris Ficelle (adoptée le 26/09), Nala et Caramel (réservés) et Tigrou (en soins).
ANIMAUX = [
    {"slug": "pistache", "nom": "Pistache", "espece": "Chatte", "age": "2 ans", "taille": "",
     "ok": ["les chats", "les enfants"], "non": ["les chiens"], "teinte": (196, 132, 64),
     "texte": "Pistache est une petite chatte tigrée, curieuse de tout. Elle aime grimper, observer "
              "par la fenêtre et réclame des caresses en fin de journée. Elle vit très bien avec "
              "d'autres chats et des enfants calmes, mais les chiens lui font peur."},
    {"slug": "gaston", "nom": "Gaston", "espece": "Chien", "age": "9 ans", "taille": "moyen",
     "ok": ["les chiens", "les enfants"], "non": ["les chats"], "teinte": (52, 98, 78),
     "texte": "Gaston a neuf ans. Il aime les longues promenades et les siestes au soleil. "
              "Il tire un peu en laisse au départ, puis se calme très vite. Doux avec les enfants "
              "et les autres chiens, il ne doit pas vivre avec un chat."},
    {"slug": "nala", "nom": "Nala", "espece": "Chatte", "age": "6 mois", "taille": "",
     "ok": ["les chats", "les chiens", "les enfants"], "non": [], "teinte": (214, 150, 86),
     "texte": "Nala est une jeune chatte pleine d'énergie. Elle joue avec tout ce qui bouge, "
              "dort en boule sur les genoux et s'entend avec tout le monde, chiens compris."},
    {"slug": "biscotte", "nom": "Biscotte", "espece": "Chienne", "age": "3 ans", "taille": "petit",
     "ok": ["les chats", "les chiens"], "non": ["les enfants"], "teinte": (70, 112, 92),
     "texte": "Biscotte est une petite chienne joyeuse et câline, qui suit son humain partout. "
              "Elle vit bien avec les chats et les autres chiens. Elle préfère un foyer sans "
              "jeunes enfants, qui la rendent nerveuse."},
    {"slug": "rocky", "nom": "Rocky", "espece": "Chien", "age": "5 ans", "taille": "grand",
     "ok": [], "non": ["les chats", "les chiens", "les enfants"], "teinte": (38, 84, 66),
     "texte": "Rocky est un grand chien sportif et très attaché à ses humains. Il réagit vivement "
              "à la vue des autres chiens : il lui faut un adoptant expérimenté, une maison sans "
              "autre animal et sans enfant, et de vraies balades chaque jour."},
    {"slug": "mirabelle", "nom": "Mirabelle", "espece": "Chatte", "age": "11 ans", "taille": "",
     "ok": ["les enfants"], "non": ["les chats", "les chiens"], "teinte": (186, 120, 58),
     "texte": "Mirabelle est une chatte âgée, tranquille et très affectueuse. Elle suit un régime "
              "alimentaire adapté. Elle cherche un foyer calme où elle sera la seule chatte."},
    {"slug": "tigrou", "nom": "Tigrou", "espece": "Chat", "age": "4 ans", "taille": "",
     "ok": ["les chats", "les enfants"], "non": ["les chiens"], "teinte": (204, 124, 52),
     "texte": "Tigrou est un beau chat roux, sociable et bavard. Il apprécie la compagnie des "
              "autres chats et des enfants, mais pas celle des chiens."},
    {"slug": "caramel", "nom": "Caramel", "espece": "Chien", "age": "1 an", "taille": "moyen",
     "ok": ["les chats", "les chiens", "les enfants"], "non": [], "teinte": (60, 104, 84),
     "texte": "Caramel est un jeune chien plein de vie, qui s'entend avec tout le monde. "
              "Il a besoin de beaucoup d'exercice et d'un jardin pour se dépenser."},
    {"slug": "lune", "nom": "Lune", "espece": "Chatte", "age": "3 ans", "taille": "",
     "ok": ["les chats", "les chiens", "les enfants"], "non": [], "teinte": (176, 128, 80),
     "texte": "Lune est une chatte noire au caractère doux. Elle s'adapte à tout : enfants, "
              "chats, chiens. Elle aime les coins chauds et les jeux de plumes."},
    {"slug": "oscar", "nom": "Oscar", "espece": "Chien", "age": "12 ans", "taille": "petit",
     "ok": ["les chats", "les chiens", "les enfants"], "non": [], "teinte": (44, 92, 72),
     "texte": "Oscar est un petit chien senior, calme et sociable. Il fait de courtes promenades "
              "et beaucoup de siestes. Un compagnon idéal pour une personne qui cherche la tranquillité."},
    {"slug": "praline", "nom": "Praline", "espece": "Chatte", "age": "8 ans", "taille": "",
     "ok": [], "non": ["les chats", "les chiens", "les enfants"], "teinte": (192, 140, 90),
     "texte": "Praline est une chatte indépendante qui a besoin de temps pour faire confiance. "
              "Une fois en confiance, elle est très câline. Elle cherche un foyer calme, sans "
              "autre animal ni enfant."},
    {"slug": "ficelle", "nom": "Ficelle", "espece": "Chienne", "age": "7 ans", "taille": "moyen",
     "ok": ["les chiens", "les enfants"], "non": ["les chats"], "teinte": (64, 108, 88),
     "texte": "Ficelle est une chienne affectueuse et obéissante. Elle adore les enfants et la "
              "compagnie des autres chiens, mais pas celle des chats."},
]

MENU = [
    ("index.html", "Accueil"),
    ("animaux.html", "Nos animaux"),
    ("adopter.html", "Adopter"),
    ("aider.html", "Nous aider"),
    ("contact.html", "Contact"),
]


def e(texte):
    return html.escape(texte, quote=True)


def resume(a):
    morceaux = [a["espece"], a["age"]]
    if a["taille"]:
        morceaux.append({"petit": "petit gabarit", "moyen": "gabarit moyen", "grand": "grand gabarit"}[a["taille"]])
    return " · ".join(morceaux)


def ententes(a):
    lignes = []
    if a["ok"]:
        lignes.append("S'entend avec " + ", ".join(a["ok"]) + ".")
    if a["non"]:
        lignes.append("Pas avec " + ", ".join(a["non"]) + ".")
    return " ".join(lignes)


def page(titre, actif, corps, racine="", fenetre=False):
    menu = "\n".join(
        '        <li><a href="{r}{href}"{cur}>{lib}</a></li>'.format(
            r=racine, href=href, lib=lib,
            cur=' aria-current="page"' if href == actif else "")
        for href, lib in MENU
    )
    fenetre_html = ""
    if fenetre:
        fenetre_html = f"""
  <div class="voile" id="fenetre-don" hidden>
    <div class="fenetre" role="dialog" aria-modal="true" aria-labelledby="fenetre-titre">
      <button type="button" class="fermer" data-fermer aria-label="Fermer">×</button>
      <img src="{racine}images/refuge-logo.svg" alt="" width="72" height="72">
      <h2 id="fenetre-titre" tabindex="-1">Sans vous, ils n'ont personne.</h2>
      <p>Chaque mois, nos 95 pensionnaires ont besoin de croquettes, de soins et d'un toit.
      Un don de 20 € nourrit un chien pendant deux semaines.</p>
      <p><a class="bouton-don" href="{racine}don.html">Je fais un don</a></p>
      <a href="#" class="refus" data-fermer>Non merci, je préfère ne pas les aider</a>
    </div>
  </div>"""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex, nofollow">
  <title>{e(titre)} · Refuge des Trois Ruisseaux</title>
  <meta name="description" content="Refuge des Trois Ruisseaux, chiens et chats à l'adoption en Normandie. Site fictif créé pour la formation Uncode School.">
  <link rel="icon" href="{racine}images/refuge-logo.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{racine}style.css">
</head>
<body>
  <header class="entete">
    <div class="conteneur">
      <a class="marque" href="{racine}index.html">
        <img src="{racine}images/refuge-logo-fond-sombre.svg" alt="" width="64" height="64">
        <span><strong>Refuge des Trois Ruisseaux</strong>
        <span>Chiens et chats à l'adoption en Normandie</span></span>
      </a>
      <a class="bouton-don" href="{racine}don.html">Faire un don</a>
    </div>
  </header>
  <nav class="menu" aria-label="Menu principal">
    <ul>
{menu}
    </ul>
  </nav>
{corps}
  <footer class="pied">
    <div class="conteneur">
      <div class="colonnes">
        <div>
          <img src="{racine}images/refuge-logo-fond-sombre.svg" alt="" width="56" height="56">
          <p><strong>Refuge des Trois Ruisseaux</strong><br>Association loi 1901<br>Chemin des Trois Ruisseaux, Normandie</p>
        </div>
        <div>
          <h2>Horaires de visite</h2>
          <p>Du mercredi au dimanche, de 14h à 17h30.<br>Fermé les jours fériés.</p>
        </div>
        <div>
          <h2>Nous joindre</h2>
          <p>Téléphone : {TELEPHONE}</p>
          <p><a href="{racine}contact.html">Formulaire de contact</a> · <a href="{racine}mentions-legales.html">Mentions légales</a></p>
        </div>
      </div>
      <p class="mention-fiction">© 2016 Refuge des Trois Ruisseaux · Site réalisé par un bénévole.<br>
      Site fictif créé pour la formation Uncode School. Aucun animal, aucune personne, aucun don et aucun message de ce site n'est réel.</p>
    </div>
  </footer>
{fenetre_html}
  <script src="{racine}site.js"></script>
</body>
</html>
"""


def accueil():
    figures = []
    points = []
    for i, a in enumerate(ANIMAUX):
        actif = " actif" if i == 0 else ""
        figures.append(
            f'        <figure class="{actif.strip()}"><img src="photos/{a["slug"]}.jpg" alt="{e(a["nom"])}, {e(a["espece"].lower())} de {e(a["age"])}">'
            f'<figcaption>{e(a["nom"])}, {e(a["age"])}</figcaption></figure>'
        )
        cur = ' aria-current="true"' if i == 0 else ""
        points.append(f'<button type="button" aria-label="Photo {i + 1} : {e(a["nom"])}"{cur}></button>')
    corps = f"""  <div class="video-accueil">
    <video src="video/refuge.mp4" autoplay muted loop playsinline></video>
    <div class="accroche">
      <div class="conteneur">
        <h1>Ils n'attendent que vous</h1>
        <p>Chiens et chats abandonnés ou trouvés cherchent une famille. Et si c'était la vôtre ?</p>
      </div>
    </div>
  </div>
  <main class="conteneur">
    <section aria-labelledby="titre-carrousel">
      <h2 id="titre-carrousel">Ils attendent une famille</h2>
      <div class="carrousel">
        <div class="carrousel-piste">
{chr(10).join(figures)}
        </div>
        <button type="button" class="carrousel-fleche prec" aria-label="Photo précédente">‹</button>
        <button type="button" class="carrousel-fleche suiv" aria-label="Photo suivante">›</button>
        <div class="carrousel-points">{"".join(points)}</div>
      </div>
      <p><a href="animaux.html">Voir tous nos animaux à l'adoption</a></p>
    </section>

    <section aria-labelledby="titre-nouvelles">
      <h2 id="titre-nouvelles">Les nouvelles du refuge</h2>
      <div class="nouvelles">
        <article class="nouvelle">
          <h3>Chaleur : promenades le matin</h3>
          <time datetime="2026-08-12">12 août 2026</time>
          <p>Pendant les fortes chaleurs, les chiens sortent tôt. Les promenades du week-end ont lieu de 7h à 10h. Merci aux bénévoles qui se lèvent avec eux !</p>
        </article>
        <article class="nouvelle">
          <h3>Merci pour la collecte !</h3>
          <time datetime="2026-07-04">4 juillet 2026</time>
          <p>Grâce à vous, 640 kg de croquettes et de litière ont été collectés devant le supermarché. De quoi tenir tout l'été. <a href="aider.html">Les autres façons de nous aider</a></p>
        </article>
        <article class="nouvelle">
          <h3>C'est la saison des chatons</h3>
          <time datetime="2026-05-18">18 mai 2026</time>
          <p>Le refuge accueille ses premiers chatons de l'année. Ils seront adoptables à partir de deux mois. <a href="animaux.html">Voir les chats à l'adoption</a></p>
        </article>
      </div>
    </section>

    <section class="appel" aria-labelledby="titre-appel">
      <div>
        <h2 id="titre-appel">Le refuge vit de vos dons</h2>
        <p>Nourriture, vétérinaire, chauffage des chatteries : chaque euro compte. <a href="aider.html">Toutes les façons de nous aider</a></p>
      </div>
      <a class="bouton-don" href="don.html">Faire un don</a>
    </section>
  </main>"""
    return page("Accueil", "index.html", corps, fenetre=True)


def catalogue():
    cartes = []
    for a in ANIMAUX:
        cartes.append(f"""      <article class="carte-animal">
        <img src="photos/{a["slug"]}.jpg" alt="{e(a["nom"])}">
        <div class="texte">
          <span class="etiquette">À adopter</span>
          <h2>{e(a["nom"])}</h2>
          <p class="infos">{e(resume(a))}</p>
          <p>{e(ententes(a))}</p>
          <a href="animaux/{a["slug"]}.html">Découvrir sa fiche</a>
        </div>
      </article>""")
    corps = f"""  <main class="conteneur">
    <h1 class="titre-page">Nos animaux à l'adoption</h1>
    <p class="chapeau">Voici les chiens et les chats qui attendent une famille. Venez les rencontrer aux heures de visite !</p>
    <p class="maj">Liste mise à jour le {MISE_A_JOUR}.</p>
    <div class="grille-animaux">
{chr(10).join(cartes)}
    </div>
  </main>"""
    return page("Nos animaux", "animaux.html", corps)


def fiche(a):
    taille = f"\n          <dt>Gabarit</dt><dd>{e(a['taille'].capitalize())}</dd>" if a["taille"] else ""
    corps = f"""  <main class="conteneur">
    <p><a href="../animaux.html">← Retour à tous nos animaux</a></p>
    <h1 class="titre-page">{e(a["nom"])}</h1>
    <div class="fiche">
      <img src="../photos/{a["slug"]}.jpg" alt="{e(a["nom"])}, {e(a["espece"].lower())} de {e(a["age"])}">
      <div>
        <dl>
          <dt>Espèce</dt><dd>{e(a["espece"])}</dd>
          <dt>Âge</dt><dd>{e(a["age"])}</dd>{taille}
          <dt>Ententes</dt><dd>{e(ententes(a))}</dd>
        </dl>
        <p>{e(a["texte"])}</p>
        <p>{e(a["nom"])} est identifié{"e" if a["espece"] in ("Chatte", "Chienne") else ""}, vacciné{"e" if a["espece"] in ("Chatte", "Chienne") else ""} et stérilisé{"e" if a["espece"] in ("Chatte", "Chienne") else ""}.</p>
        <p><a href="../adopter.html">Comment adopter {e(a["nom"])} ?</a></p>
      </div>
    </div>
  </main>"""
    return page(a["nom"], "animaux.html", corps, racine="../")


def adopter():
    corps = """  <main class="conteneur">
    <h1 class="titre-page">Adopter un animal</h1>
    <p class="chapeau">Adopter, c'est s'engager pour de nombreuses années. Nous prenons le temps de vous connaître pour trouver le compagnon qui vous convient.</p>
    <section aria-labelledby="titre-etapes">
      <h2 id="titre-etapes">Comment ça se passe ?</h2>
      <ol class="etapes">
        <li><strong>Choisissez votre compagnon</strong> sur ce site ou lors d'une visite au refuge.</li>
        <li><strong>Remplissez le questionnaire de pré-adoption</strong> (six pages). Il est à retirer à l'accueil du refuge ou à demander par téléphone.</li>
        <li><strong>Rapportez-le au refuge</strong> avec les pièces demandées ci-dessous.</li>
        <li><strong>Nous vous rappelons</strong> pour organiser une rencontre avec l'animal.</li>
      </ol>
    </section>
    <section class="encart" aria-labelledby="titre-pieces">
      <h2 id="titre-pieces">Les pièces à fournir</h2>
      <ul>
        <li>Une copie de votre pièce d'identité.</li>
        <li>Un justificatif de domicile de moins de trois mois.</li>
        <li>Des photos de votre logement et de votre jardin.</li>
        <li>La date de naissance de chaque enfant du foyer.</li>
      </ul>
    </section>
    <section aria-labelledby="titre-frais">
      <h2 id="titre-frais">Les frais d'adoption</h2>
      <p>Chien : 250 €. Chat : 150 €. Les frais se règlent au refuge. Tous nos animaux sont identifiés, vaccinés et stérilisés.</p>
      <p>Une question ? <a href="contact.html">Écrivez-nous</a> ou appelez-nous aux heures de visite.</p>
    </section>
  </main>"""
    return page("Adopter", "adopter.html", corps)


def aider():
    corps = """  <main class="conteneur">
    <h1 class="titre-page">Nous aider</h1>
    <p class="chapeau">Le refuge ne vit que grâce à ses bénévoles et à ses donateurs. Voici comment vous pouvez nous donner un coup de main.</p>
    <section class="appel" aria-labelledby="titre-don">
      <div>
        <h2 id="titre-don">Faire un don</h2>
        <p>Votre don finance la nourriture, les soins vétérinaires et l'entretien du refuge.</p>
      </div>
      <a class="bouton-don" href="don.html">Faire un don</a>
    </section>
    <section aria-labelledby="titre-benevole">
      <h2 id="titre-benevole">Devenir bénévole</h2>
      <p>Promener les chiens, s'occuper des chats, aider aux collectes : il y a toujours à faire. <a href="contact.html">Proposez-nous votre aide</a> en précisant vos disponibilités.</p>
    </section>
    <section aria-labelledby="titre-materiel">
      <h2 id="titre-materiel">Donner du matériel</h2>
      <p>Nous acceptons les couvertures, les serviettes, les jouets, les croquettes et la litière. Déposez-les à l'accueil aux heures de visite.</p>
    </section>
  </main>"""
    return page("Nous aider", "aider.html", corps)


def don():
    corps = """  <main class="conteneur">
    <h1 class="titre-page">Faire un don</h1>
    <p class="chapeau">Les dons au refuge passent par une plateforme de dons en ligne pour les associations.</p>
    <p class="encart">Site fictif : la plateforme de dons n'est pas reliée et aucun paiement n'est possible.</p>
    <p><a href="index.html">Retour à l'accueil</a></p>
  </main>"""
    return page("Faire un don", "aider.html", corps)


def contact():
    corps = f"""  <main class="conteneur">
    <h1 class="titre-page">Nous contacter</h1>
    <p class="chapeau">Une question sur un animal, une adoption, le bénévolat ? Écrivez-nous, nous vous répondons sous quelques jours. Vous pouvez aussi nous appeler au {TELEPHONE} aux heures de visite.</p>
    <form class="contact" action="#" method="post">
      <div class="champ">
        <label for="nom">Nom et prénom</label>
        <input id="nom" name="nom" type="text" autocomplete="name" required>
      </div>
      <div class="champ">
        <label for="email">Adresse e-mail</label>
        <input id="email" name="email" type="email" autocomplete="email" required>
      </div>
      <div class="champ">
        <label for="telephone">Téléphone</label>
        <input id="telephone" name="telephone" type="tel" autocomplete="tel">
      </div>
      <div class="champ">
        <label for="sujet">Sujet</label>
        <select id="sujet" name="sujet">
          <option>Adoption</option>
          <option>Bénévolat</option>
          <option>Don</option>
          <option>Autre</option>
        </select>
      </div>
      <div class="champ">
        <label for="message">Votre message</label>
        <textarea id="message" name="message" rows="6" required></textarea>
      </div>
      <div class="case">
        <input id="lettre" name="lettre" type="checkbox" checked>
        <label for="lettre">Je m'inscris à la lettre d'information du refuge</label>
      </div>
      <p class="petit">Vos informations servent à répondre à votre message. Voir les <a href="mentions-legales.html">mentions légales</a>.</p>
      <button class="bouton" type="submit">Envoyer</button>
      <p id="message-envoi" class="message-envoi" tabindex="-1" hidden>Site fictif : votre message n'a été envoyé à personne et rien n'a été enregistré.</p>
    </form>
  </main>"""
    return page("Contact", "contact.html", corps)


def mentions(hebergeur):
    corps = f"""  <main class="conteneur">
    <h1 class="titre-page">Mentions légales</h1>
    <section aria-labelledby="titre-editeur">
      <h2 id="titre-editeur">Éditeur du site</h2>
      <p>Refuge des Trois Ruisseaux, association loi 1901.<br>Chemin des Trois Ruisseaux, Normandie.<br>Téléphone : {TELEPHONE}.</p>
      <p>Directrice de la publication : Annick Delorme, présidente.</p>
    </section>
    <section aria-labelledby="titre-hebergeur">
      <h2 id="titre-hebergeur">Hébergeur</h2>
      <p>{e(hebergeur)}</p>
    </section>
    <section aria-labelledby="titre-donnees">
      <h2 id="titre-donnees">Données personnelles</h2>
      <p>Les informations envoyées par le formulaire de contact servent à vous répondre. Pour exercer vos droits, appelez-nous ou écrivez-nous par ce même formulaire.</p>
    </section>
    <section aria-labelledby="titre-fiction">
      <h2 id="titre-fiction">Un site fictif</h2>
      <p>Le Refuge des Trois Ruisseaux n'existe pas. Ce site a été créé pour la formation Uncode School, comme support de cours sur la conception d'interfaces. Il comporte volontairement des défauts. Les animaux, les personnes et le numéro de téléphone sont fictifs : le numéro appartient à une plage réservée à la fiction.</p>
    </section>
  </main>"""
    return page("Mentions légales", "mentions-legales.html", corps)


# ---------- Médias provisoires ----------

def photo_provisoire(a, chemin):
    import numpy as np
    from PIL import Image, ImageDraw, ImageFont

    W, H = 4032, 3024  # format d'un appareil photo de téléphone
    r, g, b = a["teinte"]
    haut = np.array([min(r + 60, 255), min(g + 60, 255), min(b + 60, 255)], dtype=float)
    bas = np.array([r, g, b], dtype=float)
    y = np.linspace(0, 1, H)[:, None, None]
    fond = haut * (1 - y) + bas * y
    img = Image.fromarray(np.broadcast_to(fond, (H, W, 3)).astype("uint8"))
    d = ImageDraw.Draw(img)

    # Empreinte de patte, reprise du logo, au centre
    cx, cy, k = W // 2, int(H * 0.43), 17
    clair = (251, 246, 238)
    d.ellipse([cx - 15 * k, cy - 12 * k, cx + 15 * k, cy + 12 * k], fill=clair)
    for dx, dy in [(-19, -16), (-8, -26), (8, -26), (19, -16)]:
        ex, ey = cx + dx * k, cy + dy * k
        d.ellipse([ex - 6.5 * k, ey - 8.5 * k, ex + 6.5 * k, ey + 8.5 * k], fill=clair)

    police = ICI / "outils" / "nunito-latin-800-normal.woff"
    try:
        grand = ImageFont.truetype(str(police), 300)
        petit = ImageFont.truetype(str(police), 120)
    except OSError:
        grand = petit = ImageFont.load_default()
    for texte, fonte, yy in [(a["nom"], grand, int(H * 0.555)), ("Photo provisoire", petit, int(H * 0.67))]:
        largeur = d.textlength(texte, font=fonte)
        d.text(((W - largeur) / 2, yy), texte, font=fonte, fill=clair)

    # Grain de capteur : donne le poids d'une vraie photo de téléphone (4 à 6 Mo)
    rng = np.random.default_rng(sum(map(ord, a["slug"])))
    tableau = np.asarray(img, dtype=float) + rng.normal(0, 9.5, (H, W, 1))
    Image.fromarray(np.clip(tableau, 0, 255).astype("uint8")).save(chemin, "JPEG", quality=93)


def video_provisoire(chemin):
    from PIL import Image, ImageDraw, ImageFont

    carton = ICI / "outils" / "carton-video.png"
    img = Image.new("RGB", (1920, 1080), (31, 77, 58))
    d = ImageDraw.Draw(img)
    police = ICI / "outils" / "nunito-latin-800-normal.woff"
    try:
        grand = ImageFont.truetype(str(police), 96)
        petit = ImageFont.truetype(str(police), 48)
    except OSError:
        grand = petit = ImageFont.load_default()
    for texte, fonte, yy in [("Le refuge en vidéo", grand, 300), ("Vidéo provisoire", petit, 430)]:
        largeur = d.textlength(texte, font=fonte)
        d.text(((1920 - largeur) / 2, yy), texte, font=fonte, fill=(251, 246, 238))
    img.save(carton)
    # 40 s en 1080p à 6 Mb/s, avec du grain : le poids d'une vidéo filmée au téléphone (30 Mo environ)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(carton), "-t", "40",
        "-vf", "zoompan=z='min(zoom+0.0006,1.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1000:s=1920x1080:fps=25,noise=alls=24:allf=t,format=yuv420p",
        "-c:v", "libx264", "-b:v", "6M", "-minrate", "6M", "-maxrate", "6M", "-bufsize", "12M",
        "-movflags", "+faststart", str(chemin),
    ], check=True)


def main():
    hebergeur = "github"
    if "--hebergeur" in sys.argv:
        hebergeur = sys.argv[sys.argv.index("--hebergeur") + 1]

    # On garde photos et vidéo d'une construction à l'autre : elles sont longues à fabriquer
    for f in DIST.glob("*.html"):
        f.unlink()
    (DIST / "animaux").mkdir(parents=True, exist_ok=True)
    (DIST / "photos").mkdir(exist_ok=True)
    (DIST / "video").mkdir(exist_ok=True)

    shutil.copy(ASSETS / "style.css", DIST / "style.css")
    shutil.copy(ASSETS / "site.js", DIST / "site.js")
    shutil.copytree(ASSETS / "fonts", DIST / "fonts", dirs_exist_ok=True)
    shutil.copytree(ASSETS / "images", DIST / "images", dirs_exist_ok=True)

    pages = {
        "index.html": accueil(),
        "animaux.html": catalogue(),
        "adopter.html": adopter(),
        "aider.html": aider(),
        "don.html": don(),
        "contact.html": contact(),
        "mentions-legales.html": mentions(HEBERGEURS[hebergeur]),
    }
    for a in ANIMAUX:
        pages[f"animaux/{a['slug']}.html"] = fiche(a)
    for nom, contenu in pages.items():
        (DIST / nom).write_text(contenu, encoding="utf-8")

    (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")

    for a in ANIMAUX:
        cible = DIST / "photos" / f"{a['slug']}.jpg"
        source = SOURCES / "photos" / f"{a['slug']}.jpg"
        if source.exists():
            shutil.copy(source, cible)
        elif not cible.exists():
            photo_provisoire(a, cible)

    cible = DIST / "video" / "refuge.mp4"
    source = SOURCES / "video" / "refuge.mp4"
    if source.exists():
        shutil.copy(source, cible)
    elif not cible.exists():
        video_provisoire(cible)

    poids = sum(f.stat().st_size for f in DIST.rglob("*") if f.is_file())
    print(f"docs/ construit : {len(pages)} pages, {poids / 1e6:.1f} Mo au total, hébergeur « {hebergeur} ».")


if __name__ == "__main__":
    main()
