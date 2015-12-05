from .cli import Cli, clicmd
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
import sys
from yowsup.common import YowConstants
import datetime
import os
import subprocess
import requests
import re
import json
import ast
import urllib
import signal
from subprocess import check_output
import time
from datetime import date, timedelta
import logging
import twitter
import config
import csv
from math import*
from yowsup.layers.protocol_receipts.protocolentities    import *
from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.protocol_presence.protocolentities    import *
from yowsup.layers.protocol_messages.protocolentities    import *
from yowsup.layers.protocol_acks.protocolentities        import *
from yowsup.layers.protocol_ib.protocolentities          import *
from yowsup.layers.protocol_iq.protocolentities          import *
from yowsup.layers.protocol_contacts.protocolentities    import *
from yowsup.layers.protocol_chatstate.protocolentities   import *
from yowsup.layers.protocol_privacy.protocolentities     import *
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities    import *
from yowsup.common.tools import ModuleTools
from urllib3.connectionpool import HTTPConnectionPool

APP_ID = "63e54f72"
APP_KEY = "4a72fce75ee83407bdcc08cb42a554d8"

previous_flight = ""
previous_bus = ""
is_logged_in = 0
sent_otp = 0
booked_request = 0
CRN = ""
latitude = ""
longitude = ""
nums = 0
message_sender = ""
customer_receiver = "917353659758"
save_user = ""
customer = ""
group_ind = 1
loc_list = []
care = 0
handle = ""

airport_list = {'kanpur': 'QJU', 'coimbatore': 'CJB', 'jamshedpur': 'IXW', 'chandigarh': 'IXC', 'anand': 'QNB', 'guwahati': 'GAU', 'kolkata': 'CCU', 'bombay': 'BOM', 'belgaum': 'IXG', 'ranchi': 'IXR', 'varanasi': 'VNS', 'bagdogra': 'IXB', 'goa': 'GOI', 'amritsar': 'ATQ', 'jalandhar': 'JLR', 'patna': 'PAT', 'bhopal': 'BHO', 'hyderabad': 'HYD', 'rajkot': 'RAJ', 'jaipur': 'JAI', 'thiruvananthapuram': 'TRV', 'bangalore': 'BLR', 'srinagar': 'SXR', 'ahmedabad': 'AMD', 'bhubaneswar': 'BBI', 'cochin': 'COK', 'pune': 'PNQ', 'lucknow': 'LKO', 'delhi': 'DEL', 'baronda': 'BDQ', 'nagpur': 'NAG', 'calicut': 'CCJ', 'madras': 'MAA','chennai':'MAA', 'calcutta': 'CCU','Kolkata':'CCU', 'surat': 'STV', 'tiruchirapally': 'TRZ'}
hotel_id = {'chail': '5381678877017369458', 'kumarakom': '509831601268956453', 'kishangarh': '904846775959723414', 'wankaner': '7119135585381026171', 'hospet': '5442236007651488849', 'ravangla': '6558259256211777777', 'anand': '2443319030692231630', 'guwahati': '3518826103379012321', 'deoghar': '286578240549810569', 'yercaud': '1639542103726057691', 'mundra': '8099261653431270639', 'jaipur': '4278754392716898526', 'biligiriranga hills': '6631910591111111111', 'barog': '5186446784666666666', 'raigarh': '4919899169835637044', 'hosur': '8323730995416368853', 'kanchipuram': '7943316035636087193', 'chennai': '4354390963378411938', 'cherrapunjee': '7910712990922560992', 'dhanaulti': '6425088845874313937', 'kukke': '7946955059812888888', 'alanya': '7605295074481264534', 'hisar': '7109045918550554109', 'almora': '2650028913914216165', 'kottayam': '7668653265335023650', 'auli': '5542574512537225631', 'mandi': '1942142800698979882', 'berhampur': '364636618277909542', 'bilaspur': '3246457706618132778', 'bhopal': '1309705427222288830', 'siliguri': '1076703141543671718', 'saputara': '5425650533123500633', 'diu': '3444748698309293350', 'mahabaleshwar': '7813632526399525655', 'dasada': '2354716714865968309', 'madurai': '4251640124790308184', 'tiruchendur': '5751391549356485600', 'thirukkadaiyur': '429669102710151142', 'anklesvar': '8216249432464882160', 'bidar': '6236219803229667817', 'guhagar': '2014080685220094358', 'west kameng': '3976967650409868460', 'paota': '4802917408138566689', 'pithoragarh': '8230669211306528270', 'talcher': '8207034658069196694', 'vikramgad': '2760362597285594740', 'barbil': '7325167872643381125', 'rohtak': '2182253611357095182', 'kanatal': '1501602011111111111', 'sawai madhopur': '8314560716455433059', 'valparai': '5249758188853704901', 'aronda': '6177864381790426842', 'muzaffarpur': '156860020895630517', 'sikar': '3864636785235227130', 'theni allinagaram': '4313122901731156910', 'bhandardara': '4564607930496735949', 'rikkisum': '666662234121389869', 'port blair': '4221994537604741770', 'lakshadweep': '2371815632336285450', 'vijayawada': '9125341922463979045', 'madhuban': '7491915794724365365', 'bhubaneswar': '6055181608245179114', 'tiruttani': '4389231738043999081', 'navi mumbai': '1914808440588557366', 'kalimpong': '680162234121389869', 'secunderabad': '641792803363050573', 'bhuj': '4970921134496006292', 'hansi': '5588483001098623982', 'dausa': '5167111493098382057', 'neil island': '6047705546088888888', 'baleshwar': '3334163371170104058', 'ujjain': '6499301750066218979', 'aligarh': '703436743695615208', 'sojat': '1155232567578853458', 'badami': '767346164151916001', 'gokarn': '1589221541418097800', 'firozabad': '3071983816303597998', 'ranchi': '332222994875110869', 'kumbhalgarh': '888888881382684942', 'anegundi': '1680679585600597275', 'erode': '7459077732375324433', 'sundarbans': '2893303993488888888', 'jabalpur': '6249589975474870272', 'kathgodam': '1806760684185679217', 'palampur': '3255628431166864060', 'karauli': '2787497793176678296', 'jojawar': '5815397291169458667', 'ahmedabad': '6067246467661897899', 'garhmukteshwar': '2447250318768594592', 'kanyakumari': '4049791448359331848', 'nathdwara': '2940898875768361370', 'bharuch': '1358368986005456762', 'khejarla': '8844104980766444537', 'sivaganga': '3375963683597926812', 'kashipur': '6660553334634788838', 'sariska': '3266809679902056733', 'jamshedpur': '8399297392482907494', 'rae bareli': '5755531465380493830', 'binsar': '2222222223914216165', 'satara': '1286706836037343554', 'new delhi': '2820046943342890302', 'gangavathi': '5299631784585365088', 'mohali': '877336314531270727', 'bomdila': '2948511146707552096', 'ambala': '6978466083856716327', 'haldwani (kathgodam)': '1726684544468115795', 'kolkata': '2066465017672827882', 'alwar': '2963060382483107643', 'kaziranga': '3147449693326909066', 'phalodi': '1417225450191048230', 'sivakasi': '5735886493816528501', 'murud janjira': '6988149390321964609', 'faridabad': '5092141098358928510', 'angamaly': '6056551542262426521', 'gangotri': '5001619947363078572', 'calangute': '5623949741138851217', 'srirangapatna': '243039232993823707', 'pollachi': '7025328840731286478', 'nagothana': '4064797477341811021', 'balasinor':     '4013299611085558956', 'imphal': '5044089652440751781', 'thekkady': '113710562199999999', 'lavasa': '1554245012666666666', 'bhavangadh': '2405360747539404583', 'hanumangarh': '4836716017864072672', 'karwar': '9097262997010839280', 'kollam': '9181313283980120876', 'puri': '762718351731814005', 'solapur': '1463167096263697523', 'bagdogra': '4863087818888888888', 'bhilwara': '3444986969998946096', 'panhala': '3931060669256755555', 'hodal': '1559128196799810538', 'lachung': '5735297249919412445', 'thrissur': '9163162457646324921', 'rajpipla': '2113487894226685273', 'tirupati': '18688368793823515', 'ranakpur': '2213177560508936945', 'agartala': '3048526927545682854', 'rudrapur': '1246072943449980830', 'panchkula': '1918504907582475263', 'jawhar': '1264354552680758721', 'ratnagiri': '1878646129691556535', 'tarapur': '8905169495007852837', 'sanya': '9194865050102387671', 'pauri': '3663286002349859666', 'jhunjhunun': '38298688828431456', 'belgaum': '2315788948560750093', 'vellore': '8138018222259325669', 'surat': '1174752501934903427', 'pathankot': '9136836850896816229', 'ranni': '113499961317666666', 'mandavi': '4256625737993503090', 'nilagiri': '4781203545819888306', 'siana': '3333680877280487964', 'bulandshahr': '3424036900077727534', 'ram nagar': '4511094548424244968', 'goa': '8717279093827200968', 'patnitop': '8342857729441666666', 'bareilly': '5604282523447316015', 'coonoor': '3082172792776588665', 'rajsamand': '801198381382684942', 'palani': '532717094883918055', 'shimla': '1449073512565742573', 'kurseong': '7795668900179279291', 'bhimtal': '2955676679847915145', 'kala amb': '3680307921805384444', 'poshina': '1504788899508468191', 'malpe': '4627994955829376023', 'simlipal': '4116358828596555555', 'pune': '1554245012668028405', 'diveagar': '2148788444282385034', 'lataguri': '1924800258483453613', 'matheran': '8785570642484497875', 'moradabad': '3692966613800792872', 'pinjore': '5751969294662194932', 'kasaragod': '592789400997420247', 'pench': '5625863579999999999', 'hyderabad': '2162254155836171767', 'rishikesh': '1546081981995124445', 'agatti island': '1386331600440718476', 'kanpur': '8312659373678178248', 'pushkar': '888442746688644020', 'mandawa': '4685056853136956107', 'dehradun': '1501602052591489281', 'dapoli camp': '6802487720102970772', 'bandhavgarh': '451293867744444444', 'malacca': '2167147585374904707', 'agra': '2049835366479118179', 'asansol': '2691139816779299040', 'parwanoo': '4098841562145914619', 'lonavala': '2562341919299046803', 'kandla': '4111058532336194240', 'kos': '560808534753678628', 'anantapur': '3996681253492714114', 'bahraich': '1516440844868926804', 'ludhiana': '7456787645128561245', 'somnath': '4105240388460068627', 'pahalgam': '8690604689099662109', 'guntur': '5456312398449971170', 'malwan': '9026350779881719747', 'naha': '5234347050641656651', 'pragpur': '1170236638551602338', 'sonauli': '5111607614534271482', 'gaya': '193373091590171702', 'raichak': '7747092266319772104', 'manesar': '1630191419280940875', 'raurkela': '2258194960531981962', 'mangalore': '8122644638120735625', 'canacona': '8193459841405881208', 'patiala': '436861998287687173', 'mangan': '5419223625717420102', 'bhilai': '7384305668762144446', 'macau': '8575269687125384404', 'ghaziabad': '1930868727827802776', 'haridwar': '3545728938069300513', 'nagpur': '9086912262372673635', 'dabhosa': '2626529177971548810', 'kattappana': '8123727056149230983', 'nashik': '7271871476923194551', 'alibag': '5342984967352266322', 'umaria': '451293867748418778', 'corbett': '6612277265847855481', 'bhavnagar': '4647126131404106401', 'kundapura': '4766786038269657400', 'vadodara': '1913041709781751242', 'shillong': '5893379290811218651', 'durshet': '4610879974207284983', 'velankanni': '4972767026557194463', 'jambughoda': '1913041709788888888', 'tiruvannamalai': '87537878006825382', 'jorhat': '3671215012093330041', 'gandhidham': '3117227037682032455', 'kotagiri': '2804132188718926733', 'marari': '112116643777777777', 'masinagudi': '5193828153712684320', 'jalgaon': '3545417915488090660', 'palitana': '1078335979438109242', 'bijapur': '7116969506857242754', 'jajpur': '752660950390339862', 'malappuram': '4307696439651398882', 'balrampur': '3716132655902458021', 'mamallapuram': '3838050502826668196', 'courtalam': '9161544322628146245', 'bathinda': '4193762482232235876', 'yelagiri': '722435672978995714', 'khajjiar': '5768849897857777777', 'ooty': '889033689324744753', 'bhadrachalam': '4970648159032994097', 'thanjavur': '8409018931676321597', 'gopalpur': '8444073139313737899', 'dhanbad': '3819426688609930178', 'durgapur': '3637531683705247779', 'kargil': '5909596255591977128', 'mumbai': '4213513766539949483', 'chitrakoot': '3287225515989908774', 'karjat': '117679265264838284', 'tenali': '7828005912479522511', 'karaikkudi': '8839266723457786720', 'amritsar': '6979104682588772672', 'dahej': '2291558351485331014', 'mukki': '1858119211111111111', 'puttaparthi': '5287937480265043121', 'manmad': '1682044796582225603', 'dalhousie': '3084536095241319598', 'ankola': '8188911961205191279', 'coimbatore': '3924148632351062483', 'jammu': '4423277054610635307', 'mount abu': '9195262341727064608', 'bandipur': '4789358214071755555', 'allahabad': '2764189059814305450', 'veraval': '5874643755276824133', 'mandya': '488538077236154664', 'pachmarhi': '2923185722879244397', 'igatpuri': '8420789664407530106', 'kanha': '1858119261619362733', 'jorethang': '8654397384842283437', 'mantralayam': '6123261334828772222', 'naldehra': '5555573512565742573', 'coorg': '6624397033787067229', 'gwalior': '8796441741742604098', 'udhampur': '8342857729441475735', 'alsisar': '3352303962004984661', 'bekal': '1390677863418837576', 'hampi': '1892804841293113374', 'darjeeling': '4863087815102631912', 'kushinagar': '1054157661196671846', 'balaghat': '5709435893029814407', 'shivanasamudra': '488538077236155555', 'sasan gir': '4942871005067777777', 'mandarmani': '1111111239243616096', 'visakhapatnam': '4436410759289535020', 'rohet garh': '8888888870893794769', 'shimoga': '2510520520918709430', 'sonipat': '4732253758470214042', 'kabini': '1333358671006609439', 'nawalgarh': '2702997798690416798', 'jhajjar': '8299253138504316809', 'leh': '5128830462161340517', 'devprayag': '2773385503412157510', 'udaipur': '3369724356477798574', 'meerut': '9020059428690984444', 'zirakpur': '970843905542755271', 'uttarkashi': '7903826064228823637', 'rajgir': '4372616520670443054', 'adilabad': '2691594438007517323', 'bodh gaya': '111111111190171702', 'orchha': '3893974079634926120', 'nainital': '4883398002803141725', 'krishnagiri': '3385055533153612212', 'nahan': '2295862152098631837', 'fatehpur': '2872202115079961522', 'chandrapur': '6568460547553850724', 'phagwara': '3400055537723189086', 'ramnagar': '4402982498663700575', 'churu': '3266700703234193420', 'pantnagar': '8702978431111111111', 'bambora': '6948516145471177055', 'shantiniketan': '4667984576004034952', 'mettupalayam': '1760301079813577051', 'jharsuguda': '4111034433163692875', 'morvi': '8531493646888892208', 'yamunotri': '7777777064228823637', 'daman': '486193027468146343', 'paradip': '44861377268983357', 'guruvayoor': '3240941990467631507', 'behror': '8813093841432007296', 'jamnagar': '2990227504820572234', 'jaisalmer': '8665923561677193166', 'dharmsala': '7558408766196243005', 'nagercoil': '5723612563088784030', 'chandigarh': '1490240556082995568', 'varkala': '4947247049944326597', 'nagapattinam': '347964240260347366', 'barnala': '4036183967407511453', 'dooars': '7731032782410174321', 'thiruvananthapuram': '3877384277955108166', 'kota': '5059572075609157517', 'ajmer': '5497937227335747566', 'lucknow': '9114123290289445387', 'pokhara': '7538757441157162874', 'gondal': '8320632655751720584', 'malshej ghat': '8334455643560990256', 'shahapur': '1946323537641584842', 'kedarnath': '270403037277324583', 'kolhapur': '3931060669256740310', 'shirdi': '8543796975376836518', 'kasol': '3516007103458613258', 'doha': '9069330760382121475', 'lumbini': '547330913285903480', 'rajahmundry': '1284983617884803061', 'digha': '3439561073212325240', 'panvel': '4761547441228189942', 'gandhinagar': '6413353945126501356', 'sonamarg': '2144622503355555555', 'sajan': '1155720879800785343', 'pench national park': '6465092361689666666', 'osian': '4434275337336858178', 'vapi': '5916864424882879431', 'varanasi': '710870868236923145', 'junagadh': '4942871005069592937', 'manila': '5690217789249565047', 'itanagar': '8051153097150521143', 'nagarhole': '6666667033787067229', 'khimsar': '7777777698569828714', 'howrah': '6459720941599850148', 'haflong': '8757217218861202087', 'kathmandu': '6575900005203463103', 'tiruppur': '1605852342069876120', 'namakkal': '2034713237034479962', 'srinagar': '5999885939075030137', 'mussoorie': '4206204899126402897', 'pelling': '8408111575376666666', 'lothal': '370361650998786420', 'ranthambore': '5975825609933066454', 'wellington': '5742934191899569942', 'rewari': '490253131757157834', 'mysore': '6237241643285427714', 'kufri': '1449073512999999999', 'kangra': '2482023231421888996', 'falakata': '1189742485232987917', 'bharatpur': '5480684591658727688', 'chamba': '5768849897852134061', 'idukki': '4448577645628143182', 'neemrana': '5909962555815447452', 'ranikhet': '1806671481785564467', 'pondicherry': '7247861711286471145', 'alleppey': '31335703284729576', 'vagamon': '6452845000289480285', 'dholpur': '1486256564777164989', 'raipur': '7802292548766851295', 'jalandhar': '9183124365971450275', 'madikeri': '1714717695346452173', 'kumily': '4675090819370906231', 'kanpur nagar': '3282680216504169527', 'kasauli': '4390187315908495063', 'havelock island': '3545004081111111111', 'khajuraho': '7348650681971213601', 'dibrugarh': '8112233193695852761', 'noida': '2311763083662248959', 'mathura': '33265771996272232', 'karnal': '890866864468704399', 'chiplun': '9048186197474314615', 'kumbakonam': '7625705172749674495', 'bellary': '2447221143620415641', 'kulu': '8540125979677725647', 'kaza': '5310022007043666666', 'mirik': '7116290313755255503', 'badrinathpuri': '7904948329661942601', 'manali': '2242315224277940906', 'dwarka': '8369616161009722573', 'hubli': '4175146706007535451', 'tawang': '1945596348450123067', 'chinnasalem': '7855342126469176934', 'mukteshwar': '2774263791561993722', 'gangtok': '1196252839838244621', 'nagar': '1397042982052417618', 'kozhikode': '7186114167120052770', 'pali': '6949583170893794769', 'ganpatipule': '1878646129688888888', 'ratlam': '3353204964476483321', 'carmona': '4233100988059781445', 'greater noida': '2351986185065628184', 'mcleodganj': '1307280128191747221', 'yamunanagar': '2288252101901177231', 'rameshwaram': '8481142109194274697', 'b.r. hills': '2143034057251484444', 'tezpur': '9185596256363153434', 'surendranagar': '1315628192024674882', 'kausani': '3121377666666113607', 'nagaur': '1970588698569828714', 'tenkasi': '6039349290641346007', 'porbandar': '6997269065911237268', 'bangalore': '6771549831164675055', 'kodaikanal': '444516582436447369', 'kashid': '6228214837700868579', 'kakinada': '9103404279762568565', 'panna': '35482573391540240', 'cuttack': '4088478550455809629', 'srikalahasti': '7526624291853629500', 'nanded': '3336688138651690805', 'tiruchengode': '9215310053053253838', 'naukuchiatal': '8184748706275649254', 'dindigul': '1349264278278563648', 'tirunelveli': '3083637696540047503', 'gorakhpur': '2496493766324838012', 'rajula': '3521152890740038391', 'tharangambadi': '3442428871095378402', 'munnar': '1780299204263085384', 'aurangabad': '3546476842016126643', 'chhota udaipur': '94086538555196069', 'gulmarg': '5753623020868390235', 'latur': '7166151778305093719', 'roorkee': '1268976774218365852', 'sawantwadi': '3161547721136927319', 'bhiwadi': '7188225528769381636', 'patna': '1074493438533185937', 'kollur': '7783787037713615543', 'nadiad': '8944374369899718812', 'dandeli': '8769785701740789883', 'rajkot': '7030802527799619237', 'solan': '5186446784747260557', 'bundi': '4313578615950783961', 'udupi': '6189773013719251991', 'ramgarh': '3720439157398840573', 'thane': '234055901639494539', 'kovalam': '6593905156853734893', 'panipat': '4218893261206436506', 'nagarkot': '54667327381784359', 'khandala': '3568613717100902652', 'bikaner': '1560603270455679984', 'palanpur': '3816328650169606334', 'chidambaram': '9033356370017027726', 'indore': '6727020267875173073', 'nellore': '1249024175655509470', 'nokha': '4688236772735873379', 'tiruchirappalli': '7549748421679676377', 'salem': '5328652237211326153', 'aizawl': '3581817333896630996', 'jhansi': '7090099699744070113', 'palakkad': '5880173016690161606', 'ernakulam': '8210666562286566619', 'chikmagalur': '4801527334652294087', 'sattal': '2955676444444444444', 'manipal': '5861591349670512952', 'mudumalai': '7783598650071440267', 'gurgaon': '1466927038870613796', 'dhulikhel': '7574189815595546034', 'jodhpur': '2455265397967176363', 'baddi': '4948737567311953362', 'silvassa': '3264184141358025948', 'jaisamand': '3369724356477794444', 'katra': '4084082672692346641', 'shekhawati': '6270361295348290526', 'kurukshetra': '718127000995117916', 'poovar': '3877384277555558166', 'kurnool': '6123261334828772000', 'panchgani': '6630003071254964353', 'chittaurgarh': '5885060592626219663', 'rupnagar': '2490573555811431739', 'thoothukkudi': '7915917895192102544', 'wayanad': '6194322623629521587', 'kutch': '4265693545872704087'}
logger = logging.getLogger(__name__)

class YowsupCliLayer(Cli, YowInterfaceLayer):
    PROP_RECEIPT_AUTO       = "org.openwhatsapp.yowsup.prop.cli.autoreceipt"
    PROP_RECEIPT_KEEPALIVE  = "org.openwhatsapp.yowsup.prop.cli.keepalive"
    PROP_CONTACT_JID        = "org.openwhatsapp.yowsup.prop.cli.contact.jid"
    EVENT_LOGIN             = "org.openwhatsapp.yowsup.event.cli.login"
    EVENT_START             = "org.openwhatsapp.yowsup.event.cli.start"
    EVENT_SENDANDEXIT       = "org.openwhatsapp.yowsup.event.cli.sendandexit"

    MESSAGE_FORMAT          = "[{FROM}({TIME})]:[{MESSAGE_ID}]\t {MESSAGE}"

    DISCONNECT_ACTION_PROMPT = 0
    DISCONNECT_ACTION_EXIT   = 1

    ACCOUNT_DEL_WARNINGS = 4

    def __init__(self):
        super(YowsupCliLayer, self).__init__()
        YowInterfaceLayer.__init__(self)
        self.accountDelWarnings = 0
        self.connected = False
        self.username = None
        self.sendReceipts = True
        self.disconnectAction = self.__class__.DISCONNECT_ACTION_PROMPT
        self.credentials = None

        #add aliases to make it user to use commands. for example you can then do:
        # /message send foobar "HI"
        # and then it will get automaticaly mapped to foobar's jid
        self.jidAliases = {
            # "NAME": "PHONE@s.whatsapp.net"
        }
        
    def changeDate(self, date):
        rex = datetime.datetime.strptime(date,'%d/%m/%Y')
        return datetime.datetime.strftime(rex,'%Y%m%d')
    
        
    def startMenu(self,mess):
        mess = mess.lower()
        if mess == "@bus":
            return "Selected Bus!! \nAvailable bus queries are:\n 1. For bus search: searchbus start_station end_station date_of_departure \n Example: @SearchBus bangalore chennai 29/09/2015\nPress @help for main menu"
        
        
        if "@searchbus" in mess:
            print "Entering in bus"
            a = mess.split()
            return self.getBusDetails(a[1], a[2], a[3])
            
        
        if mess == '@flight':
            return 'Selected Flight!!\nAvailable flight queries are:\n 1. For flight search: searchflight departure_airport arrival_airport date_of_departure \n Example: @SearchFlight bangalore jaipur 26/9/2015\nPress @help for main menu'    
        
        
        if "@searchflight" in mess:
            global previous_flight
            previous_flight = mess
            a = mess.split()
            print "previous is: "+ previous_flight
            return self.getFlights(a[1], a[2], a[3])
            
            
        if "@nextday" in mess:
            global previous_flight
            if "@searchflight" in previous_flight:
                
                a = previous_flight.split()
                
                a[3] = self.changeDate(a[3])
                t=time.strptime(a[3],'%Y%m%d')              
                newdate=date(t.tm_year,t.tm_mon,t.tm_mday)+timedelta(1)
                a[3] =  newdate.strftime('%d/%m/%Y')
                previous_flight = "@searchflight "+ a[1] +" "+a[2] +" "+ a[3]
                return self.getFlights(a[1], a[2], a[3])
            else:
                return "No next day flight searches are there.\nPress @help for assistance"
        
        
        if "@prevday" in mess:
            global previous_flight
            if "@searchflight" in previous_flight:
                a = previous_flight.split()
                
                a[3] = self.changeDate(a[3])
                t=time.strptime(a[3],'%Y%m%d')              
                newdate=date(t.tm_year,t.tm_mon,t.tm_mday)-timedelta(1)
                a[3] =  newdate.strftime('%d/%m/%Y')
                previous_flight = "@searchflight "+ a[1] +" "+a[2] +" "+ a[3]
                return self.getFlights(a[1], a[2], a[3])
            else:
                return "No previous day flight searches are there.\nPress @help for main menu"
        
        
        
        if "@searchhotel" in mess:
            a = mess.split()
            return self.getHotels(a[1],a[2], a[3], a[4], a[5])
        
        
        if mess == "@hotel":
            return 'Selected Hotels!!\nAvailable hotel queries are:\n 1. For hotel search: searchhotel city_name checkin_date checkout_date start_range end_range \n Example: @SearchHotel Bangalore 25/09/2015 26/09/2015 3000 4000\nPress @help for main menu'    
        
        
        if mess == "@help":
            return self.printHelp()
        
        if '@handle' in mess:
            global handle
            handle = mess.split()[1]
            print "Handle is : " + handle
            return self.start(handle)
               
#     def transferControl(self,message):
#         message = message.lower()
#         if message[0] == "#":
#             if "searchbus" in message:
#                 a = message.split()
#                 return self.getBusDetails(a[1], a[2], a[3])
#             elif "searchflight" in message:
#                 a = message.split()
#                 return self.getFlights(a[1], a[2], a[3])
#             elif "help" in message:
#                 return self.printHelp()
#             elif "create" in message:
#                 return "Group created"
#             
    
    def getBusDetails(self,start_station, end_station, dateofdepart):
        dateofdeparts = self.changeDate(dateofdepart)
        try:
            r = requests.get("http://developer.goibibo.com/api/bus/search/?app_id="+APP_ID+"&app_key="+APP_KEY+"&format=json&source="+start_station+"&destination="+end_station+"&dateofdeparture="+dateofdeparts)
        except requests.exceptions.ConnectionError, e:
            return "We are busy try in some time!!!!"
        output = r.content
        bus_list = []
        j = json.loads(output)
        
        
        if j['data']['onwardflights'] != []:
            buses = ast.literal_eval(str(j['data']['onwardflights'][1:-1]))
            #print buses
            output_string = "Top 3 bus results from "+start_station+" to "+end_station + " for "+dateofdepart+" by goibibo are: \n\n"
        
            for i in range(len(buses)):
                departure_time = str(buses[i]['DepartureTime'])
                duration = str(buses[i]['duration'])
                fare = str(buses[i]['fare']['totalfare'])
                bus_type = str(buses[i]['BusType'])
                travels = str(buses[i]['TravelsName'])
                bus_list.append((departure_time, duration, fare, bus_type, travels))
        
            final_list = sorted(bus_list,key=lambda x: x[2])
    
            for i in range(0,3):
                output_string += str(i+1)+". Departure time for bus is "+ final_list[i][0] + ", takes "+final_list[i][1]+". Fare is "+ final_list[i][2] + " INR and is a "+final_list[i][3]+" bus operated by "+final_list[i][4]+".\n"
        
            return output_string + "\n To book bus click on http://www.goibibo.com/bus/#bus-"+start_station+"-"+end_station+"-"+dateofdepart+"---0-0-\n\nCan use @nextday for next day buses and @prev day for previous day buses"
        
        else:
            return "No buses for this route.\nPress @help for main menu"    
        
        
    def printHelp(self):
        string = "Hi! This is goibibo personal assistant. Please type any one from below\n 1. For flight related info: @flight\n 2. For bus related info: @bus \n 3. For hotel details: @hotel\n 4. For personalized suggestions: @handle <Twitter handle>\n 5. @help for main menu"
        return string
    
    def getFlights(self,start_station, end_station, dateofdeparture):
        dateofdepartures = self.changeDate(dateofdeparture)
        start_station = airport_list[start_station]
        end_station = airport_list[end_station]
        try:
            r = requests.get("http://developer.goibibo.com/api/stats/minfare/?app_id="+APP_ID+"&app_key="+APP_KEY+"&format=json&vertical=flight&source="+start_station+"&destination="+end_station+"&mode=all&sdate="+dateofdepartures)
        except requests.exceptions.ConnectionError, e:
            return "We are busy try in some time!!!!"
        output = r.content
    
        flight_list = []
        j = json.loads(output)
        output_string = "Top "+str(len(j))+" flight results from "+start_station+" to "+end_station+" for "+dateofdeparture+" by goibibo are:\n"
    
        for i in range(len(j)):
            fare = j['resource'+str(i+1)]['fare']
            duration = str(ast.literal_eval(str(j['resource'+str(i+1)]['extra'][1:-1]))['duration'])
            start_time = str(ast.literal_eval(str(j['resource'+str(i+1)]['extra'][1:-1]))['deptime'].replace('t',' '))
            carrier = str(j['resource'+str(i+1)]['carrier'])
            flight_list.append((fare, duration, start_time, carrier))
        final_list = sorted(flight_list,key=lambda x: x[0])
        count = 1
        for each in final_list:
            output_string += str(count)+ ". Cost is "+str(each[0])+", Carrier is "+ each[3] + " which departs at " + each[2] + " and takes "+ each[1] + ".\n"
            count += 1
    
        flight_url = "http://www.goibibo.com/#flight-searchresult/#air-" + start_station+"-"+end_station+"-"+str(dateofdeparture)+"--"+str(1)+"-"+str(0)+"-"+str(0)+"-E\n\nCan use @nextday for next day buses and @prev day for previous day buses"
        output_string += "\n To book flight click on: " + flight_url
        return output_string   
    
    def getAverageRating(self, hotel_id):
        try:
            r = requests.get("http://ugc.goibibo.com/api/Hotels/getRatings?app_id="+APP_ID+"&app_key="+APP_KEY+"&vid="+str(hotel_id))
        except requests.exceptions.ConnectionError, e:
            return "We are busy try in some time!!!!"
        
        output = r.content
        print output
        hotel_list = []
        j = json.loads(output)
        average_rating = (j['starRating'] + j['hotelRating'] + j['vfmRating'] + j['fdRating'] + j['locRating'] + j['sqRating'] + j['cleanlinessRating'] + j['amenitiesRating'])/8.0
        hotel_name = j['hotelName']
        return average_rating, hotel_name

    def getHotels(self,city_name,check_in,check_out,range_start, range_end):
        check_in = self.changeDate(check_in)
        check_out = self.changeDate(check_out)
        
        range_start = int(range_start)
        range_end = int(range_end)
        if city_name in hotel_id:
            city_id = hotel_id[city_name]
             #   r = requests.get("http://developer.goibibo.com/api/cyclone/?app_id=63e54f72&app_key=4a72fce75ee83407bdcc08cb42a554d8&city_id=6771549831164675055&check_in=20151010&check_out=20151012")
            try:
                r = requests.get("http://developer.goibibo.com/api/cyclone/?app_id=" + APP_ID+"&app_key="+APP_KEY + "&city_id="+city_id + "&check_in=" + check_in + "&check_out=" + check_out)
            except requests.exceptions.ConnectionError, e:
                return "We are busy try in some time!!!!"
            output = r.content
            
        
            hotel_list = []
            j = json.loads(output)
        
            output_string = "Top "+str(len(j))+" results from goibibo are:\n"
            for i in j["data"]:
                hotel_list.append( (i,j["data"][i]['op_wt']))
        
            range_list = []
            for each in hotel_list:
                if(each[1] >= range_start and each[1] <= range_end):
                        range_list.append(each)
            range_list = sorted(range_list,key=lambda x: x[1])
            #print range_list
            final_list = []
            
            count = 0
            i = 0
            while count != min(5,len(range_list)):
                if (self.getAverageRating(str(range_list[i][0])) != "We are busy!!!!"):
                    rating, name = self.getAverageRating(str(range_list[i][0]))
                    if rating != 0.0:
                        final_list.append((rating, name, range_list[i][1]))
                        count += 1
                    i = i+1
                    #print final_list
                else:
                    return "We are busy try in some time!!!"
            output_string = "Top "+str(len(final_list))+" results from goibibo are: \n"
            for i in range(len(final_list)):
                output_string += str(i+1) + ". Name of hotel is " +str(final_list[i][1])+" with rate "+str(final_list[i][2])+" per night. Average rating of the hotel is: "+str(final_list[i][0])+".\n"
            
            #url = urllib.quote_plus("http://www.goibibo.com/hotels/find-hotels-in-"+city_name+"/"+city_id+"/"+city_id+"/hotels-"+city_id+"-"+check_in+"-"+check_out+"-1-1_0/")
            output_string+= '\n To book hotels click on link:' + "http://www.goibibo.com/hotels/find-hotels-in-"+city_name+"/"+city_id+"/"+city_id+"/hotels-"+city_id+"-"+check_in+"-"+check_out+"-1-1_0/"
        
            return output_string
        
        else:
            return city_name + " not in database"
    
    def square_rooted(self,x):
        return round(sqrt(sum([a*a for a in x])),3)

    def cosine_similarity(self,x,y):
        numerator = sum(a*b for a,b in zip(x,y))
        denominator = self.square_rooted(x)*self.square_rooted(y)
        return round(numerator/float(denominator),3)
    
    def start(self, handle):
        with open('data', 'rb') as f:
            reader = csv.reader(f)
            your_list = list(reader)
    
        #print len(your_list)
        #print len(your_list[1])
        data_list = []
    
        for i in range(0, len(your_list)):
            temp = []
            for j in range(1,53):
                temp.append(float(your_list[i][j].strip()))
            data_list.append([your_list[i][0], temp, your_list[i][-1]])
    
        #print len(data_list)
    
        cosine_list = []
    
        def convert_status_to_pi_content_item(s):
            # My code here
            return { 
            'userid': str(s.user.id), 
            'id': str(s.id), 
            'sourceid': 'python-twitter', 
            'contenttype': 'text/plain', 
            'language': s.lang, 
            'content': s.text, 
            'created': 1000 * s.GetCreatedAtInSeconds(),
            'reply': (s.in_reply_to_status_id == None),
            'forward': False
            }
            
    
        
    
        twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key,
                      consumer_secret=config.twitter_consumer_secret,
                      access_token_key=config.twitter_access_token,
                      access_token_secret=config.twitter_access_secret,
                      debugHTTP=True)
    
        statuses = twitter_api.GetUserTimeline(screen_name=handle,
                      count=200,
                      include_rts=False)
    
        pi_content_items_array = map(convert_status_to_pi_content_item, statuses)
        pi_content_items = { 'contentItems' : pi_content_items_array }
    
        r = requests.post(config.pi_url + '/v2/profile', 
                    auth=(config.pi_username, config.pi_password),
                    headers = {
                    'content-type': 'application/json',
                    'accept': 'application/json'
                },
                    data=json.dumps(pi_content_items)
                )
        j = json.loads(r.content)
        insights  = []
        big_five = []
        details = []
        needs = []
        values = []
    
        
        for i in range (0,5):
            big_five.append(( j['tree']['children'][0]['children'][0]['children'][i]['name'],
        j['tree']['children'][0]['children'][0]['children'][i]['percentage']))
            insights.append(( j['tree']['children'][0]['children'][0]['children'][i]['name'],
        j['tree']['children'][0]['children'][0]['children'][i]['percentage']))
    
            for k in range(0,6):
                details.append((j['tree']['children'][0]['children'][0]['children'][i]['children'][k]['name'],
        j['tree']['children'][0]['children'][0]['children'][i]['children'][k]['percentage']))
                insights.append((j['tree']['children'][0]['children'][0]['children'][i]['children'][k]['name'],
        j['tree']['children'][0]['children'][0]['children'][i]['children'][k]['percentage']))
         
        for p in range(0,12):
            needs.append( (j['tree']['children'][1]['children'][0]['children'][p]['name'],j['tree']['children'][1]['children'][0]['children'][p]['percentage']))
            insights.append( (j['tree']['children'][1]['children'][0]['children'][p]['name'],j['tree']['children'][1]['children'][0]['children'][p]['percentage']))
    
            
        
        for p in range(0,5):
            values.append( (j['tree']['children'][2]['children'][0]['children'][p]['name'],j['tree']['children'][2]['children'][0]['children'][p]['percentage']))
            insights.append( (j['tree']['children'][2]['children'][0]['children'][p]['name'],j['tree']['children'][2]['children'][0]['children'][p]['percentage']))
    
        
        insight_vector = []
    
        for i in range (0,len(insights)):
            insight_vector.append(insights[i][1])
    
        #print insight_vector
        for i in range(0, len(your_list)):
            cs = self.cosine_similarity(insight_vector, data_list[i][1])
            cosine_list.append([cs, data_list[i][0],data_list[i][-1]])
        
        cosine_list.sort(key=lambda x: x[0])
        final =  cosine_list[::-1]
        print "People similar to you are " + str(final[0][1]) + " and "+str(final[1][1])+ ". Would you like to visit " + str(final[0][2])[1:][1:-1].replace('/',',') + ", "+str(final[1][2])[1:][1:-1].replace('/',',')
        return  "Hey! Your personality is very similar to " + str(final[1][1]) + " and "+str(final[2][1])+ ". We have very special package for you for following destinations: " + str(final[1][2])[1:][1:-1].replace('/',',') + ", "+str(final[2][2])[1:][1:-1].replace('/',',')+".\nPlease visit https://www.goibibo.com/holidays/holiday-packages-india/ to know more about packages specially for you."
    
    def aliasToJid(self, calias):
        for alias, ajid in self.jidAliases.items():
            if calias.lower() == alias.lower():
                return self.normalizeJid(ajid)

        return self.normalizeJid(calias)

    def jidToAlias(self, jid):
        for alias, ajid in self.jidAliases.items():
            if ajid == jid:
                return alias
        return jid

    def normalizeJid(self, number):
        if '@' in number:
            return number
        elif "-" in number:
            return "%s@g.us" % number

        return "%s@s.whatsapp.net" % number

    def setCredentials(self, username, password):
        self.getLayerInterface(YowAuthenticationProtocolLayer).setCredentials(username, password)

    def onEvent(self, layerEvent):
        if layerEvent.getName() == self.__class__.EVENT_START:
            self.startInput()
            #print "In if"
            return True
        elif layerEvent.getName() == self.__class__.EVENT_SENDANDEXIT:
            credentials = layerEvent.getArg("credentials")
            target = layerEvent.getArg("target")
            message = layerEvent.getArg("message")
            #print "In elif 1"
            self.sendMessageAndDisconnect(credentials, target, message)

            return True
        elif layerEvent.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
             self.output("Disconnected: %s" % layerEvent.getArg("reason"))
             #print "In elif 2"
             if self.disconnectAction == self.__class__.DISCONNECT_ACTION_PROMPT:
                 self.connected = False
                 self.notifyInputThread()            
             else:
                 os._exit(os.EX_OK)

    def assertConnected(self):
        if self.connected:
            return True
        else:
            self.output("Not connected", tag = "Error", prompt = False)
            return False

    #### batch cmds #####
    def sendMessageAndDisconnect(self, credentials, jid, message):
        self.disconnectAction = self.__class__.DISCONNECT_ACTION_EXIT
        self.queueCmd("/login %s %s" % credentials)
        self.queueCmd("/message send %s \"%s\" wait" % (jid, message))
        self.queueCmd("/help")
        self.queueCmd("/L")
        self.startInput()


    ########## PRESENCE ###############
    @clicmd("Set presence name")
    def presence_name(self, name):
        if self.assertConnected():
            entity = PresenceProtocolEntity(name = name)
            self.toLower(entity)

    @clicmd("Set presence as available")
    def presence_available(self):
        if self.assertConnected():
            entity = AvailablePresenceProtocolEntity()
            self.toLower(entity)

    @clicmd("Set presence as unavailable")
    def presence_unavailable(self):
        if self.assertConnected():
            entity = UnavailablePresenceProtocolEntity()
            self.toLower(entity)

    @clicmd("Unsubscribe from contact's presence updates")
    def presence_unsubscribe(self, contact):
        if self.assertConnected():
            entity = UnsubscribePresenceProtocolEntity(self.aliasToJid(contact))
            self.toLower(entity)

    @clicmd("Subscribe to contact's presence updates")
    def presence_subscribe(self, contact):
        if self.assertConnected():
            entity = SubscribePresenceProtocolEntity(self.aliasToJid(contact))
            self.toLower(entity)

    ########### END PRESENCE #############

    ########### ib #######################
    @clicmd("Send clean dirty")
    def ib_clean(self, dirtyType):
        if self.assertConnected():
            entity = CleanIqProtocolEntity("groups", YowConstants.DOMAIN)
            self.toLower(entity)

    @clicmd("Ping server")
    def ping(self):
        if self.assertConnected():
            entity = PingIqProtocolEntity(to = YowConstants.DOMAIN)
            self.toLower(entity)

    ######################################

    ####### contacts/ profiles ####################
    @clicmd("Set status text")
    def profile_setStatus(self, text):
        if self.assertConnected():

            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("Status updated successfully")

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error updating status")

            entity = SetStatusIqProtocolEntity(text)
            self._sendIq(entity, onSuccess, onError)

    @clicmd("Get profile picture for contact")
    def contact_picture(self, jid):
        if self.assertConnected():
            entity = GetPictureIqProtocolEntity(self.aliasToJid(jid), preview=False)
            self._sendIq(entity, self.onGetContactPictureResult)

    @clicmd("Get profile picture preview for contact")
    def contact_picturePreview(self, jid):
        if self.assertConnected():
            entity = GetPictureIqProtocolEntity(self.aliasToJid(jid), preview=True)
            self._sendIq(entity, self.onGetContactPictureResult)

    @clicmd("Get lastseen for contact")
    def contact_lastseen(self, jid):
        if self.assertConnected():
            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("%s lastseen %s seconds ago" % (resultIqEntity.getFrom(), resultIqEntity.getSeconds()))

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error getting lastseen information for %s" % originalIqEntity.getTo())

            entity = LastseenIqProtocolEntity(self.aliasToJid(jid))
            self._sendIq(entity, onSuccess, onError)

    @clicmd("Set profile picture")
    def profile_setPicture(self, path):
        if self.assertConnected() and ModuleTools.INSTALLED_PIL():

            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("Profile picture updated successfully")

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error updating profile picture")

            #example by @aesedepece in https://github.com/tgalal/yowsup/pull/781
            #modified to support python3
            from PIL import Image
            src = Image.open(path)
            pictureData = src.resize((640, 640)).tobytes("jpeg", "RGB")
            picturePreview = src.resize((96, 96)).tobytes("jpeg", "RGB")
            iq = SetPictureIqProtocolEntity(self.getOwnJid(), picturePreview, pictureData)
            self._sendIq(iq, onSuccess, onError)
        else:
            logger.error("Python PIL library is not installed, can't set profile picture")

    ########### groups

    @clicmd("List all groups you belong to", 5)
    def groups_list(self):
        if self.assertConnected():
            entity = ListGroupsIqProtocolEntity()
            self.toLower(entity)

    @clicmd("Leave a group you belong to", 4)
    def group_leave(self, group_jid):
        if self.assertConnected():
            entity = LeaveGroupsIqProtocolEntity([self.aliasToJid(group_jid)])
            self.toLower(entity)

    @clicmd("Create a new group with the specified subject and participants. Jids are a comma separated list but optional.", 3)
    def groups_create(self, subject, jids = None):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')] if jids else []
            entity = CreateGroupsIqProtocolEntity(subject, participants=jids)
            self.toLower(entity)

    @clicmd("Invite to group. Jids are a comma separated list")
    def group_invite(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = AddParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Promote admin of a group. Jids are a comma separated list")
    def group_promote(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = PromoteParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Remove admin of a group. Jids are a comma separated list")
    def group_demote(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = DemoteParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Kick from group. Jids are a comma separated list")
    def group_kick(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = RemoveParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Change group subject")
    def group_setSubject(self, group_jid, subject):
        if self.assertConnected():
            entity = SubjectGroupsIqProtocolEntity(self.aliasToJid(group_jid), subject)
            self.toLower(entity)

    @clicmd("Set group picture")
    def group_picture(self, group_jid, path):
        if self.assertConnected() and ModuleTools.INSTALLED_PIL():

            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("Group picture updated successfully")

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error updating Group picture")

            #example by @aesedepece in https://github.com/tgalal/yowsup/pull/781
            #modified to support python3
            from PIL import Image
            src = Image.open(path)
            pictureData = src.resize((640, 640)).tobytes("jpeg", "RGB")
            picturePreview = src.resize((96, 96)).tobytes("jpeg", "RGB")
            iq = SetPictureIqProtocolEntity(self.aliasToJid(group_jid), picturePreview, pictureData)
            self._sendIq(iq, onSuccess, onError)
        else:
            logger.error("Python PIL library is not installed, can't set profile picture")


    @clicmd("Get group info")
    def group_info(self, group_jid):
        if self.assertConnected():
            entity = InfoGroupsIqProtocolEntity(self.aliasToJid(group_jid))
            self.toLower(entity)

    @clicmd("Get shared keys")
    def keys_get(self, jids):
        if ModuleTools.INSTALLED_AXOLOTL():
            from yowsup.layers.axolotl.protocolentities.iq_key_get import GetKeysIqProtocolEntity
            if self.assertConnected():
                jids = [self.aliasToJid(jid) for jid in jids.split(',')]
                entity = GetKeysIqProtocolEntity(jids)
                self.toLower(entity)
        else:
            logger.error("Axolotl is not installed")

    @clicmd("Send prekeys")
    def keys_set(self):
        if ModuleTools.INSTALLED_AXOLOTL():
            from yowsup.layers.axolotl import YowAxolotlLayer
            if self.assertConnected():
                self.broadcastEvent(YowLayerEvent(YowAxolotlLayer.EVENT_PREKEYS_SET))
        else:
            logger.error("Axolotl is not installed")

    @clicmd("Send init seq")
    def seq(self):
        priv = PrivacyListIqProtocolEntity()
        self.toLower(priv)
        push = PushIqProtocolEntity()
        self.toLower(push)
        props = PropsIqProtocolEntity()
        self.toLower(props)
        crypto = CryptoIqProtocolEntity()
        self.toLower(crypto)


    @clicmd("Delete your account")
    def account_delete(self):
        if self.assertConnected():
            if self.accountDelWarnings < self.__class__.ACCOUNT_DEL_WARNINGS:
                self.accountDelWarnings += 1
                remaining = self.__class__.ACCOUNT_DEL_WARNINGS - self.accountDelWarnings
                self.output("Repeat delete command another %s times to send the delete request" % remaining, tag="Account delete Warning !!", prompt = False)
            else:
                entity = UnregisterIqProtocolEntity()
                self.toLower(entity)

    @clicmd("Send message to a friend")
    def message_send(self, number, content):
        if self.assertConnected():
            outgoingMessage = TextMessageProtocolEntity(content.encode("utf-8") if sys.version_info >= (3,0) else content, to = self.aliasToJid(number))
            print(outgoingMessage)
            self.toLower(outgoingMessage)

    @clicmd("Broadcast message. numbers should comma separated phone numbers")
    def message_broadcast(self, numbers, content):
        if self.assertConnected():
            jids = [self.aliasToJid(number) for number in numbers.split(',')]
            outgoingMessage = BroadcastTextMessage(jids, content)
            self.toLower(outgoingMessage)

    #@clicmd("Send read receipt")
    def message_read(self, message_id):
        pass

    #@clicmd("Send delivered receipt")
    def message_delivered(self, message_id):
        pass

    @clicmd("Send an image with optional caption")
    def image_send(self, number, path, caption = None):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path, successEntity, originalEntity, caption)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

            self._sendIq(entity, successFn, errorFn)

    @clicmd("Send audio file")
    def audio_send(self, number, path):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path, successEntity, originalEntity)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)

            self._sendIq(entity, successFn, errorFn)

    @clicmd("Send typing state")
    def state_typing(self, jid):
        if self.assertConnected():
            entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, self.aliasToJid(jid))
            self.toLower(entity)

    @clicmd("Send paused state")
    def state_paused(self, jid):
        if self.assertConnected():
            entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_PAUSED, self.aliasToJid(jid))
            self.toLower(entity)

    @clicmd("Sync contacts, contacts should be comma separated phone numbers, with no spaces")
    def contacts_sync(self, contacts):
        if self.assertConnected():
            entity = GetSyncIqProtocolEntity(contacts.split(','))
            self.toLower(entity)

    @clicmd("Disconnect")
    def disconnect(self):
        if self.assertConnected():

            self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))

    @clicmd("Quick login")
    def L(self):
        if self.connected:
            return self.output("Already connected, disconnect first")
        self.getLayerInterface(YowNetworkLayer).connect()
        return True

    @clicmd("Login to WhatsApp", 0)
    def login(self, username, b64password):
        self.setCredentials(username, b64password)
        return self.L()

    ######## receive #########

    @ProtocolEntityCallback("chatstate")
    def onChatstate(self, entity):
        print(entity)

    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        print(entity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        #formattedDate = datetime.datetime.fromtimestamp(self.sentCache[entity.getId()][0]).strftime('%d-%m-%Y %H:%M')
        #print("%s [%s]:%s"%(self.username, formattedDate, self.sentCache[entity.getId()][1]))
        if entity.getClass() == "message":
            self.output(entity.getId(), tag = "Sent")
            #self.notifyInputThread()

    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        self.connected = True
        self.output("Logged in!", "Auth", prompt = False)
        self.notifyInputThread()

    @ProtocolEntityCallback("failure")
    def onFailure(self, entity):
        self.connected = False
        self.output("Login Failed, reason: %s" % entity.getReason(), prompt = False)

    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        notificationData = notification.__str__()
        print "Printing notification.."
        print str(notification.getType())
        
        if notificationData:
            self.output(notificationData, tag = "Notification")
            notif = notificationData.replace("\n", " ").replace(",", " ").replace("'"," ").replace(":", " ")
            notif = notif.split(" ")
            #print notif
            if "Creator" in notif and 'Subject' in notif and 'admin' in notif:
                self.message_send(notif[3], self.printHelp())
        else:
            self.output("From :%s, Type: %s" % (self.jidToAlias(notification.getFrom()), notification.getType()), tag = "Notification")
        
        if self.sendReceipts:
            self.toLower(notification.ack())

            

    @ProtocolEntityCallback("message")
    def createGroupMessage(self, groupID,messageBody):
        groupID = groupID + "@g.us" 
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            messageBody,
            to = groupID
        )
        print outgoingMessageProtocolEntity
        self.toLower(outgoingMessageProtocolEntity)    
    
    @ProtocolEntityCallback("message")
    def onMessage(self, message):
        #print(message)
        global nums
        
        messageOut = ""
        if message.getType() == "text":
            #self.output(message.getBody(), tag = "%s [%s]"%(message.getFrom(), formattedDate))
            messageOut = self.getTextMessageBody(message)
        elif message.getType() == "media":
            messageOut = self.getMediaMessageBody(message)
        else:
            messageOut = "Unknown message type %s " % message.getType()
            print(messageOut.toProtocolTreeNode())


        formattedDate = datetime.datetime.fromtimestamp(message.getTimestamp()).strftime('%d-%m-%Y %H:%M')
        sender = message.getFrom() if not message.isGroupMessage() else "%s/%s" % (message.getParticipant(False), message.getFrom())
        output = self.__class__.MESSAGE_FORMAT.format(
            FROM = sender,
            TIME = formattedDate,
            MESSAGE = messageOut.encode('latin-1').decode() if sys.version_info >= (3, 0) else messageOut,
            MESSAGE_ID = message.getId()
            )

        self.output(output, tag = None, prompt = not self.sendReceipts)
        if self.sendReceipts:
            self.toLower(message.ack())
            self.output("Sent delivered receipt", tag = "Message %s" % message.getId())
            #self.output("Sent delivered receipt abbhi", tag = "Message %s" % message.getType())
            #print(str(self.getMediaMessageBody(message)))
            out = str(output)
            #print out
            
            if message.getType() == "text":
                global message_sender
                global save_user
                global customer
                global care
                global group_ind
                global customer_receiver
                if message.isGroupMessage():
                    print "type:"
                    print message.isGroupMessage()
                    group_id = out[out.index('/')+1:out.index('@')]
                    self.message_send(group_id, self.startMenu(message.getBody()))
                
                if "@" in message.getBody() and message.isGroupMessage() is False:
                    number = message.getFrom()
                    
                    group_ind = 1
                    
                    message_sender = message.getFrom()
                    self.message_send(message_sender, self.startMenu(message.getBody()))
                elif "@bye" in message.getBody():
                    nums = 0
                    customer = 0
                    care = 0
                    self.message_send(customer_receiver, "The user has left. Thanks for support.")
                elif "@cc" in message.getBody() and nums == 0:
                    nums = 1
                    care = 1
                    customer = 1
                    save_user = message.getFrom()
                    print "save usr"
                    print save_user
                    self.message_send(customer_receiver, message.getBody())
                    
                elif customer_receiver in message.getFrom() and care == 1:
                    print "save usr 2"
                    print save_user
                    self.message_send(save_user, message.getBody())
                    
                elif customer == 1 and care == 1:
                    self.message_send(customer_receiver, message.getBody())
            print "Making system call..."
    
    
         
    def getTextMessageBody(self, message):
        return message.getBody()

    def getMediaMessageBody(self, message):
        if message.getMediaType() in ("image", "audio", "video"):
            return self.getDownloadableMediaMessageBody(message)
        else:
            return "[Media Type: %s]" % message.getMediaType()
       

    def getDownloadableMediaMessageBody(self, message):
         return "[Media Type:{media_type}, Size:{media_size}, URL:{media_url}]".format(
            media_type = message.getMediaType(),
            media_size = message.getMediaSize(),
            media_url = message.getMediaUrl()
            )


    def doSendImage(self, filePath, url, to, ip = None, caption = None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    def doSendAudio(self, filePath, url, to, ip = None, caption = None):
        entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        self.toLower(entity)

    def __str__(self):
        return "CLI Interface Layer"

    ########### callbacks ############

    def onRequestUploadResult(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):

        if requestUploadIqProtocolEntity.mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
            doSendFn = self.doSendAudio
        else:
            doSendFn = self.doSendImage

        if resultRequestUploadIqProtocolEntity.isDuplicate():
            doSendFn(filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: doSendFn(filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, async=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()

    def onGetContactPictureResult(self, resultGetPictureIqProtocolEntiy, getPictureIqProtocolEntity):
        # do here whatever you want
        # write to a file
        # or open
        # or do nothing
        # write to file example:
        #resultGetPictureIqProtocolEntiy.writeToFile("/tmp/yowpics/%s_%s.jpg" % (getPictureIqProtocolEntity.getTo(), "preview" if resultGetPictureIqProtocolEntiy.isPreview() else "full"))
        pass

    def __str__(self):
        return "CLI Interface Layer"

    @clicmd("Print this message")
    def help(self):
        self.print_usage()
    


