import math 

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.left = None
        self.right = None

'''
K-D tree implementation for 2 dimensions
'''
class SearchTree:
    def __init__(self):
        self.head = None
        self.vis = 0
    
    def push(self, x, y):
        put = Node(x, y)
        if(self.head == None):
            self.head = put 
        else:
            lvl = 0
            curr = self.head
            while(True):
                putVal = put.x
                currVal = curr.x
                if(lvl%2 == 1):
                    putVal = put.y
                    currVal = curr.y

                if(putVal < currVal):
                    if(curr.left == None):
                        curr.left = put 
                        break
                    else:
                        curr = curr.left
                else:
                    if(curr.right == None):
                        curr.right = put
                        break
                    else:
                        curr = curr.right
                lvl += 1

    def query(self, x, y, dbg):
        self.vis = 0
        return (self.dfs(self.head, 0, x, y, dbg), self.vis)

    def dfs(self, curr, lvl, x, y, dbg):
        self.vis += 1
        if(dbg):
            print('At node', curr.x, curr.y, self.vis)
            if(lvl % 2 == 0):
                print('VERTICAL')
            else:
                print('HORIZONTAL')
        res = ((x-curr.x) ** 2 + (y-curr.y) ** 2)
        qVal = x
        currVal = curr.x
        if(lvl%2 == 1):
            qVal = y
            currVal = curr.y
        
        if(qVal > currVal):
            if(curr.right != None):
                if(dbg):
                    print('Moved right')
                res = min(res, self.dfs(curr.right, lvl + 1, x, y, dbg))

            if((curr.left != None) and (abs(qVal - currVal) ** 2 < res)):
                if(dbg):
                    print('Better on left')
                res = min(res, self.dfs(curr.left, lvl + 1, x, y, dbg))
        else:
            if(curr.left != None):
                if(dbg):
                    print('Moved left')
                res = min(res, self.dfs(curr.left, lvl + 1, x, y, dbg))
            
            if((curr.right != None) and (abs(currVal - qVal) ** 2 < res)):
                if(dbg):
                    print('Better on right')
                res = min(res, self.dfs(curr.right, lvl + 1, x, y, dbg))
                
        return res


if __name__ == '__main__':
    st = SearchTree()
    st.push(2, 6)
    st.push(5, 4)
    st.push(8, 7)
    st.push(3, 1)
    st.push(10, 2)
    st.push(13, 3)
    print(st.query(9, 4, False))