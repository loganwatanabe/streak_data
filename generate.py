
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import copy

# MatchUp object class
# from matchup import MatchUp
######################################
class MatchUp(object):
	def csv(self):
		fields = [str(self.date), self.sport, self.prompt, self.team1, self.team2, str(self.winner1), str(self.winner2), str(self.result1), str(self.result2), str(self.percent1), str(self.percent2), str(self.percent_active)]
		return fields
######################################



# parses the streak page for a given date
# outputs an array of MatchUp Objects
######################################
def getMatchups(date, writer=None):
	r = requests.get("http://streak.espn.go.com/en/entry?date="+str(date))
	data = r.text
	# soup = BeautifulSoup(data, "lxml")
	soup = BeautifulSoup(data)
	# beautiful soup is messing up the parsing, but I can't get lxml to work and there is no documentation on setting it up
	# soup = fromstring(data)



	matchups = soup.find_all("div", class_="matchup-container")
	m = []
	for i in matchups:
		ob = MatchUp()

		ob.date = datetime.strptime(i.find("span", class_="startTime").get("data-locktime"), "%B %d, %Y %I:%M:%S %p %Z")
		if i.find("div", class_="sport-description") == None:
			ob.sport = "None"
		else:
			ob.sport =  i.find("div", class_="sport-description").get_text().replace(",", "")
		ob.prompt = i.strong.get_text().replace(",", "")

		table = i.table.findAll("tr")

		# some pages have broken html that BS4 can't fix 
		if( len(table) < 2):
			print("skipping matchup " + str(ob.date))
			continue
		row1 = table[0]
		row2 = table[1]


		# taking results out first to help alleviate nested <td> tags in their code
		result1 = row1.find("td", class_="result").extract().get_text()
		result2 = row2.find("td", class_="result").extract().get_text()
		if result1 == "--":
			ob.result1 = 0.0
		else:
			ob.result1 = float(result1)

		if result2 == "--":
			ob.result2 = 0.0
		else:
			ob.result2 = float(result2)

		ob.team1 = row1.find("td", class_="opponents").get_text().replace(",", "")
		ob.team2 = row2.find("td", class_="opponents").get_text().replace(",", "")


		winner1 = 1
		winner2 = 1
		if row1.find("span", class_="winner").img == None:
			winner1 = 0
		if row2.find("span", class_="winner").img == None:
			winner2 = 0

		ob.winner1 = winner1
		ob.winner2 = winner2

		ob.percent1 = float(row1.find("td", class_="wpw").get_text().replace("%", ""))
		ob.percent2 = float(row2.find("td", class_="wpw").get_text().replace("%", ""))
		
		ob.percent_active = float(row1.find("div", class_="progress-bar").get("title").replace("%", "").split()[3])

		m.append(ob)
		if writer != None:
			writer.writerow(ob.csv())

	return m
######################################




# Generate the Dates we want to look at
########################################
from datetime import date
from dateutil.rrule import rrule, DAILY

# entire set of matchups up until 3/31/2015
iterdates=iter(rrule(DAILY, dtstart=date(2008, 8, 25), until=date(2015, 3, 31)))
# takes about 16 minutes to run, with 38648 individual records

# iterdates=iter(rrule(DAILY, dtstart=date(2008, 8, 25), until=date(2009, 3, 31)))

dates = []
for i in iterdates:
	dates.append(datetime.strftime(i,"%Y%m%d"))

######################################



# import csv
# with open('matchups', 'w', newline='') as f:
# 	writer = csv.writer(f, delimiter=',',lineterminator='\n')
# 	j = getMatchups(20100917)
# 	# print(j[0].csv())
# 	for i in range(len(j)):
# 		writer.writerow(j[i].csv())




# go through all dates and get matchups from the web
######################################
import csv
with open('matchups.csv', 'w', newline='') as f:
	writer = csv.writer(f, delimiter=',',lineterminator='\n')
	print("starting up")
	matchups = []
	c = 0
	star = datetime.now()
	for date in dates:
		matchups = matchups + getMatchups(date, writer)
		c += 1
		if c%365==0:print("%d / %d"%(c,len(dates)))

	end = datetime.now()

	print(star)
	print(end)
	print(len(matchups))










######################################