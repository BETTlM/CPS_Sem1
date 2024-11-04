import flet
import os
import pygame
import pdfminer.high_level as pdfminer
from modules import writer, audiorecorder
import time

class AudioConverterApp:
    def __init__(self, page: flet.Page):
        self.page = page
        self.page.title = "Audio Converter App"
        self.page.window_width = 1600
        self.page.window_height = 900
        self.page.window_full_screen = True
        self.page.theme_mode = flet.ThemeMode.DARK
        self.page.horizontal_alignment = flet.CrossAxisAlignment.CENTER
        self.page.scroll = flet.ScrollMode.ALWAYS
        self.page.padding = flet.padding.all(20)
        
        pygame.init()
        self.loc = ''

        primary_color = "#3A7CA5"
        accent_color = "#FFD700"
        text_color = "#FFFFFF"
        
        self.login_card = flet.Card(
            content=flet.Container(
                content=flet.Column(
                    [
                        flet.Text("Audio Converter App", size=24, color=accent_color, weight=flet.FontWeight.BOLD),
                        flet.TextField(label="Username", width=300),
                        flet.TextField(label="Password", password=True, can_reveal_password=True, width=300),
                        flet.ElevatedButton(
                            "Login",
                            on_click=self.login,
                            bgcolor=primary_color,
                            color=text_color,
                            expand=True,
                        ),
                    ],
                    alignment=flet.MainAxisAlignment.CENTER,
                    horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=20,
                border_radius=10,
                bgcolor="#1E1E1E",
                animation=flet.Animation(500, flet.AnimationCurve.EASE_IN_OUT),
                shadow=flet.BoxShadow(spread_radius=5, blur_radius=15, color="#00000030"),
            )
        )

        self.upload_button = flet.ElevatedButton(
            "Upload PDF", on_click=self.upload_pdf, bgcolor=primary_color, color=text_color, visible=False
        )
        self.convert_button = flet.ElevatedButton(
            "Convert PDF to Audio", on_click=self.convert_to_audio, bgcolor=primary_color, color=text_color, visible=False
        )
        self.play_button = flet.ElevatedButton(
            "Play Audio", on_click=self.play_audio, bgcolor=primary_color, color=text_color, visible=False
        )

        self.page.add(
            flet.Column(
                [
                    self.login_card,
                    flet.Container(content=self.upload_button, animate_opacity=300),
                    flet.Container(content=self.convert_button, animate_opacity=300),
                    flet.Container(content=self.play_button, animate_opacity=300),
                ],
                alignment=flet.MainAxisAlignment.CENTER,
                horizontal_alignment=flet.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )

    def login(self, e):
        username = self.login_card.content.controls[1].value
        password = self.login_card.content.controls[2].value

        if username == "bettim" and password == "1":
            self.show_buttons()
        else:
            self.page.dialog = flet.AlertDialog(
                title=flet.Text("Login Failed"),
                content=flet.Text("Invalid username or password"),
            )
            self.page.update()

    def show_buttons(self):
        self.upload_button.visible = True
        self.convert_button.visible = True
        self.play_button.visible = True
        self.login_card.content.opacity = 0
        self.page.update()

    def upload_pdf(self, e):
        file_picker = flet.FilePicker(
            on_result=self.on_pdf_selected,
            allow_multiple=False,
            file_type="file",
            allowed_extensions=["pdf"]
        )
        self.page.overlay.append(file_picker)
        file_picker.pick_file()
        self.page.update()

    def on_pdf_selected(self, e):
        if e.files:
            self.loc = e.files[0].path
            file_name = os.path.basename(self.loc)
            self.page.dialog = flet.AlertDialog(
                title=flet.Text("File Uploaded"),
                content=flet.Text(f"PDF file '{file_name}' uploaded successfully."),
            )
            self.page.update()

    def convert_to_audio(self, e):
        try:
            content = pdfminer.extract_text(self.loc)
            writer.writenow(content)
            audiorecorder.record('/home/bettim/Documents/Kishoore/book.txt', '/home/bettim/Documents/Kishoore/recordedaudio.mp3')
            time.sleep(4)
            self.page.dialog = flet.AlertDialog(
                title=flet.Text("Audio Converted"),
                content=flet.Text("Audio can be played now."),
            )
            self.page.update()
        except Exception as error:
            self.page.dialog = flet.AlertDialog(
                title=flet.Text("Conversion Error"),
                content=flet.Text(f"An error occurred: {error}"),
            )
            self.page.update()

    def play_audio(self, e):
        audio_file = "/home/bettim/Documents/Kishoore/recordedaudio.mp3"
        if os.path.exists(audio_file):
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        else:
            self.page.dialog = flet.AlertDialog(
                title=flet.Text("File Not Found"),
                content=flet.Text("Please convert a PDF to audio first."),
            )
            self.page.update()

def main(page: flet.Page):
    AudioConverterApp(page)

flet.app(target=main)
