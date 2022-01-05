import random
import itertools

### HELPERS ###



# list of 100 common names
names = ['Alessia','Milana','Tahj','Londyn','Annamarie','Eliza','Kinzley','Sukhm','ashley','Mariah','Ashwin','Emery','Ishan','Ariyana','Willa','Desirae','Elsie','Perla','Trevin','Scarlet','Grant','Brooks','Thalia','Jacobi','Chelsea','Ariadne','Kennedi','Kabir','Elin','Isiah','Jadon','Anay','Thea','Kiana','Kingston','Jaylene','Joselin','Nataly','Leanna','Sariah','Taha','Hollis','Amy','Jahlil','Ashly','Kalani','Priscilla','Mazie','Jedidiah','Avalon','Mika','Jubilee','Koby','Lluvia','Vianney','Annika','Chanel','Cesar','Julieta','Milly','Meir','Annalise','Marcello','Dayana','Zeke','Joslynn','Jaden','Alexa','Essence','Caitlyn','Weston','Gabriella','Deonte','Kathy','Mindy','Kaysen','Jovie','Litzy','Susan','Martez','Stuart','Yair','Quinn','Nathalia','Elisha','Raymond','Jadiel','Flora','Foster','Kyra','Jayce','Cadence','Miranda','Lupita','Charley','Lukas','Symphony','Leighton','Coen','Estefania']
# list of 100 randomly generated passwords (meeting the caps, number, length conditions of our program)
passwords = ['EZoGu14dN1bS', '4w489uNW2Azc', '4LFja1704F1u', 'K3I5C4NWK%5v', 'z2yhIzs4hol', 'z_rEPpBL0lEv', 'HXzkJB4rjdqa', 'P4&e5!UFvBu1', 'co@PK1nkwY5a', 'Y?rZDh5d1%#A', 'v3xFv7JDvDc=', 'F259SPhp+8z3', '8kCR+HAGLoB@', 'MRH27E1PDJl6', '789k23iLANka', 's7&^V=a32aI', '8O7k!w3e1Sj', 'RteTVctU?AX4', 'IEHSK2l1r40=', 'Pab#cvC3?5_!', 'c2@0pH20!Xa5', 'h-#bASDF91c#xpo6', '2a194!370Xj3', 'DCgF56%U!99N', 'c9X^OXJyTScC', 'QDjIF&38Xt=d', 'A8Ar4IVI^5y4', '05NjAJVnIv?5', 'Val9u^LjSF_R', 'SpQ15Os0p4Iy', 'Kv5a0CU=d4#9', 'PiyFjX2OyS-T', 'Gm8T1-q4O0Oz', 'ckZuP#GIy3a', '5G_dJIA8O0i&', 'GFi3tm15?0n!', '7iz9mlLLLLL9+elc', '5PVJe88Qtj$9', 'oCenF82j$2', 'ka3J9G6VdjkG', 'i0_OFw49C1YQ', 'V4OAKrbFPeBI', 'YH5TcTlI!qa2', 'M_D1gT@jTXxv', 'CXvwh**6YToL', 'SHd714iaudK&', 'KRQ58@nLiZ99', 'lB80lwB=Dl6', 'M6F3b7?aj5nQ', 'e1&3vu+6_P', '2wV0J^awGn1#', 'Se$W!hIEz0j5', 'Zj2@xu79qk_E', 'jeJp!aDW1a', 'sA=wC9G30V01', 'p@_1PPPl0n8^1&4', 'f14afGJp=m-%', '1lgn=3A0oSgy', 'BXg67AeN6ETT', 'Nb98A5egx6E=', 'e-HK3B#K?BDy', 'ba=BN9GhKW4f', '2a4Eae&%3-iH', 'crpShSXL1Eb', 's907d@tK=K6z', 'TDBJBAslQNuP12', 'I8##x3mFQ-Em', 'Pc3Mc9q304Bg', '2HXiRzgv@6TO', 'YEKFk2svrKoP', '7I6b4%4l8%1w', 'iK2?UF87ST2R', 'uhQ3STAc7f6', '2#5xYe9H?-+d', '3g98cRBLM7pH', 'cwsQsL?KXr15', 'L6ar4KZMo2o', 'H4&4jWzdgVrJ', 't=Q5hLN=5@t', 'F33ebJjp15', 'U7v71wHw79dT', '635jXk1qV%1L', 'c81cgv2fmeR0', '45DbUTND29F&', 'msN2A2-QsiX', '9i+NRT+!G5?g', '3324u6Vj32$d', 'NbBWBI97d82N', 'g12s6LG7+p6+', 'CA4Ugua4+QA1', 'Palwp$Ezv&2S', 'yjB4oaQ3Stc', 'n+be$GNVJR00', '3=ShL-O4RL7B', 'J&06AZxh2r9q', 'z251nRuU9xhE', 'Vcuo1XbsB1X@', 'W?h^%6TG80=', 'zTjl@W2!a8yQ', '10T367Ha3w*9']
# random 9-digit number generator for SSNs and bank routing numnbers 
randomNum = random.randint(100000000,999999999)
# list of 1000 words for messages
wordbank = ["difficulty","roll","bean","sink","mouse","environment","noise","phrase","youth","characteristic","program","older","fell","try","young","exciting","fruit","agree","speech","aloud","continent","expect","highest","reach","substance","kitchen","sad","crack","love","nuts","tank","concerned","movie","addition","thick","neck","excellent","store","chance","strong","point","happily","where","gate","see","water","shelter","carried","minute","prove","repeat","anything","nose","blind","wise","alone","no","acres","back","beat","table","strip","grain","disappear","tea","vessels","mountain","character","block","never","beautiful","partly","worker","proud","scared","possibly","group","laugh","due","knew","hold","doing","bright","whom","feed","rock","play","shoot","cool","riding","pressure","ten","jar","cat","score","original","west","slabs","lost","canal","golden","tired","matter","married","interest","available","railroad","stepped","constantly","completely","measure","airplane","later","review","beside","somehow","cloth","passage","heard","duck","occasionally","read","pick","frozen","lack","gradually","finish","entirely","putting","caught","gun","save","setting","driver","wide","aid","football","poetry","facing","clock","hunt","stomach","equal","worry","good","medicine","empty","rich","had","struggle","hour","suddenly","bottom","atom","gentle","gather","current","grandfather","stopped","atomic","nearer","door","lot","making","ate","temperature","iron","slightly","modern","search","chicken","home","by","salmon","buffalo","shop","took","fought","result","pleasure","vegetable","exercise","thread","basis","or","throw","run","during","choice","busy","theory","maybe","oxygen","sentence","forgot","becoming","pride","sweet","just","kids","almost","so","sent","operation","meal","ahead","barn","upon","warn","spider","supply","month","mad","summer","alike","create","younger","influence","drink","our","taken","exchange","duty","college","rocky","chapter","rain","cloud","leg","hay","captain","herd","somewhere","electric","burst","made","poet","strength","quick","school","fairly","member","got","herself","under","silk","jack","slight","fort","thus","enemy","steady","coat","loss","seat","better","bet","spite","doctor","fed","everything","coffee","car","deeply","general","discuss","faster","outline","sometime","value","solid","personal","said","although","imagine","potatoes","instrument","put","fall","fireplace","leader","additional","eat","process","flag","straw","wet","neighbor","law","social","border","perhaps","balance","pan","settlers","hill","held","are","stick","every","leaf","us","night","box","boy","cattle","story","grandmother","voice","laid","bit","actually","variety","silver","generally","color","wood","whistle","sand","within","plan","wish","feel","mile","plain","cover","wear","lake","human","gold","mathematics","figure","then","me","decide","can","central","drop","cream","paint","parent","importance","unit","eager","onto","game","problem","pleasant","quarter","image","sell","music","court","baseball","instance","exact","stove","division","many","brother","watch","former","hundred","people","given","wait","kind","enough","all","business","heart","between","position","most","coming","pattern","bad","shelf","dream","ability","paper","why","twice","bridge","perfect","those","they","owner","after","seen","important","specific","invented","world","sort","am","broad","lying","is","middle","them","contrast","escape","few","present","garage","that","heading","clearly","bound","white","prevent","development","pocket","hidden","early","struck","proper","composed","cabin","sea","ask","against","smell","visitor","popular","shoulder","gray","equally","which","high","congress","party","band","practice","involved","larger","anyway","market","farmer","wonderful","hair","hearing","native","capital","doubt","safe","brief","recall","twenty","bat","long","we","ring","deep","plate","else","son","smoke","about","while","battle","stared","floor","trail","ever","around","toy","there","fierce","when","nice","shaking","rabbit","helpful","mental","rise","fifteen","except","food","useful","book","suit","able","discussion","ago","simplest","pool","fix","provide","limited","announced","detail","major","correct","some","folks","express","chemical","past","thing","exist","traffic","farther","plural","atmosphere","near","flat","eight","pupil","went","for","directly","father","ordinary","forth","change","sign","six","treated","spend","fair","circle","hit","captured","her","stairs","buried","tales","forget","solution","soldier","smooth","compass","flies","newspaper","verb","greatest","throat","grabbed","sunlight","south","very","comfortable","already","western","widely","planned","enjoy","whatever","pack","tie","fish","mine","park","famous","whispered","burn","situation","tail","determine","giving","sale","adventure","rose","shinning","now","package","center","certainly","vowel","smaller","luck","tool","field","command","egg","black","prepare","tune","handle","him","pen","citizen","star","family","tobacco","printed","into","house","met","frog","basic","seed","wheat","were","pictured","frame","curve","shown","instead","continued","word","women","control","sang","end","stronger","film","refused","section","piano","across","metal","hand","animal","still","shallow","push","blew","stock","sail","curious","stems","climate","river","skill","thank","everyone","pass","island","upper","three","pitch","stand","income","copy","secret","writing","horn","life","themselves","tears","to","claws","hospital","again","successful","gravity","pure","office","headed","bowl","without","hurt","volume","sight","mouth","desert","religious","children","cake","first","red","dirt","instant","slowly","money","written","worse","shirt","complete","top","wrapped","saved","sport","speak","follow","aboard","declared","honor","raw","minerals","spirit","earth","base","unknown","nor","pull","thousand","yourself","anyone","lift","natural","place","sold","behavior","log","castle","idea","spread","child","explore","root","earn","date","soil","opposite","satellites","outer","plane","line","draw","ranch","whose","frequently","badly","angle","softly","week","wolf","light","protection","page","glass","brought","tropical","moving","whenever","exclaimed","bill","way","number","sun","spent","did","rising","keep","zoo","breath","thirty","open","scientist","road","swimming","move","work","principle","baby","careful","seeing","straight","monkey","related","once","square","direction","arrange","simply","nodded","cannot","pilot","drawn","map","visit","dangerous","fuel","calm","mirror","something","led","nature","various","lady","customs","clear","favorite","game","year","matter","announced","leg","graph","song","ocean","lead","will","dish","sheet","known","office","city","rocky","well","trail","return","single","mine","likely","him","complete","cut","difficult","compass","fly","storm","discover","require","character","arrangement","whatever","history","unit","rubbed","sold","silly","till","wear","count","alike","wing","powder","printed","main","foreign","daughter","using","sun","told","dirt","getting","piano","effort","carefully","young","chest","kids","coach","gain","bottle","safety","massage","fat","include","news","its","stronger","settle","duck","begun","smell","identity","example","tears","your","account","wolf","plan","grass","band","lips","sink","sea","stiff","cream","gift","properly","way","sense","frequently","smaller","growth","further","she","actually","earlier","camp","energy","wrote","back","face","language","slave","relationship","useful","control","basket","jump","known","event","door","feel","top","bush","product","definition","higher","buried","compare","create","announced","worth","merely","him","cream","object","various","stiff","saw","fort","slide","week","best","greater","surface","becoming","off","courage","box","worse","touch","ate","list","tropical","honor","supply","plenty","sand","facing","deer","court","heard","fat","consider","ring","probably","arrange","friendly","settlers","minute","skill","independent","sentence","double","telephone","born","suggest","inside","peace","examine","composed","worth","compass","least","basket","easier","party","luck","large","paid","special","greatest","sad","rabbit","roof","whistle","silly","running","court","sudden","continent","needle","forty","minute","phrase","went","your","gave","spider","shelter","choice","manufacturing","evening","certainly","pleasant","beat","gather","government","engineer","riding","case","hang","this","accident","wear","court","sun","first","spin","sink","bent","broad","read","especially","noted","product","single","several","guard","chest","spirit","apartment","crop","native","possible","get","finest","fast","bear","condition","writer","attempt","mice","any","very","run","knowledge","cheese","fifteen","fallen","bar","slabs","highest","setting","hung","cover","wind","atom","laugh","industrial","thick","examine","connected","look","spirit","deal","name","had","best","control","fallen","strange","spite","alphabet","gift","lungs","badly","away","oil","view","halfway","object","hole","love","whispered","officer","branch","shown","pain","driving","hurry","rays","great","change","space","line","chicken","relationship","tent","handsome","attention","fire","monkey","serve","baseball","stove","lead","molecular","chose","radio","remember","situation","unless","lips","nearest","camera","joined","gun","wherever","deer","leg","drink","express","surprise","angry","simply","operation","missing","these","hungry","grandfather","direct","pair","fly","exact","face","cow","stick","after","noise","out","equally","contrast","ear","one","boat","replied","your","subject","western","driver","promised","home","subject","escape","safe","block","certainly","tube","supply","table","cool","soap","within","history","police","whom","bet","putting","bar","pride","without","birds","without","block","stranger","cabin","master","wonder","large","last","writing","letter","roof","indeed","off","high","lying","such","farmer","claws","except","column","try","second","stranger","right","act","wind","tin","fly","wait","silly","discussion","present","weather","far","seems","element","love","sometime","gone","together","elephant","almost","law","like","be","continued","company","part","young","finest","wheat","highway","sheet","tropical","four","couple","truth","hall","laid","stairs","especially","train","decide","dropped","tax","colony","courage","not","package","increase","nobody","raw","secret","immediately","lady","piece","so","tales","date","screen","recent","space","slope","vegetable","track","immediately","wild","roll","hundred","exactly","settle","bite","throat","than","honor","vegetable","source","central","together","increase","under","bottle","distance","help","pay","most","addition","paragraph","field","village","cool","sister","writing","ice","income","man","stronger","married","running","gulf","ahead","ordinary","gently","temperature","create","second","field","stems","watch","congress","machine","solid","pond","master","close","blow","living","willing","pink","rising","fourth","pick","addition","drink","lower","graph","think","pick","her","cannot","motion","asleep","respect","hit","failed","now","feature","farm","aboard","shoot","provide","right","ten","government","outline","total","whale","balance","grow","where","composition","speak","daily","child","foreign","secret","fallen","line","away","getting","answer","tree","control","blew","pilot","plenty","beauty","disappear","there","valuable","if","silver","that","music","beauty","select","due","composed","underline","sky","try","expression","bee","read","find","though","particular","express","failed","level","breathe","count","ants","discussion","large","chose","sea","truth","potatoes","wait","bicycle","onlinetools","local","atmosphere","morning","change","cry","promised","had","unhappy","until","arrange","somewhere","class","are","product","discover","verb","each","card","fur","powerful","note","near","ocean","directly","her","beat","object","lunch","edge","direction","separate","hour","world","compare","taste","bus","raw","somehow","purpose","southern","height","body","hundred","glad","dug","ride","crop","roll","widely","once","article","gone","chair","using","frequently","empty","garage","degree","nine","usually","view","shinning","made","hay","certain","conversation","second","easily","silver","giant","underline","union","strong","vegetable","table","flame","specific","only","throw","height","flies","some","syllable","saddle","military","specific","wash","road","especially","studying","spring","differ","ordinary","yard","acres","became","establish","talk","sharp","track","fully","temperature","practical","chest","quite","automobile","blank","vegetable","bring","discover","worse","population","largest","differ","mail","common","herself","gift","although","action","very","mathematics","tribe","not","or","sentence","weight","fat","lion","machinery","organization","dig","shape","kill","city","waste","farm","thread","living","change","work","wife","syllable","cool","belong","strange","shadow","fewer","moving","fifth","program","planet","refused","pleasure","region","for","basis","manner","goes","history","lying","hall","gun","further","current","building","flag","correct","palace","season","many","moon","total","ice","branch","breathing","scared","rhyme","shirt"]
tags = ["food", "groceries", "rent", "utilities", "sports", "fun", "transportation", "drinks", "business", "tickets", "gift", "gas"]


#### RUNNING THE COMMANDS ####

with open('commands.txt','w') as file:
    # adding 100 users
    for i in range(0, len(names)):
        if (i % 3 == 0):
            accountType = "business"
        else:
            accountType = "personal"
        file.write("XXXX,adduser," + names[i] + "," + passwords[i] + "," + accountType + "\n")
        
    # verify 90 of the users
    for i in range(0, len(names)):
        if (i % 10 == 0):
            continue
        else:
            file.write("XXXX,verify," + names[i] + "," + passwords[i] + "," + str(random.randint(100000000,999999999)) + "\n")

    # link bank for the 90 verified users
    for i in range(0, len(names)):
        if (i % 10 == 0):
            continue
        else:
            file.write("XXXX,linkbank," + names[i] + "," + str(random.randint(100000000,999999999)) + "\n")

    # deposit money into the 90 verified users with linked bank accounts
    for i in range(0, len(names)):
        if (i % 10 == 0):
            continue
        else:
            file.write("XXXX,deposit," + names[i] + "," + str(random.randint(0,1500)) + "\n")

    # friending users
    friends = []
    pairs = list(itertools.combinations(names, 2)) 
    for i in range(0, len(pairs)):
        if random.randint(0,10) > 2:
            continue
        else:
            file.write("XXXX,friend," + pairs[i][0] + "," + pairs[i][1] + "\n")
            file.write("XXXX,friend," + pairs[i][1] + "," + pairs[i][0] + "\n")
            friends.append(pairs[i])    


    # set privacy for all 100 users
    noprivacy = [13, 46, 62, 88, 97]
    for i in range(0, len(names)):
        if i in noprivacy:
            continue
        if (i % 3 == 0):
            file.write("XXXX,setprivacy," + names[i] + "," + "friends only"  + "\n")
        if (i % 2 == 0):
            file.write("XXXX,setprivacy," + names[i] + "," + "private" + "\n")
        if (i % 1 == 0):
            file.write("XXXX,setprivacy," + names[i] + "," + "public" + "\n")   

    # perform transactions using the randomly generated list of friends

    # payments
    for pair in friends:
        numPayments = random.randint(1,4)
        numRequests = random.randint(1,2)
        for i in range(numPayments):
            index = random.randint(0,1)
            messagelength = random.randint(1, 5)
            privacyindex = random.randint(1,10)
            if privacyindex == 1:
                privacy = ",-privacy,Private"
            elif privacyindex == 2:
                privacy = ",-privacy,Public"
            elif privacyindex == 3:
                privacy = ',-privacy,"Friends only"'
            else:
                privacy = ""
            tagindex = random.randint(0,15)
            try:
                tag = ",-tag," + tags[tagindex]
            except IndexError:
                tag = ""
            
            message = ""
            for i in range(messagelength):
                word = random.randint(0, 999)
                message += wordbank[word] + " "
            if message[len(message) - 1] == " ":
                message = message[0:len(message)-1]
            if index == 0:
                file.write("XXXX,pay," + pair[index] + "," + pair[1] + "," + str(random.randint(0, 50)) + "," + '"' + message + '"' + privacy + tag + "\n")
            else:
                file.write("XXXX,pay," + pair[index] + "," + pair[0] + "," + str(random.randint(0, 50)) + "," + '"' + message + '"' + privacy + tag + "\n")
# requests
        for i in range(numRequests):
            index = random.randint(0,1)
            messagelength = random.randint(1, 5)
            tagindex = random.randint(0,15)
            try:
                tag = ",-tag," + tags[tagindex]
            except IndexError:
                tag = ""
            
            message = ""
            for i in range(messagelength):
                word = random.randint(0, 999)
                message += wordbank[word] + " "
            if message[len(message) - 1] == " ":
                message = message[0:len(message)-1]
            if index == 0:
                file.write("XXXX,request," + pair[index] + "," + pair[1] + "," + str(random.randint(0, 50)) + "," + '"' + message + '"' + tag + "\n")
            else:
                file.write("XXXX,request," + pair[index] + "," + pair[0] + "," + str(random.randint(0, 50)) + "," + '"' + message + '"' + tag + "\n")

