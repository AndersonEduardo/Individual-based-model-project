##MODELO DE MORTE-VIDA COM GENOTIPOS E ORGANISMOS HAPLOIDES##

##PROXIMOS PASSOS:##
#Implementar fitness (diferenca entre individuo parasitado e nao paraditado
#implementar relacao entre especie de parasita e gen de parasita (ate agora, o tenho uma lista de gen e uma lista de sp, sem relacao)
#implementar cura depois de um tempo
#implementar hospedeiros diploides (esta haploide)
#implementar saida de dados para: virulencia (media e variancia)
##

print 'Rodando modulo do modelo...'
import pylab as pl
import numpy as np
import pandas as pd
import random as rd
import collections
import string

class organismos:
    def __init__(self,s,g):
        self.Sp = s #definindo a especie do organismo
        self.Gen = g #definindo seu genotipo
        self.parasitado = []  #definindo seu status parasitologico
        self.parGen = []
        self.parSp = []
        self.statusVida = 1 #definindo se esta vivo (1=vivo; 2=moto)
        self.sex = rd.choice(['M','F'])
        self.prenhez = 0
        self.idade = 0
        self.tempoInfectado = 0
        self.contagemInfectados = 0
        self.contagemProle = 0

class ambiente:
    def __init__(self,N,G,S,parN,parG,parS,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK): 
        self.vetorDeGen = [] #range(G)       
        self.vetorDeParSp = [] #range(parS)
        self.vetorDeParGen = [] #range(parG)
        self.numInd = N  #definindo o numero de individuos no ambiente
        self.numGen = G #definindo o numero de genes no genoma hospedeiro
        self.numSp = S #definindo o numero de especies no ambiente
        self.numParGen = parG #len(self.vetorDeParGen)
        self.numParSp = parS #len(self.vetorDeParSp)
        self.numParInd = parN
        self.populacao = [] #array de populacoes
        self.abundancia = [] #variavel para armazenar os tamanhos populacionais em cada passo de tempo
        self.abundanciaPar = [] #variavel para armazenar os tamanhos populacionais de parasitas em cada passo de tempo
        self.riquezaGenes = []
        self.riquezaGenesPar = []
        self.riquezaSpPar = []
        self.diversidadeGenes = []
        self.diversidadeGenesPar = []
        
        self.K = K
        self.tempoTcritico = tempoCriticoK
        self.proporcaoDeContatos = Ncontatos
        self.probMutaHosp = HospMuta
        self.probMutaPara = ParaMuta
        self.dadosGenParAtualizados = []
        self.dadosGenAtualizados = []
        self.contagemProle = []
        self.contagemVida = []
        self.contagemInfectados = []

    def criaPop(self):
        for i in range(self.numSp): #para cada especie...
            for j in range(self.numInd): #...crie 'numInd' organismos.
                self.PoolDeAlelos = range(1000000)
                self.PoolDeAlelos = self.PoolDeAlelos[1:]
                self.genomaNumeroSort =  rd.sample(self.PoolDeAlelos,self.numGen)
                for k in range(len(self.genomaNumeroSort)):
                    self.genomaNumero.extend(str(self.genomaNumeroSort[k]))
                self.genomaNumeroDF = pd.DataFrame(self.genomaNumero)
                #self.genomaNumero = self.genomaNumero[1:len(self.genomaNumero)-1]
                self.genomaLetraDF = pd.DataFrame( list(string.ascii_lowercase[:numGen]) )
                self.genomaDF = self.genomaNumeroDF + self.genomaLetraDF
                self.genomaDF = self.genomaDF.transpose()

                self.genomaList = []
                for k in range(len(self.genomaDF)):
                    self.genomaList.extend(list(self.genomaDF[k]))
                self.genoma = self.genomaList
                #
                self.ind = organismos(i+1,self.genoma) #criando um organismos
                self.ind.idade = rd.randint(0,10) #aleatorizando a idade
                self.populacao.append(self.ind) #adicionando o novo organismo no final do array de organismos
                self.vetorDeGen.extend([j+1,j+2]) #armazenando informacao genetica da populacao

    def criaPopPar(self): #cria a populacao de hospedeiros infectados
        for i in range(self.numParSp):
            for j in range(self.numParGen):
                for k in range(self.numParInd):
                    #self.indiceHelper = k + i*j*self.numParInd
                    self.indiceInfeccoes = rd.randint(0,len(self.populacao)-1) #infectar um individuo aleatorio
                    if self.populacao[self.indiceInfeccoes].parGen == []:
                        self.populacao[self.indiceInfeccoes].parasitado = 1 #colocando os parasitas nos hospedeiros
                        self.populacao[self.indiceInfeccoes].parSp = i+1 #colocando a Sp do parasita
                        self.populacao[self.indiceInfeccoes].parGen = j+1 #self.genotipoPar #nao usarei infeccoes multiplas
                        self.vetorDeParGen.extend([self.populacao[self.indiceInfeccoes].parGen])
                        self.vetorDeParSp.extend([self.populacao[self.indiceInfeccoes].parSp])
                        
                    # self.populacao[self.indiceHelper].parasitado = 1 #colocando os parasitas nos hospedeiros
                    # self.populacao[self.indiceHelper].parSp = i+1 #colocando a Sp do parasita
                    # self.populacao[self.indiceHelper].parGen = j+1 #nao comecarei usando multiplos genotipos para parasitas          
                    # self.vetorDeParGen.extend([self.populacao[self.indiceHelper].parGen])
                    # self.vetorDeParSp.extend([self.populacao[self.indiceHelper].parSp])

    def infeccao0(self):
    ##modela infeccao ativa generalizada (infectado infecta todos nao infectados em seu campo)##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        self.NumeroDeContatos =int(self.proporcaoDeContatos*len(self.populacao))
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].parasitado == 1):
                self.contatoInfeccioso = rd.sample(range(len(self.populacao)),self.NumeroDeContatos) #...sorteie um outro individuo na populacao...
                for j in self.contatoInfeccioso:
                    if self.populacao[j].parasitado == []:
                        self.populacao[i].contagemInfectados+=1 #coletando dados para numero de infeccoes/infectado
                        self.populacao[j].parasitado = 1
                        self.populacao[j].parGen = self.populacao[i].parGen ###
                        self.moeda = rd.random() #Mutacao: jogue uma 'modeda'...
                        if self.moeda <= self.probMutaPara: #(probebilidade de mutacao) ...se tiver sucesso...
                            #self.genotipoDoParasitaContatoComMutacao = int(np.random.normal(self.populacao[j].parGen,5))
                            self.genotipoDoParasitaContatoComMutacao = rd.randint(1,1000) #...o genotipo do parasita que sera recebido sofre mutacao...
                            if (self.genotipoDoParasitaContatoComMutacao not in self.vetorDeParGen) and (self.genotipoDoParasitaContatoComMutacao > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                self.populacao[j].parGen = self.genotipoDoParasitaContatoComMutacao #... e, se for dferente,  some a cepa do parasita residente...
                        self.vetorDeParGen.extend([self.populacao[j].parGen])
                        self.vetorDeParSp.extend([self.populacao[i].parSp])
                    
    def infeccao1(self):
    ##modela infeccao ativa genotipo-genotipo (ativa = infectado infecta todos nao infectados em seu campo)##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        self.NumeroDeContatos =int(self.proporcaoDeContatos*len(self.populacao))
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].parasitado == 1):
                self.contatoInfeccioso = rd.sample(range(len(self.populacao)),self.NumeroDeContatos) #...sorteie um outro individuo na populacao...
                for j in self.contatoInfeccioso:
                    if self.populacao[j].parasitado == []:
                        if self.populacao[i].parGen in self.populacao[j].Gen:
                            self.populacao[j].parasitado = 1
                        else:
                            self.moeda = rd.random()
                            if self.moeda < 0.1: #probabildiade de infeccao em hospedeiro heterozigoto
                                self.populacao[j].parasitado = 1
                        if self.populacao[j].parasitado == 1:
                            self.populacao[i].contagemInfectados+=1 #coletando dados sobre infeccoes/infectado
                            self.populacao[j].parGen = self.populacao[i].parGen ###
                            self.moeda = rd.random() #Mutacao: jogue uma 'modeda'...
                            if self.moeda <= self.probMutaPara: #(probebilidade de mutacao) ...se tiver sucesso...
                                #self.genotipoDoParasitaContatoComMutacao = int(np.random.normal(self.populacao[j].parGen,5))
                                self.genotipoDoParasitaContatoComMutacao = rd.randint(1,1000) #...o genotipo do parasita que sera recebido sofre mutacao...
                                if (self.genotipoDoParasitaContatoComMutacao not in self.vetorDeParGen) and (self.genotipoDoParasitaContatoComMutacao != self.populacao[i].parGen) and (self.genotipoDoParasitaContatoComMutacao > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                    self.populacao[j].parGen = self.genotipoDoParasitaContatoComMutacao #... e, se for dferente,  some a cepa do parasita residente...
                        self.vetorDeParGen.extend([self.populacao[j].parGen])
                        self.vetorDeParSp.extend([self.populacao[i].parSp])

    def infeccao2(self):
    ##modela um individuo nao infectado interagindo (aleatoriamente) com outros em seu campo de contato##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].parasitado == 0):
                self.contatoInfeccioso = rd.sample(range(len(self.populacao)),self.NumeroDeContatos) #...sorteie um outro individuo na populacao...
                for j in self.contatoInfeccioso:
                    if self.populacao[j].parasitado == 1:
                        self.populacao[j].contagemInfectados+=1 #coletando dados para numero de infeccoes/infectado
                        self.populacao[i].parasitado = 1
                        self.populacao[i].parGen = self.populacao[j].parGen 
                        self.moeda = rd.random() #Mutacao: jogue uma 'modeda'...
                        if self.moeda <= self.probMutaPara: #(probebilidade de mutacao) ...se tiver sucesso...
                            #self.genotipoDoParasitaContatoComMutacao = int(np.random.normal(self.populacao[j].parGen,5))
                            self.genotipoDoParasitaContatoComMutacao = rd.randint(1,1000) #...o genotipo do parasita que sera recebido sofre mutacao...
                            if (self.genotipoDoParasitaContatoComMutacao not in self.vetorDeParGen) and (self.genotipoDoParasitaContatoComMutacao > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                self.populacao[i].parGen = self.genotipoDoParasitaContatoComMutacao #... e, se for dferente,  some a cepa do parasita residente...
                        self.vetorDeParGen.extend([self.populacao[i].parGen])
                        self.vetorDeParSp.extend([self.populacao[i].parSp])
                        break
                    
    def infeccao3(self):
    ##modela infeccao genotipo-genotipo, em que um individuo nao infectado interage (aleatoriamente) com outros em seu campo de contato## 
        rd.shuffle(self.populacao)#embaralhando o vetor de individuos
        self.NumeroDeContatos =int(self.proporcaoDeContatos*len(self.populacao))
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].parasitado == 0):
                self.contatoInfeccioso = rd.sample(range(len(self.populacao)),self.NumeroDeContatos) #...sorteie um outro individuo na populacao...
                for j in self.contatoInfeccioso:
                    if self.populacao[j].parasitado == 1:
                        if self.populacao[j].parGen in self.populacao[i].Gen:
                            self.populacao[i].parasitado = 1
                        else:
                            self.moeda = rd.random()
                            if self.moeda < 0.1: #probabildiade de infeccao em hospedeiro heterozigoto
                                self.populacao[i].parasitado = 1
                        if self.populacao[i].parasitado == 1:
                            self.populacao[j].contagemInfectados+=1 #coletando dados sobre infeccoes/infectado
                            self.populacao[i].parGen = self.populacao[j].parGen
                            self.moeda = rd.random() #Mutacao: jogue uma 'modeda'...
                            if self.moeda <= self.probMutaPara: #(probebilidade de mutacao) ...se tiver sucesso...
                                #self.genotipoDoParasitaContatoComMutacao = int(np.random.normal(self.populacao[j].parGen,5))
                                self.genotipoDoParasitaContatoComMutacao = rd.randint(1,1000) #...o genotipo do parasita que sera recebido sofre mutacao...
                                if (self.genotipoDoParasitaContatoComMutacao not in self.vetorDeParGen) and (self.genotipoDoParasitaContatoComMutacao > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                    self.populacao[i].parGen = self.genotipoDoParasitaContatoComMutacao #... e, se for dferente,  some a cepa do parasita residente...
                        self.vetorDeParGen.extend([self.populacao[i].parGen])
                        self.vetorDeParSp.extend([self.populacao[i].parSp])
                        break
                    
    def reproduz0(self):
    ##hospedeiros se reproduzem independentemente do status parasitario e capacidade de suporte; reproducao com linkage total##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].prenhez == 0): # and (self.populacao[i].idade <= 10):
                self.sucesso = rd.random() #...jogue uma moeda...
                if self.sucesso <= 1: #...e se obtiver sucesso...
                    self.populacao[i].contagemProle+=1 #coletando dados para numero de prole/individuo
                    self.parceiroReprodutivo = rd.randint(0,len(self.populacao)-1) #...sorteie o parceiro reprodutivo...
                    self.sexoDoParceiro = self.populacao[self.parceiroReprodutivo].sex
                    self.genotipoDoParceiro = self.populacao[self.parceiroReprodutivo].Gen #..pegue um gameta do parceiro reprodutivo sorteado...
                    self.quemsou = self.populacao[i].Sp #...veja qual a especie do organismo i...
                    self.meuGenotipo = self.populacao[i].Gen #...pegue um gameta...
                    self.meuSexo = self.populacao[i].sex
                    if (self.populacao[i].sex != self.populacao[self.parceiroReprodutivo].sex) and (self.populacao[self.parceiroReprodutivo].prenhez == 0):                    
                        self.ind = organismos(self.quemsou,rd.choice([self.meuGenotipo,self.genotipoDoParceiro])) #...crie um novo organismo...
                        if self.sexoDoParceiro == 'F': 
                            self.populacao[self.parceiroReprodutivo].prenhez = 1
                        else: 
                            self.populacao[i].prenhez = 1
                            
                        self.mutacao = rd.random() #para mutacao, jogue uma modeda...
                        if self.mutacao <= self.probMutaHosp: #0.001: #...se tiver sucesso...
                            #self.genotipoMutante = int(np.random.normal(self.ind.Gen,5))
                            self.genotipoMutante = rd.randint(1,1000000) #...o genotipo do parasita que sera recebido sofre mutacao...
                            if (self.genotipoMutante not in self.vetorDeGen) and (self.genotipoMutante not in self.populacao[i].Gen) and (self.genotipoMutante > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                self.loci = rd.choice([0,self.numGen-1])
                                self.ind.Gen[self.loci] = self.genotipoMutante #...se for uma mutacao unica, faca o genotipo da prole.
                        self.populacao.append(self.ind) #adicionando o novo individuo a populacao.
                        self.vetorDeGen.extend(self.ind.Gen)

    def reproduz1(self):
    ##hospedeiros infectados podem nao se reproduzir (razao: trade-off ativacao imunologica X reproducao); reproducao com linkage total##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].prenhez == 0): # and (self.populacao[i].idade <= 10):
                if (self.populacao[i].parasitado == 0):
                    self.probRepro = 1 #se nao estiver parasitado, se o individuo se reproduz
                else:
                    self.probRepro = 0.5 #se estiver parasitado, pode nao reproduzir
                self.sucesso = rd.random() #...jogue uma moeda...
                if self.sucesso <= self.probRepro: #...e se obtiver sucesso...
                    self.populacao[i].contagemProle+=1 #coletando dados para numero de prole/individuo
                    self.parceiroReprodutivo = rd.randint(0,len(self.populacao)-1) #...sorteie o parceiro reprodutivo...
                    self.sexoDoParceiro = self.populacao[self.parceiroReprodutivo].sex
                    self.genotipoDoParceiro = self.populacao[self.parceiroReprodutivo].Gen #..pegue o parceiro reprodutivo sorteado...
                    self.quemsou = self.populacao[i].Sp #...veja qual a especie do organismo i...
                    self.meuGenotipo = self.populacao[i].Gen #...veja qual e seu genotipo...
                    self.meuSexo = self.populacao[i].sex
                    if (self.populacao[i].sex != self.populacao[self.parceiroReprodutivo].sex) and (self.populacao[self.parceiroReprodutivo].prenhez == 0):                    
                        self.ind = organismos(self.quemsou,rd.choice([self.meuGenotipo,self.genotipoDoParceiro])) #...crie um novo organismo...
                        if self.sexoDoParceiro == 'F': #deixando a femea em estado de prenhez
                            self.populacao[self.parceiroReprodutivo].prenhez = 1 #
                        else: 
                            self.populacao[i].prenhez = 1
                            
                        self.mutacao = rd.random() #para mutacao, jogue uma modeda...
                        if self.mutacao <= self.probMutaHosp: #0.001: #...se tiver sucesso...
                            #self.genotipoMutante = int(np.random.normal(self.ind.Gen,5))
                            self.genotipoMutante = rd.randint(1,1000000) #...o genotipo do parasita que sera recebido sofre mutacao...
                            if (self.genotipoMutante not in self.vetorDeGen) and (self.genotipoMutante not in self.populacao[i].Gen) and (self.genotipoMutante > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                self.loci = rd.choice([0,self.numGen-1])
                                self.ind.Gen[self.loci] = self.genotipoMutante #...se for uma mutacao unica, faca o genotipo da prole.
                        self.populacao.append(self.ind) #adicionando o novo individuo a populacao.
                        self.vetorDeGen.extend(self.ind.Gen) #adicionando informacao genetica ao vetor

    def reproduz2(self):
    ##hospedeiros se reproduzem independentemente do status parasitario e capacidade de suporte; reproducao sem linkage##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].prenhez == 0): # and (self.populacao[i].idade <= 10):
                self.sucesso = rd.random() #...jogue uma moeda...
                if self.sucesso <= 1: #...e se obtiver sucesso...
                    self.populacao[i].contagemProle+=1 #coletando dados para numero de prole/individuo
                    self.parceiroReprodutivo = rd.randint(0,len(self.populacao)-1) #...sorteie o parceiro reprodutivo...
                    self.sexoDoParceiro = self.populacao[self.parceiroReprodutivo].sex
                    self.genotipoDoParceiro = self.populacao[self.parceiroReprodutivo].Gen #..pegue um gameta do parceiro reprodutivo sorteado...
                    self.quemsou = self.populacao[i].Sp #...veja qual a especie do organismo i...
                    self.meuGenotipo = self.populacao[i].Gen #...pegue um gameta...
                    self.meuSexo = self.populacao[i].sex
                    if (self.populacao[i].sex != self.populacao[self.parceiroReprodutivo].sex) and (self.populacao[self.parceiroReprodutivo].prenhez == 0):
                        #pegando alelos sem linkage
                        self.novoGenoma = []
                        for k in range(self.numGen):
                            self.novoGenoma.extend([rd.choice([self.meuGenotipo[k],self.genotipoDoParceiro[k]])])
                            
                        self.ind = organismos(self.quemsou,self.novoGenoma) #...crie um novo organismo...
                        if self.sexoDoParceiro == 'F': 
                            self.populacao[self.parceiroReprodutivo].prenhez = 1
                        else: 
                            self.populacao[i].prenhez = 1
                            
                        self.mutacao = rd.random() #para mutacao, jogue uma modeda...
                        if self.mutacao <= self.probMutaHosp: #0.001: #...se tiver sucesso...
                            #self.genotipoMutante = int(np.random.normal(self.ind.Gen,5))
                            self.genotipoMutante = rd.randint(1,1000000) #...o genotipo do parasita que sera recebido sofre mutacao...
                            if (self.genotipoMutante not in self.vetorDeGen) and (self.genotipoMutante not in self.populacao[i].Gen) and (self.genotipoMutante > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                self.loci = rd.choice([0,self.numGen-1])
                                self.ind.Gen[self.loci] = self.genotipoMutante #...se for uma mutacao unica, faca o genotipo da prole.
                        self.populacao.append(self.ind) #adicionando o novo individuo a populacao.
                        self.vetorDeGen.extend(self.ind.Gen)

    def reproduz3(self):
    ##hospedeiros infectados podem nao se reproduzir (razao: trade-off ativacao imunologica X reproducao); reproducao sem linkage##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if (self.populacao[i].statusVida == 1) and (self.populacao[i].prenhez == 0): # and (self.populacao[i].idade <= 10):
                if (self.populacao[i].parasitado == 0):
                    self.probRepro = 1 #se nao estiver parasitado, se o individuo se reproduz
                else:
                    self.probRepro = 0.5 #se estiver parasitado, pode nao reproduzir
                self.sucesso = rd.random() #...jogue uma moeda...
                if self.sucesso <= self.probRepro: #...e se obtiver sucesso...
                    self.populacao[i].contagemProle+=1 #coletando dados para numero de prole/individuo
                    self.parceiroReprodutivo = rd.randint(0,len(self.populacao)-1) #...sorteie o parceiro reprodutivo...
                    self.sexoDoParceiro = self.populacao[self.parceiroReprodutivo].sex
                    self.genotipoDoParceiro = self.populacao[self.parceiroReprodutivo].Gen #..pegue o parceiro reprodutivo sorteado...
                    self.quemsou = self.populacao[i].Sp #...veja qual a especie do organismo i...
                    self.meuGenotipo = self.populacao[i].Gen #...veja qual e seu genotipo...
                    self.meuSexo = self.populacao[i].sex
                    if (self.populacao[i].sex != self.populacao[self.parceiroReprodutivo].sex) and (self.populacao[self.parceiroReprodutivo].prenhez == 0):
                        #pegando alelos sem linkage
                        self.novoGenoma = []
                        for k in range(self.numGen):
                            self.novoGenoma.extend([rd.choice([self.meuGenotipo[k],self.genotipoDoParceiro[k]])])

                        self.ind = organismos(self.quemsou,self.novoGenoma) #criando um novo organismo
                        if self.sexoDoParceiro == 'F': #deixando a femea em estado de prenhez
                            self.populacao[self.parceiroReprodutivo].prenhez = 1 #
                        else: 
                            self.populacao[i].prenhez = 1
                            
                        self.mutacao = rd.random() #para mutacao, jogue uma modeda...
                        if self.mutacao <= self.probMutaHosp: #0.001: #...se tiver sucesso...
                            #self.genotipoMutante = int(np.random.normal(self.ind.Gen,5))
                            self.genotipoMutante = rd.randint(1,1000000) #...o genotipo do parasita que sera recebido sofre mutacao...
                            if (self.genotipoMutante not in self.vetorDeGen) and (self.genotipoMutante not in self.populacao[i].Gen) and (self.genotipoMutante > 0): #...compare o genotipo do parasita novo com o do residente e com os exitentes no ambiente...
                                self.loci = rd.choice([0,self.numGen-1])
                                self.ind.Gen[self.loci] = self.genotipoMutante #...se for uma mutacao unica, faca o genotipo da prole.
                        self.populacao.append(self.ind) #adicionando o novo individuo a populacao.
                        self.vetorDeGen.extend(self.ind.Gen) #adicionando informacao genetica ao vetor
                        
    def morre0(self):
    ##hospedeiros morrem apenas em funcao da capacidade de suporte##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if self.populacao[i].statusVida == 1:
                if self.populacao[i].idade > 10:
                    self.populacao[i].statusVida = 0
                #
                self.numeroDeVivos = len([x for x in self.populacao if x.statusVida == 1])            
#                self.funcaoMorte = self.numeroDeVivos*self.K**-1 #funcao da dependencia de densidade

                if self.numeroDeVivos >= self.K:
                    self.funcaoMorte = 1
                else:
                    self.funcaoMorte = 0.1
                #
                self.moeda = rd.random() #jogue uma modeda...
                if self.moeda < self.funcaoMorte:
                    self.populacao[i].statusVida = 0
                #
                if self.populacao[i].statusVida == 0:
                    self.contagemProle.append(self.populacao[i].contagemProle)
                    self.contagemVida.append(self.populacao[i].idade)
                    self.contagemInfectados.append(self.populacao[i].contagemInfectados)

    def morre1(self): ##NAO USAR ESTA FUNCAO QUANDO TRABALHAR COM EXPLICITAMENTE COM ALELOS
        ##hospedeiros morrem em funcao da capacidade de suporte e da virulecia parasitaria##
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if self.populacao[i].statusVida == 1:
                if self.populacao[i].idade > 10:
                    self.populacao[i].statusVida = 0
                #
                self.numeroDeVivos = len([x for x in self.populacao if x.statusVida == 1])            
#                self.funcaoMorte = self.numeroDeVivos*self.K**-1 #funcao da dependencia de densidade
                if self.numeroDeVivos >= self.K:
                    self.funcaoMorte = 1
                else:
                    self.funcaoMorte = 0.1
                #
                self.eventoMorre = rd.random() #jogue uma modeda...
                if self.populacao[i].parasitado == 1:
                    self.funcaoMorteVirulencia = self.funcaoMorte * (1 + self.populacao[i].parGen*1000000**-1) #aumento pela virulencia corresponde ao numero do genPar (aqui, o numero atribuido aos genotipo tbm significa a forca da virulencia - usei de 1 a 1000000 genes)
                    if self.eventoMorre < self.funcaoMorteVirulencia:
                        self.populacao[i].statusVida = 0
                else:
                    if self.eventoMorre <= self.funcaoMorte:
                        self.populacao[i].statusVida = 0
                #
                if self.populacao[i].statusVida == 0:
                    self.contagemProle = self.populacao[i].contagemProle
                    self.contagemVida = self.populacao[i].idade
                    self.contagemInfectados = self.populacao[i].contagemInfectados

    def morre2(self,parametroA):
    ##hospedeiros morrem apenas em funcao da capacidade de suporte##
    ##diminui a capacidade de superte (K) ao longo do tempo##         
        rd.shuffle(self.populacao) #embaralhando o vetor de individuos
        self.tempoT = parametroA #tempo atual
        if self.tempoT < self.tempoTcritico:
            self.funcaoDegradacaoK = self.K
        else:
            self.funcaoDegradacaoK = self.K - self.tempoT*60 #parametro de inclinacao da reta igual a 1 (para K=1000 e tempo max 1000)
        #
        for i in range(len(self.populacao)): #para cada um dos organismos na populacao...
            if self.populacao[i].statusVida == 1:
                if self.populacao[i].idade > 10:
                    self.populacao[i].statusVida = 0
                #
                self.numeroDeVivos = len([x for x in self.populacao if x.statusVida == 1])            
                self.funcaoMorte = self.numeroDeVivos * self.funcaoDegradacaoK ** -1 #funcao da dependencia de densidade (com degradacao)
                self.moeda = rd.random() #jogue uma modeda...
                if self.moeda <= self.funcaoMorte:
                    self.populacao[i].statusVida = 0
                #
                if self.populacao[i].statusVida == 0:
                    self.contagemProle.append(self.populacao[i].contagemProle)
                    self.contagemVida.append(self.populacao[i].idade)
                    self.contagemInfectados.append(self.populacao[i].contagemInfectados)
                    
    def atualizaPop(self):
        self.populacao = [x for x in self.populacao if x.statusVida == 1] #contando e regitrando o numero de organismos vivos na populacao
        # for i in range(self.numSp): #para cada especie...
        #     for j in range(len(self.vetorDeGen)): #...e para cada um de seus genotipos... (numGen????)
        #         self.contagem = len([x for x in self.populacao if (x.Gen == j+1) and (x.Sp == i+1)]) #...conte quantos existem...
        #         self.abundancia.append(self.contagem) #...e registre na variavel 'abundancia'.
        #
        self.novoVetorDeParGen = []
        self.novoVetorDeGen = []
        for i in range(len(self.populacao)):
            #retirando a prenhez
            if self.populacao[i].prenhez == 1:
                self.populacao[i].prenhez = 0
            #aumentando a idade
            self.populacao[i].idade+=1
            #curando infeccao ao longo do tempo
            if self.populacao[i].tempoInfectado > 3:
                self.populacao[i].tempoInfectado = 0
            #atualizando vetor de alelos
            self.novoVetorDeGen.extend(self.populacao[i].Gen)
            if self.populacao[i].parGen != []:
                self.novoVetorDeParGen.extend([self.populacao[i].parGen])
        self.vetorDeGen = self.novoVetorDeGen
        self.vetorDeParGen = self.novoVetorDeParGen
        #abundancia hospedeiro
        self.abundancia.append(len(self.populacao)) ##Contagem simples...
        #riqueza de alelos na populacao de hospedeiros
        self.riquezaGenes.extend([len(set(self.vetorDeGen))])
        #diversidade de alelos
        if self.vetorDeGen == []:
            self.diversidadeGenes.extend([0])
        else:
            self.vetorHelper = []
            self.vetorContagens = collections.Counter(self.vetorDeGen)            
            for i in self.vetorContagens:
                self.vetorHelper.append( (self.vetorContagens[i]*len(self.vetorDeGen)**-1) * np.log(self.vetorContagens[i]*len(self.vetorDeGen)**-1) )
                
            self.shannon = -1*sum(self.vetorHelper)
            self.diversidadeGenes.extend([self.shannon]) #com indice de shannon
            #self.diversidadeGenes.extend( [max(collections.Counter(self.vetorDeGen).values())*len(self.vetorDeGen)**-1] )

#        for i in range(len(self.vetorDeParGen)): #para cada genotipo de parasitas...
        #abundancia de hospedeiros infectados
        self.contagemPar = len([x for x in self.populacao if (x.parasitado == 1 )]) #...conte quantos existem...
        self.abundanciaPar.append(self.contagemPar)
        #self.abundanciaArrayPar = np.array(self.abundanciaPar) #transformando em 'array'
        #self.abundanciaSplitPar = np.split(self.abundanciaArrayPar,len(self.abundanciaPar)/(self.numParSp*self.numParGen)) #dividindo o array
        #self.abundanciaDadosPar = pd.DataFrame(self.abundanciaSplitPar) #transformando em 'array' em 'dataframe'
        #riqueza de alelos dos parasitas
        self.riquezaGenesPar.extend([len(set(self.vetorDeParGen))])
        #self.riquezaSpPar.append( len(set(self.vetorDeParSp) ) )
        #diversidade de alelos nos parasitas
        if self.vetorDeParGen == []:
            self.diversidadeGenesPar.extend([0])
        else:
            self.vetorHelper = []
            self.vetorContagens = collections.Counter(self.vetorDeParGen)
            for i in self.vetorContagens:
                self.vetorHelper.append( (self.vetorContagens[i]*len(self.vetorDeParGen)**-1) * np.log(self.vetorContagens[i]*len(self.vetorDeParGen)**-1) )
            self.shannon = -1*sum(self.vetorHelper)
            self.diversidadeGenesPar.extend([self.shannon]) #caom indice de shannon
            #self.diversidadeGenesPar.extend( [max(collections.Counter(self.vetorDeParGen).values())*len(self.vetorDeParGen)**-1] ) #com indice de Breger-Parker

        ###Dados geneticos completos
        self.dadosGenAtualizados.append(self.vetorDeGen)
        self.dadosGenParAtualizados.append(self.vetorDeParGen)

class start:
    def __init__(self,n,g,s,nPar,gPar,sPar,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK):
        self.tempo = 500
        self.minhaPop = ambiente(n,g,s,nPar,gPar,sPar,K,Ncontatos,HospMuta,ParaMuta,tempoCriticoK)
        self.minhaPop.criaPop()
        self.minhaPop.criaPopPar() #retirar se utilizar a condicao na funcao roda()
        self.minhaPop.atualizaPop()
            
    def roda(self):
        for t in range(self.tempo):
            #if t > 500:
            #    self.minhaPop.criaPopPar()
            self.minhaPop.morre0() #morre2(t) #LEMBRE-SE: 'morre2()' depende do tempo.
            self.minhaPop.infeccao1()
            self.minhaPop.reproduz3() #reproduz0 e 1 = com linkage total; reproduz2 e 3 = sem linkage algum
            self.minhaPop.atualizaPop()
            if len(self.minhaPop.populacao) <= 0:
                break
        self.res = self.minhaPop.abundancia
        self.resPar = self.minhaPop.abundanciaPar
        self.resRiqGen = self.minhaPop.riquezaGenes
        self.resDivGen = self.minhaPop.diversidadeGenes
        self.resRiqGenPar = self.minhaPop.riquezaGenesPar
        self.resDivGenPar = self.minhaPop.diversidadeGenesPar
        self.dadosGen = self.minhaPop.dadosGenAtualizados
        self.dadosGenPar = self.minhaPop.dadosGenParAtualizados
        self.dadosProle = self.minhaPop.contagemProle
        self.dadosVida = self.minhaPop.contagemVida
        self.dadosInfeccoesRealizadas = self.minhaPop.contagemInfectados

print 'Modulo do modelo concluido!'
