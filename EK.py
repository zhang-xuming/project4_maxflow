from myBFS import BFS
import time
f=open('outgraph_7.txt','r')
graph=[]
Z={}
for line in f:
    line =line.replace("\n","")
    graph.append(list(map(int,line.split(' '))))
f.close()
s=graph[0][2]            #s为源点
t=graph[0][3]            #t为目的点
del graph[0]
for item in graph:           #将图存入字典嵌套字典的结构中
    if item[0] not in Z:
        Z[item[0]] = {}
        Z[item[0]][item[1]] = item[2]
    else:
        Z[item[0]][item[1]] = item[2]
    if item[1] not in Z:         #初始化剩余网络
        Z[item[1]] = {}
        Z[item[1]][item[0]] = 0
    else:
        if item[0] not in Z[item[1]]:
            Z[item[1]][item[0]] = 0

t0=time.perf_counter()
parent={}             #这些参数具体在myBFS.py文件中说明
level={}
level[s]=0
BFS(parent,level,Z,s)   #先进行一次BFS，找到最小跳数路径

sum=0              #记录最大流
while t in level:   #只要还存在增广路径，循环继续
    flag=t
    flow=10000
    while flag!=s:    #本次循环的作用是确定增广路径的增广容量
        if flow >= Z[parent[flag]][flag]:
            flow=Z[parent[flag]][flag]
        flag=parent[flag]
    flag=t
    while flag!=s:   #本次循环的作用是沿着增广路径输送上面求得的增广容量大小的流，并更新剩余网络
        Z[parent[flag]][flag]=Z[parent[flag]][flag]-flow
        Z[flag][parent[flag]]=Z[flag][parent[flag]]+flow
        flag=parent[flag]
    sum=sum+flow     #更新最大流值
    parent = {}
    parent[s] = ""
    level={}
    level[s]=0
    BFS(parent, level, Z, s)     #找最小跳数路径

print("maximum flow:",sum)
print("time:",time.perf_counter()-t0)


