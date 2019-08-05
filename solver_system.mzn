%takes current condition of the road and then gives out optimized decision about the traffic lights
include "globals.mzn";

%we need adjacency list for representing the map. nodes=intersections, edges=roads;
int: intersection_no;
int: road_no;
int: signal_no;
int: yellow;
array[1..intersection_no,1..intersection_no] of 1..road_no:map;  %adjacency matrix
% the graph is stored using a adjacecny matrix,map[i,j]=e means node i and node j are connected using edge e;

%arrays to store road length and no. of cars on the road;
array[1..road_no] of int:length_road;   
array[1..road_no] of int:no_of_car_road;

%signal of each intersection, here we have assumed each intersection has 4 signals max. and eaxch signal has 3 attributes signal cycle time,green start time and total green time
%signal[i,s,a] means i'th intersection's sth signal's id
array[1..intersection_no,1..4] of 1..signal_no:signal;
array[1..signal_no] of var int:green_duration;
array[1..signal_no] of var int:cycle_time;
array[1..signal_no] of var int:green_start_time;

constraint forall(i in 1..signal_no)(green_duration[i]>=0.2*cycle_time[i]/\green_duration[i]<=0.8*cycle_time[i]);  %to make sure green time is reasonable with respect to the cycle time
constraint forall(i in 1..signal_no)(
    
    green_start_time[i]>=0/\green_start_time[i]<=cycle_time[i]-green_duration[i]%to make sure that green time,green duration and cycle time is consistant with each other;

);

%all signals in the same intersection must have same cycl length
%all signals in the same  intersection must not be green at the same time

constraint forall(i in 1..intersection_no)(
    cycle_time[signal[i,1]]=cycle_time[signal[i,2]]/\cycle_time[signal[i,2]]=cycle_time[signal[i,3]]/\cycle_time[signal[i,3]]=cycle_time[signal[i,4]]
);

constraint forall(i in 1..intersection_no)(
    forall(j in 1..4,k in 1..4)
    (
        if j!=k then green_start_time[signal[i,k]]> green_start_time[signal[i,j]]+green_duration[signal[i,j]]  \/ green_start_time[signal[i,k]]<green_start_time[signal[i,j]] else true endif
    )
      

);



