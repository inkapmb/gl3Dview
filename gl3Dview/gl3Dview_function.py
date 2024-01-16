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
import pygame.locals as pgl

import OpenGL.GL as gl
import OpenGL.GLU as glu


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
    gl.glClearColor(*bc, 1.)
    gl.glShadeModel(gl.GL_SMOOTH)
    gl.glEnable(gl.GL_CULL_FACE)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_LIGHTING)
    lightZeroPosition = [10., 4., 10., 1.]
    lightZeroColor = [0.8, 1.0, 0.8, 1.0]
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, lightZeroPosition)
    gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, lightZeroColor)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.1)
    gl.glLightf(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
    gl.glEnable(gl.GL_LIGHT0)


#text funtion
def drawText( text, x, y, fontSize = 20):   
    font = pygame.font.SysFont('arial', fontSize)                                  
    textSurface = font.render(text, True, (255, 255, 66, 255), (0, 66, 0, 255))
    textData = pygame.image.tostring(textSurface, "RGBA", True)
    gl.glWindowPos2d(x, y)
    gl.glDrawPixels(textSurface.get_width(), textSurface.get_height(), gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textData)
    
    
def texON(qobj, tex):
    glu.gluQuadricTexture(qobj, gl.GL_TRUE)
    gl.glEnable  ( gl.GL_TEXTURE_GEN_R )
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex)
    

#particles funtion
def addParticule(qobj, p):
    gl.glTranslatef(*p.pos)
    gl.glRotatef(p.angle, *p.axis)
    glu.gluSphere(qobj, p.rad, 32, 16) #Draw sphere
    gl.glRotatef(-p.angle, *p.axis)
    gl.glTranslatef(*(-p.pos))
    
    
#Interactions function
def addNormalInteractions(qobj, i) :
    
    #normal force
    transVec = i.p1_pos
    angle = np.arccos(np.dot(i.iio, i.norm)) * 360 / (np.pi * 2)
    axis = np.cross(i.iio, i.norm)
        
    cylRad = i.nfDisplayNorm
    cylLen = i.p1_rad + i.p2_rad
    
    gl.glTranslatef(*transVec)
    gl.glRotatef(angle, *axis)
    
    glu.gluQuadricNormals(qobj, glu.GLU_SMOOTH)
    glu.gluQuadricTexture(qobj, gl.GL_TRUE)
    glu.gluCylinder(qobj,
                    cylRad,
                    cylRad,
                    cylLen,
                    10,10)
    
    gl.glRotatef(-angle, *axis)
    gl.glTranslatef(*(-transVec))
    
#tangential interaction force
def addTanInteractions(qobj, i) :
        
    cylRad = i.nfScaleOffset # i.nfDisplayNorm
    cylLen = i.sfDisplayNorm
    
    hTan = np.sqrt( i.nfDisplayNorm**2 - cylRad**2 )
    sIntrsNorm = i.sf/np.linalg.norm(i.sf)
    
    transVec2 = i.p1_pos + i.norm * i.p1_rad + sIntrsNorm * hTan
    axis2 = np.cross(i.iio, sIntrsNorm)
    angle2 = np.arccos(np.dot(i.iio, sIntrsNorm)) * 360 / (np.pi * 2)
    
    gl.glTranslatef(*(transVec2))
    gl.glRotatef(angle2, *axis2)
    
    glu.gluCylinder(qobj,
                cylRad,
                0,
                cylLen,
                10,10)
    
    gl.glRotatef(-angle2, *axis2)
    gl.glTranslatef(*(-transVec2))
        


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
         
         ### Display var ###
         
         nfSize = [0.05, 0.5],
         nfLogNorm = False,
         
         shearForceDisplay = False,
         sfLogNorm = False,
         sfSize = [0.1, 0.5],
         
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
         
         #interactions
         intrsKey = pygame.K_z
         ):
    
    #some var init
    char_width = 11
    
    xSize, ySize = winSize
    
    pygame.font.init()
    
    display = (xSize, ySize) #set window
    pygame.display.set_caption("3D view")
    pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
    
    gl.glEnable(gl.GL_DEPTH_TEST)
    
    #load texture
    drawbject = gl3Dc.draw()
    drawbject.loadTexture(pdata.state_types)
    
    #create objects
    newGluQ = glu.gluNewQuadric()
    
    gl.glMatrixMode(gl.GL_PROJECTION)
    glu.gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    
    gl.glMatrixMode(gl.GL_MODELVIEW)
    viewMatrix = gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)
    gl.glLoadIdentity()
    
    #light
    light()
    
    
    ############################### init Var ##################################
    
    #data class
    pdata.init(initIntrsOri = np.array([0, 0, 1]),
               
               #normal intrs
               nfLogNorm = nfLogNorm,
               nf_minSize = nfSize[0],
               nf_maxSize = nfSize[1],
               
               #tan intrs
               shearForce = shearForceDisplay,
               sfLogNorm = sfLogNorm,
               sf_minSize = sfSize[0],
               sf_maxSize = sfSize[1],
               )
    
    #cam class
    cam = gl3Dc.camera(eye=glm.vec3(cam_target) + glm.vec3(0, 0, 10),
                       target=glm.vec3(cam_target),
                       up=glm.vec3(1, 0, 0),
                       )
    
    #control class
    ctrl = gl3Dc.control(posTK = posTimeKey, 
                                negTK = negTimeKey,
                                resTK = restartTimeKey,
                                intrsK = intrsKey,
                                )
    
    
    ############################## Main Loop ##################################
    
    while ctrl.run :
        
        # init the view matrix
        gl.glPushMatrix()
        gl.glLoadIdentity()
        
        #get control
        ctrl.getMouseControl()
        ctrl.getKeyControl()
        ctrl.timeIndex(pdata)
        
        #mouse control
        if ctrl.mp2_init :
            
            mpDiff = ctrl.mPos2 - ctrl.mPos1
            
            #drag
            if ctrl.buttonState[dragButton] :
                cd = mpDiff * transFactor
                cam.drag(cd)
            
            #rotate
            elif ctrl.buttonState[rotButton] and not np.all(mpDiff == 0) :
                cam.rotate_around_target_view(glm.vec3(0), glm.vec2(*(mpDiff * rotFactor)))
        
        #zoom
        if ctrl.mWheel:
            ctrl.mWheel = False
            cz = ctrl.zoomValue * zoomFactor
            cam.zoom(cz)
            

        #update data_class time index
        pdata.time(ctrl.time_index)

        #update cam pos/ori   
        cam.update(ySize / xSize)
        viewMatrix = gl.glGetFloatv(gl.GL_MODELVIEW_MATRIX)
    
        # apply view matrix
        gl.glPopMatrix()
        gl.glMultMatrixf(viewMatrix)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT|gl.GL_DEPTH_BUFFER_BIT) #Clear the screen    
        gl.glPushMatrix()
        
        e = cam.eye
        t = cam.target
        u = cam.up
        
        #update POV 
        glu.gluLookAt(e.x, e.y, e.z, t.x, t.y, t.z, u.x, u.y, u.z)
        
        #get 3D mouse pointer position
        ctrl.get3DmPos()
        
        #draw particles
        pointedParticles = pdata.drawObj(newGluQ, drawbject, ctrl)
        
        #print info on screen +++++++++++++++++++++++++++++++++++++++++++++++++
        
        #pointer
        xdisp = len(str(pointedParticles)) * char_width
        text = 'Pointer on : ' + str(pointedParticles) + ' [index]'
        drawText(text, xSize - xdisp - 200 , 20)
        
        #time
        text = str(pdata.t)
        rText = pText(text)
        drawText('Time : ' + rText + ' [s] (' + str(ctrl.time_index + 1) + '/' + str(pdata.step_nb) + ')', 20, 20)
        
        gl.glPopMatrix()
        pygame.display.flip() #Update the screen
        pygame.time.wait(10)
    
    pygame.quit()
    sys.exit()







