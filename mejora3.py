from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup

# Preguntas del juego
questions = [
    {
        "question": "¿Cuál es la capital de Colombia?",
        "options": ["Bogotá", "Medellín", "Cali", "Cartagena"],
        "answer": "Bogotá"
    },
    {
        "question": "¿Cuál es la capital de Francia?",
        "options": ["Marsella", "Paris", "Lyon", "Toulouse"],
        "answer": "París"
    },
    {
        "question": "¿Cuál es la capital de Japón?",
        "options": ["Nagasaki", "Osaka", "Kioto", "Tokio"],
        "answer": "Tokio"
    },
    {
        "question": "¿Cuál es la capital de Brasil?",
        "options": ["Sao Paulo", "Río de Janeiro", "Brasilia", "Salvador"],
        "answer": "Brasilia"
    },
    {
        "question": "¿Cuál es la capital de Australia?",
        "options": ["Canberra", "Sídney", "Melbourne", "Perth"],
        "answer": "Canberra"
    },
    {
        "question": "¿Cuánto es 12 + 8?",
        "options": ["20", "18", "22", "24"],
        "answer": "20"
    },
    {
        "question": "¿Cuánto es 15 × 3?",
        "options": ["50", "30", "60", "45"],
        "answer": "45"
    },
    {
        "question": "¿Cuánto es 9 - 4?",
        "options": ["3", "5", "6", "7"],
        "answer": "5"
    },
    {
        "question": "¿Cuánto es 7 × 6?",
        "options": ["48", "36", "42", "40"],
        "answer": "42"
    },
    {
        "question": "¿Cuánto es 100 ÷ 4?",
        "options": ["25", "20", "30", "15"],
        "answer": "25"
    },
    {
        "question": "¿Quién desarrolló la teoría de la relatividad?",
        "options": ["Isaac Newton", "Albert Einstein", "Nikola Tesla", "Marie Curie"],
        "answer": "Albert Einstein"
    },
  {
        "question": "¿Quién formuló las leyes del movimiento y la gravitación universal?",
        "options": ["Galileo Galilei", "Albert Einstein", "Isaac Newton", "Nikola Tesla"],
        "answer": "Isaac Newton"
    },
    {
        "question": "¿Quién es conocido como el padre de la electricidad moderna?",
        "options": ["Michael Faraday", "Thomas Edison", "James Watt", "Nikola Tesla"],
        "answer": "Nikola Tesla"
    },
    {
        "question": "¿Quién descubrió la estructura del ADN?",
        "options": ["Marie Curie", "James Watson y Francis Crick", "Rosalind Franklin", "Gregor Mendel"],
        "answer": "James Watson y Francis Crick"
    },
    {
        "question": "¿Quién propuso la teoría de la evolución por selección natural?",
        "options": ["Gregor Mendel", "Jean-Baptiste Lamarck", "Alfred Wallace", "Charles Darwin"],
        "answer": "Charles Darwin"
    }
]


# Configuración inicial
TIME_LIMIT = 10  # Tiempo en segundos por pregunta


class TriviaGame(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.current_question = 0
        self.score = 0
        self.time_left = TIME_LIMIT


        # Widgets
        self.timer_label = Label(text=f"Tiempo restante: {self.time_left} s", font_size=20, size_hint=(1, 0.1))
        self.add_widget(self.timer_label)

        self.question_label = Label(text="", font_size=24, size_hint=(1, 0.3), halign="center", valign="middle")
        self.question_label.bind(size=self.question_label.setter("text_size"))
        self.add_widget(self.question_label)

        self.options_layout = BoxLayout(orientation="vertical", size_hint=(0.5, 0.5))
        self.add_widget(self.options_layout)

        self.score_label = Label(text=f"Puntaje: {self.score}", font_size=15, size_hint=(1, 0.1))
        self.add_widget(self.score_label)

        # Cargar la primera pregunta
        self.load_question()
        # Iniciar el temporizador
        Clock.schedule_interval(self.update_timer, 0.5)

    def load_question(self):
        """Carga la pregunta actual y las opciones."""
        self.options_layout.clear_widgets()
        question_data = questions[self.current_question]
        self.question_label.text = question_data["question"]

        for option in question_data["options"]:
            btn = Button(text=option, font_size=15, size_hint_y=None, height=75)
            btn.bind(on_press=lambda instance, opt=option: self.check_answer(opt))
            self.options_layout.add_widget(btn)

    def check_answer(self, selected_option):
        """Verifica si la respuesta seleccionada es correcta."""
        question_data = questions[self.current_question]
        if selected_option == question_data["answer"]:
            self.score += 1
            self.show_popup("¡Correcto!", "Respuesta correcta")
        else:
            self.show_popup("Incorrecto", f"La respuesta correcta era: {question_data['answer']}")

        self.next_question()

    def next_question(self):
        """Carga la siguiente pregunta o termina el juego."""
        self.current_question += 1
        self.time_left = TIME_LIMIT

        if self.current_question < len(questions):
            self.load_question()
        else:
            self.end_game()

    def update_timer(self, dt):
        """Actualiza el temporizador de la pregunta."""
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.text = f"Tiempo restante: {self.time_left} s"
        else:
            self.show_popup("¡Tiempo agotado!", "Se acabó el tiempo.")
            self.next_question()

    def show_popup(self, title, message):
        """Muestra un mensaje emergente."""
        popup = Popup(title=title, content=Label(text=message, font_size=15), size_hint=(0.8, 0.4))
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1)

    def end_game(self):
        """Muestra el puntaje final y cierra el juego."""
        popup = Popup(title="Fin del juego",
                      content=Label(text=f"Tu puntuación final es: {self.score}/{len(questions)}", font_size=18),
                      size_hint=(0.8, 0.4))
        popup.open()
        Clock.schedule_once(lambda dt: App.get_running_app().stop(), 4)


class TriviaApp(App):
    def build(self):
        return TriviaGame()


if __name__ == "__main__":
    TriviaApp().run()