'''
bu class aramayi yaptiktan sonra cikan sonuclar arasinda
filtreleme yapan instance metodlar icerir
'''
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingFiltration:
    def __init__(self, driver:WebDriver):
        self.driver = driver

    def apply_star_rating(self, *star_values):
        star_filtration_box = self.driver.find_element(By.ID,"filter_group_class_:R14q:")
        star_child_elements = star_filtration_box.find_elements(By.CSS_SELECTOR, "*")
        for star_value in star_values:
            for star_element in star_child_elements:
                if str(star_element.get_attribute('innerHTML')).strip() == f'{star_value} yıldız':
                    star_element.click()

    def sort_lowest_first(self):
        WebDriverWait(self.driver,30).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR,".ba1f26500a.a18ca6a206.abea3a9d71.c8b48968a2")
            )
        ) #yukaridaki css selecterundeki element, butona tiklamama engel olan bir hata veriyordu.
        # element ... not clickable because ... obscures it. seklinde
        #expected_conditions ile once o elementin gorunmez olmasini bekliyorum.

        WebDriverWait(self.driver,20).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-selected-sorter]')
            )
        ).click()  #ardindan istedigim elementin gorunur olmasini bekliyorum. ve tikliyorum.

        '''
        time.sleep(1) #eski kod
        filter_button = self.driver.find_element(By.CSS_SELECTOR, '[data-selected-sorter]')
        filter_button.click()
        #^^^^^^ eski calismayan versiyon ^^^^^^
        '''
        price_opt = self.driver.find_element(By.CSS_SELECTOR, 'button[data-id="price"]')
        price_opt.click()






'''
tek yıldızla gösterilen *args ve çift yıldızla gösterilen **kwargs

eğer bir veriden kaç tane gireceğimizi bilmiyorsak, o zaman *args kullanırız.
örneğin apply_star_rating fonksiyonunda, birden fazla yıldız sayısı girmek istiyorsak
bunu *star_value olarak tanımlarız. bu star_value adında bir array oluşturur, ve
kaç adet değer girersek onun içerisine o kadar atar

**kwargs ise daha komplextir. **kwargs yani key valued arguments
bu şekilde bir tanımlama yaparsak bu bir dictionary oluşturur. fonksiyonun içerisine
generic olarak dictionary parametreleri tanımlamamızı sağlar

    class smth
        def __init__(self, **kwargs):
            self.param = kwargs.get('param') # bu kod mesela param adindaki parametreyi  dict olarak alir ve
                                             # eger burada param adinda bir parametre tanimlanmissa onu dict olarak koyar
                                             # tanimlanmamissa o zaman None dondurur. Bu kwargs yapisina baska seyler de 
                                             # ekleyebilirsin ve bu tanimli olmak zorunda degil. ornegin 
                                             # smth(param=5, param2='another') seklinde
'''