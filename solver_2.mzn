include "globals.mzn";

int :n;
array[1..n,1..n,0..1] of float: congestion_graph;
array[1..n,1..n] of var 0..1:decision;
array[1..n] of var 1..n:index;


array[1..n] of var float:val;


array[1..n,1..n] of int:prev_dec;%keeps track of numbers of each node opened in last 100 tries

constraint forall(i in 1..n)(
    val[i] = max(j in 1..n where congestion_graph[i,j,0]>=0/\prev_dec[i,j]<congestion_graph[i,j,0]/sum(p in 1..n)(congestion_graph[i,p,0]))(
        congestion_graph[i,j,0]
    )
    
    
);
constraint forall(i in 1..n)(
    forall(j in 1..n)
    (
        if val[i]==congestion_graph[i,j,0] then index[i]=j else true endif
    )

);



constraint forall(i in 1..n)(
    forall(j in 1..n)
    (
        if j==index[i] then decision[i,j]=1 else decision[i,j]=0 endif
    
    )


);



solve satisfy;