# Recognition and First-Line Lab

For each item, write only the **best first move** or choose the best option. Do not complete a long solution unless needed to justify the choice.

## Recognition

1. A problem gives people and which pairs exchange messages. Which graph model is natural?
   A. vertices are messages  B. vertices are people and edges are communicating pairs  C. edges are people  D. colours are messages

2. You know every vertex degree but not the edge list. Which identity should you test first?
   A. inclusion-exclusion  B. `sum degrees=2|E|`  C. Pythagoras  D. a recurrence

3. Four colours are assigned to vertices, and adjacent vertices must differ. What is being counted?
   A. unrestricted assignments  B. proper vertex colourings  C. edge lengths  D. game states

4. A graph is “complete except for one missing edge.” Why does the missing edge matter in a colouring count?
   A. its endpoints may be allowed to share a colour  B. it changes the number of colours  C. it creates a loop  D. it forces every colour to be used

5. A local colour restriction is stated around a polygon. What must be checked before treating it like a line of positions?
   A. whether colours are integers  B. cyclic wrap-around  C. vertex coordinates  D. polygon area

6. You count every legal knight move from every starting square, but the question asks for unordered pairs of squares joined by a knight move. What must be verified before halving?
   A. every pair was counted exactly twice  B. the board is square  C. the knight is centred  D. every square has equal degree

7. A geometry problem asks about cevians and regions, but lengths and angles never enter the answer. Which representation may be cheaper?
   A. incidence/intersection graph  B. trigonometry  C. coordinates of every point  D. mensuration

8. Players alternately choose legal moves and try to force a win. Which warning is correct?
   A. every game is just a proper colouring  B. a static graph count may not capture turn/history information  C. degree sum always gives the winner  D. ignore strategy

## First lines

9. Six students are connected when they are friends. Write one sentence defining the vertices and edges.

10. A graph has degrees `4,3,3,2,2,2`. Write the line that determines the number of edges.

11. A triangle is properly coloured with 5 available colours. Write the stage-by-stage choice product, without evaluating it.

12. Vertices of a cycle must have different colours whenever their cyclic distance is at most 2. State which pairs become edges in the conflict graph.

13. A board problem asks for unordered knight-move pairs. Write the graph interpretation of one vertex and one edge.

14. Eight lines each pass through three selected points, and every selected point lies on exactly two of the lines. Define the incidence set you would count two ways.

15. The edges of `K5` are red/blue and monochromatic triangles are forbidden. State the local structure you should inspect first.

16. A token-moving problem is adversarial. Write the extra information a game state needs beyond the static move graph.
