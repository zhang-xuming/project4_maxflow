import time
import bucket
from myBFS import BFS
f=open('outgraph_7.txt','r')
graph=[]
Z={}
H={}
for line in f:
    line =line.replace("\n","")
    graph.append(list(map(int,line.split(' '))))
f.close()
num=graph[0][0]    #num记录图中点的总个数
s=graph[0][2]      #s记录起点
t=graph[0][3]      #t记录终点
del graph[0]
for item in graph:       #正向图Z
    if item[0] not in Z:
        Z[item[0]] = {}
        Z[item[0]][item[1]] = item[2]
    else:
        Z[item[0]][item[1]] = item[2]
    if item[1] not in Z:
        Z[item[1]] = {}
        Z[item[1]][item[0]] = 0
    else:
        if item[0] not in Z[item[1]]:
            Z[item[1]][item[0]] = 0

for item in graph:       #反向图H
    if item[1] not in H:
        H[item[1]] = {}
        H[item[1]][item[0]] = item[2]
    else:
        H[item[1]][item[0]] = item[2]
    if item[0] not in H:
        H[item[0]] = {}
        H[item[0]][item[1]] = 0
    else:
        if item[1] not in H[item[0]]:
            H[item[0]][item[1]] = 0

t0=time.perf_counter()
parent={}
parent[t]=""
level={}
level[t]=0
BFS(parent,level,H,t)    #反向BFS并设置高度，记录在level中

j=0
for i in level:
   if j<level[i]:
       j=level[i]
level[s]=j+1     #此处稍作修改，并没有维持不变式1即s点的高度为n,改为它的高度为所有节点最高高度加1，速度快很多，具体说明见报告

B=bucket.build_bucket(num)    #建立一个桶
location=[num]    #随便取一个桶中位置作为初始位置
a=[1]             #创建一个List,记录是否还有盈余,初始值设置为1
for i in level:   #将每个节点的信息初始化，并插入桶中
    flag=[0,i,level[i]]   #flag的参数依次代表盈余值、节点标号，高度
    bucket.insert(B,flag)
for i in Z[s]:       #初始化起点s，即initialize操作。进行s的出边中进行饱和推送并更新剩余网络
    if i in level:
        for flag in B[level[i]]:
            if i==flag[1] :
                flag[0]=Z[s][i]
                Z[i][s]=Z[i][s]+Z[s][i]
    Z[s][i] = 0

while a[0]!=0:    #主函数，仍然存在盈余点，循环继续
    a[0]=0
    for i in range(num*2):   #设计为每轮为2*num个元素，若有操作，则更新a[0]=1,说明有盈余；若无操作，则a[0]=0,说明没盈余了
        bucket.push_relabel(B,Z,level,location,a,t,s,num)  #push-relabel

print("maximum flow:",B[0][0][0])
print("time:",time.perf_counter()-t0)