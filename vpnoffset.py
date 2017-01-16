# -*- coding: UTF-8 -*-
import os

offset_path = 0
try:
    file = open('freeopenvpn.pyw', 'rt')
    temp = open('freeopenvpn.tmp', 'wt')

    line = file.readline()
    while line:
        if offset_path == 0 and line.find('self.directory = ') > 0:
            offset_path = file.tell() - 83
        elif line.find('self.OFFSET_PATH = ') > 0:
            line = ''.join((line[:line.find('self.OFFSET_PATH = ') + 19], str(offset_path), '\n'))

        temp.write(line)
        line = file.readline()

    file.close()
    temp.close()

    os.remove('freeopenvpn.pyw')
    os.rename('freeopenvpn.tmp', 'freeopenvpn.pyw')

except FileNotFoundError:
    print('Файл \'freeopenvpn.pyw\' не найден.')

finally:
    print('ok!')