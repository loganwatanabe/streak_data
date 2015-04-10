import time

class MatchUp(object):	
	def csv(self):
		fields = []
		# fields = (str(self.date) + "," + self.sport + "," + self.prompt + "," + self.team1 + "," + self.team2 + "," + str(self.winner1) + "," + str(self.winner2) + "," + str(self.result1) + "," + str(self.result2) + "," + str(self.percent1) + "," + str(self.percent2) + "," + str(self.percent_active))
		fields = [str(self.date), self.sport, self.prompt, self.team1, self.team2, str(self.winner1), str(self.winner2), str(self.result1), str(self.result2), str(self.percent1), str(self.percent2), str(self.percent_active)]
		# fields.append(str(self.date))
		# fields.append(self.sport)
		# fields.append(self.prompt)
		# fields.append(self.team1)
		# fields.append(self.team2)
		# fields.append(str(self.winner1))
		# fields.append(str(self.winner2))
		# fields.append(str(self.result1))
		# fields.append(str(self.result2))
		# fields.append(str(self.percent1))
		# fields.append(str(self.percent2))
		# fields.append(str(self.percent_active))
		# strang = ",".join(fields)
		return fields