import time

from booking.booking import Booking
import pandas as pd

'''
context managerlar, with gibi, programin sadece o contextte calismasini saglar.
 Bu, tum kodun bir anda degil de, parcalar halinde calismasini saglar.
 bazi seylerin isi bittiginde, o seyleri kapatmak gibi. ornegin burada
 booking clasini calistiriyoruz. bu clas browseri calistiriyor, isi 
 bittiginde de browseri kapatmasini __exit__ magic metodu soyler.
 biz onu teardown diye bir degiskenle simdilik false yaptik. ileride 
 kapanmasini istersek true yapariz.
'''

inputs = pd.read_excel('./info.xlsx', engine='openpyxl')

with Booking() as bot:
    bot.land_first_page()
    try:
        bot.close_popup()
    except:
        pass

    '''
    try:
        bot.close_google_popup()
    except Exception as e:
        print(e)
        pass
    '''
    # bot.change_currency(currency='GBP')
    try:
        bot.close_google_popup()
    except Exception as e:
        print(e)
        pass
    bot.select_place_to_go(f'{str(inputs["Where-to"][0])}')

    bot.select_dates(check_in=str(f'{inputs["Date-from"][0].strftime("%Y-%m-%d")}'), check_out=str(f'{inputs["Date-to"][0].strftime("%Y-%m-%d")}'))
    bot.select_adults(int(inputs['Adults'][0]))
    bot.click_search_button()
    bot.apply_filtration()
    bot.refresh() # robot bi kendini yenilesin ki sonuc duzgun ciksin.
    time.sleep(3)
    bot.report_results()
