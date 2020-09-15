import os 
from skimage import io
from skimage.viewer import ImageViewer
import numpy as np
from scipy.spatial import distance
import math
import matplotlib.pyplot as plt


def obterNovoPixel(linha, coluna, img, filtro):
    vetorFiltro = np.array(filtro.flatten())[0]
    if vetorFiltro.size==1:
        vetorFiltro = np.array(filtro.flatten())
    w,h = img.shape
    lm=filtro.shape[0]
    cm=filtro.shape[0]
    vetor = np.zeros(lm*cm)
    iv = 0
    m = int(lm/2)
    soma1=0
    for i in range(0,lm):
        for j in range(0,cm):
            novoI = linha+i-m
            novoJ = coluna+j-m
            if(novoI<=0): novoI=linha
            if(novoJ<=0): novoJ=coluna
            if(novoI>w-1): novoI=w-1
            if(novoJ>h-1): novoJ=h-1
            vetor[iv]=img[novoI,novoJ]
            soma1=soma1+(vetor[iv]*vetorFiltro[iv])
            iv+=1
    novoPixel = soma1
    return novoPixel

def obterImgComFiltroSobel(imgE):
    w,h = imgE.shape
    imgX = np.zeros([w, h])
    imgY = np.zeros([w, h])
    imgN = np.zeros([w, h])
    filtroSobel1 = np.matrix([[-1,-2,-1],[0,0,0],[1,2,1]])
    filtroSobel2 = np.matrix([[-1,0,1],[-2,0,2],[-1,0,1]])    
    for i in range(0,w):
            for j in range(0,h):
                imgX[i,j] = obterNovoPixel(i,j,imgE,filtroSobel1)
                imgY[i,j] = obterNovoPixel(i,j,imgE,filtroSobel2)
                imgN[i,j] = math.sqrt(math.pow(imgX[i,j],2)+math.pow(imgY[i,j],2))
    return imgN

def contruirFiltroGaussiano(size, sigma):
    kernel = np.zeros([size, size])
    sum = 0; indx = 0;
    for x in range(-1*(int(size/2)), int(size/2)+1):
        indy = 0;
        for y in range (-1*(int(size/2)) , int(size/2)+1):
            kernel[indx][indy] = (1.0 / (2* math.pi *sigma * sigma )) * math.exp ( - (x*x + y*y)/ (2*sigma*sigma));
            sum+=kernel[indx][indy]
            indy+=1
        indx+=1;
    for i in range(size):
        for j in range(0,size):
            kernel[i][j]=kernel[i][j]/sum
    return kernel
            
def obterImgComFiltroGaussiano(imgE, filtro):
    w,h = imgE.shape    
    imgN = np.zeros([w, h])
    for i in range(0,w):
        for j in range(0,h):
            imgN[i,j] = obterNovoPixel(i, j, imgE, filtro)
    return imgN


def exibirImagens(vetorImg, titulos):
    rows = 2
    cols = 4
    axes=[]
    fig=plt.figure()
    for i in range(len(vetorImg)):
        img = vetorImg[i]
        axes.append(fig.add_subplot(rows, cols, i+1) )
        axes[-1].set_title(titulos[i])  
        plt.imshow(img)
    fig.tight_layout()    
    plt.show()    

print()


filtroG5 = contruirFiltroGaussiano(5,1)
filtroG7 = contruirFiltroGaussiano(7,1)
filtroG11 = contruirFiltroGaussiano(11,1)

vetorImg = []
vetorImg.append(io.imread('noisy.jpg'))
vetorImg.append(obterImgComFiltroGaussiano(vetorImg[0],filtroG5))
vetorImg.append(obterImgComFiltroGaussiano(vetorImg[0],filtroG7))
vetorImg.append(obterImgComFiltroGaussiano(vetorImg[0],filtroG11))
vetorImg.append(io.imread('building.jpg'))
vetorImg.append(obterImgComFiltroSobel(vetorImg[4]))

titulos = [
            "Antes Filtro Gaussiano", 
            "Depois Filtro Gaussiano tamanho 5", 
            "Depois Filtro Gaussiano tamanho 7",
            "Depois Filtro Gaussiano tamanho 11",  
            "Antes Filtro Sobel", 
            "Depois Filtro Sobel"
            ]

exibirImagens(vetorImg, titulos)