#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Function 
"""

########### import ###########

# --- FUNCTION

#general
import sys
import numpy as np
import glm

#graphic 
import pygame
from pygame.locals import*
from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import *

# --- CLASS

#special class
import gl3Dview_class as gl3Dc

### FUNCTION

def getPath() :
    for path in  sys.path :
        if path.find('gl3Dview') != -1 :
             return path


#light definition            
def light(bc=[0.2, 0.2, 0.2]) :                   
    glClearColor(*bc, 1.)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    lightZeroPosition = [10., 4., 10., 1.]
    lightZeroColor = [0.8, 1.0, 0.8, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glEnable(GL_LIGHT0)


#text funtion
def drawText( text, x, y):   
    font = pygame.font.SysFont('arial', 20)                                  
    textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    glWindowPos2d(x, y)
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
    
    
def texON(qobj, tex):
    gluQuadricTexture(qobj, GL_TRUE)
    glEnable  ( GL_TEXTURE_GEN_R )
    glBindTexture(GL_TEXTURE_2D, tex)
    

#particles funtion
def addParticule(obj, p):

    glTranslatef(*p.pos)
    glRotatef(p.angle, *p.axis)
    
    gluSphere(obj, p.rad, 32, 16) #Draw sphere
    
    glRotatef(-p.angle, *p.axis)
    glTranslatef(*(-p.pos))
    
    
def addInteractions() :
    gluCylinder()


def drawObj(obj, tex, pdata, time_index):
    
    glEnable(GL_TEXTURE_2D)
    
    #add all particles    
    for i in range(pdata.particle_number) :
        
        p = gl3Dc.particles(pdata, i,time_index)
        
        #get right texture
        for texIdx, pstate in enumerate(p.state) :
            if pstate :
                ptex = tex.id[texIdx+1]
                break
        
        #or default texture
            else :
                ptex = tex.id[0]
        
        texON(obj, ptex)
        addParticule(obj, p)
    
    glDisable(GL_TEXTURE_2D)
    


#printable text
def pText(og_text, digit_length = 7) :
    
    ePos = og_text.find('e')
    
    if ePos != -1 :
        if digit_length - ePos <= 0 :
            return og_text[:digit_length] + og_text[ePos:]
        
        elif digit_length - ePos >= 0 :
            return og_text
        
    else :
        if len(og_text) > digit_length :
            return og_text[:digit_length]
        
        else :
            return og_text
    


#main fucntion

def main(pdata, 
         winSize=[1000, 1000], 
         cam_target=[0,0,0],
         
         ### control var ###
         
         #view
         rotButton = 0,
         dragButton = 2,
         
         transFactor = 0.01,
         zoomFactor = 2,
         rotFactor = 0.005,
         
         #time
         posTimeKey = pygame.K_d, #100
         negTimeKey = pygame.K_q, #113
         restartTimeKey = pygame.K_s, #115
         ):
    
    xSize, ySize = winSize
    
    pygame.font.init()
    
    display = (xSize, ySize) #set window
    pygame.display.set_caption("3D view")
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    
    glEnable(GL_DEPTH_TEST)
    
    #load texture
    tex = gl3Dc.texture()
    
    #create objects
    sphere = gluNewQuadric()
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    glMatrixMode(GL_MODELVIEW)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    glLoadIdentity()
    
    #light
    light()
    
    
    ############################### init Var ##################################
    
    #time index
    time_index = 0
    
    #cam class
    cam = gl3Dc.camera(
            eye=glm.vec3(cam_target) + glm.vec3(0, 0, 10),
            target=glm.vec3(cam_target),
            up=glm.vec3(1, 0, 0)
        )
    
    #control Var
    mWheel = False
    buttonState = np.array([False, False, False])
    
    mPos1 = np.full([2], 0)
    mPos2 = np.full([2], 0)
    
    mp1_init = False
    mp2_init = False
    
    ############################## Main Loop ##################################
    
    run = True
    
    while run :
        
        if not mp1_init :
            mPos1[0], mPos1[1] = mPos2[0], mPos2[1]
        
        # init model view matrix
        # glLoadIdentity()
    
        # init the view matrix
        glPushMatrix()
        glLoadIdentity()
        
        #### get control ####
        for event in pygame.event.get():
            
            #quit
            if event.type == pygame.QUIT:
                run = False
            
            #Zoom
            if event.type == MOUSEWHEEL :
                mWheel = True
                zoomValue = event.y
            
            #get init mouse pos
            if event.type == MOUSEBUTTONDOWN :
                mp1_init = True
                mPos1[0], mPos1[1] = pygame.mouse.get_pos() #.get_pos()
                buttonState[:] = pygame.mouse.get_pressed()[:]
                
            #get mouse pos while button is on
            if np.any(buttonState) :
                if event.type == MOUSEMOTION :
                    mp1_init = False
                    mp2_init = True
                    mPos2[0], mPos2[1] = pygame.mouse.get_pos()
                    buttonState[:] = pygame.mouse.get_pressed()[:]
            
            #get last mouse pos
            if event.type == MOUSEBUTTONUP :
                mp2_init = False
                buttonState[:] = pygame.mouse.get_pressed()[:]
            
            #quit
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    
                #change time idx
                if event.key == K_q:
                    Left = True
                if event.key == K_d:
                    Right = True


        #Manage time 
        keypress = pygame.key.get_pressed()
        
        #forward
        if keypress[posTimeKey]:
            time_index +=1
        #backward
        if keypress[negTimeKey]:
            time_index -=1
        #restart
        if keypress[restartTimeKey] :
            time_index = 0
            
        if time_index < 0 :
            time_index = pdata.step_nb - 1
        if time_index > pdata.step_nb - 1 :
            time_index = 0
        
        #mouse control
        if mp2_init :
            
            mpDiff = mPos2 - mPos1
            
            #drag
            if buttonState[dragButton] :
                cd = mpDiff * transFactor
                cam.drag(cd)
            
            #rotate
            elif buttonState[rotButton] and not np.all(mpDiff == 0) :
                cam.rotate_around_target_view(glm.vec3(0), glm.vec2(*(mpDiff * rotFactor)))
        
        #zoom
        if mWheel:
            mWheel = False
            cz = zoomValue * zoomFactor
            cam.zoom(cz)

            
        cam.update(ySize / xSize)
        
        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)
    
        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clear the screen    
        glPushMatrix()
        
        e = cam.eye
        t = cam.target
        u = cam.up
        
        gluLookAt(e.x, e.y, e.z, t.x, t.y, t.z, u.x, u.y, u.z)
        
        # print(e.x, e.y, e.z, t.x, t.y, t.z, u.x, u.y, u.z)
        
        #draw particles
        drawObj(sphere, tex, pdata, time_index)
        
        #print info on screen
        text = str(gl3Dc.time(pdata, time_index).time)
        
        rText = pText(text)
        
        drawText('Time : ' + rText + ' [s] (' + str(time_index + 1) + '/' + str(pdata.step_nb) + ')', 20, 20)
        
        glPopMatrix()
        pygame.display.flip() #Update the screen
        pygame.time.wait(10)
    
    pygame.quit()
    sys.exit()







