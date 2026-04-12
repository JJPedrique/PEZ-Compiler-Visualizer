class Tree:
    class Node:
        def __init__(self,newValue):
            self.Parent = None
            self.Token = newValue
            self.Children = []
            
    def __init__(self,RootNode):
        self.Root = None
        self.Previus = None
        self.AddNode(RootNode)
        self.ArbolList = []

    def AddTree(self,TreeB):
        TreeB.Root.Parent = self.Root
        self.Root.Children.append(TreeB.Root)
        
    def AddNode(self,newValue):
        newNode = self.Node(newValue)

        if self.Root is None:
            self.Root = newNode
            return
        
        self.Root.Children.append(newNode)
        newNode.Parent = self.Root
        self.Previus = newNode

    def InsertNode(self,newValue,index):
        newNode = self.Node(newValue)

        if self.Root is None:
            self.Root = newNode
            return
        
        index = len(self.Root.Children) + index if index < 0 else index
        self.Root.Children.insert(index,newNode)
        newNode.Parent = self.Root

    def saveTree(self,Node,prefix="",LastChild=True,LVL=0):
        connector = ("└─── " if LastChild else "├─── ") if LVL!=0 else ""
        LVL += 1 
        
        self.ArbolList.append(prefix+connector+str(Node.Token.Value))

        if Node.Children:
            newPrefix = prefix + (("     " if LastChild else "│    ") if LVL!=1 else "")
            for i,child in enumerate(Node.Children):
                LastChild = i == len(Node.Children)-1
                self.saveTree(child,newPrefix,LastChild,LVL)