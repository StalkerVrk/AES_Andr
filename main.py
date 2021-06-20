from typing import Text
from kivy.lang.builder import Instruction
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
import binascii

import time
import MY_AES128


Window.size = (400, 650)

def control_key(key): #Функция для проверки работоспособности ключая
        while True:    
            for symbol in key:
                if ord(symbol) > 0xff:
                    print('Этот ключ не сработает. Попробуйте другой, используя только латинский алфавит и цифры')
                    key = ''
                    break
                print("Всё норм")                
            break

        return key



class Digt(ScreenManager):
    def InstractionText(self): #для пояснения под приветсвием
        text = ''
        path = r"C:\Users\MiNotebook\Documents\VsKod\Kursovik\Tekst\instruction.txt"
        with open(path, 'r',encoding="utf-8") as file:
            for line in file:
                text += line
        return text
    
    
      


    
    # def Toolbar_Hellow_Text(self): #меняет шрифт у тул бара
    #     text = "Шифр AES 128"
    #     text_Encoding = self.ids.Encoding.name
    #     text_inf = self.ids.Screen_Hellow.name
    #     if text_Encoding=="Encoding":
    #         text = "Screen _Encoding"
    #         print("1")
    #     elif text_inf == "Screen_Hellow":
    #         text = "Шифр AES 128"
    #         print("2")
    #     return text
    


class Main(MDApp):


    """def get_text_inputs(self): # Вытаскиваем из полей экрана Screen_Encoding
            global text_key
            global text_input
            text_input = self.root.ids.Messeg_Vvely_id.text
            text_key= self.root.ids.Key_Vvely_id.text
            text_key = text_key[0:15]
            text_key = control_key(text_key)
            
            print(text_input,"-----",text_key)

            time_before = time.time()
            crypted_data = []
            temp = []
            for byte in data:"""
    
    def get_text_inputs(self): # Вытаскиваем из полей экрана Screen_Encoding
        global text_key
        global text_ready
        global time_finish
        text_input = self.root.ids.Messeg_Vvely_id.text.encode('utf-8')
        #print("utf8", text_input)
        text_key= self.root.ids.Key_Vvely_id.text
        text_key = text_key[0:15]
        text_key = control_key(text_key)
        
        #print(text_input,"-----",text_key)

        time_before = time.time()
        crypted_data = []
        temp = []
        for byte in text_input:
            temp.append(byte)
            if len(temp) == 16:
                crypted_part = MY_AES128.encrypt(temp, text_key)
                crypted_data.extend(crypted_part)
                del temp[:]
        else:
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                crypted_part = MY_AES128.encrypt(temp, text_key)
                crypted_data.extend(crypted_part)
        #print (crypted_data)
        #print("Последний этап",bytes(crypted_data))

        text_ready = bytes(crypted_data)
        text_ready = binascii.hexlify(text_ready)
        #print("Готово",text_ready)
        time_after = time.time()
        time_finish = time_after - time_before
        #print(time_finish)
    
    def messeg_v_result_for_messege(self, otvet):  #Для записси в строку с ответом ENCODE
        otvet.text = text_ready
    
    def time_Encod(self, Time):
        
        Time.text = str(time_finish) + " секунд"
                    
    def get_shifr_inputs(self): # Вытаскиваем из полей экрана Screen_Decoding
        global text_input_shifr
        global text_key_shifr
        global time_finish2
        text_input_shifr = self.root.ids.Shifr_Vvely_id.text.encode('utf-8')
        #print("text_input_shifr",text_input_shifr )
        #print(type(text_input_shifr))
        text_input_shifr = binascii.unhexlify(text_input_shifr)
        #print(type(text_input_shifr))
        #print("bytes",text_input_shifr )
        text_key_shifr = self.root.ids.Key_Shifr_Vvely_id.text[0:15]
        text_key_shifr = control_key(text_key_shifr)
        #print(text_input_shifr,"-----",text_key_shifr)
        time_before = time.time()
        decrypted_data = []
        temp = []
        for byte in text_input_shifr:
            temp.append(byte)
            if len(temp) == 16:
                decrypted_part = MY_AES128.decrypt(temp, text_key_shifr)
                decrypted_data.extend(decrypted_part)
                del temp[:] 
        else:
            if 0 < len(temp) < 16:
                empty_spaces = 16 - len(temp)
                for i in range(empty_spaces - 1):
                    temp.append(0)
                temp.append(1)
                decrypted_part = MY_AES128.encrypt(temp, text_key_shifr)
                decrypted_data.extend(decrypted_part) 
        #print("decrypted_data",decrypted_data)
        #print(bytes(decrypted_data))
        text_input_shifr = bytes(decrypted_data)
        #print("выход",text_input_shifr)
       
        time_after = time.time()
        time_finish2 = time_after - time_before
        #print(time_finish2)
        
    
    
    def messeg_for_oshibka_Encode(self, error):        #Оповещения о работоспособности ключа при ENCODE    
        if text_key == '':
            error.text = "Этот ключ не сработает, вернитесь назад и попробуйте другой"
        else: 
            error.text = "Выполнено успешно"             

    def messeg_for_oshibka_Decode(self, error):         #Оповещения о работоспособности ключа при DECODE
        if text_key_shifr == '':
            error.text = "Этот ключ не сработает, вернитесь назад и попробуйте другой"
        else: 
            error.text = "Выполнено успешно"  

    def messeg_v_result_for_shifr(self, otvet):  #Для записси в строку с ответом DECODE
        otvet.text = text_input_shifr
    
    def time_Decod (self, Time):
        Time.text = str(time_finish2) + " секунд"
    
    def build(self):
        Builder.load_file("digital.kv")
        return Digt()
    def on_start(self):
        self.fps_monitor_start()
    
Main().run()