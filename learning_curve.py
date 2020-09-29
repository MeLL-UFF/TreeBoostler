'''
   Learning curve experiment
   Name:         transfer_experiment.py
   Author:       Rodrigo Azevedo
   Updated:      July 23, 2018
   License:      GPLv3
'''

import os
import sys
import time
#sys.path.append('../..')

from datasets.get_datasets import *
from revision import *
from transfer import *
from mapping import *
from tboostsrl import tboostsrl
import numpy as np
import random
import json

#verbose=True
source_balanced = False
balanced = False
firstRun = False
n_runs = 6
folds = 3

nodeSize = 2
numOfClauses = 8
maxTreeDepth = 3
trees = 10

if not os.path.exists('experiments'):
    os.makedirs('experiments')

def print_function(message):
    global experiment_title
    global nbr
    if not os.path.exists('experiments/' + experiment_title):
        os.makedirs('experiments/' + experiment_title)
    with open('experiments/' + experiment_title + '/' + str(nbr) + '_' + experiment_title + '.txt', 'a') as f:
        print(message, file=f)
        print(message)

def save_experiment(data):
    if not os.path.exists('experiments/' + experiment_title):
        os.makedirs('experiments/' + experiment_title)
    results = []
    if os.path.isfile('experiments/' + experiment_title + '/' + experiment_title + '.json'):
        with open('experiments/' + experiment_title + '/' + experiment_title + '.json', 'r') as fp:
            results = json.load(fp)
    results.append(data)
    with open('experiments/' + experiment_title + '/' + experiment_title + '.json', 'w') as fp:
        json.dump(results, fp)

def get_number_experiment():
    results = []
    if os.path.isfile('experiments/' + experiment_title + '/' + experiment_title + '.json'):
        with open('experiments/' + experiment_title + '/' + experiment_title + '.json', 'r') as fp:
            results = json.load(fp)
    return len(results)

def save(data):
    with open('experiments/learning_curve.json', 'w') as fp:
        json.dump(data, fp)

experiments = [
            #{'id': '51', 'source':'yeast', 'target':'webkb', 'predicate':'proteinclass', 'to_predicate':'departmentof'},
            #{'id': '52', 'source':'webkb', 'target':'yeast', 'predicate':'departmentof', 'to_predicate':'proteinclass'},
            ##{'id': '53', 'source':'cora', 'target':'imdb', 'predicate':'samevenue', 'to_predicate':'workedunder'},
            {'id': '1', 'source':'imdb', 'target':'uwcse', 'predicate':'workedunder', 'to_predicate':'advisedby'},
            {'id': '2', 'source':'uwcse', 'target':'imdb', 'predicate':'advisedby', 'to_predicate':'workedunder'},
            ##{'id': '3', 'source':'imdb', 'target':'uwcse', 'predicate':'movie', 'to_predicate':'publication'},
            #{'id': '4', 'source':'uwcse', 'target':'imdb', 'predicate':'publication', 'to_predicate':'movie'},
            #{'id': '5', 'source':'imdb', 'target':'uwcse', 'predicate':'genre', 'to_predicate':'inphase'},
            ##{'id': '6', 'source':'uwcse', 'target':'imdb', 'predicate':'inphase', 'to_predicate':'genre'},
            ##{'id': '7', 'source':'imdb', 'target':'cora', 'predicate':'workedunder', 'to_predicate':'samevenue'},
            #{'id': '8', 'source':'imdb', 'target':'cora', 'predicate':'workedunder', 'to_predicate':'samebib'},
            ##{'id': '9', 'source':'imdb', 'target':'cora', 'predicate':'workedunder', 'to_predicate':'sameauthor'},
            #{'id': '10', 'source':'imdb', 'target':'cora', 'predicate':'workedunder', 'to_predicate':'sametitle'},
            #{'id': '11', 'source':'uwcse', 'target':'cora', 'predicate':'advisedby', 'to_predicate':'samevenue'},
            ##{'id': '12', 'source':'uwcse', 'target':'cora', 'predicate':'advisedby', 'to_predicate':'samebib'},
            ##{'id': '13', 'source':'uwcse', 'target':'cora', 'predicate':'advisedby', 'to_predicate':'sameauthor'},
            #{'id': '14', 'source':'uwcse', 'target':'cora', 'predicate':'advisedby', 'to_predicate':'sametitle'},
            ##{'id': '15', 'source':'yeast', 'target':'twitter', 'predicate':'proteinclass', 'to_predicate':'accounttype'},
            ##{'id': '16', 'source':'yeast', 'target':'twitter', 'predicate':'interaction', 'to_predicate':'follows'},
            #{'id': '17', 'source':'yeast', 'target':'twitter', 'predicate':'location', 'to_predicate':'tweets'},
            #{'id': '18', 'source':'yeast', 'target':'twitter', 'predicate':'enzyme', 'to_predicate':'tweets'},
            #{'id': '19', 'source':'yeast', 'target':'twitter', 'predicate':'function', 'to_predicate':'tweets'},
            #{'id': '20', 'source':'yeast', 'target':'twitter', 'predicate':'phenotype', 'to_predicate':'tweets'},
            #{'id': '21', 'source':'yeast', 'target':'twitter', 'predicate':'complex', 'to_predicate':'tweets'},
            #{'id': '22', 'source':'twitter', 'target':'yeast', 'predicate':'accounttype', 'to_predicate':'proteinclass'},
            ##{'id': '23', 'source':'twitter', 'target':'yeast', 'predicate':'follows', 'to_predicate':'interaction'},
            #{'id': '24', 'source':'twitter', 'target':'yeast', 'predicate':'tweets', 'to_predicate':'location'},
            #{'id': '25', 'source':'twitter', 'target':'yeast', 'predicate':'tweets', 'to_predicate':'enzyme'},
            #{'id': '26', 'source':'twitter', 'target':'yeast', 'predicate':'tweets', 'to_predicate':'function'},
            #{'id': '27', 'source':'twitter', 'target':'yeast', 'predicate':'tweets', 'to_predicate':'phenotype'},
            #{'id': '28', 'source':'twitter', 'target':'yeast', 'predicate':'tweets', 'to_predicate':'complex'},
            #{'id': '29', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'teamalsoknownas', 'to_predicate':'companyalsoknownas'},
            #{'id': '30', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'teamplaysagainstteam', 'to_predicate':'companyalsoknownas'},
            #{'id': '31', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'teamplaysagainstteam', 'to_predicate':'acquired'},
            #{'id': '32', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'teamplaysagainstteam', 'to_predicate':'bankboughtbank'},
            #{'id': '33', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'athleteplayssport', 'to_predicate':'companyceo'},
            #{'id': '34', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'athleteplayssport', 'to_predicate':'bankchiefexecutiveceo'},
            ##{'id': '35', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'athleteplaysforteam', 'to_predicate':'bankchiefexecutiveceo'},
            #{'id': '36', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'athleteplaysforteam', 'to_predicate':'companyceo'},
            ##{'id': '37', 'source':'nell_sports', 'target':'nell_finances', 'predicate':'teamplayssport', 'to_predicate':'companyeconomicsector'},
            #{'id': '38', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'companyalsoknownas', 'to_predicate':'teamalsoknownas'},
            #{'id': '39', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'companyalsoknownas', 'to_predicate':'teamplaysagainstteam'},
            #{'id': '40', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'acquired', 'to_predicate':'teamplaysagainstteam'},
            #{'id': '41', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'bankboughtbank', 'to_predicate':'teamplaysagainstteam'},
            #{'id': '42', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'companyceo', 'to_predicate':'athleteplayssport'},
            #{'id': '43', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'bankchiefexecutiveceo', 'to_predicate':'athleteplayssport'},
            #{'id': '44', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'bankchiefexecutiveceo', 'to_predicate':'athleteplaysforteam'},
            #{'id': '45', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'companyceo', 'to_predicate':'athleteplaysforteam'},
            ##{'id': '46', 'source':'nell_finances', 'target':'nell_sports', 'predicate':'companyeconomicsector', 'to_predicate':'teamplayssport'},
            ##{'id': '47', 'source':'yeast', 'target':'facebook', 'predicate':'interaction', 'to_predicate':'edge'},
            ##{'id': '48', 'source':'twitter', 'target':'facebook', 'predicate':'follows', 'to_predicate':'edge'},
            ##{'id': '49', 'source':'imdb', 'target':'facebook', 'predicate':'workedunder', 'to_predicate':'edge'},
            ##{'id': '50', 'source':'uwcse', 'target':'facebook', 'predicate':'advisedby', 'to_predicate':'edge'},
            ]

bk = {
      'imdb': ['workedunder(+person,+person).',
              'workedunder(+person,-person).',
              'workedunder(-person,+person).',
              #'recursion_workedunder(+person,`person).',
              #'recursion_workedunder(`person,+person).',
              'female(+person).',
              'actor(+person).',
              'director(+person).',
              'movie(+movie,+person).',
              'movie(+movie,-person).',
              'movie(-movie,+person).',
              'genre(+person,+genre).'],
      'uwcse': ['professor(+person).',
        'student(+person).',
        'advisedby(+person,+person).',
        'advisedby(+person,-person).',
        'advisedby(-person,+person).',
        'tempadvisedby(+person,+person).',
        'tempadvisedby(+person,-person).',
        'tempadvisedby(-person,+person).',
        'ta(+course,+person,+quarter).',
        'ta(-course,-person,+quarter).',
        'ta(+course,-person,-quarter).',
        'ta(-course,+person,-quarter).',
        'hasposition(+person,+faculty).',
        'hasposition(+person,-faculty).',
        'hasposition(-person,+faculty).',
        'publication(+title,+person).',
        'publication(+title,-person).',
        'publication(-title,+person).',
        'inphase(+person,+prequals).',
        'inphase(+person,-prequals).',
        'inphase(-person,+prequals).',
        'courselevel(+course,+level).',
        'courselevel(+course,-level).',
        'courselevel(-course,+level).',
        'yearsinprogram(+person,+year).',
        'yearsinprogram(-person,+year).',
        'yearsinprogram(+person,-year).',
        'projectmember(+project,+person).',
        'projectmember(+project,-person).',
        'projectmember(-project,+person).',
        'sameproject(+project,+project).',
        'sameproject(+project,-project).',
        'sameproject(-project,+project).',
        'samecourse(+course,+course).',
        'samecourse(+course,-course).',
        'samecourse(-course,+course).',
        'sameperson(+person,+person).',
        'sameperson(+person,-person).',
        'sameperson(-person,+person).',],
      'cora': ['sameauthor(+author,+author).',
              'sameauthor(+author,-author).',
              'sameauthor(-author,+author).',
              'samebib(+class,+class).',
              'samebib(+class,-class).',
              'samebib(-class,+class).',
              'sametitle(+title,+title).',
              'sametitle(+title,-title).',
              'sametitle(-title,+title).',
              'samevenue(+venue,+venue).',
              'samevenue(+venue,-venue).',
              'samevenue(-venue,+venue).',
              #'recursion_samevenue(+venue,`venue).',
              #'recursion_samevenue(`venue,+venue).',
              'author(+class,+author).',
              'author(+class,-author).',
              'author(-class,+author).',
              'title(+class,+title).',
              'title(+class,-title).',
              'title(-class,+title).',
              'venue(+class,+venue).',
              'venue(+class,-venue).',
              'venue(-class,+venue).',
              'haswordauthor(+author,+word).',
              'haswordauthor(+author,-word).',
              'haswordauthor(-author,+word).',
              'haswordtitle(+title,+word).',
              'haswordtitle(+title,-word).',
              'haswordtitle(-title,+word).',
              'haswordvenue(+venue,+word).',
              'haswordvenue(+venue,-word).',
              'haswordvenue(-venue,+word).'],
      'webkb': ['coursepage(+page).',
                'facultypage(+page).',
                'studentpage(+page).',
                'researchprojectpage(+page).',
                'linkto(+id,+page,+page).',
                'linkto(+id,-page,-page).',
                'linkto(-id,-page,+page).',
                'linkto(-id,+page,-page).',
                'has(+word,+page).',
                'has(+word,-page).',
                'has(-word,+page).',
                'hasalphanumericword(+id).',
                'allwordscapitalized(+id).',
                'instructorsof(+page,+page).',
                'instructorsof(+page,-page).',
                'instructorsof(-page,+page).',
                'hasanchor(+word,+page).',
                'hasanchor(+word,-page).',
                'hasanchor(-word,+page).',
                'membersofproject(+page,+page).',
                'membersofproject(+page,-page).',
                'membersofproject(-page,+page).',
                'departmentof(+page,+page).',
                'departmentof(+page,-page).',
                'departmentof(-page,+page).',
                'pageclass(+page,+class).',
                'pageclass(+page,-class).',
                'pageclass(-page,+class).'],
      'twitter': ['accounttype(+account,+type).',
                  'accounttype(+account,-type).',
                  'accounttype(-account,+type).',
                  #'typeaccount(+type,`account).',
                  #'typeaccount(`type,+account).',
                  'tweets(+account,+word).',
                  'tweets(+account,-word).',
                  'tweets(-account,+word).',
                  'follows(+account,+account).',
                  'follows(+account,-account).',
                  'follows(-account,+account).',],
      'yeast': ['location(+protein,+loc).',
                'location(+protein,-loc).',
                'location(-protein,+loc).',
                'interaction(+protein,+protein).',
                'interaction(+protein,-protein).',
                'interaction(-protein,+protein).',
                'proteinclass(+protein,+class).',
                'proteinclass(+protein,-class).',
                'proteinclass(-protein,+class).',
                #'classprotein(+class,`protein).',
                #'classprotein(`class,+protein).',
                'enzyme(+protein,+enz).',
                'enzyme(+protein,-enz).',
                'enzyme(-protein,+enz).',
                'function(+protein,+fun).',
                'function(+protein,-fun).',
                'function(-protein,+fun).',
                'complex(+protein,+com).',
                'complex(+protein,-com).',
                'complex(-protein,+com).',
                'phenotype(+protein,+phe).',
                'phenotype(+protein,-phe).',
                'phenotype(-protein,+phe).'],
      'nell_sports': ['athleteledsportsteam(+athlete,+sportsteam).',
              'athleteledsportsteam(+athlete,-sportsteam).',
              'athleteledsportsteam(-athlete,+sportsteam).',
              'athleteplaysforteam(+athlete,+sportsteam).',
              'athleteplaysforteam(+athlete,-sportsteam).',
              'athleteplaysforteam(-athlete,+sportsteam).',
              'athleteplaysinleague(+athlete,+sportsleague).',
              'athleteplaysinleague(+athlete,-sportsleague).',
              'athleteplaysinleague(-athlete,+sportsleague).',
              'athleteplayssport(+athlete,+sport).',
              'athleteplayssport(+athlete,-sport).',
              'athleteplayssport(-athlete,+sport).',
              'teamalsoknownas(+sportsteam,+sportsteam).',
              'teamalsoknownas(+sportsteam,-sportsteam).',
              'teamalsoknownas(-sportsteam,+sportsteam).',
              'teamplaysagainstteam(+sportsteam,+sportsteam).',
              'teamplaysagainstteam(+sportsteam,-sportsteam).',
              'teamplaysagainstteam(-sportsteam,+sportsteam).',
              'teamplaysinleague(+sportsteam,+sportsleague).',
              'teamplaysinleague(+sportsteam,-sportsleague).',
              'teamplaysinleague(-sportsteam,+sportsleague).',
              'teamplayssport(+sportsteam,+sport).',
              'teamplayssport(+sportsteam,-sport).',
              'teamplayssport(-sportsteam,+sport).'],
      'nell_finances': ['countryhascompanyoffice(+country,+company).',
                        'countryhascompanyoffice(+country,-company).',
                        'countryhascompanyoffice(-country,+company).',
                        'companyeconomicsector(+company,+sector).',
                        'companyeconomicsector(+company,-sector).',
                        'companyeconomicsector(-company,+sector).',
                        'economicsectorcompany(+sector,`company).',
                        'economicsectorcompany(`sector,+company).',
                        #'economicsectorcompany(+sector,+company).',
                        #'economicsectorcompany(+sector,-company).',
                        #'economicsectorcompany(-sector,+company).',
                        #'ceoeconomicsector(+person,+sector).',
                        #'ceoeconomicsector(+person,-sector).',
                        #'ceoeconomicsector(-person,+sector).',
                        'companyceo(+company,+person).',
                        'companyceo(+company,-person).',
                        'companyceo(-company,+person).',
                        'companyalsoknownas(+company,+company).',
                        'companyalsoknownas(+company,-company).',
                        'companyalsoknownas(-company,+company).',
                        'cityhascompanyoffice(+city,+company).',
                        'cityhascompanyoffice(+city,-company).',
                        'cityhascompanyoffice(-city,+company).',
                        'acquired(+company,+company).',
                        'acquired(+company,-company).',
                        'acquired(-company,+company).',
                        #'ceoof(+person,+company).',
                        #'ceoof(+person,-company).',
                        #'ceoof(-person,+company).',
                        'bankbankincountry(+person,+country).',
                        'bankbankincountry(+person,-country).',
                        'bankbankincountry(-person,+country).',
                        'bankboughtbank(+company,+company).',
                        'bankboughtbank(+company,-company).',
                        'bankboughtbank(-company,+company).',
                        'bankchiefexecutiveceo(+company,+person).',
                        'bankchiefexecutiveceo(+company,-person).',
                        'bankchiefexecutiveceo(-company,+person).'],
      'yago2s': ['playsfor(+person,+team).',
    'playsfor(+person,-team).',
    'playsfor(-person,+team).',
    'hascurrency(+place,+currency).',
    'hascurrency(+place,-currency).',
    'hascurrency(-place,+currency).',
    'hascapital(+place,+place).',
    'hascapital(+place,-place).',
    'hascapital(-place,+place).',
    'hasacademicadvisor(+person,+person).',
    'hasacademicadvisor(+person,-person).',
    'hasacademicadvisor(-person,+person).',
    'haswonprize(+person,+prize).',
    'haswonprize(+person,-prize).',
    'haswonprize(-person,+prize).',
    'participatedin(+place,+event).',
    'participatedin(+place,-event).',
    'participatedin(-place,+event).',
    'owns(+institution,+institution).',
    'owns(+institution,-institution).',
    'owns(-institution,+institution).',
    'isinterestedin(+person,+concept).',
    'isinterestedin(+person,-concept).',
    'isinterestedin(-person,+concept).',
    'livesin(+person,+place).',
    'livesin(+person,-place).',
    'livesin(-person,+place).',
    'happenedin(+event,+place).',
    'happenedin(+event,-place).',
    'happenedin(-event,+place).',
    'holdspoliticalposition(+person,+politicalposition).',
    'holdspoliticalposition(+person,-politicalposition).',
    'holdspoliticalposition(-person,+politicalposition).',
    'diedin(+person,+place).',
    'diedin(+person,-place).',
    'diedin(-person,+place).',
    'actedin(+person,+media).',
    'actedin(+person,-media).',
    'actedin(-person,+media).',
    'iscitizenof(+person,+place).',
    'iscitizenof(+person,-place).',
    'iscitizenof(-person,+place).',
    'worksat(+person,+institution).',
    'worksat(+person,-institution).',
    'worksat(-person,+institution).',
    'directed(+person,+media).',
    'directed(+person,-media).',
    'directed(-person,+media).',
    'dealswith(+place,+place).',
    'dealswith(+place,-place).',
    'dealswith(-place,+place).',
    'wasbornin(+person,+place).',
    'wasbornin(+person,-place).',
    'wasbornin(-person,+place).',
    'created(+person,+media).',
    'created(+person,-media).',
    'created(-person,+media).',
    'isleaderof(+person,+place).',
    'isleaderof(+person,-place).',
    'isleaderof(-person,+place).',
    'haschild(+person,+person).',
    'haschild(+person,-person).',
    'haschild(-person,+person).',
    'ismarriedto(+person,+person).',
    'ismarriedto(+person,-person).',
    'ismarriedto(-person,+person).',
    'imports(+person,+material).',
    'imports(+person,-material).',
    'imports(-person,+material).',
    'hasmusicalrole(+person,+musicalrole).',
    'hasmusicalrole(+person,-musicalrole).',
    'hasmusicalrole(-person,+musicalrole).',
    'influences(+person,+person).',
    'influences(+person,-person).',
    'influences(-person,+person).',
    'isaffiliatedto(+person,+team).',
    'isaffiliatedto(+person,-team).',
    'isaffiliatedto(-person,+team).',
    'isknownfor(+person,+theory).',
    'isknownfor(+person,-theory).',
    'isknownfor(-person,+theory).',
    'ispoliticianof(+person,+place).',
    'ispoliticianof(+person,-place).',
    'ispoliticianof(-person,+place).',
    'graduatedfrom(+person,+institution).',
    'graduatedfrom(+person,-institution).',
    'graduatedfrom(-person,+institution).',
    'exports(+place,+material).',
    'exports(+place,-material).',
    'exports(-place,+material).',
    'edited(+person,+media).',
    'edited(+person,-media).',
    'edited(-person,+media).',
    'wrotemusicfor(+person,+media).',
    'wrotemusicfor(+person,-media).',
    'wrotemusicfor(-person,+media).'],
    'facebook': ['edge(+person,+person).',
            'edge(+person,-person).',
            'edge(-person,+person).',
            'middlename(+person,+middlename).',
            'middlename(+person,-middlename).',
            'middlename(-person,+middlename).',
            'lastname(+person,+lastname).',
            'lastname(+person,-lastname).',
            'lastname(-person,+lastname).',
            'educationtype(+person,+educationtype).',
            'educationtype(+person,-educationtype).',
            'educationtype(-person,+educationtype).',
            'workprojects(+person,+workprojects).',
            'workprojects(+person,-workprojects).',
            'workprojects(-person,+workprojects).',
            'educationyear(+person,+educationyear).',
            'educationyear(+person,-educationyear).',
            'educationyear(-person,+educationyear).',
            'educationwith(+person,+educationwith).',
            'educationwith(+person,-educationwith).',
            'educationwith(-person,+educationwith).',
            'location(+person,+location).',
            'location(+person,-location).',
            'location(-person,+location).',
            'workwith(+person,+workwith).',
            'workwith(+person,-workwith).',
            'workwith(-person,+workwith).',
            'workenddate(+person,+workenddate).',
            'workenddate(+person,-workenddate).',
            'workenddate(-person,+workenddate).',
            'languages(+person,+languages).',
            'languages(+person,-languages).',
            'languages(-person,+languages).',
            'religion(+person,+religion).',
            'religion(+person,-religion).',
            'religion(-person,+religion).',
            'political(+person,+political).',
            'political(+person,-political).',
            'political(-person,+political).',
            'workemployer(+person,+workemployer).',
            'workemployer(+person,-workemployer).',
            'workemployer(-person,+workemployer).',
            'hometown(+person,+hometown).',
            'hometown(+person,-hometown).',
            'hometown(-person,+hometown).',
            'educationconcentration(+person,+educationconcentration).',
            'educationconcentration(+person,-educationconcentration).',
            'educationconcentration(-person,+educationconcentration).',
            'workfrom(+person,+workfrom).',
            'workfrom(+person,-workfrom).',
            'workfrom(-person,+workfrom).',
            'workstartdate(+person,+workstartdate).',
            'workstartdate(+person,-workstartdate).',
            'workstartdate(-person,+workstartdate).',
            'worklocation(+person,+worklocation).',
            'worklocation(+person,-worklocation).',
            'worklocation(-person,+worklocation).',
            'educationclasses(+person,+educationclasses).',
            'educationclasses(+person,-educationclasses).',
            'educationclasses(-person,+educationclasses).',
            'workposition(+person,+workposition).',
            'workposition(+person,-workposition).',
            'workposition(-person,+workposition).',
            'firstname(+person,+firstname).',
            'firstname(+person,-firstname).',
            'firstname(-person,+firstname).',
            'birthday(+person,+birthday).',
            'birthday(+person,-birthday).',
            'birthday(-person,+birthday).',
            'educationschool(+person,+educationschool).',
            'educationschool(+person,-educationschool).',
            'educationschool(-person,+educationschool).',
            'name(+person,+name).',
            'name(+person,-name).',
            'name(-person,+name).',
            'gender(+person,+gender).',
            'gender(+person,-gender).',
            'gender(-person,+gender).',
            'educationdegree(+person,+educationdegree).',
            'educationdegree(+person,-educationdegree).',
            'educationdegree(-person,+educationdegree).',
            'locale(+person,+locale).',
            'locale(+person,-locale).',
            'locale(-person,+locale).']
      }

if os.path.isfile('learning_curve.json'):
    with open('learning_curve.json', 'r') as fp:
        results = json.load(fp)
else:
    results = { 'save': { }}
    firstRun = True

if firstRun:
    results['save'] = {
        'experiment': 0,
        'n_runs': 0,
        'seed': 441773,
        'source_balanced' : 1,
        'balanced' : 1,
        'folds' : 3,
        'nodeSize' : 2,
        'numOfClauses' : 8,
        'maxTreeDepth' : 3
        }

start = time.time()
#while results['save']['experiment'] < len(experiments):
while results['save']['n_runs'] < n_runs:
    print('Run: ' + str(results['save']['n_runs']))
    experiment = results['save']['experiment'] % len(experiments)
#    try:
    #experiment = results['save']['experiment']
    experiment_title = experiments[experiment]['id'] + '_' + experiments[experiment]['source'] + '_' + experiments[experiment]['target']
    #if experiment_title not in results['results']:
    #    results['results'][experiment_title] = []

    #logger = setup_logger('logger_' + experiment_title, 'log/' + experiment_title + '.log')

    nbr = get_number_experiment() + 1 #len(results['results'][experiment_title]) + 1
    print_function('Starting experiment #' + str(nbr) + ' for ' + experiment_title+ '\n')

    source = experiments[experiment]['source']
    target = experiments[experiment]['target']
    predicate = experiments[experiment]['predicate']
    to_predicate = experiments[experiment]['to_predicate']

    # Load source dataset
    src_total_data = datasets.load(source, bk[source], seed=results['save']['seed'])
    src_data = datasets.load(source, bk[source], target=predicate, balanced=source_balanced, seed=results['save']['seed'])

    # Group and shuffle
    src_facts = datasets.group_folds(src_data[0])
    src_pos = datasets.group_folds(src_data[1])
    src_neg = datasets.group_folds(src_data[2])

    print_function('Start learning from source dataset\n')

    print_function('Source train facts examples: %s' % len(src_facts))
    print_function('Source train pos examples: %s' % len(src_pos))
    print_function('Source train neg examples: %s\n' % len(src_neg))

    # learning from source dataset
    background = tboostsrl.modes(bk[source], [predicate], useStdLogicVariables=False, maxTreeDepth=maxTreeDepth, nodeSize=nodeSize, numOfClauses=numOfClauses)
    [model, total_revision_time, source_structured, will, variances] = revision.learn_model(background, tboostsrl, predicate, src_pos, src_neg, src_facts, refine=None, trees=trees, print_function=print_function)

    #preds = mapping.get_preds(source_structured, bk[source])
    #print_function('Predicates from source: %s' % preds + '\n')

    #critical_preds = mapping.get_critical_preds(source_structured, bk[source])
    #print_function('Critical predicates from source: %s' % critical_preds + '\n')
    #print('Source structured tree: %s \n' % source_structured)

    # Load total target dataset
    tar_total_data = datasets.load(target, bk[target], seed=results['save']['seed'])

    if target in ['nell_sports', 'nell_finances', 'yago2s']:
        n_folds = folds
    else:
        n_folds = len(tar_total_data[0])

    results_save = []
    for i in range(n_folds):
        print_function('Starting fold ' + str(i+1) + '\n')

        ob_save = {}

        if target not in ['nell_sports', 'nell_finances', 'yago2s']:
            [tar_train_pos, tar_test_pos] = datasets.get_kfold(i, tar_total_data[0])
        else:
            t_total_data = datasets.load(target, bk[target], target=to_predicate, balanced=balanced, seed=results['save']['seed'])
            tar_train_pos = datasets.split_into_folds(t_total_data[1][0], n_folds=n_folds, seed=results['save']['seed'])[i] + t_total_data[0][0]

#            # transfer
#            print_function('Target predicate: %s' % to_predicate)
#            mapping_rules, mapping_results = mapping.get_best(preds, bk[target], datasets.group_folds(src_total_data[0]), tar_train_pos, forceHead=to_predicate) #, forcePreds=critical_preds)
#
#            if print_function:
#                print_function('Mapping Results')
#                print_function('   Knowledge compiling time   = %s' % mapping_results['Knowledge compiling time'])
#                print_function('   Generating paths time   = %s' % mapping_results['Generating paths time'])
#                print_function('   Generating mappings time   = %s' % mapping_results['Generating mappings time'])
#                print_function('   Possible mappings   = %s' % mapping_results['Possible mappings'])
#                print_function('   Max mapping   = %s' % mapping_results['Max mapping'])
#                print_function('   Numbers predicates mapping   = %s' % mapping_results['Numbers preds mapping'])
#                print_function('   Finding best mapping   = %s' % mapping_results['Finding best mapping'])
#                print_function('   Total time   = %s' % mapping_results['Total time'])
#                print_function('\n')
#
#            transferred_structured = transfer.transfer(source_structured, mapping_rules)
#
#            new_target = transfer.get_transferred_target(transferred_structured)
#            #new_target = to_predicate
#            print_function('Best mapping found: %s \n' % mapping_rules)
#            #print('Tranferred structured tree: %s \n' % transferred_structured)
#            print_function('Transferred target predicate: %s \n' % new_target)

#            if to_predicate != new_target:
#                raise Exception('Head predicate mapping is different from expected: %s and %s \n' % (new_target, to_predicate))

        # Load new predicate target dataset
        tar_data = datasets.load(target, bk[target], target=to_predicate, balanced=balanced, seed=results['save']['seed'])

        # Group and shuffle
        if target not in ['nell_sports', 'nell_finances', 'yago2s']:
            [tar_train_facts, tar_test_facts] =  datasets.get_kfold(i, tar_data[0])
            [tar_train_pos, tar_test_pos] =  datasets.get_kfold(i, tar_data[1])
            [tar_train_neg, tar_test_neg] =  datasets.get_kfold(i, tar_data[2])
        else:
            [tar_train_facts, tar_test_facts] =  [tar_data[0][0], tar_data[0][0]]
            to_folds_pos = datasets.split_into_folds(tar_data[1][0], n_folds=n_folds, seed=results['save']['seed'])
            to_folds_neg = datasets.split_into_folds(tar_data[2][0], n_folds=n_folds, seed=results['save']['seed'])
            [tar_train_pos, tar_test_pos] =  datasets.get_kfold(i, to_folds_pos)
            [tar_train_neg, tar_test_neg] =  datasets.get_kfold(i, to_folds_neg)

        print_function('Target train facts examples: %s' % len(tar_train_facts))
        print_function('Target train pos examples: %s' % len(tar_train_pos))
        print_function('Target train neg examples: %s\n' % len(tar_train_neg))
        print_function('Target test facts examples: %s' % len(tar_test_facts))
        print_function('Target test pos	 examples: %s' % len(tar_test_pos))
        print_function('Target test neg examples: %s\n' % len(tar_test_neg))

        # generate transfer file
        transferred_structured = source_structured
        tr_file = transfer.get_transfer_file(bk[source], bk[target], predicate, to_predicate, searchArgPermutation=True, allowSameTargetMap=False)
        new_target = to_predicate

        random.shuffle(tar_train_pos)
        random.shuffle(tar_train_neg)
        for amount in [0.2, 0.4, 0.6, 0.8, 1.0]:
            print_function('Amount of data: ' + str(amount))
            part_tar_train_pos = tar_train_pos[:int(amount * len(tar_train_pos))]
            part_tar_train_neg = tar_train_neg[:int(amount * len(tar_train_neg))]

            # transfer and revision theory
            background = tboostsrl.modes(bk[target], [to_predicate], useStdLogicVariables=False, maxTreeDepth=maxTreeDepth, nodeSize=nodeSize, numOfClauses=numOfClauses)
            [model, t_results, structured, pl_t_results] = revision.theory_revision(background, tboostsrl, target, part_tar_train_pos, part_tar_train_neg, tar_train_facts, tar_test_pos, tar_test_neg, tar_test_facts, transferred_structured, transfer=tr_file, trees=trees, max_revision_iterations=1, print_function=print_function)
            #t_results['Mapping results'] = mapping_results
            t_results['parameter_' + str(amount)] = pl_t_results
            ob_save['transfer_' + str(amount)] = t_results
            print_function('Dataset: %s, Fold: %s, Type: %s, Time: %s' % (experiment_title, i+1, 'Transfer (trRDN-B)', time.strftime('%H:%M:%S', time.gmtime(time.time()-start))))
            print_function(t_results)
            print_function('\n')

            print_function('Start learning from scratch in target domain\n')

            # learning from scratch (RDN-B)
            [model, t_results, structured, will, variances] = revision.learn_test_model(background, tboostsrl, new_target, part_tar_train_pos, part_tar_train_neg, tar_train_facts, tar_test_pos, tar_test_neg, tar_test_facts, trees=trees, print_function=print_function)
            ob_save['rdn_b_' + str(amount)] = t_results
            print_function('Dataset: %s, Fold: %s, Type: %s, Time: %s' % (experiment_title, i+1, 'Scratch (RDN-B)', time.strftime('%H:%M:%S', time.gmtime(time.time()-start))))
            print_function(t_results)
            print_function('\n')

            # learning from scratch (RDN)
            background = tboostsrl.modes(bk[target], [new_target], useStdLogicVariables=False, maxTreeDepth=3, nodeSize=2, numOfClauses=20)
            [model, t_results, structured, will, variances] = revision.learn_test_model(background, tboostsrl, new_target, part_tar_train_pos, part_tar_train_neg, tar_train_facts, tar_test_pos, tar_test_neg, tar_test_facts, trees=1, print_function=print_function)
            ob_save['rdn_' + str(amount)] = t_results
            print_function('Dataset: %s, Fold: %s, Type: %s, Time: %s' % (experiment_title, i+1, 'Scratch (RDN)', time.strftime('%H:%M:%S', time.gmtime(time.time()-start))))
            print_function(t_results)
            print_function('\n')

        results_save.append(ob_save)
    save_experiment(results_save)
        #results['results'][experiment_title].append(results_save)
#    except Exception as e:
#        print_function(e)
#        print_function('Error in experiment of ' + experiment_title)
#        pass
    results['save']['experiment'] += 1
    results['save']['n_runs'] += 1
    save(results)
