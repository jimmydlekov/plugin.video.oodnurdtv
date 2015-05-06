#drundoo class for handling web site

import requests
session = requests.session

#from requests2 import session

import bs4

URL = 'http://www.drundoo.com/users/login/'

#username=''

class drundoo:
	
	def __init__(self,username,password):
		self.c = session()
		self.payload = [('email',username),('password',password),('submit','\xd0\x98\xd0\xb7\xd0\xbf\xd1\x80\xd0\xb0\xd1\x82\xd0\xb8')]
		self.c.post(URL,data=self.payload)
		self.username = username
		if not self.check_login():
			plugin.log.error('Wrong Username and/or Password!')

	def check_login(self):
		if self.c.get('http://www.drundoo.com/profile').text.find(self.username) != -1:
			return True
		else:
			return False
	def logIn(self):
		self.c.post(URL,data=self.payload)

	def open_site(self,url):
		if not self.check_login():
			self.logIn()
		temp = self.c.get(url)
		temp.encoding = 'utf-8'
		return temp.text
		#return self.c.get(url).text
	
	def open_json(self,url):
		if not self.check_login():
			self.logIn()
		temp = self.c.get(url)
		#temp.encoding = 'utf-8'
		return temp.json()
	
	def play_url(self,url):
		
		link = url
		play_list = []
                play_title = []
               	
		startposition = self.open_site(link).find('playlistUrl') + 15
                endposition = self.open_site(link).find('",\n')
                temp_link = 'http://www.drundoo.com'+ self.open_site(link)[startposition:endposition]

                temp2 = self.open_site(temp_link)
                startposition = temp2.find('http')
                endposition = temp2.find('","title')
                play_link = temp2[startposition:endposition]
                play_link = play_link.replace('\\','').replace('manifest.f4m','master.m3u8')
                play_list.append(play_link)

                return play_list[0]    

        def play_live_url(self,url):
                link = url
                temp = self.open_site(link)

                if temp.find('$.getJSON("') > -1:
                    start1 = temp.find('$.getJSON("') + '$.getJSON("'.__len__()
                    end1 = temp.find('", function (data)')

                else:
                    start1 = temp.find('url: "') + 'url: "'.__len__()
                    end1 = temp.find('",\n\t\t\tdataType:')
                
                link = 'http://www.drundoo.com' + temp[start1:end1]

                temp = self.open_json(link).get('smil_url')
                
                x1 = temp.find('.m3u8')
                x2 = temp.find('auth')
                x3 = temp.find('&live')
                
                if temp.find('-VOD-') > -1:
                    x4 = temp.find('-VOD-') + '-VOD-'.__len__()
                else:
                    x4 = temp.find('-')+1
                
                myTV = temp[x4:x1]
                myStat = {'bTVHD':'3',
                            'bTV':'1',
                            'NOVA':'6',
                            'BNT1_HD':'1',
                            'BNT1':'1',
                            'TV7_2':'6',
                            'bTVComedy':'1',
                            'bTVAction':'1',
                            'bTVCinema':'1',
                            'KinoNova':'6',
                            'Diema':'6',
                            'DiemaFamily':'6',
                            'FOXCrime':'1',
                            'FOX':'1',
                            'EurosportHD':'3',
                            'NOVAsport':'6',
                            'RINGBG':'1',
                            'Super7_1':'6',
                            'CN':'6',
                            'DiscoveryCha':'6',
                            'NationalGeog_2':'6',
                            'NGWILD':'1',
                            'ViasatExplor_1':'6',
                            'Mezzo':'1',
                            'PlanetaTV':'1',
                            'PlanetaFolk':'1',
                            'Balkanika':'1',
                            'FolklorTV':'1',
                            'FANTV':'1',
                            'CityTV_2':'6',
                            '24Kitchen_2':'1',
                            'bbt_1':'6',
                            'TheVoice':'6'}
                temp = temp[0:x1]+'='+myStat[myTV]+temp[x1:x2]+'&live&'+temp[x2:x3]

                play_link = temp

                return play_link

	def make_shows(self,url,my_mode):

		#timeshift_url = 'http://www.drundoo.com/channels/97/btv_hd/'
		

		timeshift_url = url
		
		if my_mode == 'list':
			temp = self.open_site(timeshift_url)
			links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='player_start')
		elif my_mode == 'timeshift':
			temp = self.open_site(timeshift_url)
			links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='action vod player_start')
		elif my_mode == 'live':
			temp = self.open_site(timeshift_url)
			links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='button watch-now player_start cf')
		
	
		play_list = []
		play_title = []
		for link in links:
			play_title.append(link.get('data-ga-label'))
                        play_list.append('http://www.drundoo.com' + link.get('href'))

                return play_list,play_title    


	def get_list(self,url,my_op=1):
		
		my_title = []
		my_link = []
		
		#use this option to get a list of channels
		if my_op == 1:
			temp = self.open_site(url)
                	links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='item')
			for link in links:
				my_link.append('http://www.drundoo.com' + link.find('a').get('href'))
				#my_title.append(link.find('span',{'class':'title'}).renderContents().decode('unicode_escape').encode('utf-8'))	
				my_title.append(link.find('span',{'class':'title'}).renderContents())
		
		#use this option to get recorded shows list
		elif my_op == 2:
			temp = self.open_site(url)
                	links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='inner right')
			
			for link in links:
				if link.findAll(class_='button vod-ico cf'):
					my_link.append('http://www.drundoo.com' + link.findAll(class_='button vod-ico cf')[0].get('href'))
					#my_title.append(link.find('span',{'class':'title'}).renderContents().decode('unicode_escape').encode('utf-8'))	
					my_title.append(link.findAll(class_='button watch-now player_start cf')[0].get('data-ga-label'))
		
		#use this option for timeshift list. Needed a channel web site
		elif my_op == 3:
			temp = self.open_site(url)
			links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='action vod player_start')
		
			for link in links:
				my_title.append(link.get('data-ga-label'))
				my_link.append('http://www.drundoo.com' + link.get('href'))
		
		#use this option for live list
		else:	
			temp = self.open_site(url)
                	links = bs4.BeautifulSoup(temp,'html.parser').findAll(class_='inner right')
			
			for link in links:
				if link.findAll(class_='button watch-now player_start cf'):
					my_link.append('http://www.drundoo.com' + link.findAll(class_='button watch-now player_start cf')[0].get('href'))
					#my_title.append(link.find('span',{'class':'title'}).renderContents().decode('unicode_escape').encode('utf-8'))	
					my_title.append(link.findAll(class_='button watch-now player_start cf')[0].get('data-ga-label'))

		return my_title,my_link
			
