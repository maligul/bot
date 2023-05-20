from selenium import webdriver
from selenium.webdriver.common.by import By
import booking.constants as const
import time
from selenium.webdriver.common.action_chains import ActionChains
from booking.booking_filtration import BookingFiltration
from booking.booking_report import BookingReport
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
class Booking(webdriver.Firefox):
    def __init__(self,
                 teardown=False):  # cift alt tire ile baslayan metodlar magic metoddur. init metodu, program calismaya baslamadan yapilmasi gerekenleri yapar.
        super(Booking,
              self).__init__()  # super ile ust classa gidersin, webdriver i init ile alirsin programin basina eklersin
        self.teardown = teardown  # bu init metodu baslangicta yapilacaklari yapar. sayfayi ac, webdriveri al, biraz bekle. pencereyi buyut.
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()  # teardown yani isi bittiginde kapat demek. main dosyasinda 'with' context manageri icin olusmus bir magic method. isin bitince pencereyi kapat diyoruz.

    def land_first_page(self):
        self.get(const.BASE_URL)
        time.sleep(0.5)

    def change_currency(self, currency=None):
        currency_element = self.find_element(By.CSS_SELECTOR, 'span[class="e57ffa4eb5"]')
        currency_element.click()
        selected_currency_element = self.find_element(By.XPATH, (f"//div[contains(text(),'{currency}')]")
                                                      )  # xpathde contains metodu varmis. videoda id ile buluyordu. biz diyoruz ki usd veya gbp iceren seyi bul.
        selected_currency_element.click()  # ve ona tikla

    def close_popup(self):
        self.implicitly_wait(1)
        close_button = self.find_element(By.CSS_SELECTOR, 'button[aria-label="Giriş bilgisini kapat."]')
        close_button.click()
        # bunu ben yazdim bazen giris yap diye bir popup cikiyor onu kapatmak icin

    def select_place_to_go(self, place_to_go):
        search_field = WebDriverWait(self,20).until(EC.presence_of_element_located((By.ID,':Ra9:' )))
        #search_field = self.find_element(By.ID, ':Ra9:')
        search_field.clear()
        search_field.send_keys(place_to_go)
        WebDriverWait(self,20).until(EC.presence_of_element_located((By.XPATH, f"//div[contains(text(),'{place_to_go}')]"))).click()
        #alttaki iki satir eski versiyon, altta newyork butonu gorunmuyor diye sleep yapmistim
        #fakat Expected Conditions ile daha mantikli bir yaklasim oldu
        #webdriverwait(driver_objesi, max_timeout_suresi).until(EC.sart_objesi((elementi bul))).click
        #any_result_to_click = self.find_element(By.XPATH, (f"//div[contains(text(),'{place_to_go}')]"))
        #any_result_to_click.click()


    def select_dates(self, check_in, check_out):
        WebDriverWait(self,20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{check_in}"]'))).click()
        #alttaki iki satiri takvim gorunmesi kosuluna bagli olarak calissin diye ustteki koda cevirdim.
        #check_in_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_in}"]')
        #check_in_element.click()
        check_out_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{check_out}"]')
        check_out_element.click()

    def select_adults(self, count=1):
        selection_element = self.find_element(By.XPATH, ("//button[contains(text(),'yetişkin')]"))
        selection_element.click()
        while True:
            minus_button = self.find_element(By.CSS_SELECTOR, 'button.e1b7cfea84:nth-child(1)')
            minus_button.click()
            # yetiskin sayisi bir oluncaya kadar minus buttona basma loopu
            # id olan deger input elementiydi. onun icerisinde value attribute u var
            # yani soyle bir sey: <input id='group_adults' value = '1'> <diger seyler> </input>
            adults_value_element = self.find_element(By.ID, 'group_adults')
            adults_count = adults_value_element.get_attribute(
                'value'
            )  # bu bize yetiskin adedini verir
            if int(adults_count) == 1:
                break  # yetiskin adedini once 1 e esitliyoruz. 1 olunca looptan cikiyor.

        plus_button = self.find_element(By.CSS_SELECTOR,
                                        'div.b2b5147b20:nth-child(1) > div:nth-child(3) > button:nth-child(3)')
        # plus button kismi ve minus button mozilla nin selectorunden alindi.
        for _ in range(count - 1):
            plus_button.click()
            # alt tire (_) isareti i indexini kullanmayacagimiz yerlerde olur.
            # count degiskeni fonksiyona tanimlanan degiskendir.

    def click_search_button(self):
        search_button = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_button.click()

    def close_google_popup(self):
        time.sleep(1) #popup yuklensin diye
        self.switch_to.frame(self.find_element(By.TAG_NAME, 'iframe'))
        # burada iframe diye bir elementin
        # icerisinde ayri bir HTML vardi.
        #  #document diye basliyordu.
        #switch_to metodu iframe deki html yapisini almaya yariyor
        close_btn = self.find_element(By.ID, "close")
        #switch_to metidundan sonra id ile close butona rahatca ulastim
        close_btn.click()
        self.switch_to.default_content()
        #isimiz bitince popup icindeki html den ana html yapisi
        #icin tekrar switch_to fonksiyonunu kullaniyoruz.

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4,5)
        try:
            filtration.sort_lowest_first() #calismiyo
        except Exception as excp:
            print(excp)
            pass

    def report_results(self):
            result_list = self.find_element(By.ID,"search_results_table")
            report = BookingReport(result_list)
            print(report.pull_hotel_info)
            df_hotel_info = pd.DataFrame(report.pull_hotel_info, columns=['Hotel Name','Hotel Price','Hotel Point'])
            print(df_hotel_info)
            df_hotel_info.to_csv("./results/"+datetime.today().strftime('%d %m %Y') + ".csv", index=False)

