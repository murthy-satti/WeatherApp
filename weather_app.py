from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout
)
from PyQt5.QtCore import Qt, QDateTime, QTimer
import requests
from datetime import datetime


class Weather(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("Weather updates for your preferred location", self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter the City name")
        self.btn = QPushButton("Get Weather", self)
        self.datetime_label = QLabel("", self)

        self.temp_label = QLabel("", self)
        self.emoji = QLabel("", self)
        self.description = QLabel("", self)
        self.extra_info = QLabel("", self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather Application")
        self.resize(600, 800)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.btn, alignment=Qt.AlignHCenter)
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(self.emoji)
        layout.addWidget(self.description)
        layout.addWidget(self.extra_info)

        self.setLayout(layout)

        for widget in [self.label, self.line_edit, self.temp_label, self.emoji, self.description, self.extra_info, self.datetime_label]:
            widget.setAlignment(Qt.AlignCenter)

        self.label.setObjectName("label")
        self.line_edit.setObjectName("line_edit")
        self.btn.setObjectName("btn")
        self.temp_label.setObjectName("temp_label")
        self.emoji.setObjectName("emoji")
        self.description.setObjectName("description")
        self.extra_info.setObjectName("extra_info")
        self.datetime_label.setObjectName("datetime_label")

        self.setStyleSheet(""" 
            QWidget {
                background-color: #0d1117;
                color: #e6edf3;
                font-family: 'Segoe UI';
            }
            QLabel#label {
                font-size: 36px;
                font-weight: bold;
                color: #58a6ff;
                margin-top: 20px;
            }
            QLineEdit#line_edit {
                font-size: 24px;
                padding: 12px;
                margin: 20px 60px;
                border-radius: 15px;
                border: 2px solid #30363d;
                background-color: #161b22;
                color: #e6edf3;
            }
            QPushButton#btn {
                font-size: 22px;
                font-weight: bold;
                background-color: #238636;
                color: #ffffff;
                padding: 10px 15px;
                border-radius: 15px;
                border: none;
            }
            QPushButton#btn:hover {
                background-color: #2ea043;
            }
            QLabel#temp_label,
            QLabel#description,
            QLabel#extra_info {
                font-size: 22px;
                margin-top: 10px;
            }
            QLabel#emoji {
                font-size: 60px;
                margin: 10px 0;
            }
            QLabel#datetime_label {
                font-size: 16px;
                color: #8b949e;
                margin-bottom: 5px;
            }
        """)

        self.btn.clicked.connect(self.get_weather)
        self.line_edit.returnPressed.connect(self.get_weather)  # Connect Enter key to the get_weather method
        self.update_time()

        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(60000)

    def update_time(self):
        current = QDateTime.currentDateTime().toString("dddd, MMMM d yyyy - hh:mm AP")
        self.datetime_label.setText(current)

    def get_weather(self):
        api_key = "555613ac07b9f14b06f202859c57b4b5"
        city = self.line_edit.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input city")
                case 401:
                    self.display_error("Unauthorized:\nPlease check your API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid server response")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down, try later")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from server")
                case _:
                    self.display_error(f"Oops! Something went wrong:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nRequest timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, msg):
        self.temp_label.clear()
        self.description.clear()
        self.extra_info.clear()
        self.emoji.setStyleSheet("font-size: 36px; color: #ff7b72; font-weight: bold;")  
        self.emoji.setText(msg)

    def display_weather(self, data):
        temperature = data["main"]["temp"] - 273.15
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_id = data["weather"][0]["id"]
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%I:%M %p")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%I:%M %p")
        description_weather = data["weather"][0]["description"].capitalize()

        self.temp_label.setText(
            f"🌡 Temp: {temperature:.1f}°C  |  💧 Humidity: {humidity:.0f}%  |  💨 Wind: {wind_speed} m/s"
        )
        self.emoji.setStyleSheet("font-size: 60px;")
        self.emoji.setText(self.weather_emoji(weather_id))
        self.description.setText(description_weather)
        self.extra_info.setText(f"🌅 Sunrise: {sunrise}   |   🌇 Sunset: {sunset}")

    @staticmethod
    def weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif  weather_id ==762 :
            return "🌋" #ash
        elif weather_id == 771 :
            return "🎐🌫" #violent wind
        elif weather_id== 781 :
            return "🌪" #tornado
        elif weather_id ==800 :
            return "🔆" #sunny
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return "🌈"

app = QApplication([])
weather = Weather()
weather.show()
app.exec_()
