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


