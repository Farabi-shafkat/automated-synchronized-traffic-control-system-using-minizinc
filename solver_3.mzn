include "globals.mzn";

int :n;
array[1..n,1..n] of int: congestion_graph;

array[1..n,1..n] of var 0..1:decision;


int:max_cost;
int:max_turn;
  
array[1..n,1..n] of int:prev;

var 1..max_cost*n :sum_cost;
array[1..n] of var 0..max_cost:val;




constraint forall(i in 1..n)
(
    sum(j in 1..n)(decision[i,j])==1

);

constraint forall(i in 1..n,j in 1..n)
(
    if decision[i,j]==1 then prev[i,j]<max_turn*(congestion_graph[i,j]/(sum(k in 1..n)(congestion_graph[i,k]))) else true endif

);

constraint forall(i in 1..n,j in 1..n)
(
    if decision[i,j]==1 then val[i]=congestion_graph[i,j] else true endif

);



constraint sum_cost=sum(i in 1..n )( val[i]);


solve maximize sum_cost;
%5, 23, 22, 8, 25, 18, 10, 24, 14