import pygame as pg
import numpy as np

class DrawStat(object):
    def __init__(self):
        super().__init__()
        self.stat_coor = None

    def init_stat(self):
        mxf = self.font.render('Best fitness: {}'.format(str(self.HighFitness)),True,(255,255,255))
        mxsc = self.font.render('High Score: {}'.format(str(self.HighScore)),True,(255,255,255))
        gen_nr = self.font.render('Generation: {}'.format(str(self.GenerationNR)),True,(255,255,255))
        snk_nr = self.font.render('Snake Number: {}'.format(str(self.PopulationNR)),True,(255,255,255))
        current_fit = self.font.render('Prev Fitness: {}'.format(str(self.lastest_fit)),True,(255,255,255))
        prev_score = self.font.render('Prev Score: {}'.format(str(self.RunningScore)),True,(255,255,255))
        self.surface.blit(mxf,self.stat_coor['max_fit'])
        self.surface.blit(mxsc,self.stat_coor['max_score'])
        self.surface.blit(gen_nr,self.stat_coor['gen_nr'])
        self.surface.blit(snk_nr,self.stat_coor['snk_nr'])
        self.surface.blit(current_fit,self.stat_coor['cur_fit'])
        self.surface.blit(prev_score,self.stat_coor['prev_score'])
        
    def update_stat(self,header,update_val,coor_key):
        pg.draw.rect(self.surface,self.BackgroundColor,(self.stat_coor[coor_key],[self.SnakeWinsize[0],self.font_size]))
        _setter = self.font.render(''.join([header,str(update_val)]),True,(255,255,255))
        self.surface.blit(_setter,self.stat_coor[coor_key])
        