import os 
from skimage import io
import numpy as nmp
from scipy.spatial import distance
import math
import matplotlib.pyplot as plt

caminho = input("Informe o caminho (enter para Vistex): ")
arquivo = input("Informe o nome do arquivo (enter para c001_001.png): ")
qtd = input("Informe a quantidade de arquivos semelhantes retornados (enter para 2): ")

if(caminho==''):
    path = 'Vistex/'
else:
    path = caminho


files = os.listdir(path)
n = len(files)
#n = 20

if(arquivo==''):
    imgE = io.imread(path+files[0])
    arquivo = files[0]
else:
    imgE = io.imread(path+arquivo)

if(qtd==''):
    qtd=2

w,h,nc = imgE.shape
# histograma E
histogramE = nmp.zeros( (3, 256) )
for x in range(w):
    for y in range(h):
        for c in range(nc):
            histogramE[c,imgE[x,y,c]]+=1
# pdf E
pdfE = nmp.zeros( (3, 256) )
for x in range(w):
    for y in range(h):
        for c in range(nc):
            pdfE[c,imgE[x,y,c]]=histogramE[c,imgE[x,y,c]]/(w*h) # w*h mesmo?

d=nmp.zeros( (n, 2) )

for i in range (n):
    img = io.imread(path+files[i])
    w,h,nc = img.shape

    # histograma i
    histogram = nmp.zeros( (3, 256) )
    for x in range(w):
        for y in range(h):
            for c in range(nc):
                histogram[c,img[x,y,c]]+=1

    # pdf i    
    pdf = nmp.zeros( (3, 256) )
    for x in range(w):
        for y in range(h):
            for c in range(nc):
                pdf[c,img[x,y,c]]=histogram[c,img[x,y,c]]/(w*h) # w*h mesmo?

    # distancia i
    soma = 0.0
    for x in range(w):
        for y in range(h):
            for c in range(nc):
                soma += math.pow(pdfE[c,imgE[x,y,c]] - pdf[c,img[x,y,c]], 2)
    d[i,0]=math.sqrt(soma)
    d[i,1]=i

from operator import itemgetter
d = sorted(d, key=itemgetter(0))


# exibir os qtd mais semelhantes
print(qtd, "arquivos de imagens mais semelhantes:")

rows = int(qtd)+1
cols = 1
axes=[]
fig=plt.figure()
axes.append( fig.add_subplot(rows, cols, 1) )
subplot_title=("Procurada: "+arquivo)
axes[-1].set_title(subplot_title)  
plt.imshow(imgE)
for i in range(int(qtd)):
    print(files[int(d[i][1])])
    img = io.imread(path+files[int(d[i][1])])
    axes.append( fig.add_subplot(rows, cols, i+2) )
    subplot_title=("Semelhante "+ str(i+1) +": "+files[int(d[i][1])])
    axes[-1].set_title(subplot_title)  
    plt.imshow(img)

fig.tight_layout()    
plt.show()    
