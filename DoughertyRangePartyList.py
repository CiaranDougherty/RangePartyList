#!/usr/bin/env python

#written for python 3

from datetime import datetime as dt
import logging,csv,os


__author__ = "Ciaran Dougherty"
__copyright__ = "Copyright 2017, Ciaran Dougherty"
__credits__ = ["Ciaran Dougherty"]
__version__ = "0.2.8"
__maintainer__ = "Ciaran Dougherty"
__email__ = "ciaran.dougherty@gmail.com"
__status__ = "Development"


#time, logging info.  Move to __main__ when I write it...
todayiso = dt.isoformat(dt.now())[:10]
logname = "DRV%s.log" % todayiso
i=0
while os.path.exists(logname):
    i += 1
    logname = "DRV%s(%s).log" % (todayiso,i)

logging.basicConfig(filename=logname,level=logging.INFO)


def convert_ballots(ballotSet):
    """Adds a preliminary weight of 0 to each ballot
    Input ballot format: [Candidate1 Score,...,CandidateN Score,Grouping Count]"""
    for ballot in ballotSet:
        #set base load
        ballot.append(0)
        #Output format: [C1 Score,...,CN Score,Count,Load]
    return ballotSet


def calculate_totals(ballotSet):
    """Calculates the Total Initial Votes.
    Originally for ease of Load calculation with Phragmén's method.
    Overloaded to determine eligibility for multiple seats"""

    #element [-2] is the count of votes for that vote grouping
    candidateTotal = [0]*len(ballotSet[0][:-2])
    for candidate in range(len(candidateTotal)):
        for ballot in ballotSet:
            candidateTotal[candidate]+= ballot[candidate]*ballot[-2]
    return candidateTotal

def max_voting_power(ballotSet,candidateTotal):
    "Determines the candidate with the highest weighted-vote total"
    global loadedVote
    loadedVote=[]
    for candidate in range(len(ballotSet[0][:-2])):
        candidateVote = 0.0
        #if still allowable
        if candidateTotal[candidate]:
            for ballot in ballotSet:
                candidateVote += ballot[candidate]*ballot[-2]/(1+ballot[-1])
                #this should apply if and only if they contribute to the vote
        loadedVote.append(candidateVote)
    logging.info("My loaded vote: %s" % loadedVote)
    #####TO DO####
    #Implement Beam Search on Ties?
    #Break ties in favor of Max/VarPhragmen?
    #If no difference, random.rand_range(len(Paths))?
    newSeat = loadedVote.index(max(loadedVote))
    return newSeat #index

def adjust_voting_load(ballotSet,newSeat):
    "Adjusts the load according to contribution to most recently seated candidate"
    adjustment = 0 
    for ballot in ballotSet:
        '''#print(ballot[-1])'''
        #determine contribution to the candidate's total
        contribution = float(ballot[newSeat])*ballot[-2]/(1+ballot[-1])
        #adds to the load as function of contribution / weighted vote total
        ballot[-1] += contribution/float(loadedVote[newSeat])
    
        logging.debug("Added Weight %s / %s or %s" %
                      (contribution,float(loadedVote[newSeat])
                        ,contribution/float(loadedVote[newSeat])))
        #track the total adjustment
        adjustment+= (contribution/float(loadedVote[newSeat]))
        #print(ballot[-1])
        logging.debug("New Ballot Weights: %s" % ballot)
    #logs an error message if precision less than 11 decimal places
    #11 decimal places based on 1/world population, with 2 extra places for margin of error
    precision = "{:.11f}".format(adjustment % 1)[1:]
    if precision.count("0") < 11:
        logging.error("New adjustment: {:.13f}".format(adjustment))
    return ballotSet

def seat_candidates(ballotSet,seats,maxSeats):
    """Main function.  Designed to accomodate Party List
    Max Seats technically separte from total number
    Could probably default to 1 or seats, depending on most frequent use"""
    seated = []
    mySeated = []
    #while seats are available
    while len(seated) < seats:
        #find the next seat
        newSeat = max_voting_power(ballotSet,candidateTotal)
        #seat them
        seated.append(newSeat)
        #adjust load accordingly
        ballotSet = adjust_voting_load(ballotSet,newSeat)
        #remove from ballots if appropriate
        if seated.count(newSeat) >= maxSeats:
            candidateTotal[newSeat]=0
    #print(seated)
    logging.info(seated)
    candidateSeats = []
    #Also return count of seats per party
    #for ease of Party List calculation
    for candidate in set(seated):
        candidateSeats.append("%s: %s seats" % (candidate,seated.count(candidate)))
    logging.info(", ".join(candidateSeats))

def initialize_ballots(inputBallots):
    global ballotSet
    ballotSet = convert_ballots(inputBallots)
    global candidateTotal
    candidateTotal = calculate_totals(inputBallots)

logging.info("Begin Example 3.7")
PhragmenExample = [[1,1,1,0,0,0,1034],
                    [0,0,0,1,1,1,519],
                    [1,1,0,0,1,0,90],
                    [1,0,0,1,1,0,47]]
logging.info("Indexes are as follows: 0: A, 1: B, 2: C, 3: P, 4: Q, 5: R")
initialize_ballots(PhragmenExample)
seat_candidates(ballotSet,4,1)
logging.info("Phragmén's method predicts outcome to be 0,4,1/AQB")


logging.info("\nBegin Example 14.4")
ACA = [[1,1,0,0,10],
        [0,0,1,0,3],
        [0,0,0,1,12],
        [1,1,1,0,21],
        [0,0,1,1,6]]

ABC = [[1,1,0,0,11],
        [0,0,1,0,3],
        [0,0,0,1,12],
        [1,1,1,0,21],
        [0,0,1,1,6]]

logging.info("Indexes are as follows: 0: A1, 1: A2, 2: B, 3: C")
initialize_ballots(ACA)
seat_candidates(ballotSet,3,1)
logging.info("Phragmén's method predicts outcome to be 0,3,1/ACA")
initialize_ballots(ABC)
seat_candidates(ballotSet,3,1)
logging.info("Phragmén's method predicts outcome to be 0,2,3/ABC")




logging.info("\nBegin Example 14.5")
aab = [[1,1,0,0,4],
        [0,0,1,0,7],
        [1,1,1,0,1],
        [1,1,0,1,16],
        [0,0,1,1,4]]

abc = [[1,1,0,0,4],
        [0,0,1,0,6],
        [1,1,1,0,2],
        [1,1,0,1,16],
        [0,0,1,1,4]]

logging.info("Indexes are as follows: 0: A1, 1: A2, 2: B, 3: C")
initialize_ballots(aab)
seat_candidates(ballotSet,3,1)
logging.info("Phragmén's method predicts outcome to be 0,2,1/ABA")
initialize_ballots(abc)
seat_candidates(ballotSet,3,1)
logging.info("Phragmén's method predicts outcome to be 0,3,2/ACB")


logging.info("\nBegin Example 14.5a")
aab = [[1,1,0,0,4],
        [0,0,1,0,9],
        [1,1,1,0,1],
        [1,1,0,1,16],
        [0,0,1,1,4]]

abc = [[1,1,0,0,4],
        [0,0,1,0,8],
        [1,1,1,0,2],
        [1,1,0,1,16],
        [0,0,1,1,4]]

logging.info("Indexes are as follows: 0: A1, 1: A2, 2: B, 3: C")
initialize_ballots(aab)
seat_candidates(ballotSet,3,1)
logging.info("Phragmén's method predicts outcome to be 0,2,1/ABA")
initialize_ballots(abc)
seat_candidates(ballotSet,3,1)
logging.info("Phragmén's method predicts outcome to be 0,3,2/ACB")