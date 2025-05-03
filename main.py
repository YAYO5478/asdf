import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class Question:
    def __init__(self, question, correct_answer, other_answers):
        self.question = question
        self.correct_answer = correct_answer
        self.all_answers = other_answers + [correct_answer]
        self.shuffled_answers = []

    def shuffle_answers(self):
        self.shuffled_answers = self.all_answers[:]
        random.shuffle(self.shuffled_answers)

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Examen de Preguntas")
        self.questions = []
        self.current_question_index = 0
        self.selected_answer = tk.StringVar()

        # Interfaz: entrada de preguntas
        self.frame_add = tk.LabelFrame(root, text="Agregar Pregunta", padx=10, pady=10)
        self.frame_add.pack(padx=10, pady=5, fill="x")

        tk.Label(self.frame_add, text="Pregunta:").grid(row=0, column=0, sticky="w")
        self.entry_question = tk.Entry(self.frame_add, width=60)
        self.entry_question.grid(row=0, column=1, padx=5)

        tk.Label(self.frame_add, text="Respuesta Correcta:").grid(row=1, column=0, sticky="w")
        self.entry_correct = tk.Entry(self.frame_add, width=40)
        self.entry_correct.grid(row=1, column=1, sticky="w")

        self.button_add = tk.Button(self.frame_add, text="Agregar Pregunta", command=self.add_question)
        self.button_add.grid(row=2, column=0, columnspan=2, pady=5)

        # Interfaz: examen
        self.frame_exam = tk.LabelFrame(root, text="Examen", padx=10, pady=10)
        self.frame_exam.pack(padx=10, pady=5, fill="both", expand=True)

        self.label_question = tk.Label(self.frame_exam, text="", wraplength=500, justify="left")
        self.label_question.pack(anchor="w")

        self.radio_buttons = []
        for _ in range(4):
            rb = tk.Radiobutton(self.frame_exam, text="", variable=self.selected_answer, value="", anchor="w", justify="left")
            rb.pack(anchor="w")
            self.radio_buttons.append(rb)

        self.button_shuffle = tk.Button(self.frame_exam, text="Desordenar Respuestas", command=self.shuffle_current_answers)
        self.button_shuffle.pack(pady=5)

        self.button_next = tk.Button(self.frame_exam, text="Evaluar Pregunta", command=self.check_answer)
        self.button_next.pack(pady=5)

        self.feedback_label = tk.Label(self.frame_exam, text="")
        self.feedback_label.pack()

    def add_question(self):
        question = self.entry_question.get().strip()
        correct = self.entry_correct.get().strip()

        if not question or not correct:
            messagebox.showwarning("Advertencia", "Debes ingresar la pregunta y la respuesta correcta.")
            return

        other_answers = []
        while len(other_answers) < 3:
            ans = simpledialog.askstring("Respuesta Incorrecta", f"Ingresa respuesta incorrecta #{len(other_answers)+1}:")
            if ans:
                other_answers.append(ans)

        new_question = Question(question, correct, other_answers)
        self.questions.append(new_question)
        messagebox.showinfo("Éxito", "Pregunta agregada correctamente.")
        self.entry_question.delete(0, tk.END)
        self.entry_correct.delete(0, tk.END)

        if len(self.questions) == 1:
            self.display_question(0)

    def display_question(self, index):
        if index < len(self.questions):
            q = self.questions[index]
            q.shuffle_answers()
            self.selected_answer.set("")
            self.label_question.config(text=f"{index+1}. {q.question}")
            for i, ans in enumerate(q.shuffled_answers):
                self.radio_buttons[i].config(text=ans, value=ans)
                self.radio_buttons[i].pack(anchor="w")
            self.feedback_label.config(text="")

    def shuffle_current_answers(self):
        self.display_question(self.current_question_index)

    def check_answer(self):
        selected = self.selected_answer.get()
        correct = self.questions[self.current_question_index].correct_answer
        if selected == correct:
            self.feedback_label.config(text="✅ Correcto", fg="green")
        else:
            self.feedback_label.config(text="❌ Incorrecto", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
