# COMB-05 - First-Step Reference

## One router

`FORCED EXISTENCE? -> CHOOSE BOXES -> COMPARE OBJECTS WITH CAPACITY -> FORCE COLLISION`

If the problem asks for a largest/smallest possible structure rather than mere existence, switch to:

`CHOOSE AN EXTREME OBJECT -> ASK WHAT ITS EXTREMENESS FORBIDS -> COUNT/CONTRADICT -> CHECK SHARPNESS`

## Recognition atlas

| Surface clue | Structural question | First useful line |
|---|---|---|
| more objects than categories | what are the categories? | define objects and boxes explicitly |
| at least k+1 in one class | what is the maximum allowed per box if the claim fails? | failed claim gives at most k per box |
| distances / intervals / cells | can the region be partitioned into small-diameter boxes? | state the partition and its diameter bound |
| residues / divisibility | which residue or divisor-signature classes make equal-box membership useful? | name the residue classes |
| largest / smallest / nearest / farthest | what local consequence follows from that choice? | choose the extreme object and write the forbidden improvement |
| exact count requested | is existence enough? | if not, retrieve direct counting/complement/IE instead |

## Three mandatory boundaries

**Pigeonhole vs inclusion-exclusion.** Pigeonhole proves that some collision must occur; inclusion-exclusion computes the size of a union or overlap-corrected count. If no exact number of outcomes is requested, try inevitability first.

**Extremal choice vs inequality optimization.** Extremal reasoning chooses an object from a finite configuration and exploits what would improve it. Inequality optimization bounds a numerical expression. Do not replace a structural contradiction with AM-GM merely because the word maximum appears.

**Counting average vs structural inevitability.** An average can suggest a threshold, but the proof is the capacity statement: if every box stayed below the threshold, the total capacity would be too small.

## Quick checks

- Are the boxes exhaustive?
- Are they disjoint, or have you stated how ties are assigned?
- Is the capacity bound correct?
- Does the collision actually imply the target relation?
- In an extremal proof, did you use the extremal property, not merely name an extreme object?
