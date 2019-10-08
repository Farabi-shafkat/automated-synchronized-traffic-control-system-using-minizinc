include "globals.mzn";
int: n;

array[1..n,1..n] of int: congestion_graph;

var int: max_cost;
constraint max_cost=max(i in 1..n,j in 1..n)(congestion_graph[i,j]);
solve satisfy;
