# -*- coding: utf-8 -*-
import serial
import time


def not_screen_and_sensor_command(command):
    time.sleep(1)
    ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
    if not ser.isOpen:
        ser.open()
    ser.flushInput()
    ser.flushOutput()

    accept = ''
    while not accept.__contains__('0'):
        ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
        if not ser.isOpen:
            ser.open()
        ser.flushInput()
        ser.flushOutput()

        ser.write('M!'.encode('utf-8'))
        accept = ''
        while accept == '':
            accept = ser.readline()
            print(accept)
        accept = str(accept)

    ser.write(command.encode('utf-8'))


def sensor_command(command):
    time.sleep(0.5)
    ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
    if not ser.isOpen:
        ser.open()
    ser.flushInput()
    ser.flushOutput()

    accept = ''
    while not accept.__contains__('0'):
        ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
        if not ser.isOpen:
            ser.open()
        ser.flushInput()
        ser.flushOutput()

        ser.write('M!'.encode('utf-8'))
        accept = ''
        while accept == '':
            accept = ser.readline()
        accept = str(accept)

    ser.write(command.encode('utf-8'))
    accept = ''
    while accept == '':
        accept = ser.readline()
    accept = str(accept)
    return accept


def change_screen_command(command):
    time.sleep(0.5)
    ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
    if not ser.isOpen:
        ser.open()
    ser.flushInput()
    ser.flushOutput()

    accept = ''
    while not accept.__contains__('1'):
        ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
        if not ser.isOpen:
            ser.open()
        ser.flushInput()
        ser.flushOutput()

        ser.write('M!'.encode('utf-8'))
        accept = ''
        while accept == '':
            accept = ser.readline()
        accept = str(accept)

    ser.write(command.encode('utf-8'))
    ser.write(b'\xFF\xFF\xFF')


def send_screen_information_command(position_and_type, word):
    time.sleep(0.5)
    ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
    if not ser.isOpen:
        ser.open()
    ser.flushInput()
    ser.flushOutput()

    accept = ''
    while not accept.__contains__('1'):
        ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
        if not ser.isOpen:
            ser.open()
        ser.flushInput()
        ser.flushOutput()

        ser.write('M!'.encode('utf-8'))
        accept = ''
        while accept == '':
            accept = ser.readline()
        accept = str(accept)

    content = str(position_and_type) + "=" + '"' + str(word) + '"'
    print(content)
    ser.write(content.encode("GB2312"))
    ser.write(b'\xFF\xFF\xFF')


def wait_screen(position):
    time.sleep(0.5)
    ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
    if not ser.isOpen:
        ser.open()
    ser.flushInput()
    ser.flushOutput()

    accept = ''
    while not accept.__contains__('0'):
        ser = serial.Serial('/dev/ttyTHS0', 9600, timeout=0.5)
        if not ser.isOpen:
            ser.open()
        ser.flushInput()
        ser.flushOutput()

        ser.write('M!'.encode('utf-8'))
        accept = ''
        while accept == '':
            accept = ser.readline()
        accept = str(accept)

    ser.write(position.encode('utf-8'))
    accept = ser.readline()
    return bytes.decode(accept)


if __name__ == '__main__':
    change_screen_command('page 1')
    change_screen_command('page 2')
    change_screen_command('page 3')
    change_screen_command('page 4')
    change_screen_command('page 5')
    change_screen_command('page 6')
    change_screen_command('page 7')
    change_screen_command('page 8')
    change_screen_command('page 9')

    print(sensor_command('D-0!'))
    print(sensor_command('D-1!'))
    print(sensor_command('K-!'))
    print(sensor_command('L-!'))
    print(sensor_command('G-!'))
    print(sensor_command('J-0!'))

    not_screen_and_sensor_command('A-090!')
    not_screen_and_sensor_command('A-000!')
    not_screen_and_sensor_command('E-!')
    not_screen_and_sensor_command('B-000!')
    not_screen_and_sensor_command('B-111!')
    not_screen_and_sensor_command('C-!')
    not_screen_and_sensor_command('F-1000!')
    time.sleep(3)
    not_screen_and_sensor_command('F-2000!')
    not_screen_and_sensor_command('H-1!')
    time.sleep(3)
    not_screen_and_sensor_command('H-2!')
    time.sleep(3)
    not_screen_and_sensor_command('H-0!')
