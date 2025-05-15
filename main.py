from datetime import datetime
import sys
import csv

from interpreter import InterpreterRepository, Interpreter

if __name__ == "__main__":
    # Data Setup
    ic1 = Interpreter(123456, "john doe", "Spanish")
    ic2 = Interpreter(123457, "jane doe", "Arabic")
    ic3 = Interpreter(123458, "Ivan Ivanov", ['Russian','UZB'])


repo = InterpreterRepository()
repo.load_from_csv('interpreter.csv')

for interpreter in repo.list_all():
    print(interpreter)



repo2= InterpreterRepository()

# Load from CSV
repo2.load_from_csv('interpreter.csv')

# Add a new interpreter
new_interpreter = Interpreter(7, "Kim", ["Korean","Mandarin"])
repo2.add(new_interpreter)
repo2.add(ic3)

# Save back to CSV
repo2.save_to_csv('interpreter.csv') 