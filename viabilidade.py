import parHosPopGen as md #carregando o modelo
import pylab as pl
import pandas as pd
#
print 'Rodando modulo de analise de viabilidade populacional...'
#
PEhosp = []
PEpar = []
vetorExtincoesHosp = []
vetorExtincoesPar = []
#vetorPEhosp = []
#vetorPEpar = []
valorMax=1000
numDeIteracoes=20
rangeDeK = [20,40,60,80,100,200,300,400,500,600,700,800,900,1000]
parametroK = []

for i in rangeDeK: #loop para variar parametros e realizar teste de sensibilidade.
    for j in range(numDeIteracoes):
        modelo = md.start(1,1000,1, 1,100,1, i ,0.3,0.05,0.15,1000) #TUTORIAL:n,g,s,nPar,gPar,sPar,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK
        modelo.roda()
        if modelo.res[-1] > 1:
            vetorExtincoesHosp.append(0)
        else:
            vetorExtincoesHosp.append(1)
        #
        if modelo.resPar[-1] > 1:
            vetorExtincoesPar.append(0)
        else:
            vetorExtincoesPar.append(1)
    #
    PEhosp.append( sum(vetorExtincoesHosp) * len(vetorExtincoesHosp)**-1 )
    PEpar.append( sum(vetorExtincoesPar) * len(vetorExtincoesPar)**-1 )
    parametroK.append(i)

os.chdir('/home/anderson/Documentos/Pesquisa/Parasites and host population genetics/RESULTADOS/500') #MTA ATENCAO AQUI!
PEhospDF = pd.DataFrame(PEhosp)
PEparDF = pd.DataFrame(PEpar)
parametroKPF = pd.DataFrame(parametroK)
PEhospDF.to_csv('PEhospComDiv.csv')
PEparDF.to_csv('PEparComDiv.csv')
parametroKPF.to_csv('parametroK.csv')

#print 'Proabilidade de extincao da populacao de hospedeiros:', PEhosp
#print 'Probabilidade de extincao da populacao de parasitas:', PEpar
#
print 'Modelo de analise de viabilidade populacional finalizado!!'
