# U01.1 — Dossier de préparation du premier essai accompagné

Statut : **instruments vierges, soumis à validation humaine**. Aucun essai humain, résultat pédagogique ou temps réel n’est annoncé.

Branche : `docs/u01-1-dossier-experimentation`, issue de `docs/u01-1-consolidation` au commit `fcbdb8b1c73c0760e60fb4d53506d6c5d85e4fc6`. Aucun contenu U02, changement applicatif, changement du laboratoire ou de Pyodide. Aucune publication, fusion ou déploiement.

## Documents à utiliser

| Document | Word modifiable | PDF pour imprimer |
|---|---|---|
| Support élève essentiel | [01-support-eleve.docx](documents/01-support-eleve.docx) | [PDF](documents/01-support-eleve.pdf) |
| Guide et formation scientifique enseignant | [02-guide-enseignant.docx](documents/02-guide-enseignant.docx) | [PDF](documents/02-guide-enseignant.pdf) |
| Grille d’observation non nominative | [03-grille-observation.docx](documents/03-grille-observation.docx) | [PDF](documents/03-grille-observation.pdf) |
| Retour enseignant fondé sur des productions | [04-retour-enseignant.docx](documents/04-retour-enseignant.docx) | [PDF](documents/04-retour-enseignant.pdf) |
| Procédure de préparation, recueil et analyse | [05-procedure.docx](documents/05-procedure.docx) | [PDF](documents/05-procedure.pdf) |

Lire d’abord la procédure. Support élève : A4 portrait, recto simple, six pages distribuées progressivement. Grille : A4 paysage. Autres documents : A4 portrait. Impression noire, taille réelle, une page par feuille. Les PDF stabilisent la pagination contrôlée ; une autre version de Word ou une autre police peut modifier le rendu des DOCX.

Le guide comporte **toute la préparation scientifique et Python ainsi que tous les corrigés de référence**, y compris ceux des prolongements, clairement signalés. Il reste réservé à l’enseignant. Les consignes anciennes de distribution des deux Markdown, conservées dans la reprise fidèle des sources, correspondent pour cet essai à la remise du seul support élève DOCX/PDF réuni.

## Conservation et adaptations éditoriales

Les sept Markdown de `../refondation/u01/` sont conservés à l’identique ; leurs empreintes figurent dans [sources-sha256.json](sources-sha256.json). Le cours élève et les activités sont assemblés : introduction adaptée au document unique, espaces d’écriture agrandis, tableaux mis en page. Les règles, données, conventions, prédictions et activités essentielles C0, P1–E3, A1, T1–T2 et I1–I2 sont conservées. Le routage ancien vers deux fichiers est remplacé par la succession des pages ; A2/B1 sont exclus du support essentiel.

L’explication de cours relative à Microduck est conservée page 4 : la retirer réécrirait le contenu demandé. Elle est remise **après E2/E3**. Aucun corrigé d’activité ni réponse préremplie du transfert n’est inclus dans le support élève. Le transfert Nora et le bilan curseur sont recueillis avant correction. L’essai vise le parcours accompagné ; son exploitation en autonomie reste à examiner ultérieurement.

Les nouveaux instruments séparent temps, lecture, technique, productions, justifications et interventions. Ils ne calculent aucune note globale. Les réponses avec relance restent identifiables ; une production non observable n’est pas assimilée à une erreur.

## Vérification et reconstruction

Les DOCX sont construits par Python standard et Pandoc, puis ouverts en lecture seule et exportés par **Microsoft Word 16.0 réel**. Poppler et Pillow servent au contrôle et aux planches visuelles. Ces outils servent uniquement à la fabrication documentaire, sans nouvelle dépendance de l’application.

```powershell
python docs/pedagogie/experimentation-u01-1/construire_dossier.py
powershell -NoProfile -ExecutionPolicy Bypass -File docs/pedagogie/experimentation-u01-1/controler_word.ps1
python docs/pedagogie/experimentation-u01-1/controler_documents.py
```

Voir [CONTROLE_QUALITE.md](CONTROLE_QUALITE.md), [controle-word.json](controle-word.json) et [les planches](controle/). Les `.md` de `documents/` sont les intermédiaires de composition ; pour distribuer les documents, utiliser les DOCX/PDF. La reconstruction actualise les métadonnées Word : les binaires ne sont pas nécessairement identiques octet pour octet d’une génération à l’autre.

**Point d’arrêt :** dossier prêt pour relecture du commanditaire. La clarté perçue, la place suffisante pour les réponses, l’efficacité pédagogique et les vingt minutes restent des hypothèses à examiner lors d’un essai autorisé.
