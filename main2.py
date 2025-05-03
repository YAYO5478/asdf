import tkinter as tk
from tkinter import messagebox
import random

class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplicación de Examen")

        # Lista para almacenar las preguntas y respuestas
        self.questions = []

        # Crear los widgets de la interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Etiquetas y campos de entrada para la pregunta y la respuesta correcta
        self.label_question = tk.Label(self.root, text="Pregunta:")
        self.label_question.grid(row=0, column=0, padx=10, pady=10)
        self.entry_question = tk.Entry(self.root, width=50)
        self.entry_question.grid(row=0, column=1, padx=10, pady=10)

        self.label_correct_answer = tk.Label(self.root, text="Respuesta Correcta:")
        self.label_correct_answer.grid(row=1, column=0, padx=10, pady=10)
        self.entry_correct_answer = tk.Entry(self.root, width=50)
        self.entry_correct_answer.grid(row=1, column=1, padx=10, pady=10)

        self.label_incorrect_answers = tk.Label(self.root, text="Respuestas Incorrectas (Formato: A) Heap, B) Disco duro, C) JVM):")
        self.label_incorrect_answers.grid(row=2, column=0, padx=10, pady=10)
        self.entry_incorrect_answers = tk.Entry(self.root, width=50)
        self.entry_incorrect_answers.grid(row=2, column=1, padx=10, pady=10)

        # Botón para agregar la pregunta
        self.button_add_question = tk.Button(self.root, text="Agregar Pregunta", command=self.add_question)
        self.button_add_question.grid(row=3, column=0, columnspan=2, pady=10)

        # Botón para iniciar el examen
        self.button_start_exam = tk.Button(self.root, text="Iniciar Examen", command=self.start_exam)
        self.button_start_exam.grid(row=4, column=0, columnspan=2, pady=10)

        # Lista para mostrar las preguntas
        self.label_questions = tk.Label(self.root, text="Preguntas Agregadas:")
        self.label_questions.grid(row=5, column=0, columnspan=2)
        self.listbox_questions = tk.Listbox(self.root, width=50, height=10)
        self.listbox_questions.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def add_question(self):
        question = self.entry_question.get()
        correct_answer = self.entry_correct_answer.get()
        incorrect_answers_text = self.entry_incorrect_answers.get()

        # Validar que las respuestas incorrectas estén en el formato correcto
        incorrect_answers = self.parse_incorrect_answers(incorrect_answers_text)

        # Comprobar que hay al menos 4 respuestas únicas
        if len(incorrect_answers) + 1 < 4:
            messagebox.showerror("Error", "Debe haber al menos 4 respuestas únicas (1 correcta + 3 incorrectas).")
            return

        # Asegurarse de que no haya respuestas duplicadas
        all_answers = [correct_answer] + incorrect_answers
        unique_answers = list(set(all_answers))  # Eliminar respuestas duplicadas

        # Verificar si la cantidad de respuestas únicas es válida
        if len(unique_answers) < 4:
            messagebox.showerror("Error", "Las respuestas no pueden ser duplicadas. Debe haber al menos 4 respuestas únicas.")
            return

        # Agregar la pregunta y las respuestas a la lista
        self.questions.append({
            "question": question,
            "correct_answer": correct_answer,
            "answers": unique_answers
        })

        # Limpiar los campos de entrada
        self.entry_question.delete(0, tk.END)
        self.entry_correct_answer.delete(0, tk.END)
        self.entry_incorrect_answers.delete(0, tk.END)

        # Actualizar la lista de preguntas
        self.update_question_list()

    def parse_incorrect_answers(self, text):
        # Dividir las respuestas incorrectas por coma y eliminar las letras
        answers = [ans.strip().split(')', 1)[1].strip() for ans in text.split(',')]
        return answers

    def update_question_list(self):
        self.listbox_questions.delete(0, tk.END)
        for q in self.questions:
            self.listbox_questions.insert(tk.END, q["question"])

    def start_exam(self):
        if not self.questions:
            messagebox.showwarning("Advertencia", "No hay preguntas para el examen.")
            return

        # Elegir una pregunta aleatoria
        question = random.choice(self.questions)
        answers = question["answers"]

        # Desordenar las respuestas
        random.shuffle(answers)

        # Crear una ventana de examen para mostrar la pregunta y las respuestas
        exam_window = tk.Toplevel(self.root)
        exam_window.title("Examen")

        # Mostrar la pregunta
        label_question = tk.Label(exam_window, text=question["question"], font=("Arial", 14))
        label_question.pack(pady=10)

        # Mostrar las respuestas como botones
        for answer in answers:
            button = tk.Button(exam_window, text=answer, width=50, height=2, command=lambda ans=answer: self.check_answer(ans, question["correct_answer"], exam_window))
            button.pack(pady=5)

    def check_answer(self, selected_answer, correct_answer, exam_window):
        if selected_answer == correct_answer:
            messagebox.showinfo("Resultado", "¡Respuesta Correcta!")
        else:
            messagebox.showerror("Resultado", "Respuesta Incorrecta.")
        exam_window.destroy()

# Crear la ventana principal
root = tk.Tk()
app = ExamApp(root)
root.mainloop()
