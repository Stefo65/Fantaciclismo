import bs4, requests, webbrowser
from pprint import pprint

def get_list_giro(url):
    LINK = url
    PRE_LINK = 'race.asp?raceid='
    PRELINK_STAGE = 'https://cqranking.com/men/asp/gen/'
    response = requests.get(LINK)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    table_url = soup.find('table', class_=['border', 'bordertop'])
    try:
        a_tappe = table_url.find_all('a')
    except AttributeError:
        return str('1')

    lista_tappe = []
    for a_tappa in a_tappe:
        link_tappa = str(a_tappa.get('href'))
        if PRE_LINK in link_tappa:
            lista_tappe.append(PRELINK_STAGE + link_tappa)
    return lista_tappe


PRELINK_RACE = 'https://cqranking.com/men/asp/gen/race.asp?raceid='
PRELINK_TOUR = 'https://cqranking.com/men/asp/gen/tour.asp?tourid='

tipo = input('(G)iro, (L)inea...: ')

if tipo.upper()=='L':
    i = int(input('Inserisci id race: '))
    #fine = i + 1
    numRiders = 20
    LINK = PRELINK_RACE + str(i)
if tipo.upper()=='G':
    i = int(input('Inserisci id tour: '))
   # numTappe = int(input('Inserisci il numero di tappe: '))
   # fine = i + numTappe + 1
    numRiders = 4
    LINK = PRELINK_TOUR + str(i)

gara = input('Inserisci il nome della gara: ')

CONTROL_RIDER = "riderid"
CONTROL_STAGE = gara
gara += '.xls'
#da 39757 a 39777
#i = 39757
#fine = 39778

lista_url = []
if tipo.upper()=='L':
    lista_url.append(LINK)

if tipo.upper()=='G':
    lista_url = get_list_giro(LINK)

f = open(gara, 'a')

for url in lista_url:
#while i < fine:
    #LINK = PRELINK_RACE + str(i)
    #scarico la pagina
    response = requests.get(url)
    #verifica della riuscita dello scarico
    response.raise_for_status()
    #pprint(response.text)
    #estraggo il testo html
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    #identifico la table per il titolo
    table_titolo = soup.find('table', class_='borderNoOpac')
    th_titolo = table_titolo.find_all('th')
    #pprint(th_titolo)
    #identifico la table per la classifica
    table_classifica = soup.find('table', class_=['border', 'bordertop'])
    try:
        a_classifica = table_classifica.find_all('a')
    except AttributeError:
        break
    #creo lista
    lista_classifica = []

    for elemento in a_classifica:
        if CONTROL_RIDER in str(elemento.get('href')):
            rider = str(elemento.get_text())
            lista_classifica.append(rider)

    #funzione pretty print
    #pprint(lista_classifica)

    for elemento in th_titolo:
        if CONTROL_STAGE in str(elemento.get_text()):
            titolo = str(elemento.get_text())
            f.write('%s\n' % titolo)
            f.write("\n")

    for rider in lista_classifica[0:numRiders]:
        f.write('%s\n' % rider)

    #i += 1

f.close()

input('\n Adesso puoi inserire i risultati su Fantaciclismo ...')
