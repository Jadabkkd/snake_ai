import pygame as pg
import numpy as np

class DrawNeural(object):
    def __init__(self):
        super().__init__()
        self.color_status:list = [(212, 212, 212),(201, 40, 83),(18, 126, 188),(43, 189, 145)] #white red blue green
        self.node_coordinate: list = []
        self.grid_boxn = None

    def pepare_node_xy(self,size = 1):
        box_size = int(int(self.fullWinsize[1]/max(self.NetworkLayers)))
        self.grid_boxn = box_size * size
        spacing = box_size - self.grid_boxn
        row_width = int((self.fullWinsize[0] - self.SnakeWinsize[0]) / 4)
        row_spacing = self.SnakeWinsize[0] + int(row_width / 2)
        for nd in self.NetworkLayers:
            start = int((self.fullWinsize[1] - (box_size * nd))/2)
            box_xy_lis = []
            for i in range(nd):
                box_xy = [row_spacing, int(start + (self.grid_boxn/2) + (spacing)/2)]
                box_xy_lis.append(box_xy)
                start += box_size
            self.node_coordinate.append(np.array(box_xy_lis))
            row_spacing += row_width
        
        for n,_cls in zip(self.node_coordinate[-1],self.classification):
            _setter = self.font.render(_cls,True,(255,255,255))
            _y = (self.grid_boxn - self.font_size)
            self.surface.blit(_setter,np.array(n) + [self.grid_boxn*1.5,_y])
    
    def draw_node(self):
        for iwi,wi in enumerate(self.node_list):
            for iwj,wj in enumerate(wi):
                if wj <= 0.2:
                    color_stat = self.color_status[0]
                else:
                    color_stat = self.color_status[2]
                pg.draw.circle(
                    self.surface,
                    color_stat,
                    self.node_coordinate[iwi][iwj],
                    int(self.grid_boxn / 2)
                )
    
    def draw_node_line(self):
        for inn,nn in enumerate(self.SnakeBrain[self.PopulationNR-1].Brain):
            for ivy,vy in enumerate(nn):
                for ivx,vx in enumerate(vy):
                    if vx < 0.0:
                        cl_idx = 1
                    else:
                        cl_idx = 3
                    pg.draw.line(self.surface,self.color_status[cl_idx],
                        self.node_coordinate[inn][ivy] + [int(self.grid_boxn/2),0],
                        self.node_coordinate[inn+1][ivx] - [int(self.grid_boxn/2),0]
                    )