import csv
from datetime import datetime


class BatchProcessor:

    def __init__(self, csv_path, log_path="journal.log"):
        self.csv_path = csv_path
        self.log_path = log_path

        self.csv_file = None
        self.log_file = None
        self.reader = None

    def log(self, message):

        date = datetime.now()

        self.log_file.write(
            f"[{date}] {message}\n"
        )

        self.log_file.flush()

    def __enter__(self):

        try:

            self.log_file = open(
                self.log_path,
                "a",
                encoding="utf-8"
            )

            self.log("Début du traitement.")

            self.csv_file = open(
                self.csv_path,
                "r",
                encoding="utf-8",
                newline=""
            )

            self.reader = csv.reader(self.csv_file)

            print("Fichiers ouverts correctement.")

            return self

        except (OSError, csv.Error) as error:

            if self.csv_file is not None:
                self.csv_file.close()

            if self.log_file is not None:
                self.log_file.close()

            raise RuntimeError(
                f"Erreur d'ouverture : {error}"
            ) from error

    def process_operation(self, row):

        if not row:
            return None

        operation = ",".join(row).strip()

        if operation.upper() == "ERREUR":
            raise ValueError(
                "Erreur simulée pendant le traitement."
            )

        return operation.upper()

    def run(self):

        try:

            for numero, row in enumerate(
                self.reader, start=1
            ):

                if not row or not any(
                    cell.strip() for cell in row
                ):
                    continue

                operation = ",".join(row).strip()

                self.log(
                    f"Début opération {numero} : {operation}"
                )

                resultat = self.process_operation(row)

                print(
                    f"Opération {numero} : {resultat}"
                )

                self.log(
                    f"Fin opération {numero} : {resultat}"
                )

        except (OSError, csv.Error) as error:

            self.log(f"Erreur de lecture CSV : {error}")

            raise

    def __exit__(
        self, exc_type, exc_value, traceback
    ):

        try:

            if self.log_file is not None:

                if exc_type is None:
                    self.log("Traitement terminé sans erreur.")

                else:
                    self.log(
                        f"Traitement interrompu : "
                        f"{exc_type.__name__} — {exc_value}"
                    )

        finally:

            if (
                self.csv_file is not None
                and not self.csv_file.closed
            ):
                self.csv_file.close()

            if (
                self.log_file is not None
                and not self.log_file.closed
            ):
                self.log_file.close()

        return False


if __name__ == "__main__":

    with BatchProcessor(
        "operations.csv",
        "journal.log"
    ) as processor:

        processor.run()