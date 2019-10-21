import requests
import urllib
import itertools
import json
import sys

## Bruteforce
# aprire console: 'codicegiocata' serve
# cookie non so

codicegiocata = "6585506_1571645189990"
cookie = "JSESSIONID=7EEEB5C24D327EC25BB91025CB489F6F; _ga=GA1.2.153827826.1566888205; _cb_ls=1; _cb=DuqJZVDRWwEuBJ12rV; wt_geid=eGVUVu6PEa0WmaZDv2Gdfxi4; _chartbeat2=.1571050414212.1571058926148.1.ChcFbID-oQn8CsIpFhCJ_Xlrv90Lq.1; _cb_svref=https%3A%2F%2Fwww.google.com%2F; wt_cdbeid=1; _chartbeat4=t=TJJVzDFpks2D2scnld9D5SCOSAUR&E=70&x=0&c=12.98&y=978&w=963; wt_r=1; wt_rla=292330999892453%2C4%2C1571058926245"
firstWord = "Mosca"
lastWord = "Religiosa"
words = ["Funzione", "Ponte", "Croce", "Bianca", "Comando", "Testa", "Rosa", "Sonora", "Deserto", "Onda"]

# SKIP permutation that does not have word Y in X position [0-9] (e.g. ["Fortuna", 0])
posWords = []
# SKIP permutation that does not have coupled words (e.g ["Fortuna", "Atterraggio"]) 
# niente couples con le first and last word
coupleWords = [["Onda", "Sonora"], ["Comando", "Ponte"], ["Deserto", "Sonora"], ["Testa", "Croce"]]


postUrl = "https://giochi.rsi.ch/gameserver/game/play.do?"

perms = list(itertools.permutations(words))


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def checkPerm(perm):

    # posWords
    for posWord in posWords:
        if perm[posWord[1]] != posWord[0]:
            return False

    # coupleWords
    for coupleWord in coupleWords:
        pos = perm.index(coupleWord[0])
        if pos == 0:
            if perm[pos+1] != coupleWord[1]:
                return False
        if pos == 9:
            if perm[pos-1] != coupleWord[1]:
                return False
        else:
            if perm[pos-1] != coupleWord[1] and perm[pos+1] != coupleWord[1]:
                return False

    
    return True

def sendRequest(data, perm):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
        'Accept': '*/*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookie
    }

    s = requests.Session()
    s.post(postUrl, data=ajaxData)
    content = s.post(postUrl, data=data, headers=headers)
    json_data = json.loads(content.text)
    print(json_data)
    if json_data['risposta'] == True:
        print("\n")
        print("\n")
        print("Trovato!:")
        print("\n")
        print(perm)
        print("\n")
        print("\n")
        quit()

def URLencode(perm):
    x = ""
    count = 0
    length = len(perm) - 1
    for item in perm:
        if count == length:
            x = x + urllib.parse.quote(item)
        else:
            x = x + urllib.parse.quote(item) + "%2C"
        count = count + 1

    return x

count = 1
    
for perm in perms:

    if checkPerm(perm):
        risposta = list(perm)
        risposta.insert(0, firstWord)
        risposta.append(lastWord)
        encoded = URLencode(risposta)
        ajaxData = "codicegiocata=" + codicegiocata + "&listaparole=" + encoded + "&stepnumber=0"
        sendRequest(ajaxData,perm)

    printProgressBar(count, 3628800, prefix = 'Progress:', suffix = 'Complete')
    count = count+1








