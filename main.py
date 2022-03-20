import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import smtplib

def createGmailPasswort():
    gmail_password = ""
    with open("gmailPasswort.txt", "r", encoding="utf8") as file:
        for line in file:
            gmail_password = line
    return gmail_password
    
def createGmailUser():
    gmail_user = ""
    with open("gmailUser.txt", "r", encoding="utf8") as file:
        for line in file:
            gmail_user = line
    return gmail_user
    

# Dinge fuer die Email
gmail_user = createGmailUser()
gmail_password = createGmailPasswort()

sent_from = gmail_user
to = gmail_user
subject = 'Ebay-Kleinanzeigen'
body = "Es gibt eine neue Anzeige, die interessant aussieht."

email_text = """\
From: %s
To: %s
Subject: %s
%s
""" % (sent_from, ", ".join(to), subject, body)


now = datetime.now()
prefix = "[" + now.strftime("%H:%M:%S") + "] - "

# Eine Funktion um eine Text-Datei zu beschreiben.
def writeFile(response, name ,fileType):
    with open(name + fileType, "a", encoding="utf8") as f:
        f.write(response)


def checkconnection():
    device = socket.gethostbyname("raspberrypi")

    time.sleep(10)
    if os.system("ping -c 1 " + device) == 0:
        print ("Device ist erreichbar")
        return True
    else:
        print ("Device ist NICHT erreichbar")
        return False

def createURL():
    URL = ""
    with open("url.txt", "r", encoding="utf8") as file:
        for line in file:
            URL = line
    return URL


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}

URL = createURL()

# Gibt den HTML text der Website in eine Variable wieder.
response = requests.get(url=URL, headers=headers)

# Setzt den Content der Website in eine Variable.
page = response.content

# Erstellt eine BeautifulSoup-Instanz mit dem Website-Content und einem passendem Parser.
soup = BeautifulSoup(page, "html.parser")

# Setzt die Search-Results-Content in eine Variable.
srchRsltsContent = soup.find("div", id="srchrslt-content")

# Setzt die Einträge inheralb der Seach-Results und dem Table dortdrinn in eine Variable / Array.
srchRslts = soup.find_all("li")

def createGreenlist():
    greenlist = []
    with open("greenlist.txt", "r", encoding="utf8") as file:
        for line in file:
            greenlist += [line.strip()]
    return greenlist

def createBlacklist():
    blacklist = []
    with open("blacklist.txt", "r", encoding="utf8") as file:
        for line in file:
            blacklist += [line.strip()]
    return blacklist

def createBlacklistBsp():
    blacklistbsp = []
    with open("blacklistbsp.txt", "r", encoding="utf8") as file:
        for line in file:
            blacklistbsp += [line.strip()]
    return blacklistbsp



# Liste fuer Begriffe die im Titel vorkommen muessen
greenlist = createGreenlist()
# Liste mit Begriffen die nicht im Titel vorkommen duerfen
blacklist = createBlacklist()
# Liste mit Begriffen die nicht in der Beschreibung vorkommen duerfen
blacklistbsp = createBlacklistBsp()

print(URL)

schonvorhandenArt = []
schonvorhandenBsp = []


def sortElementsByTitle():
    artcounter = 0
    for srchRslt in srchRslts:
        # Nimmt sich alles mit dem <strong> tag.
        preise = srchRslt.find_all("strong")
        # Nimmt sich alles mit dem <a> tag und der ellipsis Klasse.
        articels = soup.find_all("a", class_="ellipsis", href=True)
        # Geht durch jedes Element mit dem <a> tag und der ellipsis Klasse durch.
        for art in articels:
            artcounter = artcounter + 1
            if(artcounter <= 27):
                s = any(d  in art.text for d in greenlist) #prueft ob ein Elemnent aus greenlis im Titel ist
                if s:
                    y = any(x  in art.text for x in blacklist)  #prueft ob ein Elemnent aus blacklist im Titel ist
                    if not y:  # Wenn der Titel kein Element aus blacklist enthaelt werden alle uebrig gebliebene Titel ausgegeben
                        n2 = any(m2  in art.text for m2 in schonvorhandenArt)
                        if not n2:
                            schonvorhandenArt.append(art.text)
                            sortElementsByDescription(art, art.text)


def sortElementsByDescription(pString, name):
    URL2 = "https://www.ebay-kleinanzeigen.de" + pString.get("href")
    response2 = requests.get(url=URL2, headers=headers)
    page2 = response2.content
    soup2 = BeautifulSoup(page2, "html.parser")
    srchRsltsContent2 = soup2.find("div", class_="splitlinebox l-container-row")
    srchRslts2 = soup2.find_all("p")
    for srchRslt2 in srchRslts2:
        beschreibung = soup2.find_all("p", class_="text-force-linebreak")
        for bsp in beschreibung:
            w = any(g  in bsp.text for g in blacklistbsp)
            if not w:
                n = any(m  in bsp.text for m in schonvorhandenBsp)
                if not n:
                    schonvorhandenBsp.append(bsp.text)
                    print(name)
                    print(bsp.text)
                    print("")
                    print("")
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.ehlo()
                    server.login(gmail_user, gmail_password)
                    server.sendmail(sent_from, to, email_text + "Rennrad: " + URL2)
                    server.close
                   

while True:
    #if(checkconnection()):
    response = requests.get(url=URL, headers=headers)
    page = response.content
    soup = BeautifulSoup(page, "html.parser")
    time.sleep(3)
    sortElementsByTitle()

