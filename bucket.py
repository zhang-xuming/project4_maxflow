def build_bucket(num):
    B=[[] for i in range(num*2) ]    #建立2*num大小的桶
    return B

def insert(B,flag):        #元素根据高度插入桶中
    i=flag[2]
    B[i].append(flag)

def push_relabel(B,Z,level,location,a,t,s,num):
    j=0
    if B[location[0]]:   #当桶对应位置不为空
        for flag in B[location[0]]:   #遍历对应位置桶中元素
            mark = 0      #用来判断是否进行了push操作
            if flag[0]>0:       #对应位置桶中元素有盈余
                a[0]=1
                for i in Z[flag[1]]:    #在字典中找它的邻点
                    if i in level:
                        if Z[flag[1]][i]>0 and level[i]+1==level[flag[1]]:   #满足有flag[1]到i的增广边且满足高度不变式
                            push(Z,B,level,i,flag,a,t,s)               #向i点推送
                            mark=1
                    if flag[0]==0:     #若把盈余推完了则提前结束小循环
                        break
                if mark==0:           #说明有盈余但没有push操作，则需进行relabel操作
                    if flag[1]!=t:    #终点t不能relabel，为了维护高度不变式
                        flag=B[location[0]].pop(j)   #取出该元素
                        flag[2] = flag[2] + 1        #relabel，高度增加1
                        level[flag[1]]=level[flag[1]]+1
                        insert(B,flag)        #插入桶中对应位置
                    location[0] = location[0] + 1
                    return 1   #此处的return只起到提前结束本次函数调用的作用
            j=j+1
    location[0]=location[0]-1    #更新location值
    if len(B[location[0]])==1 and location[0]==0:   #起到循环作用
        location[0]=num*2-1

def push(Z,B,level,i,flag,a,t,s):
    if flag[0]>=Z[flag[1]][i] :    #饱和推送
        for item in B[level[i]]:     #节点i在桶中的位置
            if item[1]==i:            #进行饱和推送
                item[0]=item[0]+Z[flag[1]][i]
                flag[0]=flag[0]-Z[flag[1]][i]
                break
        Z[i][flag[1]]=Z[i][flag[1]]+Z[flag[1]][i]  # 更新剩余网络
        Z[flag[1]][i]=0
    else:
        Z[i][flag[1]]=Z[i][flag[1]]+flag[0]    #更新剩余网络
        Z[flag[1]][i]=Z[flag[1]][i]-flag[0]
        for item in B[level[i]]:     #节点i在桶中的位置
            if item[1]==i:          #进行非饱和推送
                item[0]=item[0]+flag[0]
                flag[0]=0
                break
    if i==s:        #如果是发现向源点s推送流，则不再更新源点s的盈余值，以防止其在后面的循环中s进行relabel操作，破坏了高度不变式。这里将s的盈余值设置为0
        item[0]=0
