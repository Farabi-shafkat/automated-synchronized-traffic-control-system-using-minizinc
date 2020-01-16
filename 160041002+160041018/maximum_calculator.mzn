include "globals.mzn";
int: n;

array[1..n,1..n] of int: congestion_graph;

array[1..n,1..n] of int: importance;


var int: max_cost;
var int: max_imp;

constraint max_cost=max(i in 1..n,j in 1..n)(congestion_graph[i,j]);

constraint max_imp=max(i in 1..n,j in 1..n)(importance[i,j]);

solve satisfy;
