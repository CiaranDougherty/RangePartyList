# Update 2017-06-02

My previous improvement to my algorithm?  Yeah.  It's Thiele's method, which was previously reinvented as Reweighted Range Voting.  Already attempted, and something I already dismissed as being problematic with Party List elections.   That was almost enough to make me give up on mulit-seat score/approval systems altogether.

Almost.  Instead, I decided to approach the problem from an entirely different angle.

Every Multi-Seat system using Range/Approval ballots I have seen to date focuses on changing the *weight* of ballots when a candidate has been seated.  Why?  Yes, you can consider that to be what is happening in a system such as Single Transferable Vote, but it occurs to me that such a conceptualization is a remove from what is actually going on.

In STV, when you seat a candidate and remove a Quota, are you really proportionally lowering the weight of everyone who voted that way?  Or are you saying that a proportion of that group directly elected the seated candidate?  Aren't you really just allowing the voters to sort themselves into ad-hoc "districts" based on policy rather than geography?  

Approached from that angle, isn't it effectively the antithesis of Gerrymandering?  Doesn't that mean that such a system might be the cure to disease that has plagued our nation almost from its founding?

To that end, the system I am working on allocates seats, by Hare quota.  For Range Voting, fractional quotas can be used because a fractional contribution to total is still meaningful.  For Majority Judgement, you might need to use Floor(Hare).  Droop or Hagenbach-Bischoff quotas are unnecessary for the same reason that ranked ballots have favorite betrayal: every ballot can (and does) contribute to/detract from all ballots concurrently.  With ranked ballots, it is necessary to have some number of ballots that are thrown out as "losing."  There is no such need with score/approval ballots... with one exception below.

Since score ballots have the option of scoring multiple ballots evenly, simply removing ballots with the highest score for the seated candidate doesn't work.  Instead, I order them by "degree of expressed preference," defined as Score(Candidate)/Score(AllCandidates).  Thus, bullet voters are eliminated first, and those that would be happy with other  candidates remain, continuing in their contributions to other candidates.

Which brings us to our exception.  Because a ballot which scores all candidates identically has no discriminative power, such "Full" (or "Empty") ballots are taken out of the totals when determining the Hare Quota, to be distributed evenly amongst all the seats.  While it would be easier to simply remove such ballots as meaningless, I believe it more representative to include them in the totals for each candidate.



# Update 2017-05-02

Turns out my algorithm's failure of the "Consistency" voting criterion is *way* bigger a problem than original anticipated.  What's more, the problem is only amplified by increased numbers of candidates and/or breadth of possible scores.  That defeats the purpose of my attempt to improve things, and I consider it wholly unacceptable.

The problem arose from my adjusting weights based on each ballot-grouping's proportion of votes that seated that candidate.  While improving Monotonicity, it was too strong an adjustment away from the flaws in Phragmén's method.  One solution I'm considering is to weight according to how much each ballot/voter *likes* the candidate that was just seated, not the total.  This appears (at least superficially) to be derivative of D'Hondt's method (at least for Approval voting).  Looking into that presently.





# RangePartyList
An algorithm for allocating multiple seats using Approval or Range voting systems.

Based on Lars Edvard Phragmen's Unordered Method (originally written ~1895 c.e.), this code means to allocate multiple seats using Range or Approval voting methods.

The basic principle is that whenever a candidate is seated, that "uses up" some of the voting power of the ballots that seated them, but still can contribute some amount to later candidates.  This is accomplished by dividing the vote contribution by 1+W, where W is proportional to that ballot group's contribution to the vote totals of candidates that ballot has helped to seat.

Where Phragmen's system sums votes of all ballots containing a paritcular candidate A, and divides them all by the sum of the weights (W) for all those ballots, mine only applies those weights to the ballots that originally incurred those weights.  Additionally, where Phragmen distributes the weight of seating candidate A *and* that candidate A voters previously accrued proprtionately to their support for A, I only ever distribute the weight of A, never redistributing weights, only ever adding to them.

I believe that, because of these differnces, my algorithm likely meets Montonicity Criterion of voting systems (q.v. "Monotonicity Criterion" on Wikpedia) where Phragmen's original algorithm does not.

If it does meet that criterion, if it can eliminate Favorite Betrayal, I would love for it to be implemented far and wide, as I believe that Favorite Betrayal is antithetical to democracy.

I'll decide on a license when I can wrap my head around the implications thereof.


