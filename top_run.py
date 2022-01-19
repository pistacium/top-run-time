import csv
import easygui
import datetime

print('key:')
print('scp - settings change pause')
print('dlp - dimension load pause')
print('tdlp - timed dimension load pause')
print('np - normal pause')
print('up - untimed pause')
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
    ptype = line[-1].split()
    plength = converttosecs(ptype[0])
    
    if ptype[-1] == 'player)':
        print('for the pause from', line[1], 'to', line[2])
        ptype = input('enter type of pause: ')
        while ptype not in ['scp', 'dlp', 'tdlp', 'np', 'up']:
            ptype = input('try again champ: ')
        
    elif ptype[-1] == 'dimension)':
        print('the time from', line[1], 'to', line[2], 'is a dimension load')
        ptype = 'dl'
    else:
        print(line)
        input('tell meera about this smth weird happened')
        quit()
    #print(line)
    newl = ptype+spaces(len(ptype))+str(line[1].split()[0])+'      '+str(line[2].split()[0])+'      '+str(line[-1].split()[0])+'      '
    return plength, ptype, newl

fpath = easygui.fileopenbox()
with open(fpath, newline='') as f:
    r = csv.reader(f)
    file = list(r)
with open(fpath, newline='') as f:
    lines = f.readlines()
    origfile = [line.rstrip() for line in lines]

newf = ['type     start RTA      end RTA        length         time added\n']
file = file[5:]

igt = file[-1][0].split()
igt = converttosecs(igt[-1])
print('starting igt =', igt, 'seconds')
print()

nline = 5
for line in file[:-1]:
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
ftime = str(datetime.timedelta(seconds=igt))
print(ftime[:-3])

newf.append('')
newf.append(origfile[-1])
newf.append('retimed IGT for top run retiming to '+ftime)
#print(newf)
with open('topretimed.txt', 'w') as f:
    for line in newf:
        f.write(line+'\n')

input('press enter to exit...')
