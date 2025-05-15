from typing import Dict, Optional
import csv


class Interpreter:
    """
    The Interpreter object
    """
    def __init__(self, id: int, name: str, language: tuple):
        self.id = id
        self.name = name
        self.language = language

    def __str__(self):
        return f"Name: {self.id}, name: {self.name}, language: {self.language}"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "language": self.language
        }


class InterpreterRepository:
    """
    Repository to store and manage Interpreter objects.
    """
    def __init__(self):
        self._interpreters: Dict[int, Interpreter] = {}

    def add(self, interpreter: Interpreter):
        if interpreter.id in self._interpreters:
            raise ValueError(f"Interpreter with id {interpreter.id} already exists.")
        self._interpreters[interpreter.id] = interpreter

    def get(self, id: int) -> Optional[Interpreter]:
        return self._interpreters.get(id)

    def remove(self, id: int):
        if id in self._interpreters:
            del self._interpreters[id]
        else:
            raise KeyError(f"No interpreter found with id {id}.")

    def list_all(self):
        return list(self._interpreters.values())

    def load_from_csv(self, file_path: str):
        import csv
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id = int(row['id'])
                name = row['name']
                language = row['language']
                interpreter = Interpreter(id, name, language)
                self.add(interpreter)
    


    
    def save_to_csv(self, file_path: str):
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['id', 'name', 'language'])
            writer.writeheader()
            for interpreter in self._interpreters.values():
                writer.writerow({
                    'id': interpreter.id,
                    'name': interpreter.name,
                    'language': interpreter.language
                })
            for interpreter in self.list_all():
                print("*",interpreter)