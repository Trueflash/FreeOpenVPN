# -*- coding: UTF-8 -*-
from collections import OrderedDict
from tkinter.messagebox import showwarning
import tkinter.filedialog
import tkinter.ttk
import tkinter
import subprocess
import base64
import shutil
import sys
import os

from robobrowser import RoboBrowser
import PIL.ImageTk
import PIL.Image
import numpy
import png

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Browser(object):
    def __init__(self):
        self.USER_AGENT = 'Mozilla/5.0 (compatible; ABrowse 0.4; Syllable)'
        self.VPN = 'https://www.freeopenvpn.org/'

        self.browser = RoboBrowser(user_agent=self.USER_AGENT, parser='html.parser')
        self.TEMP = os.environ['TEMP']

#-------------------------------------------------------------------------------
    def captcha_address(self, address):
        self.browser.open(address)
        soup = self.browser.find_all('script')
        for script in soup:
            list_string = str(script).split('"')
            if 'adblock.php' in list_string:
                return '%slogpass/%s' % (self.VPN, list_string[1])

        return None

#-------------------------------------------------------------------------------
    def download(self, address, name):
        response = self.browser.session.get(address, stream=True)
        with open(name, 'wb') as file:
            file.write(response.content)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Captcha(object):
    def __init__(self, name):
        pngfile = png.Reader(name).read()
        self.name = name
        self.cols = pngfile[0]
        self.rows = pngfile[1]
        self.captcha = numpy.array(list(map(lambda row: list(row), list(pngfile[2]))))
        self.alpha = pngfile[3]['alpha']
        self.bitdepth = pngfile[3]['bitdepth']
        self.greyscale = pngfile[3]['greyscale']
        self.interlace = pngfile[3]['interlace']
        self.planes = pngfile[3]['planes']

#-------------------------------------------------------------------------------
    def histogram(self):
        rgb = tuple(self.captcha.ravel())
        colors = OrderedDict()

        for i in range(0, len(rgb), 3):
            try:
                key = str(rgb[i: i+3])
                colors[key] += 1
            except:
                colors.update({key: 1})

        return sorted(colors.items(), key=lambda item: item[1], reverse=True)

#-------------------------------------------------------------------------------
    def noise(self, histogram, frequence=30, exception=((255, 255, 255),)):
        colors = list()
        for color in histogram:
            if color[1] > frequence:
                color = eval(color[0])
                if color not in exception:
                    colors.append(list(color))
            else:
                return colors

#-------------------------------------------------------------------------------
    def clear(self, noise):
        for row in range(len(self.captcha)):
            for col in range(0, len(self.captcha[0]), 3):
                if list(self.captcha[row][col: col+3]) in noise:
                    self.captcha[row][col: col+3] = [255, 255, 255]

#-------------------------------------------------------------------------------
    def save(self, name):
        with open(name, 'wb') as file:
            pngfile = png.Writer(len(self.captcha[0])//3,
                                 len(self.captcha),
                                 alpha=self.alpha,
                                 bitdepth=self.bitdepth,
                                 greyscale=self.greyscale,
                                 interlace=self.interlace,
                                 planes=self.planes)

            pngfile.write(file, self.captcha)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Tesseract(Captcha):
    def __init__(self, file):
        Captcha.__init__(self, file)
        histogram = self.histogram()
        noise = self.noise(histogram)
        self.clear(noise)
        self.save(self.name)

        self.CREATE_NO_WINDOW = 0x08000000
        self.TEMP = os.environ['TEMP']
        self.password = os.path.join(self.TEMP, 'password')
        self.file = file

        try:
            self.tesseract = os.path.join(os.environ['TESSDATA_PREFIX'], 'tesseract.exe')
        except:
            self.tesseract = None

#-------------------------------------------------------------------------------
    def start(self):
        if self.tesseract:
            line = ' '.join((self.tesseract, self.file, self.password, 'digits'))
            subprocess.call(line, creationflags=self.CREATE_NO_WINDOW)
            with open(self.password + '.txt', 'rt') as file:
                password = file.read()
                return password.replace(' ', '').strip()
        else:
            return ''

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Download(Browser):
    def __init__(self, country, config, progress_bar=None):
        Browser.__init__(self)

        if country == 'Россия':
            self.country = ('ovpn/Russia_freeopenvpn_udp.ovpn',
                            'ovpn/Russia_freeopenvpn_tcp.ovpn',
                            'logpass/russia.php')
        elif country == 'Латвия':
            self.country = ('ovpn/Latvia_freeopenvpn_udp.ovpn',
                            'ovpn/Latvia_freeopenvpn_tcp.ovpn',
                            'logpass/latvia.php')
        elif country == 'США':
            self.country = ('ovpn/freeopenvpn_USA_udp.ovpn',
                            'ovpn/freeopenvpn_USA_tcp.ovpn',
                            'cf/usa.php')
        elif country == 'Германия':
            self.country = ('ovpn/Germany_freeopenvpn_udp.ovpn',
                            'ovpn/Germany_freeopenvpn_tcp.ovpn',
                            'logpass/germany.php')
        elif country == 'Швеция':
            self.country = ('ovpn/Sweden_freeopenvpn_udp.ovpn',
                            'ovpn/Sweden_freeopenvpn_tcp.ovpn',
                            'logpass/sweden.php')
        elif country == 'Нидерланды':
            self.country = ('ovpn/Netherlands_freeopenvpn_udp.ovpn',
                            'ovpn/Netherlands_freeopenvpn_tcp.ovpn',
                            'logpass/netherlands.php')
        elif country == 'Япония':
            self.country = ('ovpn/freeopenvpn_Japan_udp.ovpn',
                            'ovpn/freeopenvpn_Japan_tcp.ovpn',
                            'cf/japan.php')

        self.progress_bar = progress_bar
        self.progress_step = 25
        self.config = config

#-------------------------------------------------------------------------------
    def start(self):
        address = os.path.join(self.VPN, self.country[0])
        name = os.path.join(self.TEMP, self.country[0][5:])
        self.download(address, name)
        self.progress_bar['value'] += self.progress_step
        self.progress_bar.update()

        address = os.path.join(self.VPN, self.country[1])
        name = os.path.join(self.TEMP, self.country[1][5:])
        self.download(address, name)
        self.progress_bar['value'] += self.progress_step
        self.progress_bar.update()

        address = os.path.join(self.VPN, self.country[2])
        address = self.captcha_address(address)
        name = os.path.join(self.TEMP, 'password.png')
        if address:
            self.download(address, name)
            self.progress_bar['value'] += self.progress_step
            self.progress_bar.update()

            password = Tesseract(name).start()
            self.progress_bar['value'] += self.progress_step
            self.progress_bar.update()
            if not password:
                showwarning('Внимание', 'tesseract-ocr не установлен')

            password_window = tkinter.Toplevel()
            password_window.title('Введите пароль')
            icon = os.path.join(self.TEMP, 'freeopenvpn.ico')
            password_window.iconbitmap(icon)

            password_png = os.path.join(self.TEMP, 'password.png')
            image = PIL.ImageTk.PhotoImage(PIL.Image.open(password_png))
            tkinter.Label(password_window, image=image).grid(row=0, column=0)

            def press_ok():
                name = '.'.join((self.country[0][5:-5], 'pwd'))
                name = os.path.join(self.config, name)
                with open(name, 'wt') as file:
                    file.write('freeopenvpn\n')
                    file.write(password_entry.get())

                for i in range(2):
                    name = self.country[i][5:]
                    tmp_name = os.path.join(self.TEMP, name)
                    cfg_name = os.path.join(self.config, name)
                    tmp_file = open(tmp_name, 'rt')
                    cfg_file = open(cfg_name, 'wt')
                    name = name.replace('ovpn', 'pwd\n')
                    for line in tmp_file:
                        if line == 'auth-user-pass\n':
                            cfg_file.write(' '.join((line[:-1], name)))
                        else:
                            cfg_file.write(line)
                    tmp_file.close()
                    cfg_file.close()

                password_window.destroy()

            password_entry = tkinter.Entry(password_window, font='verdana 10', width=9)
            password_entry.grid(row=0, column=1)
            password_entry.insert(0, password)

            password_button = tkinter.ttk.Button(password_window, text = 'Ok', command=(lambda: press_ok()))
            password_button.grid(row=1, column=0, columnspan=2)

            if password:
                password_button.focus_set()
            else:
                password_entry.focus_set()

            password_window.resizable(False, False)
            password_window.focus_set()
            password_window.grab_set()
            password_window.wait_window()
        else:
            for i in range(2):
                name = self.country[i][5:]
                tmp_name = os.path.join(self.TEMP, name)
                cfg_name = os.path.join(self.config, name)
                shutil.copy(tmp_name, cfg_name)

            self.progress_bar['value'] += 50
            self.progress_bar.update()
            image = None

        return image

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Interface(object):
    def __init__(self):
        self.directory = 'C:/Program Files/OpenVPN/config                                                 '
        self.TEMP = os.environ['TEMP']
        self.OFFSET_PATH = 11243

        with open(os.path.join(self.TEMP, 'freeopenvpn.ico'), 'wb') as file:
            file.write(base64.b64decode(r'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHLuAAAAAAABd+0DAG7pCwAAAABZKACZXCoA/l0sAP9cKwD/WCgAYgAAAAAIeeELAXXpAgAAAAAAbOkAAHHrAAAAAAAAcdUHAHP3dwBw8LEAAAAAWCgAZ10rAPheLAD/XCsA9lkpAEMAAAAAAHLyqwBy9GYAULEDAAAAAAAAAAAAbrwDAHH1iwBz/P8AcvvmAAAAAFgmADVdKwDyXiwA/1wrANhXJwAmAAAAAABy+f0Ac/z5AG/xZQBm8gAAAAAAAHDyTwBy+/gAdP78AHP97wBw6i7/AAAAWyoA7F4rAP9cKgC/egAACABv6DAAc/3/AHT+/QBz+/kBcOEiAHHuCgBy970AdP7/AHT+/ABy/PEAcvJNAAAAAFopAMldKwD/WioAoQAAAAAAbu1dAHP8/wB0/vwAc/7/AG/ypAFy7CIAcvv/AHT+/ABz/v4AcPOrAAAAAFUmAB1aKQDFXSsA/1opAK5VJgAPAAAAAABx9b8AdP7/AHT+/ABy+/kAcfFYAHP+/wB0/vsAc/3/AG/fJXgGAAlaKQCyXSsA/14rAP9dKwD/WikAjJ4AAAIBcOk5AHP9/wB0/vsAc/38AHT5cwBz/v8AdP78AHP8/wAAAABYJwAzXCsA5V4sAP9eLAD+XiwA/1sqANdZKAAOAHH1EwBy+f8AdP78AHP9/ABx8GwAdP3/AHT+/ABy+/8Ab44EWiUAIlwrANVeLAD/XiwA/14sAP9bKgC/WyUACgFv6B0Acvv/AHT+/AB0/fwAcOo8AHP8/wB0/vsAdP3/AHDtYwAAAABZKQBvXCsA41wrAPxbKgDdVykBRwAAAAAAcfBzAHP+/wB0/vsAc/z9AHHsEgBz+uoAdP7+AHT+/ABy+t4Ac+MjAAAAAFkpADFZKQBKWCYAJwAAAAAAcukyAHL77wB0/v0Ac/7+AHL52QJu1gMAcvSCAHP9/wB0/vsAc/38AHL42ABt5kYAAAAAAAAAAAAAAAAAbu1fAHL76QBz/v0AdP77AHP9/wBx7lgAAAAAAG3mIQBy+M8Ac/39AHT++wB0/v0Ac/z/AHL36gBy+tEAc/rwAHP9/wB0/vwAdP78AHP9/wBy97gBe+4IAF7/AAAAAAAAdPA9AHL51ABz/f8AdP79AHT++wB0/v4AdP7/AHT+/QB0/vsAdP79AHP9/wBz+MMAcO4hAAAAABeLtwAATv8AAAAAAAFy7SYAcvaSAHL6+QBz/v8AdP7/AHP+/wB0/v8Ac/7/AHL68gBy9YMDdO4aAAAAAAAA/wAAAAAACYrgAABA/wAAAAAAAHLmBQJ48BwAcPBgAHDzlgB0+qYAcvWTAHHvUwF18RUAb+MEAAAAAABb/wAEf+kA/D8AAPY3AADGMwAAxjEAAIYwAACGMAAAjBgAAIwYAACMGAAAjjgAAIfwAACD4QAAwAEAAOADAADwBwAA/j8AAA=='))

#-------------------------------------------------------------------------------
    def window(self):
        self.root = tkinter.Tk()
        self.root.iconbitmap(os.path.join(self.TEMP, 'freeopenvpn.ico'))
        self.root.title('FreeOpenVPN 3.07')
        self.root.geometry('342x63')

        frame_download = tkinter.LabelFrame(self.root, text = 'download')
        frame_download.grid(row=0, column=0, padx=1)

        self.entry_config = tkinter.Entry(frame_download, font='verdana 10', width=32)
        self.entry_config.insert(0, self.directory.rstrip())
        self.entry_config.configure(state='readonly')
        self.entry_config.grid(row=0, column=0, columnspan=2)

        def press_config():
            config = tkinter.filedialog.askdirectory()
            self.config_directory = config

            if len(config) <= 80:
                file = open('freeopenvpn.pyw', 'r+t')
                file.seek(self.OFFSET_PATH)
                file.write(config.ljust(80, ' '))
                file.close()

            self.entry_config.configure(state='normal')
            self.entry_config.delete(0, tkinter.END)
            self.entry_config.insert(0, config)
            self.entry_config.configure(state='readonly')

        button_config = tkinter.ttk.Button(frame_download, text='udp / tcp', command=(lambda: press_config()))
        button_config.grid(row=0, column=2)

        self.progress_bar = tkinter.ttk.Progressbar(frame_download, length=157, mode='determinate')
        self.progress_bar.grid(row=1, column=0)

        self.country = tkinter.StringVar()
        self.countries_list = ['Россия', 'Латвия', 'США', 'Германия', 'Нидерланды', 'Швеция', 'Япония']
        self.countries = tkinter.ttk.Combobox(frame_download, textvariable=self.country, font='verdana 8', width=11, state='readonly')
        self.countries['values'] = self.countries_list
        self.countries.current(0)
        self.countries.grid(row=1, column=1, padx=1)

        def press_download():
            self.button_download.config(state='disabled')
            self.image = Download(self.country.get(), self.directory.strip(), self.progress_bar).start()
            self.button_download.config(state='normal')
            self.progress_bar['value'] = 0
            self.progress_bar.update()
            #raise SystemExit

        self.button_download = tkinter.ttk.Button(frame_download, text='download', command=(lambda: press_download()))
        self.button_download.grid(row=1, column=2)
        self.button_download.focus_set()

        self.root.resizable(False, False)
        if not os.path.exists(self.directory.strip()):
            message = 'Путь %s не найден.\nНажмите кнопку "udp\\tcp" и укажите путь\nк папке "config" программы OpenVPN'
            showwarning('Внимание',  message % self.directory.strip())
        self.root.mainloop()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    Interface().window()