
### Gazebo Turtlebot

Certifique-se de que seu `.bashrc` têm as variáveis `ROS_IP` e `ROS_MASTER_URI` desabilitadas antes de rodar o Gazebo


Você pode iniciar o Gazebo usando **uma** das opções:

    roslaunch turtlebot3_gazebo turtlebot3_stage_4.launch

    roslaunch turtlebot3_gazebo turtlebot3_stage_1.launch

    roslaunch turtlebot3_gazebo turtlebot3_stage_2.launch

    roslaunch turtlebot3_gazebo turtlebot3_stage_3.launch

    roslaunch turtlebot3_gazebo turtlebot3_house.launch

    roslaunch turtlebot3_gazebo turtlebot3_world.launch

O Gazebo já abre um `roscore` implicitamente. 

Note que a questão 1 **exige** que seja o `turtlebot3_house.launch`.


## catkin_make

Executar `catkin_make` após fazer o download do projeto: 

    cd ~/catkin_ws/
    catkin_make

## Onde baixar os arquivos

O código deve sempre ser baixado na pasta `cd ~/catkin_make/src` :

    cd ~/catkin_make/src
    git clone <nome do repo>

## Arquivos executáveis

Certifique-se de que seus scripts Python são executáveis

    roscd p1_20
    cd scripts
    chmod a+x *py

## Executar prova

Para executar, faça:

    rosrun p1_20 arquivo.py 

Onde `arquivo.py` é algum script Python executável que você deve ter na pasta `p1_20/scripts`.


Certifique-se de que seus scripts ROS rodam com Python 2 e têm sempre no começo:

    #! /usr/bin/env python
    # -*- coding:utf-8 -*-
    
    from __future__ import division, print_function


## Commit no Github

    Lembre-se, de regularmente fazer
        cd ~/catkin_ws/src/PROVA
        git add --all
        git commit -m "Mensagem aqui"
        git push

