#!/usr/bin/python3
#-*- encoding: Utf-8 -*-
from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory

from collections import OrderedDict
from asyncio import get_event_loop
from subprocess import run, PIPE
from colorsys import hsv_to_rgb
from binascii import a2b_base64
from json import loads, dumps
from time import time, sleep
from copy import deepcopy
from hashlib import md5
from struct import pack
from shlex import quote
from html import escape
from os import urandom
from re import sub
import _thread
import magic

from salt import SALT

pokemon = {1:'Bulbizarre',2:'Herbizarre',3:'Florizarre',4:'Salamèche',5:'Reptincel',6:'Dracaufeu',7:'Carapuce',8:'Carabaffe',9:'Tortank',10:'Chenipan',11:'Chrysacier',12:'Papilusion',13:'Aspicot',14:'Coconfort',15:'Dardargnan',16:'Roucool',17:'Roucoups',18:'Roucarnage',19:'Rattata',20:'Rattatac',21:'Piafabec',22:'Rapasdepic',23:'Abo',24:'Arbok',25:'Pikachu',26:'Raichu',27:'Sabelette',28:'Sablaireau',29:'Nidoran♀',30:'Nidorina',31:'Nidoqueen',32:'Nidoran♂',33:'Nidorino',34:'Nidoking',35:'Mélofée',36:'Mélodelfe',37:'Goupix',38:'Feunard',39:'Rondoudou',40:'Grodoudou',41:'Nosferapti',42:'Nosferalto',43:'Mystherbe',44:'Ortide',45:'Rafflesia',46:'Paras',47:'Parasect',48:'Mimitoss',49:'Aéromite',50:'Taupiqueur',51:'Triopikeur',52:'Miaouss',53:'Persian',54:'Psykokwak',55:'Akwakwak',56:'Férosinge',57:'Colossinge',58:'Caninos',59:'Arcanin',60:'Ptitard',61:'Tétarte',62:'Tartard',63:'Abra',64:'Kadabra',65:'Alakazam',66:'Machoc',67:'Machopeur',68:'Mackogneur',69:'Chétiflor',70:'Boustiflor',71:'Empiflor',72:'Tentacool',73:'Tentacruel',74:'Racaillou',75:'Gravalanch',76:'Grolem',77:'Ponyta',78:'Galopa',79:'Ramoloss',80:'Flagadoss',81:'Magneti',82:'Magneton',83:'Canarticho',84:'Doduo',85:'Dodrio',86:'Otaria',87:'Lamantine',88:'Tadmorv',89:'Grotadmorv',90:'Kokiyas',91:'Crustabri',92:'Fantominus',93:'Spectrum',94:'Ectoplasma',95:'Onix',96:'Soporifik',97:'Hypnomade',98:'Krabby',99:'Krabboss',100:'Voltorbe',101:'Electrode',102:'Noeunoeuf',103:'Noadkoko',104:'Osselait',105:'Ossatueur',106:'Kicklee',107:'Tygnon',108:'Excelangue',109:'Smogo',110:'Smogogo',111:'Rhinocorne',112:'Rhinoféros',113:'Leveinard',114:'Saquedeneu',115:'Kangourex',116:'Hypotrempe',117:'Hypocéan',118:'Poissirène',119:'Poissoroy',120:'Stari',121:'Staross',122:'Mr.Mime',123:'Insécateur',124:'Lippoutou',125:'Elektek',126:'Magmar',127:'Scarabrute',128:'Tauros',129:'Magicarpe',130:'Léviator',131:'Lokhlass',132:'Métamorph',133:'Evoli',134:'Aquali',135:'Voltali',136:'Pyroli',137:'Porygon',138:'Amonita',139:'Amonistar',140:'Kabuto',141:'Kabutops',142:'Ptéra',143:'Ronflex',144:'Artikodin',145:'Electhor',146:'Sulfura',147:'Minidraco',148:'Draco',149:'Dracolosse',150:'Mewtwo',151:'Mew',152:'Germignon',153:'Macronium',154:'Méganium',155:'Héricendre',156:'Feurisson',157:'Typhlosion',158:'Kaïminus',159:'Crocrodil',160:'Aligatueur',161:'Fouinette',162:'Fouinar',163:'Hoot-hoot',164:'Noarfang',165:'Coxy',166:'Coxyclaque',167:'Mimigal',168:'Migalos',169:'Nostenfer',170:'Loupio',171:'Lanturn',172:'Pichu',173:'Mélo',174:'Toudoudou',175:'Togépi',176:'Togétic',177:'Natu',178:'Xatu',179:'Wattouat',180:'Lainergie',181:'Pharamp',182:'Joliflor',183:'Marill',184:'Azumarill',185:'Simularbre',186:'Tarpaud',187:'Granivol',188:'Floravol',189:'Cotovol',190:'Capumain',191:'Tournegrin',192:'Héliatronc',193:'Yanma',194:'Axoloto',195:'Maraiste',196:'Mentali',197:'Noctali',198:'Cornebre',199:'Roigada',200:'Feuforêve',201:'Zarbi',202:'Qulbutoke',203:'Girafarig',204:'Pomdepic',205:'Foretress',206:'Insolourdo',207:'Scorplane',208:'Steelix',209:'Snubbull',210:'Granbull',211:'Qwilfish',212:'Cizayox',213:'Caratroc',214:'Scarhino',215:'Farfuret',216:'Teddiursa',217:'Ursaring',218:'Limagma',219:'Volcaropod',220:'Marcacrain',221:'Cochignon',222:'Corayon',223:'Remoraid',224:'Octillery',225:'Cadoizo',226:'Demanta',227:'Airmure',228:'Malosse',229:'Démolosse',230:'Hyporoi',231:'Phanpy',232:'Donphan',233:'Porygon2',234:'Cerfrousse',235:'Queulorior',236:'Débugant',237:'Kapoera',238:'Lippouti',239:'Elekid',240:'Magby',241:'Ecremeuh',242:'Leuphorie',243:'Raïkou',244:'Enteï',245:'Suicune',246:'Embrylex',247:'Ymphect',248:'Tyranocif',249:'Lugia',250:'Ho-oh',251:'Célébi',252:'Arcko',253:'Massko',254:'Jungko',255:'Poussifeu',256:'Galifeu',257:'Brasegali',258:'Gobou',259:'Flobio',260:'Laggron',261:'Medhyena',262:'Grahyena',263:'Zigzaton',264:'Lineon',265:'Chenipotte',266:'Armulys',267:'Charmillon',268:'Blindalys',269:'Papinox',270:'Nenupiot',271:'Lombre',272:'Ludicolo',273:'Grainipiot',274:'Pifeuil',275:'Tengalice',276:'Nirondelle',277:'Heledelle',278:'Goelise',279:'Bekipan',280:'Tarsal',281:'Kirlia',282:'Gardevoir',283:'Arakdo',284:'Maskadra',285:'Balignon',286:'Chapignon',287:'Parecool',288:'Vigoroth',289:'Monaflemit',290:'Ningale',291:'Ninjask',292:'Munja',293:'Chuchmur',294:'Ramboum',295:'Brouhabam',296:'Makuhita',297:'Hariyama',298:'Azurill',299:'Tarinor',300:'Skitty',301:'Delcatty',302:'Tenefix',303:'Mysdibule',304:'Galekid',305:'Galegon',306:'Galeking',307:'Meditikka',308:'Charmina',309:'Dynavolt',310:'Elecsprint',311:'Posipi',312:'Negapi',313:'Muciole',314:'Lumivole',315:'Roselia',316:'Gloupti',317:'Avaltout',318:'Carvanha',319:'Sharpedo',320:'Wailmer',321:'Wailord',322:'Chamallot',323:'Camerupt',324:'Chartor',325:'Spoink',326:'Groret',327:'Spinda',328:'Kraknoix',329:'Vibrannif',330:'Libegon',331:'Cacnea',332:'Cacturne',333:'Tylton',334:'Altaria',335:'Mangriff',336:'Seviper',337:'Seleroc',338:'Solaroc',339:'Barloche',340:'Barbicha',341:'Ecrapince',342:'Colhomar',343:'Balbuto',344:'Kaorine',345:'Lilia',346:'Vacilys',347:'Anorith',348:'Armaldo',349:'Barpau',350:'Milobellus',351:'Morpheo',352:'Kecleon',353:'Polichombr',354:'Branette',355:'Skelenox',356:'Teraclope',357:'Tropius',358:'Eoko',359:'Absol',360:'Okéoké',361:'Stalgamin',362:'Oniglali',363:'Obalie',364:'Phogleur',365:'Kaimorse',366:'Coquiperl',367:'Serpang',368:'Rosabyss',369:'Relicanth',370:'Lovdisc',371:'Draby',372:'Drakhaus',373:'Drattak',374:'Terhal',375:'Metang',376:'Metalosse',377:'Regirock',378:'Regice',379:'Registeel',380:'Latias',381:'Latios',382:'Kyogre',383:'Groudon',384:'Rayquaza',385:'Jirachi',386:'Deoxys',387:'Tortipouss',388:'Boskara',389:'Torterra',390:'Ouisticram',391:'Chimpenfeu',392:'Simiabraz',393:'Tiplouf',394:'Prinplouf',395:'Pingoleon',396:'Étourmi',397:'Étourvol',398:'Étouraptor',399:'Keunotor',400:'Castorno',401:'Crikzik',402:'Melocrik',403:'Lixy',404:'Luxio',405:'Luxray',406:'Rozbouton',407:'Roserade',408:'Kranidos',409:'Charkos',410:'Dinoclier',411:'Bastiodon',412:'Cheniti',413:'Cheniselle',414:'Papilord',415:'Apitrini',416:'Apireine',417:'Pachirisu',418:'Mustebouée',419:'Musteflott',420:'Ceribou',421:'Ceriflor',422:'Sancoki',423:'Tritosor',424:'Capidextre',425:'Baudrive',426:'Grodrive',427:'Laporeille',428:'Lockpin',429:'Magirêve',430:'Corboss',431:'Chaglam',432:'Chaffreux',433:'Korillon',434:'Moufouette',435:'Moufflair',436:'Archeomire',437:'Archeodong',438:'Manzaï',439:'MimeJr.',440:'Ptiravi',441:'Pijako',442:'Spiritomb',443:'Griknot',444:'Carmache',445:'Carchacrok',446:'Goinfrex',447:'Riolu',448:'Lucario',449:'Hippopotas',450:'Hippodocus',451:'Rapion',452:'Drascore',453:'Cradopaud',454:'Coatox',455:'Vortente',456:'Ecayon',457:'Lumineon',458:'Babimanta',459:'Blizzi',460:'Blizzaroi',461:'Dimoret',462:'Magnezone',463:'Coudlangue',464:'Rhinastoc',465:'Bouldeneu',466:'Elekable',467:'Maganon',468:'Togekiss',469:'Yanmega',470:'Phyllali',471:'Givrali',472:'Scorvol',473:'Mammochon',474:'Porygon-Z',475:'Gallame',476:'Tarinorme',477:'Noctunoir',478:'Momartik',479:'Motisma',480:'Crehelf',481:'Crefollet',482:'Crefadet',483:'Dialga',484:'Palkia',485:'Heatran',486:'Regigigas',487:'Giratina',488:'Cresselia',489:'Phione',490:'Manaphy',491:'Darkrai',492:'Shaymin',493:'Arceus'}



clients = {}
users = {}
refcnts = {}
backlog = {}
imglog = {}

# Alias with default parameters
json = lambda obj: dumps(obj, ensure_ascii=False, separators=(',', ':')).encode('utf8')

def imgPurge():
    MAXIMGS = 100
    while True:
        sleep(60)
        for room in imglog:
            if len(imglog[room]) < MAXIMGS:
                continue

            purge = imglog[room][:-MAXIMGS]
            imglog[room] = imglog[room][-MAXIMGS:]
            for img in purge:
                run("rm static/img/uploads/%s" % img).stdout


class LoultServer(WebSocketServerProtocol):

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))
        
        retn = {}
        try:
            ck = request.headers['cookie'].split('id=')[1].split(';')[0]
        
        except (KeyError, IndexError):
            ck = urandom(16).hex()
            retn = {'Set-Cookie': 'id=%s; expires=Tue, 19 Jan 2038 03:14:07 UTC; Path=/' % ck}
        
        ck = md5((ck + SALT).encode('utf8')).digest()
        
        self.speed = (ck[5] % 50) + 100
        self.pitch = ck[0] % 100
        self.voiceId = ck[1]
        
        self.pokeid = (ck[2] | (ck[3] << 8)) % len(pokemon) + 1
        self.pokename = pokemon[self.pokeid]
        
        self.color = hsv_to_rgb(ck[4] / 255, 1, 0.5)
        self.color = '#' + pack('3B', *(int(255 * i) for i in self.color)).hex()
        
        self.userid = ck.hex()[-5:]
        
        self.channel = request.path.lower().split('/', 2)[-1]
        self.cnx = False
        self.sendend = 0
        self.lasttxt = 0
       
        return (None, retn)

    def onOpen(self):
        print("WebSocket connection open.")
        
        info = {
            'userid': self.userid,
            'params': {
                'name': self.pokename,
                'img': '/pokemon/%s.gif' % str(self.pokeid).zfill(3),
                'color': self.color
            }
        }
        
        if self.channel not in clients:
            clients[self.channel] = set()
            users[self.channel] = OrderedDict()
            refcnts[self.channel] = {}
            
            if self.channel not in backlog:
                backlog[self.channel] = []
        
        if self.userid not in refcnts[self.channel]:
            for i in clients[self.channel]:
                i.sendMessage(json({
                    'type': 'connect',
                    **info
                }))
            refcnts[self.channel][self.userid] = 1
            users[self.channel][self.userid] = info
        
        else:
            refcnts[self.channel][self.userid] += 1
        
        clients[self.channel].add(self)
        
        self.cnx = True
        
        myUsers = deepcopy(users)
        myUsers[self.channel][self.userid]['params']['you'] = True
        self.sendMessage(json({
            'type': 'userlist',
            'users': list(myUsers[self.channel].values())
        }))
        
        self.sendMessage(json({
            'type': 'backlog',
            'msgs': backlog[self.channel]
        }))

    def onMessage(self, payload, isBinary):
        msg = loads(payload.decode('utf8'))
        
        if msg['type'] == 'msg':
            text = msg['msg'][:500]
            text = sub('(https?://[^ ]*[^.,?! :])', 'cliquez mes petits chatons', text)
            text = text.replace('#', 'hashtag ')
            text = quote(text.strip(' -"\'`$();:.'))
            
            now = time()
            
            if now - self.lasttxt <= 0.1:
                return
            self.lasttxt = now

            # File support

            fName = False
            if 'raw' in msg and msg['raw']:
                allowedTypes = { "image/jpeg":"jpg", "image/png": "png" }
                try:
                    rawData = a2b_base64(msg['raw'].split(",")[1])

                except:
                    return

                mime = magic.Magic(mime = True)
                mime = mime.from_buffer(rawData)

                if mime not in allowedTypes:
                    return

                fName = "%s%d.%s" % (self.userid, now, allowedTypes[mime])
                fh = open('static/img/uploads/' + fName, 'wb') # Relative to script
                fh.write(rawData)
                fh.close()

                if self.channel not in imglog:
                    imglog[self.channel] = []
                imglog[self.channel].append(fName)

            # Language support
            
            if 'lang' in msg and msg['lang'] in ['en', 'es', 'de']:
                if msg['lang'] == 'en':
                    lang, voice = 'us', (1, 2, 3)
                elif msg['lang'] == 'es':
                    lang, voice = 'es', (1, 2)
                elif msg['lang'] == 'de':
                    lang, voice = 'de', (4, 5, 6, 7)
            else:
                lang, voice = 'fr', (1, 2, 3, 4, 6, 7)
            
            voice = voice[self.voiceId % len(voice)]
            
            if lang != 'fr':
                sex = voice
            else:
                sex = 4 if voice in (2, 4) else 1

            #volume = {'us3': 3.48104, 'fr3': 1.01283, 'fr5': 2.44384, 'es1': 3.26885, 'fr6': 1.35412, 'us2': 1.7486, 'fr2': 1.60851, 'fr1': 1.17138, 'us1': 1.658, 'es2': 1.84053, 'fr7': 1.96092, 'fr4': 1.0964}['%s%d' % (lang, voice)]
            volume = 1
            if lang != 'fr' and lang != 'de':
                volume = {'us1': 1.658, 'us2': 1.7486, 'us3': 3.48104, 'es1': 3.26885, 'es2': 1.84053}['%s%d' % (lang, voice)] * 0.5

            """
            if (lang, voice) == ('es', 1):
                volume = 2.5
            elif (lang, voice) == ('us', 3):
                volume = 2
            #elif lang == 'us':
            #    volume = 1.3
            else:
                volume = 1
            """
            
            # Synthesis & rate limit
            
            wav = run('MALLOC_CHECK_=0 espeak -s %d -p %d --pho -q -v mb/mb-%s%d %s | MALLOC_CHECK_=0 mbrola -v %g -e /usr/share/mbrola/%s%d/%s%d - -.wav' % (self.speed, self.pitch, lang, sex, text, volume, lang, voice, lang, voice), shell=True, stdout=PIPE, stderr=PIPE).stdout
            wav = wav[:4] + pack('<I', len(wav) - 8) + wav[8:40] + pack('<I', len(wav) - 44) + wav[44:]
                
            calc_sendend = max(self.sendend, now)
            calc_sendend += len(wav) * 8 / 6000000
            
            synth = calc_sendend < now + 2.5
            if synth:
                self.sendend = calc_sendend
        
            info = {
                'user': users[self.channel][self.userid]['params'],
                'msg': sub('(https?://[^ ]*[^.,?! :])', r'<a href="\1" target="_blank">\1</a>', escape(msg['msg'][:500])),
                'file': fName,
                'date': now * 1000
            }
            
            backlog[self.channel].append(info)
            backlog[self.channel] = backlog[self.channel][-10:]
            
            for i in clients[self.channel]:
                i.sendMessage(json({
                    'type': 'msg',
                    'userid': self.userid,
                    'msg': info['msg'],
                    'file': fName,
                    'date': info['date']
                }))
                
                if synth:
                    i.sendMessage(wav, True)

    def onClose(self, wasClean, code, reason):
        if hasattr(self, 'cnx') and self.cnx:
            try:
                refcnts[self.channel][self.userid] -= 1
                
                if refcnts[self.channel][self.userid] < 1:
                    clients[self.channel].discard(self)
                    del users[self.channel][self.userid]
                    del refcnts[self.channel][self.userid]
                    
                    for i in clients[self.channel]:
                        i.sendMessage(json({
                            'type': 'disconnect',
                            'userid': self.userid
                        }))
                    
                    if not clients[self.channel]:
                        del clients[self.channel]
                        del users[self.channel]
                        del refcnts[self.channel]
                        
                        if not backlog[self.channel]:
                            del backlog[self.channel]
            
            except KeyError:
                pass
        
        print("WebSocket connection closed: {0}".format(reason))


import asyncio

_thread.start_new_thread(imgPurge, ())
factory = WebSocketServerFactory(server='Lou.lt/NG') # 'ws://127.0.0.1:9000', 
factory.protocol = LoultServer
factory.setProtocolOptions(autoPingInterval=60, autoPingTimeout=30)

loop = get_event_loop()
coro = loop.create_server(factory, '127.0.0.1', 9000)
server = loop.run_until_complete(coro)

loop.run_forever()

