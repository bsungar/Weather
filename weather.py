from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv

class WeatherData:
    def __init__(self, date, temperature, weather, humidity):
        self.date = date
        self.temperature = temperature
        self.weather = weather
        self.humidity = humidity
 
 
class FileHandler:
       
    def read_input_file(self, file_path, city):
        with open(file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if row[1].lower() == city.lower():
                    return row[2]
    
        
 
    def write_final_output(self, city, district, weather_data_list, filepath):
        with open(filepath, 'a', encoding='utf-8') as file:
            for weather_data in weather_data_list:
                pm_value = self.read_input_file('pm.txt', city)
                file.write(
                        f"{city.capitalize()},{district.capitalize()},{weather_data.date},{weather_data.temperature},{weather_data.weather},{weather_data.humidity},{pm_value}\n")
                
 
   
    def write_output_file(self, file_path, weather_data_list, city, district):
        with open(file_path, "a", encoding="utf-8") as file:
            for weather_data in weather_data_list:
                file.write(
                    f"{city.capitalize()},{district.capitalize()},{weather_data.date},{weather_data.temperature},{weather_data.weather},{weather_data.humidity}\n")
 
#Bu sınıf, hava durumu verilerini temsil eden bir veri yapısı oluşturuyor. İlgili tarih, sıcaklık, hava durumu ve nem değerlerini saklar. 
class WeatherApp:
    def __init__(self):
        self.weather_data_list = []
 
#get_weather_data metodu, belirtilen bir şehir ve ilçe için hava durumu verilerini çekmek için kullanılır. 
#Bu metod, selenium kütüphanesini kullanarak hava durumu web sitesine bağlanır, verileri çeker ve WeatherData nesneleri oluşturur.
    def get_weather_data(self, city, district):
        browser_profile = Options()
        browser = webdriver.Chrome(options=browser_profile)
 
        try:
            url = f"https://www.mgm.gov.tr/tahmin/il-ve-ilceler.aspx?il={city}&ilce={district}"
            browser.get(url)
 
            kaynak = browser.page_source
            soup = BeautifulSoup(kaynak, "html.parser")
            anlikDurumTarih = soup.find("span", {"class": "ad_time ng-binding"})
            anlikDerece = soup.find("div", {"class": "anlik-sicaklik-deger ng-binding"})
            if anlikDerece is not None:
                anlikDerece = anlikDerece.text.replace(",", ".")
 
            anlikHava = soup.find("div", {"class": "anlik-sicaklik-havadurumu-ikonismi ng-binding"})
            anlikNem = soup.find("div", {"class": "anlik-nem-deger-kac ng-binding"})
 
            weather_data = WeatherData(anlikDurumTarih.text, anlikDerece, anlikHava.text, anlikNem.text)
            self.weather_data_list.append(weather_data)
 
        finally:
            browser.quit()
 
    def display_weather_data(self):
        print("Hava Durumu Bilgileri:")
        print("-----------------------")
 
        for weather_data in self.weather_data_list:
            print(f"Tarih: {weather_data.date}")
            print(f"Sıcaklık: {weather_data.temperature}°C")
            print(f"Hava: {weather_data.weather}")
            print(f"Nem: %{weather_data.humidity}")
            print("-----------------------")
 
 
if __name__ == "__main__":
    city = input("İl: ").lower().capitalize()
    district = input("İlçe: ").lower().capitalize()
 
    app = WeatherApp()
 
    app.get_weather_data(city, district)
 
    app.display_weather_data()
 
    file_handler = FileHandler()
 
    file_handler.write_output_file("output.txt", app.weather_data_list, city, district)
    file_handler.write_final_output(city, district, app.weather_data_list, "final_output.txt")
 
 
 
# bu method ile csv dosyasını txt ye çevirdim 
with open("PM10.csv", 'r',encoding="utf-8") as csvdosya, open("pm.txt", 'w',encoding="utf-8") as txtdosya:
    csv_okuyucu = csv.reader(csvdosya)
    next(csv_okuyucu)  
 
    for satir in csv_okuyucu:
        txtdosya.write(','.join(satir) + '\n')
 
print("Seçtiğiniz ilin PM değerini öğrenmek için, 'final_output.txt' dosyasının son elemanına bakın.")