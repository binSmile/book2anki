import sys
import csv
import re

ifile = '2022 - Paoletta - Gap size-dependent plasmonic enhancement in TJ.txt' # txt or epub
startW = 0 # word for start
ToLang = 'ru'


from translate import Translator
try:
    with open('email.txt', encoding="utf-8") as f:
        email = f.read()
except:
    print('Put your email adress to "email.txt" for extend limit')
    email = False
translator = Translator(to_lang=ToLang,email=email)


def gettext(name):
    if name[-3:] == 'epub':
        from epub2txt import epub2txt
        res = epub2txt(name)
        return res
    elif name[-3:] == 'txt':
        with open(name, encoding="utf-8") as f:
            read_data = f.read()
            return read_data
    else:
        print('I don\'t know how to open it')
        sys.exit()


def num_there(s):
    return any(i.isdigit() for i in s)


def analize(text):

    text = text.title()
    words = text.split()
    words = [word.strip('.,!;():[]—') for word in words]
    dellist = ["'s", '&', '?', '’s', 'n’t', ',', '.',':']

    for dl in dellist:
        words = [word.replace(dl, '') for word in words]


    patternNotEn = re.compile(r'[^a-zA-Z]')

    # finding unique
    unique = []
    for word in words:
        if not patternNotEn.search(word) \
                    and len(word) > 2 \
                    and word not in unique:
                        unique.append(word)

    # for word in words:
    #     if not num_there(word) \
    #             and len(word) > 2 \
    #             and 'http' not in word \
    #             and word not in unique:
    #                 unique.append(word)

    # sort
    unique.sort()
    return unique


def translateWord(word):
    # print(word)
    try:
        value = translator.translate(word)
        if 'MYMEMORY WARNING' in value:
            print(value)
            sys.exit(1)
        elif len(value) > 30:
            print('Some problems with %s. Was translated as: %s' % (word,value))
        return value
    except:
        print('Problems with translation on "%s"' % word)


def SaveData(res_dct,outfile):
    with open(outfile, 'w', newline='',encoding="utf-8") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['En', ToLang])
        for k in res_dct:
            print(k)
            spamwriter.writerow([k,res_dct[k]])

def start_progress(title):
    global progress_x
    sys.stdout.write(title + ": [" + "-"*40 + "]" + chr(8)*41)
    sys.stdout.flush()
    progress_x = 0

def progress(x):
    global progress_x
    x = int(x * 40 // 100)
    sys.stdout.write("#" * (x - progress_x))
    sys.stdout.flush()
    progress_x = x

def end_progress():
    sys.stdout.write("#" * (40 - progress_x) + "]\n")
    sys.stdout.flush()


if __name__ == '__main__':
    text = gettext(ifile)
    stat = analize(text)
    print('I found %s uniq words.' % len(stat))
    # Restriction for  50000 chars/day (with email)
    counter = 0
    if email:
        CounterLimit = 50000
    else:
        CounterLimit = 5000 # Free, anonymous usage is limited to 5000 chars/day by MyMemory
    res_dct = {}
    start_progress('Translating')
    for i in range(startW, len(stat)):
        counter += len(stat[i])
        if counter < CounterLimit:
            progress(i/(len(stat)))
            res_dct[stat[i]] = translateWord(stat[i])
        else:
            print('The limit was reach for today. Start from %s\'s word' % i)
    end_progress()
    SaveData(res_dct,'AnkiDesk.csv')
    print('Success')
