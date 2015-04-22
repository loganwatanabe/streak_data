records = load 'matchups.csv' using PigStorage(',') as (time:chararray, sport:chararray, question:chararray, choice1:chararray, choice2:chararray, winner1:int, winner2:int, score1:float, score2:float, percent1:float, percent2:float, percentactive:float);

matchups = FOREACH records GENERATE ToDate(time, 'y-M-d H:m:s') AS time, sport, question, choice1, choice2, winner1, winner2, score1, score2, percent1, percent2, percentactive;

spor = group matchups by sport;
sports = foreach spor generate group as sport, COUNT(matchups.sport) AS count;
store sports into 'sports';

majority = foreach matchups generate time, sport, question, (percent1>percent2?choice1:choice2), (percent1>percent2?winner1:winner2), (percent1>percent2?percent1:percent2), percentactive;


choi = load 'choices.csv' using PigStorage(',') as (time:chararray, sport:chararray, question:chararray, choice:chararray, winner:float, score:float, percent:float, percentactive:float);

choices = FOREACH choi GENERATE ToDate(time, 'y-M-d H:m:s') AS time, sport, question, choice, winner, score, percent, percentactive;

--VARIABLES


--PERCENT PREDICTED
percent_bins = foreach choices generate time, sport, question, choice, winner, score, FLOOR(percent/5) AS percent, percentactive;
percents = group percent_bins by percent;

percent_accuracy = foreach percents generate group*5 AS percent, AVG(percent_bins.winner) AS accuracy;
store percent_accuracy into 'percent_accuracy';



--SPECIFIC SPORTS

nfl = filter percent_bins by sport == 'NFL';
nfl_bins = group nfl by percent;
nfl_accuracy = foreach nfl_bins generate group AS percent, AVG(nfl.winner) AS accuracy;
store nfl_accuracy into 'nfl_accuracy';

mlb = filter percent_bins by sport == 'MLB';
mlb_bins = group mlb by percent;
mlb_accuracy = foreach mlb_bins generate group AS percent, AVG(mlb.winner) AS accuracy;
store mlb_accuracy into 'mlb_accuracy';

nba = filter percent_bins by sport == 'NBA';
nba_bins = group nba by percent;
nba_accuracy = foreach nba_bins generate group AS percent, AVG(nba.winner) AS accuracy;
store nba_accuracy into 'nba_accuracy';

ncb = filter percent_bins by sport == 'NCB';
ncb_bins = group ncb by percent;
ncb_accuracy = foreach ncb_bins generate group AS percent, AVG(ncb.winner) AS accuracy;
store ncb_accuracy into 'ncb_accuracy';

ncf = filter percent_bins by sport == 'NCF';
ncf_bins = group ncf by percent;
ncf_accuracy = foreach ncf_bins generate group AS percent, AVG(ncf.winner) AS accuracy;
store ncf_accuracy into 'ncf_accuracy';

nhl = filter percent_bins by sport == 'NHL';
nhl_bins = group nhl by percent;
nhl_accuracy = foreach nhl_bins generate group AS percent, AVG(nhl.winner) AS accuracy;
store nhl_accuracy into 'nhl_accuracy';

tennis = filter percent_bins by sport == 'Tennis';
tennis_bins = group tennis by percent;
tennis_accuracy = foreach tennis_bins generate group AS percent, AVG(tennis.winner) AS accuracy;
store tennis_accuracy into 'tennis_accuracy';

soccer = filter percent_bins by sport == 'Soccer';
soccer_bins = group soccer by percent;
soccer_accuracy = foreach soccer_bins generate group AS percent, AVG(soccer.winner) AS accuracy;
store soccer_accuracy into 'soccer_accuracy';

golf = filter percent_bins by sport == 'Golf';
golf_bins = group golf by percent;
golf_accuracy = foreach golf_bins generate group AS percent, AVG(golf.winner) AS accuracy;
store golf_accuracy into 'golf_accuracy';


-- PERCENT ACTIVE

active_bins = foreach choices generate time, sport, question, choice, winner, score, FLOOR(percent/5) as percent, FLOOR(percentactive/5) as percentactive;
actives = group active_bins by (percentactive, percent);

active_accuracy = foreach actives generate group.percent*5 AS percent, group.percentactive*5 AS percentactive, AVG(active_bins.winner) AS accuracy;
store active_accuracy into 'active_accuracy';


--TIME
time_bins = foreach choices generate time, GetHour(time) as hour, sport, question, choice, winner, score, FLOOR(percent/5) as percent, percentactive;
times = group time_bins by (hour, percent);

time_accuracy = foreach times generate group.hour AS hour, group.percent*5 as percent, AVG(time_bins.winner) AS accuracy;
store time_accuracy into 'time_accuracy';


--MATCHUP TYPE

--need to find matchup keywords so we can sort by them







