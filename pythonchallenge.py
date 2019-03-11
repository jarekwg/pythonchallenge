import codecs
import re
import requests
import xmlrpc.client
from io import BytesIO

from PIL import Image

# Q0 - http://www.pythonchallenge.com/pc/def/0.html
print(2**38)


# Q1 - http://www.pythonchallenge.com/pc/def/map.html
translation = str.maketrans('abcdefghijklmnopqrstuvwxyz', 'cdefghijklmnopqrstuvwxyzab')
s = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmuynnjw ml rfc spj."
print(s.translate(translation))
print('map'.translate(translation))


# Q2 - http://www.pythonchallenge.com/pc/def/ocr.html
from collections import Counter  # noqa isort:skip
text = requests.get('http://www.pythonchallenge.com/pc/def/ocr.html').text
chars = re.search(r'find rare characters in the mess below:.*<!--(?P<chars>.*)-->', text, flags=re.DOTALL).groupdict()['chars']
print(''.join(k for k, v in Counter(chars).items() if v == 1))


# Q3 - http://www.pythonchallenge.com/pc/def/equality.html
text = requests.get('http://www.pythonchallenge.com/pc/def/equality.html').text
garbage = re.search(r'<!--(?P<garbage>.*)-->', text, flags=re.DOTALL).groupdict()['garbage']
print(''.join(re.findall(r'[^A-Z][A-Z]{3}(?P<smol>[a-z])[A-Z]{3}[^A-Z]', garbage)))


# Q4 - http://www.pythonchallenge.com/pc/def/linkedlist.php
next_nothing = '12345'
for _ in range(400):
    text = requests.get(f'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing={next_nothing}').text
    try:
        next_nothing = re.search(r'next nothing is (?P<nothing>\d+)', text).groupdict()['nothing']
    except AttributeError:
        if 'divide by two' in text.lower():
            next_nothing = str(int(next_nothing) // 2)
        else:
            print(text)
            break
    print(f"{text} --> {next_nothing}")


# Q5 - http://www.pythonchallenge.com/pc/def/peak.html
import pickle  # noqa isort:skip
pic = pickle.loads(requests.get('http://www.pythonchallenge.com/pc/def/banner.p').content)
result = ''
for row in pic:
    for col in row:
        result += col[0] * col[1]
    result += '\n'
print(result)


# Q6 - http://www.pythonchallenge.com/pc/def/channel.html
import zipfile  # noqa isort:skip
response = requests.get('http://www.pythonchallenge.com/pc/def/channel.zip', stream=True)
zf = zipfile.ZipFile(BytesIO(response.content))
next_nothing = '90052'
result = ''
while True:
    result += zf.getinfo(f'{next_nothing}.txt').comment.decode()
    text = zf.read(f'{next_nothing}.txt').decode()
    try:
        next_nothing = re.search(r'Next nothing is (?P<nothing>\d+)', text).groupdict()['nothing']
    except AttributeError:
        print(text)
        break
    print(f"{text} --> {next_nothing}")
print(result)


# Q7 - http://www.pythonchallenge.com/pc/def/oxygen.html
response = requests.get('http://www.pythonchallenge.com/pc/def/oxygen.png', stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)
pixels = image.load()
result = ''
for x in range(0, image.width, image.width // 80):
    r, g, b, _ = pixels[x, image.height // 2]
    if r == g and g == b:
        result += chr(r)
print(result)
seq = re.search(r'\[(?P<seq>(?:\d+,? ?)+)\]', result).groupdict()['seq']
print(''.join(list(map(chr, map(int, seq.split(', '))))))


# Q8 - http://www.pythonchallenge.com/pc/def/integrity.html
text = requests.get('http://www.pythonchallenge.com/pc/def/integrity.html').text
garbage = re.search(r'<!--(?P<garbage>.*)-->', text, flags=re.DOTALL).groupdict()['garbage']
auth = re.search(r"un: '(?P<un>.*?)'.*?pw: '(?P<pw>.*?)'", garbage, flags=re.DOTALL).groupdict()
print('un:', codecs.decode(codecs.decode(auth['un'], 'unicode_escape').encode('latin-1'), 'bz2').decode())
print('pw:', codecs.decode(codecs.decode(auth['pw'], 'unicode_escape').encode('latin-1'), 'bz2').decode())


# Q9 - http://www.pythonchallenge.com/pc/return/good.html
import matplotlib.pyplot as plt  # noqa isort:skip
text = requests.get('http://www.pythonchallenge.com/pc/return/good.html', auth=('huge', 'file')).text
first, second = re.search(r"first:\n(?P<first>.*?)\n\nsecond:\n(?P<second>.*?)\n\n", text, flags=re.DOTALL).groupdict().values()
first = list(map(int, ''.join(first.split()).split(',')))
second = list(map(int, ''.join(second.split()).split(',')))
plt.figure()
plt.plot(first[::2], first[1::2], '.-')
plt.plot(second[::2], second[1::2], '.-')
plt.gca().invert_yaxis()
plt.show(block=False)


# Q10 - http://www.pythonchallenge.com/pc/return/bull.html
from itertools import groupby  # noqa isort:skip
a = ['1']
for _ in range(30):
    a.append(''.join([f"{len(e)}{e[0]}" for e in [list(g) for k, g in groupby(a[-1])]]))
print(len(a[30]))


# Q11 - http://www.pythonchallenge.com/pc/return/5808.html
response = requests.get('http://www.pythonchallenge.com/pc/return/cave.jpg', auth=('huge', 'file'), stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)
pixels = image.load()
for x in range(image.width):
    for y in range(image.height):
        if (x + y) % 2 == 1:
            pixels[x, y] = (0, 0, 0)
image.show()


# Q12 - http://www.pythonchallenge.com/pc/return/evil.html
print(requests.get('http://www.pythonchallenge.com/pc/return/evil4.jpg', auth=('huge', 'file')).text)
response = requests.get('http://www.pythonchallenge.com/pc/return/evil2.gfx', auth=('huge', 'file'))
FILE_TYPES = ['jpg', 'png', 'gif', 'png', 'jpg']
for i in range(5):
    with open(f'q12_{i}.{FILE_TYPES[i]}', 'wb') as f:
        f.write(response.content[i::5])
print('Files written out to q12_...')


# Q13 - http://www.pythonchallenge.com/pc/return/disproportional.html
with xmlrpc.client.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php') as proxy:
    print(proxy.phone('Bert'))


# Q14 - http://www.pythonchallenge.com/pc/return/italy.html
response = requests.get('http://www.pythonchallenge.com/pc/return/wire.png', auth=('huge', 'file'), stream=True)
response.raw.decode_content = True
image = Image.open(response.raw)
pixels = image.load()
i = Image.new('RGB', (100, 100))
p = i.load()
for y in range(i.height):
    for x in range(i.width):
        p[x, y] = pixels[y * i.width + x, 0]
i.show()
# widths = [i * 2 for i in range(198, 0, -4)]
# i = Image.new('RGB', (396, 50))
# p = i.load()
# for y in range(i.height):
#     for x in range(widths[y]):
#         p[x, y] = pixels[sum(widths[:y]) + x, 0]
# i.show()
widths = [i // 2 for i in range(200, 1, -1)]
i = Image.new('RGB', (100, 100))
p = i.load()
pos = (-1, 0)
for c in range(len(widths)):
    xdir = (c + 3) % 4 // 3 - (c + 1) % 4 // 3
    ydir = (c + 2) % 4 // 3 - c % 4 // 3
    for z in range(widths[c]):
        pos = (pos[0] + xdir, pos[1] + ydir)
        p[pos[0], pos[1]] = pixels[sum(widths[:c]) + z, 0]
i.show()


# Q15 - http://www.pythonchallenge.com/pc/return/uzi.html
import calendar  # noqa isort:skip
possible_years = [y for y in range(1006, 1997, 10) if calendar.isleap(y) and calendar.weekday(y, 1, 26) == 0]
# He ain't the youngest, he is the second.
print(possible_years[-2])
# todo: buy flowers for tomorrow
# -> wikipedia Jan 27 1756


# Q16 - http://www.pythonchallenge.com/pc/return/mozart.html
response = requests.get('http://www.pythonchallenge.com/pc/return/mozart.gif', auth=('huge', 'file'), stream=True)
response.raw.decode_content = True
image = Image.open(response.raw).convert('RGB')
pixels = image.load()
i = Image.new('RGB', (image.width, image.height))
p = i.load()
for y in range(image.height):
    for x in range(image.width):
        if pixels[x, y] == (255, 0, 255):
            offset = x
            break
    for x in range(image.width):
        p[(x - offset) % image.width, y] = pixels[x, y]
i.show()


# Q17 - http://www.pythonchallenge.com/pc/return/romance.html
import urllib.parse  # noqa isort:skip
next_busynothing = '12345'
result = ''
for _ in range(400):
    response = requests.get(f'http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing={next_busynothing}')
    text = response.text
    result += response.cookies['info']
    try:
        next_busynothing = re.search(r'next busynothing is (?P<busynothing>\d+)', text).groupdict()['busynothing']
    except AttributeError:
        print(text)
        break
    print(f"{text} --> {next_busynothing} [{response.cookies['info']}]")
print(codecs.decode(urllib.parse.unquote_plus(result, 'latin-1').encode('latin-1'), 'bz2').decode())
with xmlrpc.client.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php') as proxy:
    print(proxy.phone('Leopold'))
response = requests.post('http://www.pythonchallenge.com/pc/stuff/violin.php', cookies={'info': 'the flowers are on their way'})
print(response.content.decode().split('\n')[-4][:-7])


# Q18 - http://www.pythonchallenge.com/pc/return/balloons.html, http://www.pythonchallenge.com/pc/return/brightness.html
import difflib  # noqa isort:skip
import gzip  # noqa isort:skip
deltas = requests.get('http://www.pythonchallenge.com/pc/return/deltas.gz', auth=('huge', 'file'), stream=True)
res = gzip.decompress(deltas.content).decode()
left = []
right = []
for line in res.split('\n'):
    leftline = line[:53].strip()
    if leftline:
        left.append(leftline)
    rightline = line[56:].strip()
    if rightline:
        right.append(rightline)
same = [d[2:] for d in difflib.ndiff(left, right) if d.startswith('  ')]
diff_pos = [d[2:] for d in difflib.ndiff(left, right) if d.startswith('+ ')]
diff_neg = [d[2:] for d in difflib.ndiff(left, right) if d.startswith('- ')]
Image.open(BytesIO(codecs.decode(''.join(' '.join(same).split()), 'hex'))).show()
Image.open(BytesIO(codecs.decode(''.join(' '.join(diff_pos).split()), 'hex'))).show()
Image.open(BytesIO(codecs.decode(''.join(' '.join(diff_neg).split()), 'hex'))).show()


# Q19 - http://www.pythonchallenge.com/pc/hex/bin.html
import os  # noqa isort:skip
import email  # noqa isort:skip
text = requests.get('http://www.pythonchallenge.com/pc/hex/bin.html', auth=('butter', 'fly')).text
raw_msg = re.search(r'<!--\n(?P<raw_msg>.*)-->', text, flags=re.DOTALL).groupdict()['raw_msg']
msg = email.message_from_string(raw_msg)
for part in msg.walk():
    if not part.is_multipart():
        open(f'q19_{part.get_filename()}', 'wb').write(part.get_payload(decode=True))
print('File written out to q19_...')
os.system('open q19_indian.wav')

# http://www.pythonchallenge.com/pc/hex/sorry.html
# - "what are you apologizing for?"

# http://www.pythonchallenge.com/pc/hex/india.html
# nnn. what could this mean?
