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

import pygame
import OpenGL.GL as gl

#import own function
import gl3Dview_function as gl3Df

# ++++++++++++++++++++++++++++++ USE ++++++++++++++++++++++++++++++++++++++

#patern to import data
#Data[time, particle, other]

# +++++++++++++++++++++++++++++++ main ++++++++++++++++++++++++++++++++++++

### Import data class ###
class data_class :
    
    def get_time(self, 
                 time_step=None, 
                 time_index=None):
        
        self.time_step = time_step
        self.step_nb = len(time_index)
        self.time = time_index * time_step
    
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
        
        self.all_state_types = state_types
        self.all_state = states
        self.particle_number = len(radius)
        self.all_rad = radius       
        self.all_pos = positions
        self.all_ori = orientations
        # self.all_vel = velocities
        # self.all_avel = rotation_velocities
        # self.all_f = forces
        # self.all_t = torques
    
    def get_interactions(self, norm, nf, sf) :
        self.all_norm = norm
        self.all_nf = nf
        self.all_sf = sf


### Use class ###
class time :    
    def __init__(self, data, t_index):
        self.dt = data.time_step
        self.time = data.time[t_index]


class particles :
    def __init__(self, data, p_index, t_index):
        
        self.p_index = p_index
        self.t_index = t_index
        self.state = data.all_state[t_index, p_index]
        
        self.rad = data.all_rad[p_index]
        self.pos = data.all_pos[t_index, p_index]
        self.raw_ori = data.all_ori[t_index, p_index]
        self.angle = self.raw_ori[0]
        self.axis = self.raw_ori[1:]
        
        # self.vel = data.all_vel[t_index, p_index]
        # self.avel = data.all_avel[t_index, p_index]
        # self.f = data.all_f[t_index, p_index]
        # self.t = data.all_t[t_index, p_index]
        
        self.iNorm = data.all_norm[t_index][p_index]
        self.iNf = data.all_nf[t_index][p_index]
        self.iSf = data.all_sf[t_index][p_index]
        
        
# --------------------------- #### Texture #### ------------------------------#

class texture :
    def __init__(self, fileNames = []) :
        
        path = gl3Df.getPath() + '/texture/'
        
        #get list of texture files
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)) and file[-4:] == '.png' :
                fileNames.append(file)
        
        fileNames.sort()
        tex = []
        
        for file in fileNames :
            textureSurface = pygame.image.load(path + file)
            textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
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
            
            tex.append(texid)
            
        self.id = tex
            
    def read(filename):
        textureSurface = pygame.image.load(filename)
        textureData = pygame.image.tostring(textureSurface, "RGBA", 1)
        width = textureSurface.get_width()
        height = textureSurface.get_height()

        gl.glEnable(gl.GL_TEXTURE_2D)
        texid = gl.glGenTextures(1)

        gl.glBindTexture(gl.GL_TEXTURE_2D, texid)
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, width, height,
                     0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, textureData)

        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)

        return texid

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
        
        # print(self.eye, self.target, self.up)
        
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
        axis  = glm.vec3(-delta.y, -delta.x, 0)
        angle = glm.length(delta)
    
        R  = glm.rotate( glm.mat4(1), angle, axis )
        RP = glm.translate(glm.mat4(1), pivot) * R * glm.translate(glm.mat4(1), -pivot)
        NV = RP * V
    
        C = glm.inverse(NV)
        targetDist  = glm.length(self.target - self.eye)
        self.eye    = glm.vec3(C[3])
        self.target = self.eye - glm.vec3(C[2]) * targetDist 
        self.up     = glm.vec3(C[1])

