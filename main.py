# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# bdir = 'C:\\Users\\al\\ExtDrive\\GlobalProjects\\STM-Electroluminescence\\Literature\\'

ifile = 'C:\\Users\\al\\ExtDrive\\PhysicsStorage\\insomania\\python\\pyPdf2EN\\The_Flatshare_by_Beth_O_39_Leary.epub'
# file = '2022 - Paoletta - Gap size-dependent plasmonic enhancement in TJ.txt'

def gettext(name):
    from epub2txt import epub2txt
    res = epub2txt(name)
    return res

def num_there(s):
    return any(i.isdigit() for i in s)

def analize(text):
    text = text.lower()
    words = text.split()
    words = [word.strip('.,!;()[]') for word in words]
    words = [word.replace("'s", '') for word in words]

    # finding unique
    unique = []
    for word in words:
        if not num_there(word):
            if word not in unique:
                if len(word) > 2:
                    unique.append(word)

    # sort
    unique.sort()
    res = unique


def translateWord(word):
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = gettext(ifile)
    stat = analize(text)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
