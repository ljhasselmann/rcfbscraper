import scrapy
import re
import string
import os
import errno
import csv
import pdb
from ESPN_Scraper.items import BOX_GameItem
from Team_Game_Statistics import *

# Make sure os path exists, create it if not
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Returns the contents of a .csv file in an array
def Read_CSV(file_name):
	print "Reading " + str(file_name) + "..."
	data = []
	with open(file_name, "r") as csvfile:
		data_reader = csv.reader(csvfile)
		for row in data_reader:
			data.append(row)
	for i in range(0, len(data)):
		for j in range(0, len(data[i])):
			data[i][j] = re.sub("\"", "", data[i][j])
	return data

# Writes the contents of data to a .csv file
def Write_CSV(data, file_name):
	with open(file_name, "w") as csvfile:
		data_writer = csv.writer(csvfile, lineterminator = '\n')
		data_writer.writerows(data)
		csvfile.close()

def Parse_Box(rows, team_TGS, team_abbvs):
	debug = False
	for i in range(0, len(rows)):
		rush_team = re.search(r"(?P<team>.+) Rushing", rows[i][0])
		if rush_team:
			for team_abbv in team_abbvs:
				team_name = rush_team.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team" and rows[i][0] != "No Rush Information":
						i += 1
					if rows[i][0] == "No Rush Information":
						team_TGS.Rush_Att = 0
						team_TGS.Rush_Yard = 0
						team_TGS.Rush_TD = 0
						break
					team_TGS.Rush_Att = rows[i][1]
					team_TGS.Rush_Yard = rows[i][2]
					team_TGS.Rush_TD = rows[i][4]
					break
		pass_team = re.search(r"(?P<team>.+) Passing", rows[i][0])
		if pass_team:
			for team_abbv in team_abbvs:
				team_name = pass_team.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team" and rows[i][0] != "No Pass Information":
						i += 1
					if rows[i][0] == "No Pass Information":
						team_TGS.Pass_Att = 0
						team_TGS.Pass_Comp = 0
						team_TGS.Pass_Yard = 0
						team_TGS.Pass_TD = 0
						team_TGS.Pass_Int = 0
						break
					cmp_att = re.match(r"(?P<cmp>\d+)\/(?P<att>\d+)", rows[i][1])
					team_TGS.Pass_Att = cmp_att.group("att")
					team_TGS.Pass_Comp = cmp_att.group("cmp")
					team_TGS.Pass_Yard = rows[i][2]
					team_TGS.Pass_TD = rows[i][4]
					team_TGS.Pass_Int = rows[i][5]
					break
		ret_team = re.search(r"(?P<team>.+) Kick Returns", rows[i][0])
		if ret_team:
			for team_abbv in team_abbvs:
				team_name = ret_team.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team" and rows[i][0] != "No Kickoff Returns":
						i += 1
					if rows[i][0] == "No Kickoff Returns":
						team_TGS.Kickoff_Ret = 0
						team_TGS.Kickoff_Ret_Yard = 0
						team_TGS.Kickoff_Ret_TD = 0
						break
					team_TGS.Kickoff_Ret = rows[i][1]
					team_TGS.Kickoff_Ret_Yard = rows[i][2]
					team_TGS.Kickoff_Ret_TD = rows[i][5]
					break
		ret_team = re.search(r"(?P<team>.+) Punt Returns", rows[i][0])
		if ret_team:
			for team_abbv in team_abbvs:
				team_name = ret_team.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team" and rows[i][0] != "No Punt Returns":
						i += 1
					if rows[i][0] == "No Punt Returns":
						team_TGS.Punt_Ret = 0
						team_TGS.Punt_Ret_Yard = 0
						team_TGS.Punt_Ret_TD = 0
						break
					team_TGS.Punt_Ret = rows[i][1]
					team_TGS.Punt_Ret_Yard = rows[i][2]
					team_TGS.Punt_Ret_TD = rows[i][5]
					break
		ret_team = re.search(r"(?P<team>.+) Interceptions", rows[i][0])
		if ret_team:
			for team_abbv in team_abbvs:
				team_name = ret_team.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team" and rows[i][0] != "No Interception Information":
						i += 1
					if rows[i][0] == "No Interception Information":
						team_TGS.Int_Ret = 0
						team_TGS.Int_Ret_Yard = 0
						team_TGS.Int_Ret_TD = 0
						break
					team_TGS.Int_Ret = rows[i][1]
					team_TGS.Int_Ret_Yard = rows[i][2]
					team_TGS.Int_Ret_TD = rows[i][3]
					break
		ret_team = re.search(r"(?P<team>.+) Kicking", rows[i][0])
		if ret_team:
			for team_abbv in team_abbvs:
				team_name = ret_team.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team":
						i += 1
					fg_att = re.match(r"(?P<good>\d+)\/(?P<att>\d+)", rows[i][1])
					xp_att = re.match(r"(?P<good>\d+)\/(?P<att>\d+)", rows[i][4])
					team_TGS.Field_Goal_Att = fg_att.group("att")
					team_TGS.Field_Goal_Made = fg_att.group("good")
					team_TGS.Off_XP_Kick_Att = xp_att.group("att")
					team_TGS.Off_XP_Kick_Made = xp_att.group("good")
					break
		punt = re.search(r"(?P<team>.+) Punting", rows[i][0])
		if punt:
			for team_abbv in team_abbvs:
				team_name = punt.group("team").lower().replace("-", "")
				team_name = team_name.lower().replace(" ", "")
				team_abbv[0] = team_abbv[0].lower().replace("-", "")
				team_abbv[0] = team_abbv[0].lower().replace(" ", "")
				team_abbv[2] = team_abbv[2].lower().replace("-", "")
				team_abbv[2] = team_abbv[2].lower().replace(" ", "")
				if (int(team_abbv[1]) == int(team_TGS.Team_Code)) and (team_abbv[0] == team_name or team_abbv[2] == team_name):
					while rows[i][0] != "Team" and rows[i][0] != "No Punts":
						i += 1
					if rows[i][0] == "No Punts":
						team_TGS.Punt = 0
						team_TGS.Punt_Yard = 0
						break
					team_TGS.Punt = rows[i][1]
					team_TGS.Punt_Yard = rows[i][2]
					break
	return team_TGS

# SPIDER
class boxscoreSpider(scrapy.Spider):
	name = "boxscore"
	allowed_domains = ["espn.go.com"]

	# Build URLs from scraped data
	start_urls = []
	for i in range(1, 18):
		make_sure_path_exists("week_" + str(i))
		folder = "week_" + str(i)
		os.chdir(folder)
		for filename in os.listdir(os.getcwd()):
			new_game = BOX_GameItem()
			with open (filename, "r") as f:
				data = f.read()
				# Get start URL
				m = re.search(r"Box: (?P<url>\S+)", data)
				if ''.join(e for e in m.group("url") if e.isalnum()) == "httpscoresespngocom":
					continue
				start_urls.append(m.group("url"))
				new_game['link'] = m.group("url")
				# Get date
				m = re.search(r"Date: (?P<date>\d+)", data)
				new_game['date'] = m.group("date")
				# Get home
				m = re.search(r"Home: \D+ \((?P<code>\d+)\)", data)
				new_game['home_code'] = m.group("code")
				# Get visitor
				m = re.search(r"Visitor: \D+ \((?P<code>\d+)\)", data)
				new_game['visitor_code'] = m.group("code")
			infofile = ''.join(e for e in new_game['link'] if e.isalnum())
			make_sure_path_exists(os.getcwd() + "/../tmpfiles/")
			with open(os.getcwd() + "/../tmpfiles/" + infofile + ".txt", 'w') as f:
				f.write(new_game['link'] + "\n")
				f.write("Code: " + str(new_game['visitor_code']).zfill(4))
				f.write(str(new_game['home_code']).zfill(4))
				f.write(new_game['date'])
				f.close()
		os.chdir("..")

	def parse(self, response):
		# Get this game code from file
		with open(os.getcwd() + "/tmpfiles/" + ''.join(e for e in response.url if e.isalnum()) + ".txt") as f:
			data = f.read()
			m = re.search(r"Code: (?P<code>\d+)", data)
			code = str(m.group('code')).zfill(16)
		# Scrape box score and save raw file
		table = response.xpath('//table[contains(@class, "mod-data")]')
		rows = []
		visitor = int(code) / 1000000000000
		home = (int(code) / 100000000) % 1000
		date = int(code) % 100000000
		for row in table.xpath('.//tr'):
			new_rows1 = [x.xpath('.//text()').extract() for x in row.xpath('.//td')]
			if len(new_rows1) > 0:
				rows.append(new_rows1)
			new_rows2 = [x.xpath('.//text()').extract() for x in row.xpath('.//th')]
			if len(new_rows2) > 0:
				if len(new_rows2) == 3:
					new_rows2 = [new_rows2[0], "", new_rows2[1], new_rows2[2]]
				rows.append(new_rows2)
			for i in range(0, len(rows[len(rows)-1])):
				rows[len(rows)-1][i] = ''.join([re.sub(r"\[u'\\xa0'\]|', |\[u'|u'|'\]|\[|\]", '', str(rows[len(rows)-1][i]))])
		Write_CSV(rows, "box/" + str(visitor).zfill(4) + str(home).zfill(4) + str(date) + ".csv")
		# Convert to team-game-statistics format
		visitor_TGS = Team_Game_Statistics(code, visitor)
		home_TGS = Team_Game_Statistics(code, home)
		team_names = Read_CSV("2014 Stats/team.csv")
		team_names = team_names[1:]
		team_abbvs = Read_CSV("2014 Stats/abbrevations.csv")
		# Get score
		for i in range(0, len(rows)):
			first_qtr = re.search(r"FIRST QUARTER", rows[i][0])
			if first_qtr:
				while len(rows[i+1]) >= 5:
					i += 1
				visitor_TGS.Points = rows[i][4]
				home_TGS.Points = rows[i][5]
			second_qtr = re.search(r"SECOND QUARTER", rows[i][0])
			if second_qtr:
				while len(rows[i+1]) >= 5:
					i += 1
				visitor_TGS.Points = rows[i][4]
				home_TGS.Points = rows[i][5]
			third_qtr = re.search(r"THIRD QUARTER", rows[i][0])
			if third_qtr:
				while len(rows[i+1]) >= 5:
					i += 1
				visitor_TGS.Points = rows[i][4]
				home_TGS.Points = rows[i][5]
			fourth_qtr = re.search(r"FOURTH QUARTER", rows[i][0])
			if fourth_qtr:
				while len(rows[i+1]) >= 5:
					i += 1
				visitor_TGS.Points = rows[i][4]
				home_TGS.Points = rows[i][5]
		# Box score stats
		for i in range(0, len(rows)):
			# Total 1st downs
			first_downs = re.search(r"1st Downs", rows[i][0])
			if first_downs:
				visitor_TGS.First_Down_Total = rows[i][1]
				home_TGS.First_Down_Total = rows[i][2]
			# 3rd down conversions
			third_downs = re.search(r"3rd down efficiency", rows[i][0])
			if third_downs:
				eff = re.match(r"(?P<conv>\d+)\-(?P<att>\d+)", rows[i][1])
				visitor_TGS.Third_Down_Att = eff.group("att")
				visitor_TGS.Third_Down_Conv = eff.group("conv")
				eff = re.match(r"(?P<conv>\d+)\-(?P<att>\d+)", rows[i][2])
				home_TGS.Third_Down_Att = eff.group("att")
				home_TGS.Third_Down_Conv = eff.group("conv")
			# 4th down conversions
			fourth_downs = re.search(r"4th down efficiency", rows[i][0])
			if fourth_downs:
				eff = re.match(r"(?P<conv>\d+)\-(?P<att>\d+)", rows[i][1])
				visitor_TGS.Fourth_Down_Att = eff.group("att")
				visitor_TGS.Fourth_Down_Conv = eff.group("conv")
				eff = re.match(r"(?P<conv>\d+)\-(?P<att>\d+)", rows[i][2])
				home_TGS.Fourth_Down_Att = eff.group("att")
				home_TGS.Fourth_Down_Conv = eff.group("conv")
			# Penalties
			penalties = re.search(r"Penalties", rows[i][0])
			if penalties:
				num_yrds = re.search(r"(?P<num>\d+)\-(?P<yrds>\d+)", rows[i][1])
				visitor_TGS.Penalty = num_yrds.group("num")
				visitor_TGS.Penalty_Yard = num_yrds.group("yrds")
				num_yrds = re.search(r"(?P<num>\d+)\-(?P<yrds>\d+)", rows[i][2])
				home_TGS.Penalty = num_yrds.group("num")
				home_TGS.Penalty_Yard = num_yrds.group("yrds")
			# Possession
			possession = re.search(r"Possession", rows[i][0])
			if possession:
				visitor_TGS.Time_Of_Possession = rows[i][1]
				home_TGS.Time_Of_Possession = rows[i][2]
			# Fumbles Lost
			fum_lost = re.search(r"Fumbles lost", rows[i][0])
			if fum_lost:
				visitor_TGS.Fum_Lost = rows[i][1]
				home_TGS.Fum_Lost = rows[i][2]
				visitor_TGS.Fum_Ret = home_TGS.Fum_Lost
				home_TGS.Fum_Ret = visitor_TGS.Fum_Lost
		# Find stats
		visitor_TGS = Parse_Box(rows, visitor_TGS, team_abbvs)
		# START DEBUG --
		#if int(visitor_TGS.Rush_Att) + int(visitor_TGS.Pass_Att) == 0:
			#pdb.set_trace()
			#visitor_TGS = Parse_Box(rows, visitor_TGS, team_abbvs)
		# END DEBUG --
		home_TGS = Parse_Box(rows, home_TGS, team_abbvs)
		# START DEBUG --
		#if int(home_TGS.Rush_Att) + int(home_TGS.Pass_Att) == 0:
			#pdb.set_trace()
			#home_TGS = Parse_Box(rows, visitor_TGS, team_abbvs)
		# END DEBUG --

		if os.path.isfile("2014 Stats/team-game-statistics.csv"):
			f = open("2014 Stats/team-game-statistics.csv",'a')
			data_writer = csv.writer(f, lineterminator = '\n')
			new_rows = []
			new_rows.append(visitor_TGS.Compile())
			new_rows.append(home_TGS.Compile())
			data_writer.writerows(new_rows)
			f.close()
		else:
			new_rows = []
			new_rows.append(visitor_TGS.Header())
			new_rows.append(visitor_TGS.Compile())
			new_rows.append(home_TGS.Compile())
			Write_CSV(new_rows, "2014 Stats/team-game-statistics.csv")