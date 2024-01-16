#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
By MAHJOUB-BONNAIRE Provence, INRAE

gl3Dview classes

"""


# +++++++++++++++++++++++++++++++ import ++++++++++++++++++++++++++++++++++++

#classic
import os
import glm
import numpy as np

import pygame as pg
import pygame.locals as pgl

import OpenGL.GL as gl
import OpenGL.raw as raw
# import OpenGL.GLU as glu

#import own function
import gl3Dview_function as gl3Df

# ++++++++++++++++++++++++++++++ USE ++++++++++++++++++++++++++++++++++++++

#patern to import data
#Data[time, particle, other]

# +++++++++++++++++++++++++++++++ main ++++++++++++++++++++++++++++++++++++


class data_class :
    
    ### Import data ###
    def get_time(self, 
                 dt=None, 
                 dt_index=None):
        
        self.time_step = dt
        self.step_nb = len(dt_index)
        self.time_array = dt_index * dt
    
    def get_particles(self, 
                      state_types=None, 
                      states=None, 
                      radius=None, 
                      positions=None, 
                      orientations=None, 
                      # velocities=None, 
                      # rotation_velocities=None, 
                      # forces=None, 
                      # torques=None,
                      ):
        
        self.state_types = state_types
        self.all_state = states
        self.particle_number = len(radius)
        self.all_rad = radius       
        self.all_pos = positions
        self.all_ori = orientations
        # self.all_vel = velocities
        # self.all_avel = rotation_velocities
        # self.all_f = forces
        # self.all_t = torques
    
    def get_interactions(self, 
                         intrsPid=None,
                         intrsNorm=None, 
                         intrsNF=None, 
                         intrsSF=None
                         ) :
        
        self.intrs_pid = intrsPid
        self.intrs_norm = intrsNorm
        self.intrs_nf = intrsNF
        self.intrs_sf = intrsSF

    
    ### Use Class ### ---------------------------------------------------
    
    #init fucntion
    def init(self, 
             initIntrsOri = np.array([0, 0, 1]),
             
             nf_minSize = 0.05,
             nf_maxSize = 0.5,
             nfLogNorm = False,
             
             shearForce = False,
             sf_minSize = 0.05,
             sf_maxSize = 0.5,
             sfLogNorm = False,
             ):
        
        self.iio = initIntrsOri
        self.nfLogNorm = nfLogNorm
        self.sfRpz = shearForce
        self.sfLogNorm = sfLogNorm
        
        #find max interacion force
        max_nf = 0
        max_sf = 0
        min_nf = None
        min_sf = None
        
        for tidx in range(self.step_nb) :
            for pidx in range(len(self.intrs_pid[tidx])) :
                for iidx in range(len(self.intrs_pid[tidx][pidx])) :
                    
                    #max
                    if np.linalg.norm(self.intrs_nf[tidx][pidx][iidx]) > max_nf :
                        max_nf = np.linalg.norm(self.intrs_nf[tidx][pidx][iidx])
                    if np.linalg.norm(self.intrs_sf[tidx][pidx][iidx]) > max_sf :
                        max_sf = np.linalg.norm(self.intrs_sf[tidx][pidx][iidx])
                        
                    #min
                    if min_nf == None :
                        min_nf = np.linalg.norm(self.intrs_nf[tidx][pidx][iidx])
                    elif np.linalg.norm(self.intrs_nf[tidx][pidx][iidx]) < min_nf :
                        min_nf = np.linalg.norm(self.intrs_nf[tidx][pidx][iidx])
                        
                    if min_sf == None :
                        min_sf = np.linalg.norm(self.intrs_sf[tidx][pidx][iidx])
                    if np.linalg.norm(self.intrs_sf[tidx][pidx][iidx]) < min_sf :
                        min_sf = np.linalg.norm(self.intrs_sf[tidx][pidx][iidx])
                        
        self.maxNF = max_nf
        self.minNF = min_nf
        self.maxSF = max_sf
        self.minSF = min_sf
        
        #nf scale
        if self.nfLogNorm :
            self.nfScale = (nf_maxSize - nf_minSize) / np.log(1 + max_nf)
            self.nfScaleOffset = nf_minSize - np.log(1 + min_nf)

        else :
            self.nfScale = (nf_maxSize - nf_minSize)/(max_nf - min_nf)
            self.nfScaleOffset = nf_minSize - min_nf * (nf_maxSize - nf_minSize) / (max_nf - min_nf)
        
        #sf scale
        if self.sfRpz :
            if self.sfLogNorm :
                self.sfScale = (sf_maxSize - sf_minSize) / np.log(1 + max_sf)
                self.sfScaleOffset = sf_minSize - np.log(1 + min_sf)
                
            else :
                self.sfScale = (sf_maxSize - sf_minSize)/(max_sf - min_sf)
                self.sfScaleOffset = sf_minSize - min_nf * (sf_maxSize - sf_minSize) / (max_nf - min_nf)
    
    #GET INFO
    
    #get time info
    def time(self, t_index):
        self.t_index = t_index
        self.t = self.time_array[t_index]
        self.intrsNb = len(self.intrs_pid[self.t_index])
    
    #get particles infos
    def particles(self, p_index):
        self.p_index = p_index
        self.state = self.all_state[self.t_index][p_index]
        self.rad = self.all_rad[p_index]
        self.pos = self.all_pos[self.t_index][p_index]
        self.raw_ori = self.all_ori[self.t_index][p_index]
        self.angle = self.raw_ori[0]
        self.axis = self.raw_ori[1:]
        
    #get interaction infos
    def interactions(self, i_index) :
        self.pid = self.intrs_pid[self.t_index][i_index]
        self.p1_pos = self.all_pos[self.t_index, self.pid[0]]
        self.p2_pos = self.all_pos[self.t_index, self.pid[1]]
        self.p1_rad = self.all_rad[self.pid[0]]
        self.p2_rad = self.all_rad[self.pid[1]]
        self.norm = self.intrs_norm[self.t_index][i_index]
        self.nf = self.intrs_nf[self.t_index][i_index]
        self.sf = self.intrs_sf[self.t_index][i_index]
        
        if self.nfLogNorm :
            nfNorm = np.log(np.linalg.norm(self.nf) + 1)
            self.nfDisplayNorm = nfNorm * self.nfScale + self.nfScaleOffset
        else :
            nfNorm = np.linalg.norm(self.nf)
            self.nfDisplayNorm = nfNorm * self.nfScale + self.nfScaleOffset
        
        if self.sfRpz : 
            if self.sfLogNorm :
                sfNorm = np.log(np.linalg.norm(self.sf) + 1)
                self.sfDisplayNorm = sfNorm * self.sfScale + self.sfScaleOffset
            else :
                sfNorm = np.linalg.norm(self.sf)
                self.sfDisplayNorm = sfNorm * self.sfScale + self.sfScaleOffset
        
        self.inIntrs = True
        
        
    def getDistanceToParticle(self, ctrl) :
        self.dFromP = np.linalg.norm(np.cross(ctrl.far - ctrl.near, ctrl.far - self.pos))/np.linalg.norm(ctrl.far - ctrl.near)
        
    def getDistanceToInteraction(self, ctrl):
        A = self.p2_pos - self.p1_pos
        B = ctrl.far - ctrl.near
        
        lenIntrs = np.linalg.norm(A)
        unitIntrs = A / lenIntrs
        
        unitPointerVec = B / np.linalg.norm(B)
        
        cross = np.cross(unitIntrs, unitPointerVec);
        denom = np.linalg.norm(cross)**2
        
        #view vec and intrsVec are parallel
        if denom == 0 :
            d0 = np.dot(unitIntrs,(ctrl.near-self.p1_pos))
            d1 = np.dot(unitIntrs,(ctrl.far-self.p1_pos))
                                    
            if d0 >= lenIntrs <= d1:
                if np.absolute(d0) < np.absolute(d1):
                    self.dFromI = np.linalg.norm(self.p2_pos-ctrl.near)
                self.dFromI = np.linalg.norm(self.p2_pos-ctrl.far)
        
        else :
            t = (ctrl.near - self.p1_pos);
            
            detA = np.linalg.det([t, unitPointerVec, cross])
            detB = np.linalg.det([t, unitIntrs, cross])
            
            t0 = detA/denom;
            t1 = detB/denom;
            
            pA = self.p1_pos + (unitIntrs * t0)
            pB = ctrl.near + (unitPointerVec * t1)            
                
            # Clamp projection intrs
            if t0 < 0 or t0 > lenIntrs:
                if t0 < 0:
                    pA = self.p1_pos
                    self.inIntrs = False
                elif t0 > lenIntrs:
                    pA = self.p2_pos
                    self.inIntrs = False
                
                dot = np.dot(unitPointerVec,(pA-ctrl.near))
                if dot < 0:
                    dot = 0
                pB = ctrl.near + (unitPointerVec * dot)
            
            #clamp eye point
            if t1 < 0 :
                pB = ctrl.near
                self.inIntrs = False
                dot = np.dot(unitIntrs,(pB-self.p1_pos))
                
                if dot < 0:
                    dot = 0
                elif dot > lenIntrs:
                    dot = lenIntrs
                pA = self.p1_pos + (unitIntrs * dot)
    
            self.dFromI = np.linalg.norm(pA-pB)


    #Draw FUNCTION
    def drawObj(self, newGluQ, draw, ctrl):
        
        p_idx = None
        p_dist = np.linalg.norm(ctrl.far - ctrl.near)
        
        #add all particles 
        if ctrl.showParticles :
            
            gl.glEnable(gl.GL_TEXTURE_2D)
            
            for i in range(self.particle_number) :
            
                self.particles(i)
            
                #get right texture
                ptex = draw.tex[self.state]
                
                gl3Df.texON(newGluQ, ptex)
                gl3Df.addParticule(newGluQ, self)
                
                self.getDistanceToParticle(ctrl)
                
                if self.dFromP < self.rad :
                    if np.linalg.norm(self.pos - ctrl.near) < p_dist :
                        p_dist = np.linalg.norm(self.pos - ctrl.near)
                        p_idx = self.p_index
            
            gl.glDisable(gl.GL_TEXTURE_2D)
                
        elif ctrl.showIntrs :
            
            for idx in range(self.intrsNb) :
                
                self.interactions(idx)
                
                #normal
                gl3Df.addNormalInteractions(newGluQ, self)
                
                #tan
                if self.sfRpz :
                    gl3Df.addTanInteractions(newGluQ, self)
                
                self.getDistanceToInteraction(ctrl)
                
                if self.dFromI < self.nfDisplayNorm and self.inIntrs :
                    if np.linalg.norm((self.p1_pos + self.p2_pos)/2 - ctrl.near) < p_dist :
                        p_dist = np.linalg.norm((self.p1_pos + self.p2_pos)/2 - ctrl.near)
                        p_idx = self.pid
                
        return p_idx

        
        
# --------------------------- #### Texture #### ------------------------------#

class draw :
    # def __init__(self) :
    #     self.particles = True
    #     self.interaction = False
    #     self.tex = {}
        
    #texture load
    def loadTexture(self, state_types, fileNames = [], default_key = '') :
        
        path = gl3Df.getPath() + '/texture/'
        
        #get list of texture files
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and file[-4:] == '.png' :
                fileNames.append(file[:-4])
        
        fileNames.sort()
        
        #default set ?
        defSet = False
        texStateIdx = np.full([len(fileNames)], np.nan)
        
        if np.any(np.array(fileNames) == default_key) :
            defSet = True
            texStateIdx[0] = np.where(np.array(fileNames) == default_key)[0][0]
        
        #other state def ?
        for i, s in enumerate(state_types) :
            if np.any(np.array(fileNames) == s) :
                texStateIdx[i+1] = np.where(np.array(fileNames) == s)[0][0]
        
        #load each texture
        tex = {}
        
        for i, file in enumerate(fileNames) :
            
            textureSurface = pg.image.load(path + file + '.png')
            textureData = pg.image.tostring(textureSurface, "RGBA", 1)
            width = textureSurface.get_width()
            height = textureSurface.get_height()
    
            gl.glEnable(gl.GL_TEXTURE_2D)
            texid = gl.glGenTextures(1)
    
            gl.glBindTexture(gl.GL_TEXTURE_2D, texid)
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height,
                         0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textureData)
    
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST) #GL_NEAREST #GL_LINEAR
            gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST) #GL_NEAREST
            
            wasDef = False
            for s_idx in texStateIdx :
                if s_idx == i :
                    tex[file] = texid
                    wasDef = True
            
            if not wasDef :
                if not defSet :
                    tex[default_key] = texid
                    defSet = True
            
                else :
                    tex[state_types[i-1]] = texid
        
        self.tex = tex

### CONTROL CLASS

class control :
    def __init__(self,
                 posTK = None,
                 negTK = None,
                 resTK = None,
                 intrsK = None,
                 ) :
        
        #run var
        self.run = True
        
        #mouse control var
        self.mWheel = False
        self.buttonState = np.array([False, False, False])
        self.mPos1 = np.full([2], 0)
        self.mPos2 = np.full([2], 0)
        self.mp1_init = False
        self.mp2_init = False
        
        #key control var
        self.time_index = 0
        self.posTimeKey = posTK
        self.negTimeKey = negTK
        self.restartTimeKey = resTK
        self.intrsKey = intrsK
        
        #3D pointer var
        self.mv_mat = (gl.GLdouble * 16)()
        self.p_mat  = (gl.GLdouble * 16)()
        self.v_rect = (gl.GLint * 4)()
    
    ### MOUSE CONTROL ###
    def getMouseControl(self) :
        if not self.mp1_init :
            self.mPos1[0], self.mPos1[1] = self.mPos2[0], self.mPos2[1]

        #### get control ####
        for event in pg.event.get():
            
            #quit
            if event.type == pg.QUIT:
                self.run = False
            
            #Zoom
            if event.type == pgl.MOUSEWHEEL :
                self.mWheel = True
                self.zoomValue = event.y
            
            #get init mouse pos
            if event.type == pgl.MOUSEBUTTONDOWN :
                self.mp1_init = True
                self.mPos1[0], self.mPos1[1] = pg.mouse.get_pos()
                self.buttonState[:] = pg.mouse.get_pressed()[:]
                
            #get mouse pos while button is on
            if np.any(self.buttonState) :
                if event.type == pgl.MOUSEMOTION :
                    self.mp1_init = False
                    self.mp2_init = True
                    self.mPos2[0], self.mPos2[1] = pg.mouse.get_pos()
                    self.buttonState[:] = pg.mouse.get_pressed()[:]
            
            #get last mouse pos
            if event.type == pgl.MOUSEBUTTONUP :
                self.mp2_init = False
                self.buttonState[:] = pg.mouse.get_pressed()[:]
            
            #quit
            if event.type == pgl.KEYDOWN:
                if event.key == pgl.K_ESCAPE:
                    self.run = False
                    
    ### KEY CONTROL ###
    def getKeyControl(self):
        #Manage time 
        keypress = pg.key.get_pressed()
        
        #forward
        if keypress[self.posTimeKey]:
            self.time_index +=1
        #backward
        if keypress[self.negTimeKey]:
            self.time_index -=1
        #restart
        if keypress[self.restartTimeKey] :
            self.time_index = 0
        
        #show interaction
        self.showParticles = True
        self.showIntrs = False
        if keypress[self.intrsKey] :
            self.showParticles = False
            self.showIntrs = True
            
    #control and get time index
    def timeIndex(self, pdata) :
        if self.time_index < 0 :
            self.time_index = pdata.step_nb - 1
        if self.time_index > pdata.step_nb - 1 :
            self.time_index = 0
        return self.time_index
    
    #get position of pointer in 3D space
    def get3DmPos(self) :
        gl.glGetDoublev(gl.GL_MODELVIEW_MATRIX, self.mv_mat)
        gl.glGetDoublev(gl.GL_PROJECTION_MATRIX, self.p_mat)
        gl.glGetIntegerv(gl.GL_VIEWPORT, self.v_rect)
        mouse_pos = pg.mouse.get_pos()
        mouse_pos = mouse_pos[0], self.v_rect[3] - mouse_pos[1]
    
        temp_val = [gl.GLdouble() for _ in range(3)]
        raw.GLU.gluUnProject(*mouse_pos, 0, self.mv_mat, self.p_mat, self.v_rect, *temp_val)
        self.near = np.array([v.value for v in temp_val])  
        raw.GLU.gluUnProject(*mouse_pos, 1, self.mv_mat, self.p_mat, self.v_rect, *temp_val)
        self.far = np.array([v.value for v in temp_val])
        

# ---------------------------- #### Camera #### ------------------------------#
class camera ():
    
    def __init__(
        self,
        eye=None, target=None, up=None,
        fov=None, near=0.1, far=100000
    ):
        self.eye = eye or glm.vec3(0, 0, 1)
        self.target = target or glm.vec3(0, 0, 0)
        self.up = up or glm.vec3(0, 1, 0)
        self.original_up = glm.vec3(self.up)
        self.fov = fov or glm.radians(45)
        self.near = near
        self.far = far
        
    
    def update(self, aspect):
        
        self.view = glm.lookAt(
            self.eye, self.target, self.up
        )
        self.projection = glm.perspective(
            self.fov, aspect, self.near, self.far
        )
    
    
    def drag(self, dragVec) :
        
        sideVec = glm.normalize(glm.cross(self.eye - self.target, self.up))
        disp = glm.vec3(sideVec * dragVec[0] + self.up * dragVec[1])
        
        self.eye += disp
        self.target += disp
    
    
    def zoom(self, zoomValue) :
        self.eye += glm.vec3(glm.normalize(self.eye - self.target) * zoomValue)
    
    
    def rotate_target(self, delta):
        
        right = glm.normalize(glm.cross(self.target - self.eye, self.up))
        M = glm.mat4(1)
        M = glm.translate(M, self.eye)
        M = glm.rotate(M, delta.y, right)
        M = glm.rotate(M, delta.x, self.up)
        M = glm.translate(M, -self.eye)
        
        self.target = glm.vec3(M * glm.vec4(self.target, 1.0))
    
    
    def rotate_around_target_view(self, target, delta):
    
        V = glm.lookAt(self.eye, self.target, self.up)
    
        pivot = glm.vec3(V * glm.vec4(target.x, target.y, target.z, 1))
        axis  = glm.vec3(delta.y, delta.x, 0)
        angle = glm.length(delta)
    
        R  = glm.rotate( glm.mat4(1), angle, axis )
        RP = glm.translate(glm.mat4(1), pivot) * R * glm.translate(glm.mat4(1), -pivot)
        NV = RP * V
    
        C = glm.inverse(NV)
        targetDist  = glm.length(self.target - self.eye)
        self.eye    = glm.vec3(C[3])
        self.target = self.eye - glm.vec3(C[2]) * targetDist 
        self.up     = glm.vec3(C[1])

