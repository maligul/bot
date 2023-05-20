# arama sonucu oldugunda her kutunun icerisini gormek icin
# metotlar icerir
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.remote.webdriver import WebDriver
import pandas as pd

class BookingReport:
    def __init__(self, boxes_section_element: WebElement):

        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()
        #self.driver = driver
        '''
        boxes_section_element booking.py dosyasinda calisan
        report_results fonksiyonunun icinde, orada sonuclarin 
        listelendigi buyuk div elementini bulup
        BookingReport classina parametre olarak veriyor.
        burada init icerisinde boxes_section_element:WebElement sadece
        format bildirir icerisine biz result_list koydugumuzda o
        degeri alip buraya koyuyor. deal_boxes ise div elementinin
        icindeki her bir otel. onu asagida tanimladik. burada
        initiate olsun, baslarken calissin diye burada init fonksiyonunda
        construct ettik. yani baslarken once booking.py dan 
        result_list i boxes_section_element olarak aliyor. ardindan
        ordan her bir kutucugu asagidaki fonksiyonu cagirarak
        cekiyor.
        '''


    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(
            By.CSS_SELECTOR,".a826ba81c4.fa2f36ad22.afd256fc79.d08f526e0d.ed11e24d01.ef9845d4b3.da89aeb942"
        )


    @property
    def pull_hotel_info(self):
        collection = []
        for deal_box in self.deal_boxes:

            #burasi calismadi bir sure, try-except yapisi sebebi, bazi otellerde puan olmuyor ve bu sorun yapiyordu. o sebebple puani olmayanlari boyle yaptim

            hotel_name = deal_box.find_element(
                By.CSS_SELECTOR,".fcab3ed991.a23c043802"
            ).get_attribute('innerHTML').strip()

            hotel_price = deal_box.find_element(
                By.CSS_SELECTOR,".fcab3ed991.fbd1d3018c.e729ed5ab6"
            ).get_attribute('innerHTML').strip().replace("&nbsp;"," ")
            try:
                Hotel_point = deal_box.find_element(
                    By.CSS_SELECTOR,'div[aria-label^="Puanı"]'
                ).get_attribute('innerHTML').strip()

            except:
                print(f'No point data for hotel {hotel_name}')
                Hotel_point = ''
                pass
            collection.append([hotel_name, hotel_price, Hotel_point])

        return collection

    """
    hotel_point = WebDriverWait(self,20).until(
                 EC.visibility_of_element_located(
                     (By.CSS_SELECTOR,'.b5cd09854e.d10a6220b4')
                 )
             )
    """

    """
         hotel_point = WebDriverWait(self.driver,20).until(
                 EC.presence_of_element_located(
                     (By.CSS_SELECTOR,'[aria-label^="Puanı]')
                 )
             ).get_attribute('innerHTML').strip()
    """
