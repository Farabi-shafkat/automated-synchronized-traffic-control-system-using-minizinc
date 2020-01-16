include "globals.mzn";

int :n;
array[1..n,1..n] of int: congestion_graph;

array[1..n,1..n] of var 0..1:decision;

array[1..n,1..n] of int: importance;


int:max_imp;
int:max_cost;
int:max_turn;
  
array[1..n,1..n] of int:prev;

var 1..max_cost*n :sum_cost;
array[1..n] of var 0..max_cost:val;
array[1..n] of var 0..max_imp: imp_val;
var 1..max_imp*n :sum_imp;


constraint forall(i in 1..n)
(
    sum(j in 1..n)(decision[i,j])==1   %to make sure only one road in each intersection is open

);

constraint forall(i in 1..n,j in 1..n)
(
    if decision[i,j]==1 then prev[i,j]<=max_turn*(congestion_graph[i,j]/(sum(k in 1..n)(congestion_graph[i,k]))) else true endif    %to make sure that no direction can monopolize the road
                                                                                                                                    /*
                                                                                                                                      This is making sure that the number of times a road at an intersection is 
                                                                                                                                      kept open never exceeds its maximum limit, which is :
                                                                                                                                           max_turn*(congestion of that road)/sum of congestion of that
                                                                                                                                                                               intersection              
                                                                                                                                       prev array keeps track of how many times the which road was open in past           
                                                                                                                                       100 turns.
                                                                                                                                       
                                                                                                                                       this ensures other roads are eventually opened even if the same road 
                                                                                                                                       always remains congested;   
                                                                                                                                           
                                                                                                  
                                                                                                                                    
                                                                                                                                    */

);

constraint forall(i in 1..n,j in 1..n)
(
    if decision[i,j]==1 then val[i]=congestion_graph[i,j] else true endif  % to make sure val[i] carries the decision so that later can be summed



);

constraint forall(i in 1..n,j in 1..n)
(
    if decision[i,j]==1 then imp_val[i]=importance[i,j] else true endif %to make sure imp_val[i] carries the importance of the ith chosen road's importance road
);

constraint forall(i in 1..n,j in 1..n)
(

    if decision[i,j]==1 then congestion_graph[i,j]!=0 else true endif %no matter how important a road is, it will never open when it is empty
  

);
constraint forall(i in 1..n,j in 1..n)
(

    if decision[i,j]==1 then importance[i,j]>=0 else true endif  %assigning negative importance completely shuts downm a road;

);

constraint sum_cost=sum(i in 1..n )( val[i]);   %sum of all cost values
constraint sum_imp=sum(i in 1..n)(imp_val[i]);  %sum of all importance values

solve maximize (sum_cost+sum_imp);   %the sum of both have to be minimized, meaning that the system
                                     %has to find a compromise between opening the most congested 
                                     % and the most important roads. 
                                     %it gives slight priority to roads that have highesr importance values
                                     %it eventually opens other less important roads with accumulated traffic
                                     %it will open roads with more umportance values
                                     %more frequenctly 
%5, 23, 22, 8, 25, 18, 10, 24, 14