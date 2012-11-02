import dateutil.parser
import datetime
import re
import urllib
import xml.etree.ElementTree
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
	def _get_leaderboard(self):
		atom = xml.etree.ElementTree.parse(urllib.urlopen("https://madgoater:madgoaterismad@mail.google.com/mail/feed/atom/goat/"))

		goatee = {}

		for entry in atom.getroot().getchildren()[5:]:
			date_goated = entry[4].text
			date_goated = dateutil.parser.parse(date_goated)
			if not date_goated.replace(tzinfo=None) > datetime.datetime.now() - datetime.timedelta(days=7):
				continue
			goatee.setdefault(entry[6][1].text, 0)
			goatee[entry[6][1].text] = goatee[entry[6][1].text] + 1

		goat_counts = ['Number of Times Goated']
		users = ['Users']
		for username, number_of_times_goated in goatee.iteritems():
			goat_counts.append(number_of_times_goated)
			users.append(re.sub("@yelp.com", "", username))
		return [users, goat_counts]

	def get(self):
		self.write("""
<html>
  <head>
    <META HTTP-EQUIV="REFRESH" CONTENT="5">
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable(%s);

        var options = {
          title: 'Goat Leaderboard',
        };

        var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
        chart.draw(data, options);
      }
    </script>
  </head>
  <body>
    <div id="chart_div" style="width: 900px; height: 500px;"></div>
  </body>
</html>
""" % self._get_leaderboard())

application = tornado.web.Application([
		(r"/", MainHandler),
])

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.instance().start()
