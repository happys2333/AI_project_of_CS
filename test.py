s = 'print(\'s=\',s,\'\\\'\');s = list(\'s=\\\'\'+s+\'\\\'\'+s);s = s.reverse()\n\
for x in s:\n\
    print(x,end=\'\')'
print('s=\'',s,'\'',s)
s = list('s=\''+s+'\''+s)
s.reverse()
for x in s:
    print(x,end='')