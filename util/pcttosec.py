#!/usr/local/bin/python3
import math

media_length = 22 * 60 + 46

while True:
    position = input('Position (%) or "Q" to quit: ')
    if position.upper() == 'Q':
        break
    try:
        position = float(position)
    except:
        print('Invalid position number, try again.')
    else:
        seconds = position * 0.01 * media_length
        minutes = math.floor(seconds / 60)
        seconds = seconds - (minutes * 60)
        print(position, '%  => ', minutes, 'minutes and', round(seconds, 2), 'seconds')
