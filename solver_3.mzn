include "globals.mzn";

int :n;
array[1..n,1..n,0..1] of int: congestion_graph;
array[1..n,1..n] of var 0..1:decision;
%array[1..n] of var 1..n:index;

int:max_cost;




var 1..max_cost*n :sum_cost;
array[1..n] of var 0..max_cost:val;


%array[1..n,1..n] of int:prev_dec;%keeps track of numbers of each node opened in last 100 tries

constraint forall(i in 1..n)
(
    sum(j in 1..n)(decision[i,j])==1

);

constraint forall(i in 1..n,j in 1..n)
(
    if decision[i,j]==1 then val[i]=congestion_graph[i,j,0] else true endif

);

constraint sum_cost=sum(i in 1..n )( val[i]);


solve maximize sum_cost;