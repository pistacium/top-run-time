import csv
import easygui
import datetime

#modication of meera's top run retimer script to work with SpeedrunIGT versions 8+

print('key:')
print('scp - settings change pause')
print('dlp - dimension load pause')
print('tdlp - timed dimension load pause')
print('np - normal pause')
print('up - untimed pause')
print('\n')
print('this tool is designed to work with version 8+ logs')
print('if the timer version is 7.2.4 or lower, user the other retimer')
print('\n\n')

def spaces(n):
    s = ''
    while n<9:
        s += ' '
        n += 1
    return s

def converttosecs(time):
    '''takes time in mm:ss:xxx and converts to seconds'''
    mins = int(time[0:2])
    secs = int(time[3:5])
    ms = int(time[6:9]) / 1000

    time = mins*60 + secs + ms
    return time

def decider(line):
    '''takes each listed pause in a given line and asks
        user what type of pause it is. returns pause
        length and inputted pause type'''

    #extract the needed information from the line
    pnum = str(line[0].split()[0])
    igt = line[0].split()[1]
    startrta = line[0].split()[2]
    endrta = line[0].split()[3]
    plength = float(line[0].split()[4])
    ptype = line[-2].split()

    if ptype[-1] == 'player':
        print('for pause', pnum)
        print('from', startrta, 'to', endrta, 'at', igt, 'IGT')
        ptype = input('enter type of pause: ')
        while ptype not in ['scp', 'dlp', 'tdlp', 'np', 'up']:
            ptype = input('try again champ: ')

    elif ptype[-1] == 'dimension' or ptype[-1] == 'load?' or ptype[-1] == 'ticks':
        print('the time from', startrta, 'to', endrta, 'is a dimension load', pnum)
        ptype = 'dl'

    elif ptype[-1] == 'world':
        print('relog incident')
        print(startrta, 'to', endrta, 'counted as dimension load', pnum, ', add back any penalty manually')
        ptype = 'dl'
        
    else:
        print(line)
        print('tell salix about this smth weird happened')
        input('probably not my fault tho')
        quit()
        
    newl = ptype+spaces(len(ptype))+startrta+'      '+endrta+'      '+"%.3f" % plength+'          '

    return plength, ptype, newl

fpath = easygui.fileopenbox()
with open(fpath, newline='') as f:
    r = csv.reader(f)
    file = list(r)
with open(fpath, newline='') as f:
    lines = f.readlines()
    origfile = [line.rstrip() for line in lines]

newf = ['type     start RTA      end RTA        length         time added\n']

file = file[1:]

igt = file[-5][0].split()
igt = converttosecs(igt[-1])
print('starting igt =', igt, 'seconds')
print()


nline = 1
for line in file[:-6]:
    plength, ptype, newl = decider(line)

    if ptype == 'scp':
        if plength > 5:
            igt += plength - 5
            print('everything after first 5s of this scp added back in =', plength-5)
            newl += str(plength - 5)
            newf.append(newl)
        else:
            print('no time added back for this scp of length =', plength)
            newl += '0'
            newf.append(newl)
    elif ptype == 'dlp':
        print('no time added back in for this dlp of length =', plength)
        origfile[nline] += ' - dimension load pause, untimed'
        newl += '0'
        newf.append(newl)
    elif ptype == 'tdlp':
        igt += plength
        print('length of this tdlp added back in =', plength)
        newl += str(plength)
        newf.append(newl)
    elif ptype == 'np':
        igt += plength
        print('length of this np added back in =', plength)
        newl += str(plength)
        newf.append(newl)
    elif ptype == 'up':
        print('no time added back for this up of length =', plength)
        origfile[nline] += ' - untimed pause'
        newl += '0'
        newf.append(newl)
    elif ptype == 'dl':
        print('no time added back for this dimension load of length =', plength)
        newl += str('0')
        newf.append(newl)
    nline += 1
    print()
igt = round(igt, 3)
print('final igt =', igt, 'seconds')
ftime = (str(datetime.timedelta(seconds=igt)))[:-3]
print(ftime)

newf.append('')
newf.append(origfile[-5])
newf.append('retimed IGT for top run retiming to '+ftime)
#print(newf)
fname = input('enter name for output file: ')
with open(fname+'.txt', 'w') as f:
    for line in newf:
        f.write(line+'\n')

input('press enter to exit...')
