class Dotdict(dict):
    def __init__(self,**kwargs):
        super(Dotdict,self).__init__(**kwargs)

    def __getattr__(self,attr):
        return self.get(attr)

    def __setattr__(self,k,v):
        self.__setitem__(k,v)

    def __setitem__(self,k,v):
        super(Dotdict,self).__setitem__(k,v)