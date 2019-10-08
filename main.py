import pymzn as pm
import os
from collections import deque
import time

adj_list=[]
prev_queue=deque()
def initialize():
    print("initializing")
    print(".......")
    print(".......")
    print("number of intersections:")
    n=int(input())
    
    data=[]
    importance=[]
    for i in range(n): 
        global adj_list
        print("input the nodes associated with current node and the congestion and importance of the road conncting them in the format \"road cogestion imortance\""+str(i+1))
        inp=input()
        inp=inp.split()
        lst=[int (j) for j in inp ]
        final_lst=[]
        index=0
        while index<len(lst):
            final_lst.append([lst[index],lst[index+1],lst[index+2]])
            index=index+3
        print(final_lst)
        adj_list.append(final_lst)
        lst2=[0]*(n)
        lst_imp=[0]*(n)
        for j in final_lst:
            print(j)
            lst2[j[0]-1]=j[1]
            lst_imp[j[0]-1]=j[2]
        data.append(lst2)
        importance.append(lst_imp)   

    data_max={'n':n,'congestion_graph':data,'importance':importance}
    dzn=pm.dict2dzn(data_max,fout='max_find.dzn')
    sol_max=pm.minizinc('maximum_calculator.mzn','max_find.dzn')
    

    max_cost=sol_max[0]['max_cost']
    max_imp=sol_max[0]['max_imp']
    print(max_cost,"look at this max_cost")
    print(max_imp,"look at this max_imp")
    max_turn=25
    print("how fast do you want the system to update signals?")
    signal_period=int(input())
    prev=[[0]*(n)]*(n)
    data={'n':n,'congestion_graph':data,'max_cost':max_cost,'max_turn':max_turn,'prev':prev,'importance':importance,'max_imp':max_imp}
    print(data)
    dzn=pm.dict2dzn(data,fout='datafrompython.dzn')
    return [dzn,signal_period]




def print_decision(decision):
    gr_list=[0]*len(decision)
    data=pm.dzn2dict('datafrompython.dzn')
    print(data)
    graph=data['congestion_graph']
    importance=data['importance']
    for lst_in in range(len(decision)):
        for i in range(len(decision[lst_in])):
            if decision[lst_in][i]==1:
                gr_list[lst_in]=i+1

    print(gr_list)
    for i in range(len(adj_list)):
        print("for intersection "+str(i+1)+" =============================>>>>>>>>>")
        for j in range (len(adj_list[i])):
            if adj_list[i][j][0]==gr_list[i]:
                print("  road towards intersection "+str(adj_list[i][j][0])+" congestion:"+str(graph[i][adj_list[i][j][0]-1])+" importance: "+str(importance[i][adj_list[i][j][0]-1]) +" decision :## GREEN ## ")
            else:
                print("  road towards intersection "+str(adj_list[i][j][0])+" congestion:"+str(graph[i][adj_list[i][j][0]-1])+" importance: "+str(importance[i][adj_list[i][j][0]-1]) +" decision :## RED ## ")
        print("-------------------")


def update_cost(solns,dzn,period):
    data=pm.dzn2dict('datafrompython.dzn')
    decision=solns[0]['decision']
    gr=data['congestion_graph']
    rate_dec=2
    for i in range(len(adj_list)):
        reduction=rate_dec*period
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
    for pair in prev_queue:
        prev[pair[0]][pair[1]]+=1
    data['prev']=prev 
    dzn=pm.dict2dzn(data)
    return dzn       
                
                



if __name__ == "__main__":
    print("system online")
    os.chdir("E:/AI project/")
    [dzn,signal_period]=initialize()
    print("starting operation")
    print(".....................................")
    print(".....................................")
    i=0
    while True:
        i+=1
        print("decision for interval #"+str(i))
        solns=pm.minizinc('main_solver.mzn',data=dzn)
        decision=solns[0]['decision']
        print_decision(decision)
        dzn=update_cost(solns,dzn,signal_period)
        print("to quit type CTRL+C")
        time.sleep(signal_period)

    

