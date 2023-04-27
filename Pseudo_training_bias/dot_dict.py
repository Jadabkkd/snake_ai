class Dotdict(dict):
    def __init__(self,**kwargs) -> None:
        super(Dotdict,self).__init__(**kwargs)

    def __getattr__(self,attr) -> dict:
        return self.get(attr)

    def __setattr__(self,k,v) -> None:
        self.__setitem__(k,v)

    def __setitem__(self,k,v) -> None:
        super(Dotdict,self).__setitem__(k,v)