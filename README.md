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
You needed to import your data in the used classes, by following the schem ```array[time_index, particle_index, other]```. 

1. Create data class :

  ```ruby
  data_class_name = gl3Dc.data_class()
  ```

2. Import time data :
  ```ruby
  data_class_name.get_time(time_step,                    #float
                           time_index_array[time_index]) #int
  ```
   
3. Import particles data :

  States reffer to the different textures you want to apply to particles. 
  Better to adimentionalize particle size (radius) and position by the mean particle size.
   
  ```ruby
  data_class_name.get_particles(array_of_state_name       [state_index],                                       #str
                                array_of_state            [time_index, particle_index, state_index],           #bool
                                array_of_particles_radius [particle_index],                                    #float
                                array_of_position         [time_index, particle_index, coord_index],           #float
                                array_of_orientation      [time_index, particle_index, angle:axis_coord_index],#float
                                array_of_velocity         [time_index, particle_index, coord_index],           #float
                                array_of_rotation_velocity[time_index, particle_index, coord_index],           #float
                                array_of_force            [time_index, particle_index, coord_index],           #float
                                array_of_torque           [time_index, particle_index, coord_index])           #float
  ```

4. Import data interactions (in comming) :

  ```ruby
  data_class_name.get_interactions()
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

### Add More texture

By default 3 textures are aviable (`0.png`, `1.png`, `2.png`). More texture can be add in ```./gl3Dview/texture```, the original texture template is avaible in ```./gl3Dview/texture/texture.xcf``` with layering to modifiy back ground color.

Note that the ```gl3Dc.texture``` class will load every file with ```.png``` extention present in ```./gl3Dview/texture``` and sort it by alphabetic order.

*Be carefull loading to heavy texture will result of a lack of fluidity.*



