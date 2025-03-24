from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import requests

class Weather(QWidget):
    def __init__(self):
        super().__init__() 
        
        self.label = QLabel("Weather updates for your preferred location",self)
        self.line_edit =QLineEdit(self)
        self.line_edit.setPlaceholderText("Enter the City name")
        self.btn = QPushButton("Get Weather",self)
        self.temp_label = QLabel("",self)
        self.emoji =QLabel("",self)
        self.description = QLabel("",self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.btn.setFocus()
        self.btn.setFixedWidth(500)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.line_edit)
        vbox.addWidget(self.btn,alignment=Qt.AlignHCenter)
        vbox.addWidget(self.temp_label)
        vbox.addWidget(self.emoji)
        vbox.addWidget(self.description)
        self.setLayout(vbox)

        self.label.setAlignment(Qt.AlignCenter)
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.temp_label.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.description.setAlignment(Qt.AlignCenter)

        self.label.setObjectName("label")
        self.line_edit.setObjectName("line_edit")
        self.btn.setObjectName("btn")
        self.temp_label.setObjectName("temp_label")
        self.emoji.setObjectName("emoji")
        self.description.setObjectName("description")

        self.setStyleSheet("""
            QLabel ,QPushButton {
                font : Calibri;
                font-size :35px;
                margin : 20px;
            }
            QLineEdit{
                font-size : 30px;
                margin: 20px 80px 20px 80px;
                padding : 9px ;
                border : 2px solid  ;
                border-radius : 25px ;
            }
            QLabel#label{
                color : #0532fc;
                margin : 20px 20px 9px 20px ;
                font-weight : bold ;
            }
            QPushButton#btn {
                font-size : 30px ;
                margin : 0px 90px 0px 90px ;
                border : 2px solid ;
                border-radius : 25px ;
                padding : 9px  ;
                background-color : hsl(44, 2%, 27%) ;
                color : white;
                font-weight : bold;
            }
            QPushButton#btn:hover {
                 background-color : hsl(44, 2%, 37%) ;
            }
            QLabel#temp_label{
                font-size : 40px ;
                color :hsl(229, 99.20%, 50.20%);
            }
            QLabel#emoji{
                font-size : 65px ;
                font-weight : Segoe UI Emoji;
                }
            QLabel#description{
                font-size : 50px;
                color :hsl(229, 99.20%, 50.20%);
            }

        """)
        self.btn.clicked.connect(self.get_weather)
        

    def get_weather(self):
        api_key = "555613ac07b9f14b06f202859c57b4b5"
        city=self.line_edit.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try :
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200 :
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code :
                case 400 :
                    self.display_error("Bad Request :\n  Please check your input city")
                case 401 :
                    self.display_error("Unauthorised :\n    Please check your API key")
                case 403:
                    self.display_error("Forbidden :\n    Access is denied")
                case 404 :
                    self.display_error("Not found :\n    City does not found")
                case 500 :
                    self.display_error("Internal Server Error :\n    Please try again later")
                case 502 :
                    self.display_error("Bad Gateway\n    Invalid response from server")
                case 503 :
                    self.display_error("Service Unavailable\n    Server is down, try again later")
                case 504 :
                    self.display_error("Gateway timeout\n    No response from server")
                case _ :
                    self.display_error(f"Oops something went wrong\n  {http_error}")
                
                    
        
        except requests.exceptions.ConnectionError :
            self.display_error("Connection error :\n   Check your internet connection")
        except requests.exceptions.Timeout :            
            self.display_error("Timeout error :\n   Time for your request is complete")
        except requests.exceptions.TooManyRedirects :
            self.display_error("Too many redirects :\n   Please check the URL")
        except requests.exceptions.RequestException as req_error :
            self.display_error(f"Request error :\n   {req_error}")

    def display_error (self,msg):
        self.emoji.setStyleSheet("font-size : 40px;" "color : #fc0505;" "font-weight : bold;")
        self.temp_label.clear()
        self.description.clear()
        self.emoji.setText(msg)

    def display_weather(self,data):
        temperature = data["main"]["temp"]
        temperature_c =temperature -273.15
        humidity = data["main"]["humidity"]
        weather_id = data["weather"][0]["id"]
        self.temp_label.setText(f" Temperature : {temperature_c:.01f}°C\n Humidity : {humidity:.01f}%")
        set_emoji = self.weather_emoji(weather_id)
        self.emoji.setText(set_emoji)
        description_weather = data["weather"][0]["description"]
        self.description.setText(description_weather)

    @staticmethod
    def weather_emoji(weather_id):
        if 200 <= weather_id <=232 :
            return "⛈⛈" #thunder strom
        elif 300 <= weather_id <=321 :
            return "🌤🌤" #partial clouds
        elif 500 <= weather_id <=531 :
            return "🌧🌧" #rain
        elif 600 <= weather_id <=622 :
            return "🌨❄🌨" #snow
        elif 701 <= weather_id <= 741:
            return "🌫️༄" #fog
        elif  weather_id ==762 :
            return "🌋" #ash
        elif weather_id == 771 :
            return "🎐🌫" #violent wind
        elif weather_id== 781 :
            return "🌪" #tornado
        elif weather_id ==800 :
            return "🔆🔆" #sunny
        elif 801 <= weather_id <=804 :
            return "🌥🌥" #clouds
        else :
            return ""



       
app = QApplication([])
weather = Weather()
weather.show()
app.exec_() 
