print 'Rodando modulo de itecacoes...'

import pandas as pd
import pylab as pl
import numpy as np
import os 
os.chdir('/home/anderson/Documentos/Pesquisa/Parasites and host population genetics') #MTA ATENCAO AQUI!
import teste2genes as md #carregando o modelo
import FST

numDeIteracoes = 10
controleDiv=[]
controleRiq=[]
controleDadosFST=[]
tratamentoDiv=[]
tratamentoRiq=[]
tratamentoDadosFST=[]
controleDivPar=[]
controleRiqPar=[]
controleDadosFSTpar=[]
tratamentoRiqPar=[]
tratamentoDivPar=[]
tratamentoDadosFSTpar=[]
FSToutput=[]
suceptibilidadeControle = []
suceptibilidadeControleMed = []
suceptibilidadeControleStd = [] 
suceptibilidadeTratamento = []
suceptibilidadeTratamentoMed = []
suceptibilidadeTratamentoStd = []
virulenciaTratamento = []
virulenciaTratamentoMed = []
virulenciaTratamentoStd = []
dadosSuceptibilidadeControle = []
dadosSuceptibilidadeControleMed = []
dadosSuceptibilidadeControleStd = []
dadosSuceptibilidadeTratamento = []
dadosSuceptibilidadeTratamentoMed = []
dadosSuceptibilidadeTratamentoStd = []
dadosVirulenciaTratamento = []
dadosVirulenciaTratamentoMed = []
dadosVirulenciaTratamentoStd = []
#
for i in range(numDeIteracoes):
    modelo = md.start(1000,1,1, 0,0,0, 1000,0.3,0.05,0.15,1000) #TUTORIAL:n,g,s,nPar,gPar,sPar,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK
    modelo.roda()
    #hospedeiro
    controleDiv.append(modelo.resDivGen)
    controleRiq.append(modelo.resRiqGen)
    controleDadosFST.append(modelo.dadosGen)
    #parasita - para os casos de cenarios com controle parasitado 
    controleDivPar.append(modelo.resDivGenPar)
    controleRiqPar.append(modelo.resRiqGenPar)
    controleDadosFSTpar.append(modelo.dadosGenPar)

for i in range(numDeIteracoes):
    modelo = md.start(1,1000,1, 100,1,1, 1000,0.3,0.05,0.15,1000) #TUTORIAL:n,g,s,nPar,gPar,sPar,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK
    modelo.roda()
    #hospedeiro
    tratamentoDiv.append(modelo.resDivGen)
    tratamentoRiq.append(modelo.resRiqGen)
    tratamentoDadosFST.append(modelo.dadosGen)
    #parasita 
    tratamentoDivPar.append(modelo.resDivGenPar)
    tratamentoRiqPar.append(modelo.resRiqGenPar)
    tratamentoDadosFSTpar.append(modelo.dadosGenPar)
####
# #analise da variacao no numero de genes e tamanho populacional
# vetorDeGenes=[1,2,3,4,5] #range(10)
# vetorDeK=[100,200,300,400,500] #[50,100,150,200,250,300,350,400,450,500,600,700,800,900,1000]
# #
# dadosDivHosp=[];dadosRiqHosp=[];dadosAbunHosp=[];dadosDivPar=[];dadosRiqPar=[];dadosAbunPar=[]
# #
# for i in vetorDeGenes:
#     dadosDivHospK=[]
#     dadosRiqHospK=[]
#     dadosAbunHospK=[]
#     dadosDivParK=[]
#     dadosRiqParK=[]
#     dadosAbunParK=[]
#     for j in vetorDeK:
#         #for k in range(numDeIteracoes):
#         modelo = md.start(j,i,1, j,1,1, j,0.3,0.05,0.15,1000) #TUTORIAL:n,g,s,nPar,gPar,sPar,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK
#         modelo.roda()
#         #
#         dadosDivHospK.append(modelo.resDivGen[-1]); print dadosDivHospK
#         dadosRiqHospK.append(modelo.resRiqGen[-1])
#         dadosAbunHospK.append(modelo.res[-1])
#         #
#         dadosDivParK.append(modelo.resDivGenPar[-1])
#         dadosRiqParK.append(modelo.resRiqGenPar[-1])
#         dadosAbunParK.append(modelo.resPar[-1])
#     #
#     dadosDivHosp.append(dadosDivHospK)
#     dadosRiqHosp.append(dadosRiqHospK)
#     dadosAbunHosp.append(dadosAbunHospK)
#     #
#     dadosDivPar.append(dadosDivParK)
#     dadosRiqPar.append(dadosRiqParK)
#     dadosAbunPar.append(dadosAbunParK)
# #
# x=y=len(vetorDeK)*len(vetorDeGenes)
# pl.pcolor(vetorDeK,vetorDeGenes,dadosDivHosp); pl.xlabel('vetorDeK'); pl.ylabel('vetorDeGenes')

#
# for i in range(numDeIteracoes): #somente Div por enquanto...
#     pl.plot(controleRiq[i],'.',c='b')
#     pl.plot(tratamentoRiq[i],'.',c='r')
# pl.show()
#
#Div
controleDivDF = pd.DataFrame(controleDiv)    
controleDivMed = controleDivDF.mean()
controleDivSTD = controleDivDF.std()
#
tratamentoDivDF = pd.DataFrame(tratamentoDiv)
tratamentoDivMed = tratamentoDivDF.mean()
tratamentoDivSTD = tratamentoDivDF.std()
#parasita# 
tratamentoDivParDF = pd.DataFrame(tratamentoDivPar)
tratamentoDivParMed = tratamentoDivParDF.mean()
tratamentoDivParSTD = tratamentoDivParDF.std()
#
pl.plot((tratamentoDivMed),c='r',lw=2)
pl.plot((tratamentoDivMed+tratamentoDivSTD),c='r',lw=0.5)
pl.plot((tratamentoDivMed-tratamentoDivSTD),c='r',lw=0.5)
#
pl.plot((controleDivMed),c='b',lw=2)
pl.plot((controleDivMed+controleDivSTD),c='b',lw=0.5)
pl.plot((controleDivMed-controleDivSTD),c='b',lw=0.5)
pl.show()
#Riq
controleRiqDF = pd.DataFrame(controleRiq)    
controleRiqMed = controleRiqDF.mean()
controleRiqSTD = controleRiqDF.std()
#
tratamentoRiqDF = pd.DataFrame(tratamentoRiq)
tratamentoRiqMed = tratamentoRiqDF.mean()
tratamentoRiqSTD = tratamentoRiqDF.std()
#parasita#
tratamentoRiqParDF = pd.DataFrame(tratamentoRiqPar)
tratamentoRiqParMed = tratamentoRiqParDF.mean()
tratamentoRiqParSTD = tratamentoRiqParDF.std()
#
pl.plot((tratamentoRiqMed), c='r',lw=2)
pl.plot((tratamentoRiqMed+tratamentoRiqSTD),c='r',lw=0.5)
pl.plot((tratamentoRiqMed-tratamentoRiqSTD),c='r',lw=0.5)
#
pl.plot((controleRiqMed),c='b',lw=2)
pl.plot((controleRiqMed+controleRiqSTD),c='b',lw=0.5)
pl.plot((controleRiqMed-controleRiqSTD),c='b',lw=0.5)
pl.show()
#
##FST
# vetorHelper = []
# for i in range(len(tratamentoDadosFSTpar)):
#     for j in range(len(tratamentoDadosFSTpar[i])):    
#         vetorHelper.append([x for x in tratamentoDadosFSTpar[i][j] if x!= [] ])
# tratamentoDadosFSTpar = vetorHelper
    
# for i in range(numDeIteracoes):
#     vetorDeFSTnoTempo=[]
#     for t in range(len(controleDadosFST[i])):
#         popControle = controleDadosFST[i][t]
# #        tempo.append(t)
#         suceptibilidadeControle.append(controleDadosFST[i][t])
#         suceptibilidadeControleMed.append(np.mean(controleDadosFST[i][t]))
#         suceptibilidadeControleStd.append(np.std(controleDadosFST[i][t]))
#         #
#         popTratamento = tratamentoDadosFST[i][t]
#         suceptibilidadeTratamento.append(tratamentoDadosFST[i][t])
#         suceptibilidadeTratamentoMed.append(np.mean(tratamentoDadosFST[i][t]))
#         suceptibilidadeTratamentoStd.append(np.std(tratamentoDadosFST[i][t]))
#         # virulenciaTratamento.append(tratamentoDadosFSTpar[i][t]) #retirar quando rodar duas populacoes sem parasitas
#         # virulenciaTratamentoMed.append(np.mean(tratamentoDadosFSTpar[i][t])) #retirar quando rodar duas populacoes sem parasitas
#         # virulenciaTratamentoStd.append(np.std(tratamentoDadosFSTpar[i][t])) #retirar quando rodar duas populacoes sem parasitas
#         #
#         vetorDePop = [popControle,popTratamento]        
#         FSTcalculado = FST.FST(vetorDePop,10000)
#         vetorDeFSTnoTempo.extend(FSTcalculado)
#     FSToutput.append(vetorDeFSTnoTempo)
#     # dadosSuceptibilidadeControle.append(suceptibilidadeControle)
#     # dadosSuceptibilidadeControleMed.append(suceptibilidadeControleMed)
#     # dadosSuceptibilidadeControleStd.append(suceptibilidadeControleStd)
#     # dadosSuceptibilidadeTratamento.append(suceptibilidadeTratamento)
#     # dadosSuceptibilidadeTratamentoMed.append(suceptibilidadeTratamentoMed)
#     # dadosSuceptibilidadeTratamentoStd.append(suceptibilidadeTratamentoStd)
#     # dadosVirulenciaTratamento.append(virulenciaTratamento) #retirar quando rodar duas populacoes sem parasitas
#     # dadosVirulenciaTratamentoMed.append(virulenciaTratamentoMed) #retirar quando rodar duas populacoes sem parasitas
#     # dadosVirulenciaTratamentoStd.append(virulenciaTratamentoStd) #retirar quando rodar duas populacoes sem parasitas
# #dataframes da virulencia e suceptibildiade
# # suceptibilidadeControleDF = pd.DataFrame(dadosSuceptibilidadeControle)
# # suceptibilidadeTratamentoDF = pd.DataFrame(dadosSuceptibilidadeTratamento)
# # virulenciaTratamentoDF = pd.DataFrame(dadosVirulenciaTratamento)
# #media e desvio padrao do FSToutput
# FSTdataFrame = pd.DataFrame(FSToutput)
# FSTmed = np.mean(pd.DataFrame(FSToutput))
# FSTstd = np.std(pd.DataFrame(FSToutput))
# #
# ##Grafico do FSToutput
# # for i in range(numDeIteracoes):
# #     pl.plot(FSToutput[i],'.',c='b')
# # pl.show()
# #
# ##Grafico do FST medio
# pl.plot(FSTmed,c='b',lw=2)
# pl.plot(FSTmed+FSTstd,c='b',lw=0.5)
# pl.plot(FSTmed-FSTstd,c='b',lw=0.5)
# pl.show()
# #
# ##FST do parasita - para os casos de controle parasitado
# # for i in range(numDeIteracoes):
# #     vetorDeFSTnoTempo=[]
# #     for t in range(len(controleDadosFSTpar[i])):
# #         popControle = controleDadosFSTpar[i][t]
# #         popTratamento = tratamentoDadosFSTpar[i][t]
# #         vetorDePop = [popControle,popTratamento]        
# #         FSTcalculado = FST.FST(vetorDePop,1000)
# #         vetorDeFSTnoTempo.extend(FSTcalculado)
# #     FSToutput.append(vetorDeFSTnoTempo)
# # #media e desvio padrao do FSToutput
# # FSTparMed = np.mean(pd.DataFrame(FSToutput))
# # FSTparStd = np.std(pd.DataFrame(FSToutput))
# #
#Salvando em arquivos
os.chdir('/home/anderson/Documentos/Pesquisa/Parasites and host population genetics/RESULTADOS') #MTA ATENCAO AQUI!
#tabela de medias e std#
dados = pd.DataFrame([controleRiqMed,controleRiqSTD,controleDivMed,controleDivSTD,tratamentoRiqMed,tratamentoRiqSTD,tratamentoDivMed,tratamentoDivSTD,tratamentoRiqParMed,tratamentoRiqParSTD,tratamentoDivParMed,tratamentoDivParSTD,FSTmed,FSTstd])
#
dados=dados.transpose()
#
dados.columns = ['controleRiqMed','controleRiqSTD','controleDivMed','controleDivSTD','tratamentoRiqMed','tratamentoRiqSTD','tratamentoDivMed','tratamentoDivSTD','tratamentoRiqParMed','tratamentoRiqParSTD','tratamentoDivParMed','tratamentoDivParSTD','FSTmed','FSTstd']
#
dados.to_csv('dados.csv')
#
#dados brutos#
controleRiqDF.to_csv('dadosControleRiqDF.csv')
controleDivDF.to_csv('dadosControleDivDF.csv')
tratamentoRiqDF.to_csv('dadosTratamentoRiqDF.csv')
tratamentoDivDF.to_csv('dadosTratamentoDivDF.csv')
tratamentoRiqParDF.to_csv('dadosTratamentoRiqParDF.csv')
tratamentoDivParDF.to_csv('dadosTratamentoDivParDF.csv')
FSTdataFrame.to_csv('FSTdataFrame.csv')
# suceptibilidadeControleDF.to_csv('suceptibilidadeControleDF.csv')
# suceptibilidadeTratamentoDF.to_csv('suceptibilidadeTratamentoDF.csv')
# virulenciaTratamentoDF.to_csv('virulenciaTratamentoDF.csv')
#
print 'Modulo de iteracoes concluidas, ManoBrow!!'
