print 'Rodando modulo de graficos...'
import pandas as pd
import pylab as pl
import numpy as np
import os 

os.chdir('/home/anderson/Documentos/Pesquisa/Parasites and host population genetics/RESULTADOS') #MTA ATENCAO AQUI!

##Div
controleDivDF = pd.read_csv('dadosControleDivDF.csv',header=0)
#controleDivDF = controleDivDF.drop(0)
controleDivDF = controleDivDF.drop('Unnamed: 0',axis=1)
controleDivMed = np.array(controleDivDF.mean())
controleDivSTD = np.array(controleDivDF.std())
#
tratamentoDivDF = pd.read_csv('dadosTratamentoDivDF.csv',header=0)
#tratamentoDivDF = tratamentoDivDF.drop(0)
tratamentoDivDF = tratamentoDivDF.drop('Unnamed: 0',axis=1)
tratamentoDivMed = tratamentoDivDF.mean()
tratamentoDivSTD = tratamentoDivDF.std()
#parasita# 
tratamentoDivParDF = pd.read_csv('dadosTratamentoDivParDF.csv',header=0)
#tratamentoDivParDF = tratamentoDivParDF.drop(0)
tratamentoDivParDF = tratamentoDivParDF.drop('Unnamed: 0',axis=1)
tratamentoDivParMed = np.array(tratamentoDivParDF.mean())
tratamentoDivParSTD = np.array(tratamentoDivParDF.std())
##
pl.plot((tratamentoDivMed),c='r',lw=2)
pl.plot((tratamentoDivMed+tratamentoDivSTD),c='r',lw=0.5)
pl.plot((tratamentoDivMed-tratamentoDivSTD),c='r',lw=0.5)
#
pl.plot((controleDivMed),c='b',lw=2)
pl.plot((controleDivMed+controleDivSTD),c='b',lw=0.5)
pl.plot((controleDivMed-controleDivSTD),c='b',lw=0.5)
pl.savefig('dominancia.jpg'); pl.axis([0,len(tratamentoDivMed),0,1])
pl.clf()
#parasitas
pl.plot((tratamentoDivParMed),c='r',lw=2)
pl.plot((tratamentoDivParMed+tratamentoDivParSTD),c='r',lw=0.5)
pl.plot((tratamentoDivParMed-tratamentoDivParSTD),c='r',lw=0.5)
pl.savefig('dominanciaPar.jpg'); pl.axis([0,len(tratamentoDivParMed),0,1])
pl.clf()
##Riq
controleRiqDF = pd.read_csv('dadosControleRiqDF.csv',header=0)
#controleRiqDF = controleRiqDF.drop(0)
controleRiqDF = controleRiqDF.drop('Unnamed: 0',axis=1)
controleRiqMed = controleRiqDF.mean()
controleRiqSTD = controleRiqDF.std()
#
tratamentoRiqDF = pd.read_csv('dadosTratamentoRiqDF.csv',header=0)
#tratamentoRiqDF = tratamentoRiqDF.drop(0)
tratamentoRiqDF = tratamentoRiqDF.drop('Unnamed: 0',axis=1)
tratamentoRiqMed = np.array(tratamentoRiqDF.mean())
tratamentoRiqSTD = np.array(tratamentoRiqDF.std())
#parasita#
tratamentoRiqParDF = pd.read_csv('dadosTratamentoRiqParDF.csv',header=0)
#tratamentoRiqParDF = tratamentoRiqParDF.drop(0)
tratamentoRiqParDF = tratamentoRiqParDF.drop('Unnamed: 0',axis=1)
tratamentoRiqParMed = np.array(tratamentoRiqParDF.mean())
tratamentoRiqParSTD = np.array(tratamentoRiqParDF.std())
#
pl.plot((tratamentoRiqMed), c='r',lw=2)
pl.plot((tratamentoRiqMed+tratamentoRiqSTD),c='r',lw=0.5)
pl.plot((tratamentoRiqMed-tratamentoRiqSTD),c='r',lw=0.5)
#
pl.plot((controleRiqMed),c='b',lw=2)
pl.plot((controleRiqMed+controleRiqSTD),c='b',lw=0.5)
pl.plot((controleRiqMed-controleRiqSTD),c='b',lw=0.5)
pl.savefig('riqueza.jpg'); pl.axis([0,len(tratamentoRiqMed),0,tratamentoRiqMed.max()])
pl.clf()
#parasitas
pl.plot((tratamentoRiqParMed),c='r',lw=2)
pl.plot((tratamentoRiqParMed+tratamentoRiqParSTD),c='r',lw=0.5)
pl.plot((tratamentoRiqParMed-tratamentoRiqParSTD),c='r',lw=0.5)
pl.savefig('riquezaPar.jpg'); pl.axis([0,len(tratamentoRiqParMed),0,tratamentoRiqParMed.max()])
pl.clf()
#
##FST
dados = pd.read_csv('dados.csv',header=0,index_col=False)
#dados = dados.drop(0)
dados = dados.drop('Unnamed: 0',axis=1)
FSTmed = np.array(dados['FSTmed'])
FSTstd = np.array(dados['FSTstd'])

##Grafico do FSToutput
# for i in range(numDeIteracoes):
#     pl.plot(FSToutput[i],'.',c='b')
# pl.show()
#
##Grafico do FST medio
pl.plot(FSTmed,c='b',lw=2)
pl.plot(FSTmed+FSTstd,c='b',lw=0.5)
pl.plot(FSTmed-FSTstd,c='b',lw=0.5)
pl.savefig('FST.jpg'); pl.axis([0,len(tratamentoRiqParMed),0,1])
pl.clf()
#
##FST do parasita - para os casos de controle parasitado
##
print 'Modulo de graficos finalizado...'
