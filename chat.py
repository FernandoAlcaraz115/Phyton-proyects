import tkinter as tk
from tkinter import scrolledtext, ttk
import datetime
import random
import operator
import re
from typing import Optional, Tuple, Dict, Callable, List

class ChatbotApp:
    """A simple chatbot application using Tkinter."""

    # Mathematical operations
    OPERATIONS: Dict[str, Callable[[float, float], float]] = {
        '**': operator.pow,
        '*': operator.mul,
        '/': operator.truediv,
        '+': operator.add,
        '-': operator.sub,
    }

    # Jokes list
    JOKES: List[str] = [
        "¿Por qué los programadores confunden Halloween con Navidad? Porque OCT 31 == DEC 25.",
        "¿Qué le dice un bit al otro? Nos vemos en el bus.",
        "¿Por qué el código estaba triste? Porque tenía demasiados bugs.",
        "¿Cómo se despiden los químicos? Ácido un placer.",
        "¿Qué hace una abeja en el gimnasio? ¡Zum-ba!"
    ]

    # Facts list
    FACTS: List[str] = [
        "¿Sabías que los pulpos tienen tres corazones?",
        "Un día en Venus dura más que un año en Venus.",
        "Los tiburones existen desde antes que los árboles.",
        "Las abejas pueden reconocer rostros humanos.",
        "El corazón de una ballena azul puede pesar más de 180 kg."
    ]

    # Common typos correction
    CORRECTIONS: Dict[str, str] = {
        "grasias": "gracias",
        "ora": "hora",
        "fechaa": "fecha",
        "holaa": "hola",
        "chistee": "chiste",
        "operasion": "operación",
        "resutado": "resultado",
        "cuanto": "cuánto",
        "comoo": "cómo"
    }

    def __init__(self, root: tk.Tk):
        """
        Initialize the Chatbot application.
        
        Args:
            root (tk.Tk): The root window.
        """
        self.root = root
        self.setup_ui()
        self.greet_user()

    def setup_ui(self):
        """Set up the user interface."""
        self.root.title("Chatbot Pro")
        self.root.geometry("600x500")
        self.root.configure(bg="#1e1e1e")

        # Configure styles
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", 
                        font=("Segoe UI", 10, "bold"), 
                        background="#007acc", 
                        foreground="white", 
                        borderwidth=0)
        style.map("TButton", 
                  background=[('active', '#005f9e')])

        # Chat area
        self.chat_area = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            state=tk.DISABLED, 
            font=("Segoe UI", 11), 
            bg="#252526", 
            fg="#d4d4d4",
            insertbackground="white",
            borderwidth=0,
            highlightthickness=0
        )
        self.chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Tag configuration for coloring messages
        self.chat_area.tag_config("user", foreground="#569cd6") # Blue-ish for user
        self.chat_area.tag_config("bot", foreground="#ce9178")  # Orange-ish for bot

        # Input frame
        frame_input = tk.Frame(self.root, bg="#1e1e1e")
        frame_input.pack(pady=(0, 15), fill=tk.X, padx=15)

        # Entry field
        self.entry_field = tk.Entry(
            frame_input, 
            font=("Segoe UI", 11), 
            bg="#3c3c3c", 
            fg="#ffffff", 
            insertbackground="white",
            relief=tk.FLAT,
            bd=5
        )
        self.entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.entry_field.bind("<Return>", lambda event: self.process_input())

        # Send button
        btn_send = ttk.Button(frame_input, text="Enviar", command=self.process_input)
        btn_send.pack(side=tk.RIGHT)

        # Clear button
        btn_clear = ttk.Button(self.root, text="Limpiar Chat", command=self.clear_chat)
        btn_clear.pack(pady=(0, 10))

    def greet_user(self):
        """Display the initial greeting message."""
        self.add_message("Bot: 🤖 Chatbot Pro listo. Puedes pedirme la hora, fecha, operaciones, un chiste o un dato curioso.\nTambién puedo responder si me dices cómo te sientes.", "bot")

    def add_message(self, message: str, tag: str = None):
        """
        Add a message to the chat area.

        Args:
            message (str): The message to display.
            tag (str, optional): The tag to apply for styling (e.g., 'user', 'bot').
        """
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, message + "\n", tag)
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def clear_chat(self):
        """Clear the chat area."""
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def correct_errors(self, text: str) -> str:
        """Correct common typos in the text."""
        words = text.split()
        corrected = [self.CORRECTIONS.get(word, word) for word in words]
        return ' '.join(corrected)

    def clean_text(self, text: str) -> str:
        """Clean and normalize the input text."""
        text = text.lower().strip()
        text = self.correct_errors(text)
        text = re.sub(r'[¿?¡!.,;:]', '', text)
        return text

    def get_time(self) -> str:
        """Get the current time."""
        now = datetime.datetime.now()
        return f"La hora actual es {now.strftime('%H:%M:%S')}."

    def get_date(self) -> str:
        """Get the current date."""
        today = datetime.date.today()
        return f"La fecha de hoy es {today.strftime('%d/%m/%Y')}."

    def tell_joke(self) -> str:
        """Return a random joke."""
        return random.choice(self.JOKES)

    def random_fact(self) -> str:
        """Return a random fact."""
        return random.choice(self.FACTS)

    def find_operation(self, text: str) -> Tuple[Optional[float], Optional[str]]:
        """
        Find and execute a mathematical operation in the text.

        Returns:
            Tuple[Optional[float], Optional[str]]: The result and the operation string, or (None, None).
        """
        for symbol in sorted(self.OPERATIONS, key=len, reverse=True):
            # Regex to find numbers and operator
            pattern = rf'(-?\d+(?:\.\d+)?)\s*{re.escape(symbol)}\s*(-?\d+(?:\.\d+)?)'
            match = re.search(pattern, text)
            if match:
                try:
                    a, b = float(match.group(1)), float(match.group(2))
                    result = self.OPERATIONS[symbol](a, b)
                    return result, f"{a} {symbol} {b}"
                except ZeroDivisionError:
                    return None, "división por cero"
                except Exception:
                    return None, "error desconocido"
        return None, None

    def respond_emotion(self, text: str) -> Optional[str]:
        """Respond to emotional keywords."""
        if any(word in text for word in ["estoy bien", "todo bien", "muy bien"]):
            return "¡Qué gusto que te encuentres bien! 😊 Puedes pedirme la hora, la fecha, una operación o un chiste."
        elif any(word in text for word in ["estoy mal", "muy mal", "me siento mal", "triste"]):
            return "Lamento que te sientas así 😢. Si quieres distraerte, puedo contarte un chiste o decirte la hora."
        elif any(word in text for word in ["más o menos", "mas o menos", "normal", "ahí voy"]):
            return "Entiendo, a veces hay días así. Si necesitas algo, ¡estoy aquí para ayudarte!"
        return None

    def convert_units(self, text: str) -> Optional[str]:
        """Convert units found in the text."""
        match = re.search(r'(\d+\.?\d*)\s*(km|kilometros|celsius|°c|kg)', text)
        if match:
            amount = float(match.group(1))
            unit = match.group(2)
            if unit in ["km", "kilometros"]:
                miles = round(amount * 0.621371, 2)
                return f"{amount} kilómetros son aproximadamente {miles} millas."
            elif unit in ["celsius", "°c"]:
                fahrenheit = round(amount * 9/5 + 32, 2)
                return f"{amount}°C son aproximadamente {fahrenheit}°F."
            elif unit == "kg":
                pounds = round(amount * 2.20462, 2)
                return f"{amount} kg son aproximadamente {pounds} libras."
        return None

    def respond_faq(self, text: str) -> Optional[str]:
        """Respond to frequently asked questions."""
        if "quien eres" in text:
            return "Soy un chatbot en Python, diseñado para ayudarte y entretenerte. 😎"
        if "que puedes hacer" in text:
            return "Puedo darte la hora, fecha, contar chistes, hacer operaciones, decirte un dato curioso y convertir unidades. ¡Pruébame!"
        if "eres inteligente" in text:
            return "¡Estoy aprendiendo más cada día! 🤖"
        if "cumpleaños" in text:
            return "¡Feliz cumpleaños! 🎉 Espero que tengas un día increíble."
        return None

    def process_input(self):
        """Process the user input and generate a response."""
        user_text = self.entry_field.get()
        self.entry_field.delete(0, tk.END)
        
        if not user_text.strip():
            return

        self.add_message(f"Tú: {user_text}", "user")
        clean_text = self.clean_text(user_text)

        if clean_text in ["salir", "adios", "me voy"]:
            self.add_message("Bot: ¡Hasta pronto! 👋", "bot")
            self.root.after(1000, self.root.quit)
            return

        # Check for various response types
        response = self.respond_emotion(clean_text)
        if response:
            self.add_message(f"Bot: {response}", "bot")
            return

        response = self.respond_faq(clean_text)
        if response:
            self.add_message(f"Bot: {response}", "bot")
            return

        response = self.convert_units(clean_text)
        if response:
            self.add_message(f"Bot: {response}", "bot")
            return

        if any(p in clean_text for p in ["dato curioso", "sorprendeme", "cuentame algo", "curioso"]):
            self.add_message(f"Bot: {self.random_fact()}", "bot")
            return

        if "hora" in clean_text:
            self.add_message(f"Bot: {self.get_time()}", "bot")
        elif "fecha" in clean_text or "dia" in clean_text:
            self.add_message(f"Bot: {self.get_date()}", "bot")
        elif "chiste" in clean_text or "broma" in clean_text:
            self.add_message(f"Bot: {self.tell_joke()}", "bot")
        elif any(p in clean_text for p in ["hola", "buenas", "saludos", "hey"]):
            self.add_message("Bot: ¡Hola! ¿Cómo estás?", "bot")
        elif "gracias" in clean_text:
            self.add_message("Bot: ¡Con gusto!", "bot")
        elif "como estas" in clean_text:
            self.add_message("Bot: Estoy excelente, gracias por preguntar. ¿Y tú cómo estás?", "bot")
        elif any(op in clean_text for op in self.OPERATIONS) or "resultado" in clean_text or "cuanto es" in clean_text or "calcula" in clean_text:
            result, operation = self.find_operation(clean_text)
            if result is not None:
                self.add_message(f"Bot: El resultado de {operation} es {result}", "bot")
            elif operation == "división por cero":
                self.add_message("Bot: No puedo dividir por cero. 💥", "bot")
            else:
                self.add_message("Bot: No entendí la operación. Intenta con algo como 'dame el resultado de 5 + 3'", "bot")
        else:
            self.add_message("Bot: No entendí eso. Puedes pedirme la hora, la fecha, una operación, un chiste o un dato curioso.", "bot")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()