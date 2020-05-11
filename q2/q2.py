#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "../../robot20/media/lines.mp4"

def check_exists_size(name, size):
    """
        Função para diagnosticar se os arquivos estão com problemas
    """
    if os.path.isfile(name):
        stat = os.stat(name)
        print("Informações do arquivo ", name, "\n", stat)
        if stat.st_size !=size:
            print("Tamanho errado para o arquivo ", name, " Abortando ")
            mensagem_falta_arquivos()
            sys.exit(0)
    else:
        print("Arquivo ", name, " não encontrado. Abortando!")
        mensagem_falta_arquivos()
        sys.exit(0)

def mensagem_falta_arquivos():
    msg = """ls
    ls

    Tente apagar os arquivos em robot20/ros/exemplos_python/scripts:
         MobileNetSSD_deploy.prototxt.txt
         MobileNetSSD_deploy.caffemodel
    Depois
        No diretório robot20/ros/exemplos_python/scripts fazer:
        git checkout MobileNetSSD_deploy.prototxt.txt
        Depois ainda: 
        git lfs pull 

        No diretório No diretório robot20/media

        Fazer:
        git lfs pull

        Ou então baixe os arquivos manualmente nos links:
        https://github.com/Insper/robot20/tree/master/ros/exemplos_python/scripts
        e
        https://github.com/Insper/robot20/tree/master/media
    """
    print(msg)

#### Funções da solução ####

import math
import random

def do_houghlines(img, output,  color, seg):
    lines = cv2.HoughLinesP(image=img, rho=10, theta=math.pi/180.0, threshold=253, lines=np.array([]), minLineLength=70, maxLineGap=2)
    if lines is None:
        return # Nenhuma linha encontrada
    a,b,c = lines.shape
    for i in range(a):
        # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
        cv2.line(output, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), color, 1, cv2.LINE_AA)
        # Guarda aquele segmento
        seg.append(((lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3])))

# Usaremos o algoritmo que calcula interseção de retas dados 2 segmentos que foi fornecido na [atividade de ponto de fuga](https://github.com/Insper/robot20/blob/master/aula03/atividade_Semana03.ipynb).

def find_m_h(segmento):
    a = segmento[0]
    b = segmento[1]
    m = (b[1] - a[1])/(b[0] - a[0])
    h = a[1] - m*a[0]
    return m,h

def intersect_segs(seg1, seg2):
    m1,h1 = find_m_h(seg1)
    m2,h2 = find_m_h(seg2)
    x_i = (h2 - h1)/(m1-m2)
    y_i = m1*x_i + h1
    return x_i, y_i

def intersection(lista1, lista2):
    if len(lista1) > 1 and len(lista2) > 1:
        seg1 = random.choice(lista1)
        seg2 = random.choice(lista2)
        pt = intersect_segs(seg1, seg2)
        return (int(pt[0]), int(pt[1]))
    else:
        return None

# Vamos usar a função de crosshair da [aula 2 - exemplos](https://github.com/Insper/robot20/blob/master/aula02/Atividade2_Exemplos.ipynb) mas modificado para fazer cada segmento de uma cor: 
def crosshair(img, point, size, color1, color2):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    if point is None:
        return
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color1,5)
    cv2.line(img,(x,y - size),(x, y + size),color2,5)    

################################


if __name__ == "__main__":


    # Checando se os arquivos necessários existem
    check_exists_size(video, 942014)

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)

    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")


    while(True):
        # Capture frame-by-frame
        ret, frame_bgr = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        # ### Convertendo para RGB que é mais fácil raciocinar neste caso específico
        frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        # Separando R, G e B. Veja o notebook para discussao
        R = frame[:,:,0]
        G = frame[:,:,1]
        B = frame[:,:, 2]

        # Apesar de o contraste estar muito bom, ainda não é perfeito. Notam-se alguns traçoes em cinza. 
        # # Vamos recorrer à função cv2. threshold que foi vista na aula 2.
        ret, R2 = cv2.threshold(R, 200, 255, cv2.THRESH_OTSU)
        ret, G2 = cv2.threshold(G, 200, 255, cv2.THRESH_OTSU)
        ret, B2 = cv2.threshold(B, 250, 255, cv2.THRESH_OTSU)

        filtradas_rgb = [R2, G2, B2]

        # Listas para guardas segumentos encontrados por hough
        seg_r = []
        seg_g = []
        seg_b = []

        # Frame para saida
        out = frame.copy()
        out[:,:,:] = 0 # Criamos uma imagem em branco igual à de entrada

        # tuplas de cores
        r_color = (255,0,0)
        g_color = (0,255,0)
        b_color = (0,0,255)

        colors = [r_color, g_color, b_color]

        # Lista de lista vazias que vai nos ajudar no futuro
        segs = [seg_r, seg_g, seg_b]

        for i in range(len(filtradas_rgb)):
            do_houghlines(filtradas_rgb[i], out, colors[i], segs[i])

        names = ["red", "green", "blue"]


        # Segmentos encontrados:
        # for i in range(len(names)):
        #    print(names[i])
        #    for s in segs[i]:
        #        print(s)



        # Verificando `intersect_segs`com os valores de teste fornecidos na aula 03:
        # intersect_segs([(3,2.5),(4, 0.6)],[(1,2.4),(.6,1.1)])



        inter_r_b = intersection(seg_r, seg_g)
        crosshair(out, inter_r_b, 10, r_color, g_color)


        inter_g_b = intersection(seg_g, seg_b)
        crosshair(out, inter_g_b, 10, g_color, b_color)

        inter_b_r = intersection(seg_b, seg_r)
        crosshair(out, inter_b_r, 10, b_color, r_color)

        cv2.imshow("Intersecoes", out)
            
        cv2.imshow('imagem', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


