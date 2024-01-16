# gl3Dview
3D viewer for granular material

## Requirement

Use ```pip install name``` to install needed package

### Lib Name

General :

```
sys
numpy
PyGLM
```

Graphic :

```
pygame
pyOpenGL
```

## Use

### Data importation
You needed to import your data in the used classes, by following this schem. 

`[index_1][index_2][etc]` represent list.

`int[index_1, index_2, etc]` represent array with type and index in order.


1. Create data class :

  ```ruby
  data_class_name = gl3Dc.data_class()
  ```

2. Import time data :
  ```ruby
  data_class_name.get_time(dt =         float -> time_step,    
                           time_index = numpy.int[time_index])
  ```
   
3. Import **particles** data :

+ `states_type` is the list name of the differents state.
+ `states` is the differents state for each particles for each time step, default state is `''`.
+ `radius` is the particles radius for ech particles.
+ `positions` is the position of each particles for each time step.
+ `orientation` is the orientation each particles for each time step, it must be like `[angle, x, y, z]` where the `angle` is in degree and `x, y, z` represent the rotation axis.

Unsed for the moment :
  ▫️ `velocities` is the velocities of each particles at each time step.  <br />
  ▫️ `rotation_velocities` is the rotation velocities of each particles at each time step. <br />
  ▫️ `forces` is the forces of each particles at each time step. <br />
  ▫️ `torques` is the torques of each particles at each time step. <br />

  
&emsp; **It's better to adimentionalize particle size (radius) and position by the mean particle size.**
   
  ```ruby
  data_class_name.get_particles(states_type =          numpy.str[state_index],
                                states =               numpy.str[time_index, particle_index],
                                radius =               numpy.float[particle_index],
                                positions =            numpy.float[time_index, particle_index, coord_index],
                                orientations =         numpy.float[time_index, particle_index, angle:axis_coord_index],
                                #velocities =          numpy.float[time_index, particle_index, coord_index],
                                #rotation_velocities = numpy.float[time_index, particle_index, coord_index],
                                #forces =              numpy.float[time_index, particle_index, coord_index],
                                #torques =             numpy.float[time_index, particle_index, coord_index])
  ```

4. Import **interactions** data :

+ `inrtsPid` is the index of particles involve in this interaction.
+ `intrsNorm` is the norm of the interction (unit vector in between the two particles).
+ `intrsNF` is the normal force of the interaction.
+ `intrsSF` is the shear force of teh interaction.

  
  ```ruby
  data_class_name.get_interactions(intrsPid =  [time_index][interactions_index] -> numpy.int[p1_index, p2_index],
                                   intrsNorm = [time_index][interactions_index] -> numpy.float[coord_index],
                                   intrsNF =   [time_index][interactions_index] -> numpy.float[coord_index],
                                   intrsSF =   [time_index][interactions_index] -> numpy.float[coord_index],)
  ```

### Display 3D View

Call ```gl3f.main(data_class_name)``` to display with default setting.

Some setting can be apply as :
```ruby
gl3f.main(data_class_name,
          winSize = [xSize, ySize], #int
          cam_target = [0, 0, 0])   #float
```

Control can also be modified as :
```ruby
gl3f.main(data_class_name,
          rotButton = 0,                      #int
          dragButton = 2,                     #int
         
          transFactor = 0.01,                 #float
          zoomFactor = 2,                     #float
          rotFactor = 0.005,                  #float

          posTimeKey = pygame.K_d, #100       #int
          negTimeKey = pygame.K_q, #113       #int
          restartTimeKey = pygame.K_s, #115   #int
         )
```
## Texture and State

States reffer to the different textures you want to apply to particles. By default the first texture (`0.png`) is applyied, then state[0] is for the second texture (`1.png`), etc... 

### Add More texture

By default 3 textures are aviable (`0.png`, `1.png`, `2.png`). More texture can be add in ```./gl3Dview/texture```, the original texture template is avaible in ```./gl3Dview/texture/texture.xcf``` with layering to modifiy back ground color.

Note that the ```gl3Dc.texture``` class will load every file with ```.png``` extention present in ```./gl3Dview/texture``` and sort it by alphabetic order.

&emsp; *Be carefull loading heavy texture will result of a lack of fluidity.*



