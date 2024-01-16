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

`int[index_1][index_2][etc]` represent array with type `int` and index in order `[index_1][index_2]`.


1. Create data class :

  ```ruby
  data_class_name = gl3Dc.data_class()
  ```

2. Import time data :
  ```ruby
  data_class_name.get_time(dt =         float -> time_step,    
                           time_index = int[time_index])
  ```
   
3. Import **particles** data :

+ `states_type` is the list name of the differents state.
+ `states` is the differents state for each particles for each time step, default state is `''`.
+ `radius` is the particles radius for ech particles.
+ `positions` is the position of each particles for each time step.
+ `orientation` is the orientation each particles for each time step, it must be like `[angle, x, y, z]` where the `angle` is in degree and `x, y, z` represent the rotation axis.

Unsed for the moment :  <br />
   ▫️ `velocities` is the velocities of each particles at each time step.  <br />
   ▫️ `rotation_velocities` is the rotation velocities of each particles at each time step. <br />
   ▫️ `forces` is the forces of each particles at each time step. <br />
   ▫️ `torques` is the torques of each particles at each time step. <br />

  
&emsp; **It's better to adimentionalize particle size (radius) and position by the mean particle size.**
   
  ```ruby
  data_class_name.get_particles(states_type =          str[state_index],
                                states =               str[time_index][particle_index],
                                radius =               float[particle_index],
                                positions =            float[time_index][particle_index, coord_index],
                                orientations =         float[time_index][particle_index, angle:axis_coord_index],
                                #velocities =          float[time_index][particle_index, coord_index],
                                #rotation_velocities = float[time_index][particle_index, coord_index],
                                #forces =              float[time_index][particle_index, coord_index],
                                #torques =             float[time_index][particle_index, coord_index])
  ```

4. Import **interactions** data :

+ `inrtsPid` is the index of particles involve in this interaction.
+ `intrsNorm` is the norm of the interction (unit vector in between the two particles).
+ `intrsNF` is the normal force of the interaction.
+ `intrsSF` is the shear force of teh interaction.

  
  ```ruby
  data_class_name.get_interactions(intrsPid =  int[time_index][interactions_index][p1_index:p2_index],
                                   intrsNorm = float[time_index][interactions_index][coord_index],
                                   intrsNF =   float[time_index][interactions_index][coord_index],
                                   intrsSF =   float[time_index][interactions_index][coord_index],)
  ```

### Display 3D View

Call ```gl3f.main(data_class_name)``` to display with default setting.

1. **Display setting** :

   + `winSize` is the window size in pixels.
   + `cam_target` is the point where the view is pointing at the begining.

```ruby
gl3f.main(data_class_name,
          winSize = [xSize, ySize], #int
          cam_target = [0, 0, 0])   #float
```

2. **Interaction setting** :

   + `nfLogNorm` set a log scale for normal force.
   + `nfSize` set the *minimum size first* and *maximum size second* for normal force.
   + `shearForceDisplay` allow to display shear interactions.
   + `sfLogNorm` set a log scale for shear force.
   + `sfSize` set the *minimum size first* and *maximum size second* for shear force.

```ruby
gl3f.main(data_class_name,
          nfLogNorm = False,         #bool    
          nfSize = [0.05, 0.5],      #float
                   
          shearForceDisplay = False, #bool
          sfLogNorm = False,         #bool
          sfSize = [0.1, 0.5],)      #float
```


4. **Control Setting** :

   + `rotButton` set the rotation button of the mouse.
   + `dragButton` set the drag button of the mouse.
   + `transFactor` set the transaltion speed (drag).
   + `zoomFactor` set the zoom speed.
   + `rotFactor` set the rotation speed.
   + `posTimeKey` set the button to get to +1 time step.
   + `negTimeKey` set the button to get to -1 time step.
   + `restartTimeKey` set the button to get to 0 time step.


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



