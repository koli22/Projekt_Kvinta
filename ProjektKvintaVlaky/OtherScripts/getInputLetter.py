import pygame
from pygame import *

class getLetter:
    def gL(self,keys):
        letters = []
        
        for event in keys:
            if event.type == KEYDOWN:
                if event.key == K_a:
                    letters.append("a") 
                elif event.key == K_b:
                    letters.append("b")            
                elif event.key == K_c:
                    letters.append("c")
                elif event.key == K_d:
                    letters.append("d")
                elif event.key == K_e:
                    letters.append("e")
                elif event.key == K_f:
                    letters.append("f")
                elif event.key == K_g:
                    letters.append("g")
                elif event.key == K_h:
                    letters.append("h")
                elif event.key == K_i:
                    letters.append("i")
                elif event.key == K_j:
                    letters.append("j")
                elif event.key == K_k:
                    letters.append("k")
                elif event.key == K_l:
                    letters.append("l")
                elif event.key == K_m:
                    letters.append("m")
                elif event.key == K_n:
                    letters.append("n")
                elif event.key == K_o:
                    letters.append("o")
                elif event.key == K_p:
                    letters.append("p")
                elif event.key == K_q:
                    letters.append("q")
                elif event.key == K_r:
                    letters.append("r")
                elif event.key == K_s:
                    letters.append("s")
                elif event.key == K_t:
                    letters.append("t")
                elif event.key == K_u:
                    letters.append("u")
                elif event.key == K_v:
                    letters.append("v")
                elif event.key == K_w:
                    letters.append("w")
                elif event.key == K_x:
                    letters.append("x")
                elif event.key == K_y:
                    letters.append("y")
                elif event.key == K_z:
                    letters.append("z")
                
                elif event.key == K_RETURN:
                    letters.append(-1)
                elif event.key == K_ESCAPE:
                    letters.append(-2)
                elif event.key == K_BACKSPACE:
                    letters.append(-3)
                
        return letters
            
