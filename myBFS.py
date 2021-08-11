def BFS(parent,level,Z,s):
    frontier = [s]      #前继节点集合
    i=1
    while frontier:
        next = []
        for u in frontier:
            for v in Z[u]:
                if v not in level and Z[u][v] > 0:  #增广容量不为零
                    level[v] = i       #level记录在BFS中的层数
                    parent[v] = u      #记录母节点
                    next.append(v)     #将子节点加入next集合中
        frontier = next
        i=i+1

