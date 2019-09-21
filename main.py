import pymzn as pm
from collections import deque
import time
#solns=pm.minizinc('solver_3.mzn','data2.dzn')
#decisions=solns[0]['decision']
#print(decisions)


adj_list=[]
prev_queue=deque()
def initialize():
    
    #global adj_list
    #adj_list=[]
    print("initializing")
    print(".......")
    print(".......")
    print("number of intersections:")
    n=int(input())
    
    data=[]
    for i in range(n): 
       # print("how many nodes associated with node "+str(i))
        #m=input(i)
        global adj_list
        print("input the nodes associated with node and the density of the road conncting them "+str(i+1))
        inp=input()
        inp=inp.split()
        lst=[int (j) for j in inp ]
        final_lst=[]
        index=0
        while index<len(lst):
            final_lst.append([lst[index],lst[index+1]])
            index=index+2
        print(final_lst)
        adj_list.append(final_lst)
        lst2=[0]*(n)
        for j in final_lst:
            print(j)
            lst2[j[0]-1]=j[1]
       # for j in range len(lst):
        data.append(lst2)
    max_cost=40
    max_turn=25
    print("how fast do you want the system to update signals?")
    signal_period=int(input())
    prev=[[0]*(n)]*(n)
    data={'n':n,'congestion_graph':data,'max_cost':max_cost,'max_turn':max_turn,'prev':prev}
    print(data)
    dzn=pm.dict2dzn(data,fout='datafrompython.dzn')
    #pm.dict2dzn(dzn, fout='capacity.dzn')
    return [dzn,signal_period]




def print_decision(decision):
    gr_list=[0]*len(decision)
    
    #print(decision)
    for lst_in in range(len(decision)):
        for i in range(len(decision[lst_in])):
            if decision[lst_in][i]==1:
                #print(lst_in)
                gr_list[lst_in]=i+1

    print(gr_list)
    for i in range(len(adj_list)):
        print("for intersection "+str(i))
        for j in range (len(adj_list[i])):
            if adj_list[i][j][0]==gr_list[i]:
                print("  road towards intersection "+str(adj_list[i][j][0])+" :## GREEN ## ",end='')
            else:
                print("  road towards intersection "+str(adj_list[i][j][0])+" :## RED ## ",end='')
        print("-------------------")


def update_cost(solns,dzn,period):
    data=pm.dzn2dict('datafrompython.dzn')
    decision=solns[0]['decision']
    gr=data['congestion_graph']

    #print("decision")
    #print(decision)


    rate_dec=2
    for i in range(len(adj_list)):
        reduction=3*period
        for j in range(len(adj_list)):
            if decision[i][j]==1:
                if reduction>gr[i][j]:
                    reduction=gr[i][j]
                gr[i][j]-=reduction

                prev_queue.append([i,j])
                if len(prev_queue)>100:
                    prev_queue.popleft()
            elif  j in adj_list[i]:
                gr[j][i]+=reduction//3
    print("congestion_graph")
    print(gr)
    data['congestion_graph']=gr
    n=len(gr)
    prev = [[0] * n for i in range(n)]
    #print("prev queue")
    #print(prev_queue)
    #(prev[0])[1]=-2
   # print(prev)
    #exit()
    for pair in prev_queue:
       # print(pair)
        #print(pair[0])
        
        #print(pair[1])
        #prev[0][0]=1
        prev[pair[0]][pair[1]]+=1
      #  print(prev)
    data['prev']=prev 
   # print("prev")
    #print(prev)
    dzn=pm.dict2dzn(data)
    return dzn       
                
                



if __name__ == "__main__":
    print("system online")
    [dzn,signal_period]=initialize()
    print("starting operation")
    print(".....................................")
    print(".....................................")
    i=0
    while 1==1:
        i+=1
        print("decision for interval #"+str(i))
        solns=pm.minizinc('solver_3.mzn',data=dzn)
        decision=solns[0]['decision']
        print_decision(decision)
        dzn=update_cost(solns,dzn,signal_period)
      #  exit()
        time.sleep(5)

    

#implement u-turn
