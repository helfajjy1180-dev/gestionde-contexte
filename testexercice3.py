import csv
from exercice3 import BatchProcessor


def creer_csv(nom_fichier, operations):

    with open(
        nom_fichier,
        "w",
        encoding="utf-8",
        newline=""
    ) as fichier:

        writer = csv.writer(fichier)

        for operation in operations:
            writer.writerow([operation])


def test_normal():

    print("\n===== TEST NORMAL =====")

    creer_csv(
        "operations_test.csv",
        [
            "ajouter utilisateur",
            "modifier salle",
            "supprimer reservation"
        ]
    )

    with BatchProcessor(
        "operations_test.csv",
        "journal_test.log"
    ) as processor:

        processor.run()

    print("Test normal réussi.")


def test_erreur():

    print("\n===== TEST ERREUR =====")

    creer_csv(
        "operations_erreur.csv",
        [
            "ajouter utilisateur",
            "ERREUR",
            "modifier salle"
        ]
    )

    try:

        with BatchProcessor(
            "operations_erreur.csv",
            "journal_test.log"
        ) as processor:

            processor.run()

    except ValueError as error:

        print("Exception capturée :", error)

    print("Test erreur terminé.")


if __name__ == "__main__":

    test_normal()

    test_erreur()