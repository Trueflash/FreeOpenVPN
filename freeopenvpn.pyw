#-------------------------------------------------------------------------------
# -*- coding: UTF-8 -*-
#-------------------------------------------------------------------------------
# Name:        FreeOpenVPN ver. 2.01
# Python:      3.4.4
# Created:     16.08.2016
# Copyright:   (c) box.pupkin@gmail.com
# pip install: robobrowser, pillow, numpy, pypng
#-------------------------------------------------------------------------------
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk
import tkinter
import PIL.ImageTk
import PIL.Image
import robobrowser
import requests
import zipfile
import base64
import pickle
import numpy
import math
import time
import png
import sys
import os

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Base(object):
    def __init__(self, captcha, number):
        b64 = r'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'
        with open(os.environ['TEMP'] + '\\numbers.zip', 'wb') as file:
            b64 = base64.b64decode(b64)
            file.write(b64)

        db = zipfile.ZipFile(os.environ['TEMP'] + '\\numbers.zip', 'r')
        db.extract('numbers.bin', os.environ['TEMP'])
        db.close()

        with open(os.environ['TEMP'] + '\\numbers.bin', 'rb') as file:
            numbers = pickle.load(file)

        self.captcha = self.convert(captcha)
        self.numbers = numbers[number]

#-------------------------------------------------------------------------------
    def convert(self, captcha):
        convert_captha = list()
        for i in range(0, len(captcha)):
            convert_captha.append([])

            for j in range(0, len(captcha[i]), 3):
                convert_captha[i].append(int(numpy.sum(captcha[i][j:j+3]) < 500))

        return numpy.array(convert_captha)

#-------------------------------------------------------------------------------
    def tostring(self):
        password = ''

        for i in range(9):
            results = list()

            for j in range(10):
                results.append(numpy.sum(self.captcha[:, :len(self.numbers[j][0])] ^ self.numbers[j]))

            self.captcha = self.captcha[:, len(self.numbers[results.index(min(results))][0]):]
            password += str(results.index(min(results)))

        return password

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class One(Base):
    def __init__(self, captcha):
        super(One, self).__init__(captcha, 0)

        array = self.captcha[2:12, 4:14]

        for i in range(8):
            array = numpy.hstack((array, self.captcha[2:12, 20+i*16:30+i*16]))

        self.captcha = array

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Two(Base):
    def __init__(self, captcha):
        super(Two, self).__init__(captcha, 1)

        if not numpy.sum(self.captcha[:1, :]):
            self.captcha = self.captcha[2:, 3:]
        elif not numpy.sum(self.captcha[12:, :]):
            self.captcha = self.captcha[:11, 3:]
        else:
            self.captcha = self.captcha[1:12, 3:]

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Three(Base):
    def __init__(self, captcha):
        super(Three, self).__init__(captcha, 2)

        if not numpy.sum(self.captcha[:1, :]):
            self.captcha = self.captcha[2:, :]
        elif not numpy.sum(self.captcha[12:, :]):
            self.captcha = self.captcha[:11, :]
        else:
            self.captcha = self.captcha[1:12, :]

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Four(Base):
    def __init__(self, captcha):
        super(Four, self).__init__(captcha, 3)

        array = self.captcha[:, :13]

        for i in range(1, 9):
            array = numpy.hstack((array, self.captcha[:, 14*i:14*i+13]))

        self.captcha = array

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Five(Base):
    def __init__(self, captcha):
        super(Five, self).__init__(captcha, 4)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Snatch(object):
    def __init__(self, file_name):
        file = png.Reader(file_name)
        self.captcha = list(file.read()[2])

    def password(self):
        if len(self.captcha[0]) - len(self.captcha) == 424:
            return One(self.captcha).tostring()
        elif len(self.captcha[0]) - len(self.captcha) == 347:
            return Two(self.captcha).tostring()
        elif len(self.captcha[0]) - len(self.captcha) == 554:
            return Three(self.captcha).tostring()
        elif len(self.captcha[0]) - len(self.captcha) == 361:
            return Four(self.captcha).tostring()
        elif len(self.captcha[0]) - len(self.captcha) == 360:
            return Five(self.captcha).tostring()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class Download(object):
    def __init__(self, countries_list, freeopenvpn_path, progress_bar = None):
        self.freeopenvpn_path = freeopenvpn_path
        self.progress_bar = progress_bar
        self.freeopenvpn = 'https://www.freeopenvpn.org/'
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        self.countries_list = {'Россия' : ('Russia_freeopenvpn_udp.ovpn', 'Russia_freeopenvpn_tcp.ovpn', 'logpass/russia.php'),
                               'США' : ('freeopenvpn_USA_udp.ovpn', 'freeopenvpn_USA_tcp.ovpn'),
                               'Германия' : ('Germany_freeopenvpn_udp.ovpn', 'Germany_freeopenvpn_tcp.ovpn', 'logpass/germany.php'),
                               'Нидерланды' : ('NL_freeopenvpn_udp.ovpn', 'NL_freeopenvpn_tcp.ovpn', 'logpass/netherlands.php'),
                               'Япония' : ('freeopenvpn_Japan_udp.ovpn', 'freeopenvpn_Japan_tcp.ovpn'),
                               'Корея' : ('freeopenvpn_South_Korea_udp.ovpn', 'freeopenvpn_South_Korea_tcp.ovpn'),
                               'Вьетнам' : ('freeopenvpn_Vietnam_udp.ovpn', 'freeopenvpn_Vietnam_tcp.ovpn')}

        for key in list(self.countries_list.keys()):
            if key not in countries_list:
                self.countries_list.pop(key)

        self.progress = math.ceil(100 / sum(2*len(value) for value in self.countries_list.values()))

#-------------------------------------------------------------------------------
    def page_captcha(self, page_country):
        browser = robobrowser.RoboBrowser(history = False, user_agent = self.user_agent, parser = 'html.parser')
        browser.open(self.freeopenvpn + page_country)
        self.captcha = str(browser.find_all('script')[3]).split('"')[-2]
        return 'https://www.freeopenvpn.org/logpass/' + self.captcha

#-------------------------------------------------------------------------------
    def download(self, address):
        with open(os.path.join(os.environ['TEMP'], os.path.basename(address)), 'wb') as file:
            response = requests.get(address, stream = True)
            file.write(response.content)

#-------------------------------------------------------------------------------
    def modify_ovpn(self, name):
        with open(os.path.join(os.environ['TEMP'], name), 'rt') as temp:
            file = open(os.path.join(self.freeopenvpn_path, name), 'wt')
            for line in temp:
                if line == 'auth-user-pass\n':
                    line = line[:-1] + ' "' + self.freeopenvpn_path + '/' + name[:-9] + '.pwd"\n'

                file.write(line)

#-------------------------------------------------------------------------------
    def start(self):
        for country in self.countries_list.values():
            self.download('https://www.freeopenvpn.org/ovpn/' + country[0])
            self.progress_bar['value'] += self.progress
            self.progress_bar.update()

            self.download('https://www.freeopenvpn.org/ovpn/' + country[1])
            self.progress_bar['value'] += self.progress
            self.progress_bar.update()

            if len(country) == 3:
                address_captcha = self.page_captcha(country[2])
                self.progress_bar['value'] += self.progress
                self.progress_bar.update()

                self.download(address_captcha)
                self.progress_bar['value'] += self.progress
                self.progress_bar.update()

                password = Snatch(os.path.join(os.environ['TEMP'], self.captcha)).password()

                file = open(os.path.join(self.freeopenvpn_path, country[0][:-9] + '.pwd'), 'wt')
                file.write('freeopenvpn\n' + password)
                self.progress_bar['value'] += self.progress
                self.progress_bar.update()
                file.close()

            self.modify_ovpn(country[0])
            self.modify_ovpn(country[1])
            self.progress_bar['value'] = 100
            self.progress_bar.update()

            report_window = tkinter.Toplevel()
            report_window.title('Report')
            report_window.iconbitmap(os.environ['TEMP'] + '\\icon.ico')
            tkinter.Label(report_window, text = country[0]).grid(row = 0, column = 0)
            tkinter.Label(report_window, text = '-').grid(row = 0, column = 1)
            tkinter.Label(report_window, text = 'ok').grid(row = 0, column = 2)
            tkinter.Label(report_window, text = country[1]).grid(row = 1, column = 0)
            tkinter.Label(report_window, text = '-').grid(row = 1, column = 1)
            tkinter.Label(report_window, text = 'ok').grid(row = 1, column = 2)

            if len(country) == 3:
                image = PIL.ImageTk.PhotoImage(PIL.Image.open(os.path.join(os.environ['TEMP'], os.path.basename(self.captcha))))

                tkinter.Label(report_window, image = image).grid(row = 2, column = 0)
                tkinter.Label(report_window, text = '-').grid(row = 2, column = 1)
                tkinter.Label(report_window, text = password).grid(row = 2, column = 2)
                tkinter.Label(report_window, text = 'Если пароль определен неверно, напишите на\nbox.pupkin@gmail.com').grid(row = 3, column = 0, columnspan = 3)
            else:
                image = None

            tkinter.ttk.Button(report_window, text = 'Continue', command = report_window.destroy).grid(row = 4, column = 0, columnspan = 3)
            report_window.resizable(False, False)
            report_window.focus_set()
            report_window.grab_set()
            report_window.wait_window()

            self.progress_bar['value'] = 0
            self.progress_bar.update()

        return image

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
class FreeOpenVPN(object):
    def __init__(self):
        self.udptsp_directory = 'C:/Program Files/OpenVPN/config                                                                                                                                 '

        with open(os.path.join(os.environ['TEMP'], 'icon.ico'), 'wb') as file:
            ico = r'AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHLuAAAAAAABd+0DAG7pCwAAAABZKACZXCoA/l0sAP9cKwD/WCgAYgAAAAAIeeELAXXpAgAAAAAAbOkAAHHrAAAAAAAAcdUHAHP3dwBw8LEAAAAAWCgAZ10rAPheLAD/XCsA9lkpAEMAAAAAAHLyqwBy9GYAULEDAAAAAAAAAAAAbrwDAHH1iwBz/P8AcvvmAAAAAFgmADVdKwDyXiwA/1wrANhXJwAmAAAAAABy+f0Ac/z5AG/xZQBm8gAAAAAAAHDyTwBy+/gAdP78AHP97wBw6i7/AAAAWyoA7F4rAP9cKgC/egAACABv6DAAc/3/AHT+/QBz+/kBcOEiAHHuCgBy970AdP7/AHT+/ABy/PEAcvJNAAAAAFopAMldKwD/WioAoQAAAAAAbu1dAHP8/wB0/vwAc/7/AG/ypAFy7CIAcvv/AHT+/ABz/v4AcPOrAAAAAFUmAB1aKQDFXSsA/1opAK5VJgAPAAAAAABx9b8AdP7/AHT+/ABy+/kAcfFYAHP+/wB0/vsAc/3/AG/fJXgGAAlaKQCyXSsA/14rAP9dKwD/WikAjJ4AAAIBcOk5AHP9/wB0/vsAc/38AHT5cwBz/v8AdP78AHP8/wAAAABYJwAzXCsA5V4sAP9eLAD+XiwA/1sqANdZKAAOAHH1EwBy+f8AdP78AHP9/ABx8GwAdP3/AHT+/ABy+/8Ab44EWiUAIlwrANVeLAD/XiwA/14sAP9bKgC/WyUACgFv6B0Acvv/AHT+/AB0/fwAcOo8AHP8/wB0/vsAdP3/AHDtYwAAAABZKQBvXCsA41wrAPxbKgDdVykBRwAAAAAAcfBzAHP+/wB0/vsAc/z9AHHsEgBz+uoAdP7+AHT+/ABy+t4Ac+MjAAAAAFkpADFZKQBKWCYAJwAAAAAAcukyAHL77wB0/v0Ac/7+AHL52QJu1gMAcvSCAHP9/wB0/vsAc/38AHL42ABt5kYAAAAAAAAAAAAAAAAAbu1fAHL76QBz/v0AdP77AHP9/wBx7lgAAAAAAG3mIQBy+M8Ac/39AHT++wB0/v0Ac/z/AHL36gBy+tEAc/rwAHP9/wB0/vwAdP78AHP9/wBy97gBe+4IAF7/AAAAAAAAdPA9AHL51ABz/f8AdP79AHT++wB0/v4AdP7/AHT+/QB0/vsAdP79AHP9/wBz+MMAcO4hAAAAABeLtwAATv8AAAAAAAFy7SYAcvaSAHL6+QBz/v8AdP7/AHP+/wB0/v8Ac/7/AHL68gBy9YMDdO4aAAAAAAAA/wAAAAAACYrgAABA/wAAAAAAAHLmBQJ48BwAcPBgAHDzlgB0+qYAcvWTAHHvUwF18RUAb+MEAAAAAABb/wAEf+kA/D8AAPY3AADGMwAAxjEAAIYwAACGMAAAjBgAAIwYAACMGAAAjjgAAIfwAACD4QAAwAEAAOADAADwBwAA/j8AAA=='
            ico = base64.b64decode(ico)
            file.write(ico)

#-------------------------------------------------------------------------------
    def press_udptcp(self):
        udttcp = tkinter.filedialog.askdirectory()

        if len(udttcp) <= 160:
            file = open('freeopenvpn.pyw', 'r+t')
            file.seek(14342)
            file.write(udttcp.ljust(160, ' '))
            file.close()

        self.entry_udptcp.configure(state = 'normal')
        self.entry_udptcp.delete(0, tkinter.END)
        self.entry_udptcp.insert(0, udttcp)
        self.entry_udptcp.configure(state = 'readonly')

#-------------------------------------------------------------------------------
    def press_create(self):
        if self.root.winfo_height() == 63:
            self.button_open_create.configure(text = '↑')
            self.root.geometry('342x103')
            self.button_download.config(state = 'disabled')
            self.countries.configure(state = 'disabled')
        else:
            self.button_download.config(state = 'normal')
            self.countries.configure(state = 'readonly')
            self.button_open_create.configure(text = '↓')
            self.root.geometry('342x63')

#-------------------------------------------------------------------------------
    def press_download(self):
        self.button_download.config(state = 'disabled')

        if len(self.udptsp_directory.strip()):
            self.image = Download((self.country.get(),), self.udptsp_directory.strip(), self.progress_bar).start()
        else:
            self.image = Download((self.country.get(),), os.getcwd(), self.progress_bar).start()

        self.button_download.config(state = 'normal')

#-------------------------------------------------------------------------------
    def create_light(self):
        countries = {'ru':'Россия', 'us':'США', 'de':'Германия', 'nl':'Нидерланды', 'jp':'Япония', 'kr':'Корея', 'vn':'Вьетнам'}
        countries_list = 'Download(['

        for country in self.countries_create:
            if self.countries_create[country].get():
                countries_list += '\'' + countries[country] + '\', '

        if len(countries_list) > 10:
            def read_write(start, length):
                donor.seek(start)
                block = donor.read(length)
                recipient.write(block)

            donor = open('freeopenvpn.pyw', 'rb')
            recipient = open('light.pyw', 'wb')

            read_write(0, 449)
            read_write(577, 11862)
            read_write(12538, 77)
            read_write(12700, 118)
            read_write(12925, 32)
            read_write(13062, 268)
            read_write(13435, 100)
            read_write(25046, 197)

            recipient.write(bytes(countries_list[:-2] + '], \'' + self.udptsp_directory.strip() + '\').start()\n', 'utf8'))
            tkinter.messagebox.showinfo('info', 'Файл light.pyw создан.')

            recipient.close()
            donor.close()

        else:
            tkinter.messagebox.showerror('error', 'Не выбрано ни одной страны.')

#-------------------------------------------------------------------------------
    def window(self):
        self.root = tkinter.Tk()
        self.root.iconbitmap(os.environ['TEMP'] + '\\icon.ico')
        self.root.title('FreeOpenVPN 2.01')
        self.root.geometry('342x63')

        frame_download = tkinter.LabelFrame(self.root, text = 'download')
        frame_download.grid(row = 0, column = 0, padx = 1)

        self.entry_udptcp = tkinter.Entry(frame_download, font = 'verdana 10', width = 32)
        self.entry_udptcp.insert(0, self.udptsp_directory.rstrip())
        self.entry_udptcp.configure(state = 'readonly')
        self.entry_udptcp.grid(row = 0, column = 0, columnspan = 3)

        button_udptcp = tkinter.ttk.Button(frame_download, text = 'upd / tcp', command = (lambda: self.press_udptcp()))
        button_udptcp.grid(row = 0, column = 3)

        self.button_open_create = tkinter.ttk.Button(frame_download, width = 1, text = '↓', command = (lambda: self.press_create()))
        self.button_open_create.grid(row = 1, column = 0)

        self.progress_bar = tkinter.ttk.Progressbar(frame_download, length = 141, mode = 'determinate')
        self.progress_bar.grid(row = 1, column = 1)

        self.country = tkinter.StringVar()
        self.countries_list = ['Россия', 'США', 'Германия', 'Нидерланды', 'Япония', 'Корея', 'Вьетнам']
        self.countries = tkinter.ttk.Combobox(frame_download, textvariable = self.country, font = 'verdana 8', width = 11, state='readonly')
        self.countries['values'] = self.countries_list
        self.countries.current(0)
        self.countries.grid(row = 1, column = 2, padx = 1)

        self.button_download = tkinter.ttk.Button(frame_download, text = 'download', command = (lambda: self.press_download()))#, command = (lambda: Download(self.country.get()).start()))
        self.button_download.grid(row = 1, column = 3)

        frame_open_create = tkinter.LabelFrame(self.root, text = 'create')
        frame_open_create.grid(row = 1, column = 0)

        self.countries_create = {'ru':tkinter.BooleanVar(), 'us':tkinter.BooleanVar(), 'de':tkinter.BooleanVar(), 'nl':tkinter.BooleanVar(), 'jp':tkinter.BooleanVar(), 'kr':tkinter.BooleanVar(), 'vn':tkinter.BooleanVar()}

        self.countries_create['ru'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'ru', variable = self.countries_create['ru'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 0, padx = 1)

        self.countries_create['us'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'us', variable = self.countries_create['us'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 1, padx = 1)

        self.countries_create['de'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'de', variable = self.countries_create['de'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 2, padx = 1)

        self.countries_create['nl'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'nl', variable = self.countries_create['nl'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 3, padx = 1)

        self.countries_create['jp'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'jp', variable = self.countries_create['jp'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 4, padx = 1)

        self.countries_create['kr'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'kr', variable = self.countries_create['kr'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 5, padx = 1)

        self.countries_create['vn'].set(False)
        ru = tkinter.ttk.Checkbutton(frame_open_create, text = 'vn', variable = self.countries_create['vn'], onvalue = True, offvalue = False)
        ru.grid(row = 0, column = 6, padx = 1)

        tkinter.Label(frame_open_create, text = ' ').grid(row = 0, column = 7, padx = 3)

        button_create = tkinter.ttk.Button(frame_open_create, text = 'create', command = (lambda: self.create_light()))
        button_create.grid(row = 0, column = 8)

        self.root.resizable(False, False)
        self.root.mainloop()

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) == 1:
        FreeOpenVPN().window()
    else:
        root = tkinter.Tk()
        root.title('password')
        image = PIL.ImageTk.PhotoImage(PIL.Image.open(sys.argv[1]))
        tkinter.Label(root, image = image).grid(row = 0, column = 0)
        password = Snatch(sys.argv[1]).password()
        tkinter.Label(root, text = ' -  ' + password).grid(row = 0, column = 1)
        root.resizable(False, False)
        root.mainloop()