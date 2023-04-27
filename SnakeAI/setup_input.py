from os import stat_result
import numpy as np
from itertools import groupby
from dot_dict import Dotdict

class SetupInput(object):
    def __init__(self):
        super().__init__()
        self.eigth_marker: np.ndarray = None
        self.pos_to_edge_val: np.ndarray = None
        self.BoxtoLine:list[list] = []
        self.foodOutlines:list = []
        self.AI_input:list = []
    
    def calc_dist(self,p1,p2):
        dist = np.sqrt(np.sum(np.abs(p2-p1)**2))
        return abs(dist)
    
    def check_back_head(self):
        if self.direction == "L":
            return 1                  
        elif self.direction == "R":
            return 3
        elif self.direction == "U":
            return 2
        elif self.direction == "D":
            return 0
    
    def lineIntersectionBody(self,p0,p1,p2,p3,head_idx): #p0,p1 is body outline p2,p3 is the vision line of snake
        if self.check_back_head() != head_idx:
            p0 = Dotdict(
                x = p0[0],
                y = p0[1]
            )
            p1 = Dotdict(
                x = p1[0],
                y = p1[1]
            )
            p2 = Dotdict(
                x = p2[0],
                y = p2[1]
            )
            p3 = Dotdict(
                x = p3[0],
                y = p3[1]
            )
            vxmin,vxmax = ( min(p2.x,p3.x),max(p2.x,p3.x) )
            vymin,vymax = ( min(p2.y,p3.y),max(p2.y,p3.y) )
            A1 = p1.y - p0.y
            B1 = p0.x - p1.x
            C1 = ( A1 * p0.x ) + ( B1 * p0.y )
            A2 = p3.y - p2.y
            B2 = p2.x - p3.x
            C2 = ( A2 * p2.x ) + ( B2 * p2.y )
            denominator = (A1 * B2) - (A2 * B1)
            if denominator != 0:
                intersect_x = (( B2 * C1 ) - ( B1 * C2 )) / denominator
                intersect_y = (( A1* C2 ) - ( A2 * C1 )) / denominator
                if p0.x == p1.x:
                    if p0.y <= intersect_y <= p1.y and vxmin <= intersect_x <= vxmax:
                        return self.calc_dist(
                            np.array([p2.x,p2.y]),
                            np.array([intersect_x,intersect_y])
                        )
                elif p0.y == p1.y:
                    if p0.x <= intersect_x <= p1.x and vymin <= intersect_y <= vymax:
                        return self.calc_dist(
                            np.array([p2.x,p2.y]),
                            np.array([intersect_x,intersect_y])
                        )
                        
    def lineIntersectionFood(self,p0,p1,p2,p3,v_idx):
        p0 = Dotdict(
            x = p0[0],
            y = p0[1]
        )
        p1 = Dotdict(
            x = p1[0],
            y = p1[1]
        )
        p2 = Dotdict(
            x = p2[0],
            y = p2[1]
        )
        p3 = Dotdict(
            x = p3[0],
            y = p3[1]
        )
        vxmin,vxmax = ( min(p2.x,p3.x),max(p2.x,p3.x) )
        vymin,vymax = ( min(p2.y,p3.y),max(p2.y,p3.y) )
        A1 = p1.y - p0.y
        B1 = p0.x - p1.x
        C1 = ( A1 * p0.x ) + ( B1 * p0.y )
        A2 = p3.y - p2.y
        B2 = p2.x - p3.x
        C2 = ( A2 * p2.x ) + ( B2 * p2.y )
        denominator = (A1 * B2) - (A2 * B1)
        if denominator != 0:
            intersect_x = (( B2 * C1 ) - ( B1 * C2 )) / denominator
            intersect_y = (( A1* C2 ) - ( A2 * C1 )) / denominator
            if v_idx < 4:
                if p0.x == p1.x:
                    if p0.y <= intersect_y <= p1.y and vxmin <= intersect_x <= vxmax:
                        return self.calc_dist(
                            np.array([p2.x,p2.y]),
                            np.array([intersect_x,intersect_y])
                        )
                elif p0.y == p1.y:
                    if p0.x <= intersect_x <= p1.x and vymin <= intersect_y <= vymax:
                        return self.calc_dist(
                            np.array([p2.x,p2.y]),
                            np.array([intersect_x,intersect_y])
                        )
            else:
                if p0.x == p1.x:
                    if p0.y < intersect_y < p1.y and vxmin < intersect_x < vxmax:
                        return self.calc_dist(
                            np.array([p2.x,p2.y]),
                            np.array([intersect_x,intersect_y])
                        )
                elif p0.y == p1.y:
                    if p0.x < intersect_x < p1.x and vymin < intersect_y < vymax:
                        return self.calc_dist(
                            np.array([p2.x,p2.y]),
                            np.array([intersect_x,intersect_y])
                        )
       
    def groupBoxtoLine(self):
        self.BoxtoLine.clear()
        self.AI_input.clear()
        #Group with tag in list of dict of self.SnakeBody
        #Group them two times first group by tag and then group by same coordinate XY
        group_of_box = []
        key_ = lambda x : x.tag
        for k1,bx1 in groupby(self.SnakeBody[2:],key_):
            _bx = [x.coordinate for x in list(bx1)]
            if k1 == 'X':
                second_group_idx = 0
            else:
                second_group_idx = 1
            second_key = lambda x : x[second_group_idx]
            for k2,bx2 in groupby(_bx,second_key):
                final_group = list(bx2)
                final_group.sort()
                final_group.insert(0,k1)
                group_of_box.append(final_group)
                
        def BoxtoLinefnc(box):
            for i in box:
                if i[0] == 'X':
                    i = i[1:]
                    line0 = [ [ i[0][0], i[0][1] ], [ i[0][0], i[-1][1] + self.GridSize ] ]
                    line1 = [ [ i[0][0] + self.GridSize, i[0][1] ], [ i[0][0] + self.GridSize, i[-1][1] + self.GridSize ] ]
                    line2 = [ [ i[0][0], i[0][1] ], [ i[0][0] + self.GridSize, i[0][1] ] ]
                    line3 = [ [ i[0][0], i[-1][1] + self.GridSize ], [ i[0][0] + self.GridSize, i[-1][1]  + self.GridSize ] ]
                else:
                    i = i[1:]
                    line0 = [ [ i[0][0], i[0][1] ], [ i[-1][0] + self.GridSize, i[0][1]] ]
                    line1 = [ [ i[0][0], i[0][1] + self.GridSize ], [ i[-1][0] + self.GridSize, i[0][1] + self.GridSize ] ]
                    line2 = [ [ i[0][0], i[0][1] ], [ i[0][0], i[0][1] + self.GridSize ] ]
                    line3 = [ [ i[-1][0] + self.GridSize, i[0][1] ], [ i[-1][0] + self.GridSize, i[0][1]  + self.GridSize ] ]
                self.BoxtoLine.extend([
                    line0,line1,line2,line3
                ])
        BoxtoLinefnc(group_of_box)
    
    def checkVisions(self):
        for p_head,p_screen in zip(self.eigth_marker,self.pos_to_edge_coor):
            p_all = [p_head[:2].tolist(),p_screen.tolist()]
            p_all.sort()
            isOntheEdge = self.calc_dist(np.array(p_all[0]),np.array(p_all[1]))
            isHitBody = 0
            isHitFood = 0
            
            for pb in self.BoxtoLine:
                intersect_body = self.lineIntersectionBody(pb[0],pb[1],p_all[0],p_all[1],p_head[-1])
                if intersect_body:
                    if intersect_body == 0:
                        isHitBody = 0
                        break
                    elif isHitBody == 0:
                        isHitBody = intersect_body
                    elif isHitBody > intersect_body:
                        isHitBody = intersect_body
                    
            for pf in self.foodOutlines:
                intersect_food = self.lineIntersectionFood(pf[0],pf[1],p_all[0],p_all[1],p_head[-1])
                if intersect_food:
                    if intersect_food == 0:
                        isHitFood = 0
                        break
                    elif isHitFood == 0:
                        isHitFood = intersect_food
                    elif isHitFood > intersect_food:
                        isHitFood = intersect_food
            self.AI_input.extend([isOntheEdge,isHitBody,isHitFood])
            
    def checkDirection(self):
        self.AI_input.extend(self.one_hot_encode(self.direction))
        self.AI_input.extend(self.check_obj_direction(self.SnakeBody[0].coordinate,self.SnakeBody[-1].coordinate))