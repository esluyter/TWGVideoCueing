#!/usr/local/bin/python3

import sys
import os
import csv
import shutil

if len(sys.argv) != 2:
    print('USAGE: cuelistconverter.py path')
    sys.exit()

path = sys.argv[1]
show_name = os.path.basename(os.path.normpath(path))
old_cuedata_path = os.path.join(path, 'cuedata.csv')
old_cuelist_path = os.path.join(path, 'cuelist.csv')
old_mediainfo_path = os.path.join(path, 'mediainfo.txt')
if not (os.path.isfile(old_cuedata_path) and os.path.isfile(old_cuelist_path) and os.path.isfile(old_mediainfo_path)):
    print('Files don\'t exist in specified path!')
    sys.exit()

print('Importing old cue data...')
old_cuedata = []
with open(old_cuedata_path, 'r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    next(reader)
    for row in reader:
        old_cuedata.append(row)
old_cuelist = []
with open(old_cuelist_path, 'r', newline='') as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
        old_cuelist.append(row)

print('Creating new cue list...')
new_cues = []
for row in old_cuelist:
    name = row[0]
    take = row[1]
    old_cue = [cue for cue in old_cuedata if cue[0] == name and cue[1] == take][-1]
    buses = []
    for i in range(5):
        start = i * 7 + 2
        old_bus = old_cue[start:start+7]
        media = old_bus[0]
        pos = old_bus[1]
        if old_bus[2] == 'n':
            speed = 'n'
            ramp = 'n'
        else:
            speedlist = old_bus[2].split(' ')
            if len(speedlist) == 1:
                speed = speedlist[0]
                ramp = '0'
            elif len(speedlist) == 2:
                speed, ramp = speedlist
            else:
                print('Speed items error!', name, speedlist)
                sys.exit()
        zoom = old_bus[3]
        db = old_bus[5]
        buses.append([media, pos, speed, ramp, zoom, db])
    notes = old_cue[5*7+2]
    matrix = old_cue[6*7]
    new_cues.append([name] + [x for bus in buses for x in bus] + [notes, matrix])

print(show_name)
new_path = os.path.join(path, show_name)
new_cues_path = os.path.join(new_path, 'cues.csv')
new_mediainfo_path = os.path.join(new_path, 'mediainfo.txt')

print('Writing files to', new_path, '...')
os.mkdir(new_path)
os.mkdir(os.path.join(new_path, 'backups'))

header = 'Cue,A media,A pos,A speed,A ramp,A zoom,A db,B media,B pos,B speed,B ramp,B zoom,B db,C media,C pos,C speed,C ramp,C zoom,C db,D media,D pos,D speed,D ramp,D zoom,D db,E media,E pos,E speed,E ramp,E zoom,E db,Notes,Matrix\n'

with open(new_cues_path, 'w', newline='') as csv_file:
    csv_file.write(header)
    writer = csv.writer(csv_file)
    for cue in new_cues:
        writer.writerow(cue)

shutil.copyfile(old_mediainfo_path, new_mediainfo_path)
