import csv
import unicodedata

class NormalText:
    def __init__(self, csv_path: str = "similar_chars.csv") -> None:
        self.similar = self.load_csv(csv_path)

    def load_csv(self, path: str) -> dict[str, str]:
        mapping = {}

        with open(path, encoding = "utf-8") as file:
            reader = csv.reader(file)
            next(reader)

            for src, dst in reader:
                mapping[src] = dst

        return mapping

    def normalize(self, text: str, form: str = "NFKD") -> str:
        text = unicodedata.normalize(form, text)
        text = "".join(self.similar.get(char, char) for char in text)
        text = text.upper()
        text = text.replace(" ", "")

        return text
    
    def update(self, data: dict[str, str]) -> None:
        self.similar(data)
    
    def corpus(self) -> dict[str, str]:
        return self.similar

    def __call__(self) -> dict[str, str]:
        return self.similar