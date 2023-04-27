import numpy as np

class SnakeRadar(object):
    def __init__(self):
        super().__init__()
        
    def cal_new_xy(self,pos,nr):
        new_xy = []
        if nr == 0:
            on_cal_vec = pos[0]
            new_xy = np.array([0,pos[1] - pos[0]])
            if (new_xy < [0,0]).any():
                new_xy = np.array([ abs(new_xy[1]), 0 ])       
        
        elif nr == 1:
            on_cal_vec = (self.SnakeWinsize[0] - pos[0])
            new_xy = np.array([self.SnakeWinsize[0],pos[1] - on_cal_vec])
            if (new_xy < [0,0]).any():
                new_xy = np.array([self.SnakeWinsize[0] - abs(new_xy[1]),0])   

        elif nr == 2:
            on_cal_vec = (self.SnakeWinsize[1] - pos[1])
            new_xy = np.array([pos[0] + on_cal_vec,self.SnakeWinsize[1]])
            if (new_xy > [self.SnakeWinsize[0],self.SnakeWinsize[0]]).any():
                new_xy = np.array([self.SnakeWinsize[0], self.SnakeWinsize[1] - int((new_xy[0] - self.SnakeWinsize[0]))])

        elif nr == 3:
            on_cal_vec = (self.SnakeWinsize[1] - pos[1])
            new_xy = np.array([pos[0] - on_cal_vec,self.SnakeWinsize[1]])
            if (new_xy < [0,0]).any():
                new_xy = np.array([0, self.SnakeWinsize[1] - abs(new_xy[0])])
            
        return new_xy

    def pos_to_edge(self):
        #for straight line
        for i,pos in enumerate(self.eigth_marker[:4,:2]):
            if i == 0:
                end_pos = pos * [1,0]
                yield end_pos
            elif i == 1:
                end_pos = np.array([self.SnakeWinsize[0],pos[1]])
                yield end_pos
            elif i == 2:
                end_pos = np.array([pos[0],self.SnakeWinsize[1]])
                yield end_pos
            elif i == 3:
                end_pos = pos * [0,1]
                yield end_pos
        
        #for 45* line
        for i,pos in enumerate(self.eigth_marker[4:,:2]):
                new_ang_pos = self.cal_new_xy(pos,i)
                yield new_ang_pos

    def init_visions(self,pos):
        eigth_mark = np.array([
            pos + [int(self.GridSize/2),0],
            pos + [ int(self.GridSize),int(self.GridSize/2) ],
            pos + [ int(self.GridSize/2),int(self.GridSize) ],
            pos + [ 0,int(self.GridSize/2) ],
            pos,
            pos + [int(self.GridSize),0],
            pos + [ int(self.GridSize),int(self.GridSize) ],
            pos + [ 0,int(self.GridSize) ],
        ])
        _8mlis = []
        for i,_it in enumerate(eigth_mark):
            t = _it.tolist()
            t.append(i)
            _8mlis.append(t)
        self.eigth_marker = np.array(_8mlis)
        self.pos_to_edge_val = np.array(list(self.pos_to_edge()))
            
    def modify_visions(self):
        self.eigth_marker[:,:2] += (self.movement)
        self.pos_to_edge_val = np.array(list(self.pos_to_edge()))