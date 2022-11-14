import requests,sys,os

def chaplist(html_s):
	caps = {}
	for i in range(len(html_s)):
		if 'Get notified when' in html_s[i]:
			break
		elif 'class="part__label"' in html_s[i]:
			capName = html_s[i+1].split('<')[0]
			capUrl = html_s[i-1].split('"')[1]
			caps[capName] = 'https://www.wattpad.com'+capUrl

	if caps=={}:
		return False

	return caps

# comeÃ§o do programa
headers = {'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9','user-agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Mobile Safari/537.36'}
#cookies = {'sn__time': 'j%3Anull', 'locale': 'en_US', 'ff': '1', 'dpr': '1', 'te_session_id': '1591428023340', 'rt': 'r=https%3A%2F%2Fwww.wattpad.com%2F784482887-vendida-ao-dono-do-morro-i-apresenta%25C3%25A7%25C3%25A3o&ul=1591429391760&hd=1591429391795', 'lang': '6', 'tz': '3', 'fs__exp': '1', 'signupFrom': 'story_reading', 'wp_id': '1f4e51c7-10a5-4c7d-8fd9-43bb1bec445f'}
#cookies = {'OptanonControl':'ccc=BR&otvers=5.9.0&reg=global&pctm=0&vers=1.4.4', '__cf_bm':'384d4e5328cb0ad74c4e5acee15f2ded684279c3-1592076506-1800-AfK1qaeQZy6Bt5cKb3OXinBoQLn9InTl/cVCY7M5RU5vtMbfJRSKp25b/7q2LTYn1/fPOcBpdH+CSyPp4hvjySM=', '__cfduid':'da88a16bdde405967dfabb0e5cc0de8221590583479', 'ajs_anonymous_id':'%2262ed800d-36a0-48c2-88c8-131711db7601%22','OptanonConsent':'isIABGlobal=false&datestamp=Sat+Jun+13+2020+16%3A47%3A46+GMT-0300+(Brasilia+Standard+Time)&version=5.9.0&landingPath=NotLandingPage&groups=1%3A1%2Cad%3A1%2Csm%3A1%2C0_139823%3A1%2C0_139856%3A1%2C0_139852%3A1%2C0_139848%3A1%2C0_139844%3A1%2C0_139840%3A1%2C0_139869%3A1%2C0_139836%3A1%2C0_139865%3A1%2C0_139832%3A1%2C0_139861%3A1%2C0_139828%3A1%2C0_139857%3A1%2C0_139824%3A1%2C0_139853%3A1%2C0_139849%3A1%2C0_139845%3A1%2C0_139870%3A1%2C0_139841%3A1%2C0_139866%3A1%2C0_139837%3A1%2C0_139862%3A1%2C0_139833%3A1%2C0_139858%3A1%2C0_139829%3A1%2C0_139854%3A1%2C0_139825%3A1%2C0_139850%3A1%2C0_139846%3A1%2C0_139842%3A1%2C0_139871%3A1%2C0_139838%3A1%2C0_139867%3A1%2C0_139834%3A1%2C0_139863%3A1%2C0_139830%3A1%2C0_139859%3A1%2C0_139826%3A1%2C0_139855%3A1%2C0_139822%3A1%2C0_139851%3A1%2C0_139847%3A1%2C0_139843%3A1%2C0_139839%3A1%2C0_139872%3A1%2C0_139835%3A1%2C0_139868%3A1%2C0_139831%3A1%2C0_139864%3A1%2C0_139827%3A1%2C0_139860%3A1&AwaitingReconsent=false','OptanonAlertBoxClosed':'2020-06-13T19:44:39.272Z'}
cookies = {'wp_id':'120acbd0-70d2-4f60-9f6a-70f579fa6cbe',
	'sn__time':'j%3Anull',
	'locale':'pt_PT',
	'lang':'6',
	'fs__exp':'1',
	'RT':'',
}

baseurl = 'https://www.wattpad.com'
#url = 'https://www.wattpad.com/story/4850058-suicidal-harry-styles'
#url = 'https://www.wattpad.com/story/66458978-moods-joshler'
#url = 'https://www.wattpad.com/story/164450444-democracinha-ciro-x-haddad'

url = sys.argv[1]
fanfic_title = sys.argv[2].strip()
fanfic_titleOrig = fanfic_title
fanfic_title = fanfic_title.replace(' ','_')

if url=='' or fanfic_title=='':
	exit(3)

chapters_url = []

html = requests.get(url,headers=headers,cookies=cookies).text
html_s = html.split('>')

# nome dos capitulos:
chapters = chaplist(html_s)
default_chapname = False

#print('\n[*] downloading %s'%fanfic_titleOrig)

if chapters==False:
	sys.stderr.write('[!] nao foi possivel pegar a lista de capitulos\n')
	sys.exit(404)

all_fanfic = '<head><meta charset="utf-8"/><style rel="stylesheet"> h1 {font-size:33} h2 {font-size:29.5} body {padding:6px} p {font-size:25;} </style></head> <body> <h1 style="text-align:center">%s</h1>'%fanfic_titleOrig.title()

#if not default_chapname:
	#all_fanfic += '<h2 style="text-align:center">%s</h2>'%chapters_name[0]

cont = 0
for chapter in chapters:
	chap = chapters[chapter]
	cont_page = 1
	
	all_fanfic += '<h2 style="text-align:center">'+chapter+'</h2><span style="text-align:justify">'

	chaphtml = ''
	while True: # busca todas as paginas de cada capitulo
		chap_pag = chap+'/page/%d'%cont_page
		chaphtml_ = requests.get(chap_pag,headers=headers,cookies=cookies).text
		
		# verifica se Ã© o ultima pag do capitulo
		if 'data-p-id="' in chaphtml_:
			chaphtml = chaphtml_
		else:
			break

		cont_page += 1
		all_fanfic += chaphtml[chaphtml.index('<pre>')+5 : chaphtml.index('</pre>')]
	
	cont += 1

all_fanfic += '</span></body>'

with open('%s.html'%fanfic_title,'w',encoding="utf-8") as f:
	f.write(all_fanfic)

#os.system(f'./wkhtmltopdf {fanfic_title}.html {fanfic_title}.pdf 2> /dev/null')
downloadUrl = os.popen(f'curl -s --upload-file {fanfic_title}.html https://free.keep.sh').read().rstrip()+'/download'

print(downloadUrl)

