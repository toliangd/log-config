import os # работа с файловой системой
from datetime import datetime
import configparser # работа с конфигами

"""Открываем файл с логами для txt.txt.
   Разбиваем логи на список line=[стороки файла][части лога].
   Пример лога - ("[15/08/2020:13:11:58]" "sig-1")"""
def log(name):
    f_log = open('/home/tolik/program/linix/log/{}'.format(name), 'r')
    line = [l[1:-2].split('" "') for l in f_log]
    f_log.close()
    return line

"""для каждого файла указанного в default.cfg сравниваем время создания с текущим временем"""
def time_default(val1, i, time):
    t_change = datetime.fromtimestamp(os.path.getmtime(val1 + '/' + i)) # время последнего изменения файла
    t_system = datetime.today()
    print(i, ':', '\n',
          type(t_change), ' - ', t_change, '\n',
          type(t_system), ' - ', t_system, '\n')
    if (t_system - t_change).days <= 1:
        delta = ((t_system - t_change).seconds) / 60  # разница в минутах
        print('2. разница в минутах:', '\n', int(delta), '\n')
        if delta <= time:
            print('3. файл', i, 'был обновлен', '\n')
        else:
            print('3. время с последнего обновления превышено')
    else:
        print('2. разница больше одного дня', '\n', '3. время с последнего обновления превышено', '\n')
    return 0

def conf(val2, n, i, f_file):
    config = configparser.ConfigParser()
    config.read('val2' + '/' + i)

    """вывод из конфигурационных файлов"""
    print('4.', n, 'конфигурационный файл: ', config.sections())
    if line_default.count(config[i]['path']) == 0: # если файл не был указан в default.cfg
        print('-', config[i]['path'])
        print('-', config[i]['time'])
        print('-', config[i]['sig'])

        """поиск в val1 файлов с именами указанными в конфигах"""
        if f_file.index(config[i]['path']) != None:
            if config[i]['path'] == 'txt.txt':
                line_conf = log('access.log.1')
            elif config[i]['path'] == 'arhiv2.zip':
                line_conf = log('access.log.2')
            elif config[i]['path'] == 'arhiv1.tar':
                line_conf = log('access.log.3')
            for j in line_conf:
                date_log = datetime.strptime(j[0][1:-1], "%d/%m/%Y:%H:%M:%S")
                date_delta = datetime.today() - date_log
                if config[i]['sig'] == j[1]:
                    if date_delta.days < 1 and int(date_delta.seconds/60) < int(config[i]['time']):

                        print('\n', 'Найдена сигнатура:', '\n', config[i]['sig'] , '-', date_log, int(date_delta.seconds/60), '\n')
                    else:
                        print('сигнатура', config[i]['sig'], '-', date_log, 'не попала во временной промежуток', config[i]['time'])
    else:
        print('\n', 'файл', config[i]['path'], 'указан в default')
    return 0


time = 1400
val1 = '/home/tolik/program/linix/val1'
val2 = '/home/tolik/program/linix/val2'

"""считываем файл default.cfg"""
f_default = open('val2' + '/default.cfg', 'r')
line_default = [l.strip() for l in f_default]
print('1. файлы в default.cfg: ', '\n', line_default, '\n')
f_default.close()
for i in line_default:
    time_default(val1, i, time)

"""считываем из конфигурационных файлов в val1 и val2"""
f_conf = os.listdir(val2)
f_file = os.listdir(val1)
n = 0
for i in f_conf:
    if i == 'default.cfg':
        continue
    else:
        n += 1
        conf(val2, n, i, f_file)