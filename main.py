import random
import math
import csv
import copy
import matplotlib.pyplot as plt

#LISTA COM OS NOMES DAS CIDADES
cidades_nome = ["Santa Paula","Campos","Riacho de Fevereiro","Algas","Além-do-Mar","Guardião","Foz da Água Quente","Leão","Granada","Lagos","Ponte-do-Sol","Porto","Limões"]

#cidade1,cidade2,custo da viagem (h),custo da viagem($)
with open('custo-cidades.csv', newline='') as f:
  reader = csv.reader(f)
  cidades = list(reader)

#item,peso (kg),tempo de roubo (h),valor($),cidade
with open('info-itens.csv', newline='') as f:
  reader = csv.reader(f)
  itens = list(reader)

#FUNÇÕES
def calcular(cidAnterior, cidAtual):
  tempo_roubos = 0  # tempo dos roubos
  valor_roubo = 0   # valor arrecadado dos roubos
  peso_roubos = 0   # peso da bolsa com os itens

  tempo_viagens = 0 # tempo das viagens
  custo_viagens = 0 # custo das viagens

  #Usando um loop for dentro da lista de itens, onde para cada item, cujo o elemento de indice 4 é igual a cidade atual, somamos o peso do     item, o tempo do roubo e o valor do item
  for item in itens:
    if item[4] == cidAtual:
      peso_roubos += int(item[1])
      tempo_roubos += int(item[2])
      valor_roubo += int(item[3])

  #Usando outro loop for, para cada cidade que liga a cidade anterior à cidade atual, somamos o tempo de viagem e o custo da viagem.
  for cidade in cidades:
    if (cidade[0] == cidAnterior and cidade[1] == cidAtual) or (cidade[1] == cidAnterior and cidade[0] == cidAtual):
      tempo_viagens += int(cidade[2])
      custo_viagens += int(cidade[3])

  #Retornamos: 
  #-O peso total dos itens roubados da cidade atual
  #-O tempo total gasto entre os roubos e viagens
  #-O valor total subtraindo o valor do roubo pelo custo das viagens
  return peso_roubos, (tempo_roubos + tempo_viagens), (valor_roubo - custo_viagens)

def inicializacao():
    individuo = ['Escondidos']  # obrigatoriamente é a primeira cidade
    limite_tempo = 72           # limite de tempo em horas
    limite_peso = 20            # limite de peso da bolsa em Kg
    valor = 0                   # valor total arrecadado

    #Loop while que irá executar enquanto ainda tivermos tempo disponivel para deslocamento entre cidades, ou seja, enquanto o tempo que tivermos disponivel for maior que 9 Horas, que é o maior tempo possivel de viagem ate Escondidos.
    while limite_tempo > 9:
        #Cria uma lista de possibilidades de cidades que ainda não foram visitadas
        possibilidades_validas = [item for item in cidades_nome if item not in individuo]

        if not possibilidades_validas:
            break

        #Define a cidade atual como a última cidade visitada na rota e escolhe aleatoriamente outra cidade dentro da lista de cidades validas para visita
        cidade_atual = individuo[-1]
        prox_cidade = random.choice(possibilidades_validas)

        #Calcula o peso, tempo e valor da cidade atual até a próxima cidade e depois adiciona e remove os valores correspondentes para os calculos totais
        peso, tempo, valor_roubo = calcular(cidade_atual, prox_cidade)
        valor += valor_roubo
        limite_peso -= peso
        limite_tempo -= tempo

        #Se ultrapassar o limite de peso ou tempo da rota, remove a última cidade visitada e encerra o loop
        if limite_peso < 0 or limite_tempo < 0:
            individuo.pop() 
            break
          
        #Adiciona a proxima cidade na rota
        individuo.append(prox_cidade)

        #Se a proxima cidade for Escondidos, sabemos que será a ultima então encerramos o loop
        if prox_cidade == 'Escondidos':
            break
          
    #Adicionamos Escondidos no final da rota e retornamos o individuo(rota) gerado(a)
    individuo.append('Escondidos')
    return individuo

def funcao_fitness(individuo):
    fit = 0
    peso_limite = 20    # peso máximo da bolsa com os itens
    tempo_limite = 72   # tempo restante da viagem

    peso_atual = 0      # peso da bolsa com os itens atuais
    tempo_atual = 0     # tempo gasto com a rota atual
    valor_atual = 0     # valor gasto e obtido com as viagens e roubos

    # Percorre a lista de itens do indivíduo e calcula o peso, tempo e valor de cada item
    for i in range(0, len(individuo)-1):
        peso, tempo, valor = calcular(individuo[i], individuo[i+1])
        peso_atual += peso
        tempo_atual += tempo
        valor_atual += valor

    # Calcula o peso e tempo restantes depois de adicionar os itens do indivíduo
    peso_limite -= peso_atual
    tempo_limite -= tempo_atual


    #Atribuição de valores de fitness para mochila em cada caso
  
    # Verifica se o peso ultrapassou o limite máximo da bolsa
    if (peso_limite <= -5):
        fit -= 10000
    # Verifica se o peso ficou entre -5kg e 0kg (limite máximo - 5kg)
    elif (peso_limite < 0 and peso_limite > -5):
        # Peso ultrapassou o limite, mas ainda está dentro da margem de tolerância
        fit -= 3000
    # Verifica se sobrou entre 0kg e 4kg de peso na bolsa
    elif (peso_limite >= 0 and peso_limite <= 4):
        fit += 1750
    # Verifica se sobrou entre 5kg e 13kg de peso na bolsa
    elif (peso_limite >= 5 and peso_limite <= 13): 
        fit += 1000

    #Atribuição de valores de fitness para o tempo em cada caso
  
    # Verifica se o tempo restante é menor ou igual a -4 horas
    if (tempo_limite <= -4):
        fit -= 20000
    # Verifica se o tempo restante é negativo
    elif (tempo_limite < 0):
        fit -= 3000
    # Verifica se sobrou entre 0 e 10 horas de tempo na viagem
    elif (tempo_limite >= 0 and tempo_limite <= 10):
        fit += 1500
    # Verifica se sobrou entre 11 e 19 horas de tempo na viagem
    elif (tempo_limite >= 11 and tempo_limite <= 19):
        fit += 1100
    # Verifica se sobrou mais de 20 horas de tempo na viagem
    elif (tempo_limite > 20):
        fit += 500

    #VALOR ARRECADADO
    fit += valor_atual

    # Retorna o valor do fitness do indivíduo
    return fit
  
def mutacao(individuo, taxa):
  # Calcula a quantidade de genes a serem mutados
  qtd_genes = math.ceil(len(individuo) * taxa)
  
  # Cria uma cópia do indivíduo original
  individuo_mutado = list(individuo)
  
  # Loop para mutar cada gene
  for _ in range(qtd_genes):
    # Cria uma lista de possibilidades que contém todas as cidades ainda não visitadas
    possibilidades = [item for item in cidades_nome if item not in individuo_mutado]
    
    # Escolhe aleatoriamente um gene a ser mutado, exceto o primeiro e o último
    gene = random.choice(range(1,len(individuo)-2))
    
    # Escolhe aleatoriamente uma nova cidade a partir da lista de possibilidades
    i = random.choice(range(0,len(possibilidades)-1))
    individuo_mutado[gene] = possibilidades[i]

  # Retorna o indivíduo mutado
  return individuo_mutado

def crossover(populacao):
  # faz uma cópia da população original
  pop = copy.deepcopy(populacao)
  # cria duas listas para armazenar as partes dos indivíduos que serão combinadas
  parte1 = []
  parte2 = []
  # cria uma lista vazia para armazenar os novos indivíduos gerados
  crossovers = []

  # separa as partes dos indivíduos que serão combinadas
  for individuo in pop:
    parte1.append(individuo[1:4])
    parte2.append(individuo[4:-1])
  
  # seleciona as partes dos indivíduos que serão combinadas
  bestParts = selecionarIndividuos(parte1 + parte2)

  # itera sobre as partes selecionadas, tentando combinar cada parte com a parte anterior e posterior
  for i in range(1, len(bestParts) - 1):
    # obtém as cidades que não estão presentes na parte anterior
    cities = [item for item in bestParts[i] if item not in bestParts[i - 1]]
    # se existem cidades para combinar, cria um novo indivíduo e o adiciona à lista de crossovers
    if cities:
      lista = bestParts[i - 1] + cities
      lista.insert(0, "Escondidos")
      lista.append("Escondidos")
      if lista not in populacao and lista not in crossovers:
        crossovers.append(lista)
    # obtém as cidades que não estão presentes na parte posterior
    cities = [item for item in bestParts[i - 1] if item not in bestParts[i]]
    # se existem cidades para combinar, cria um novo indivíduo e o adiciona à lista de crossovers
    if cities:
      lista = bestParts[i] + cities
      lista.insert(0, "Escondidos")
      lista.append("Escondidos")
      if lista not in populacao and lista not in crossovers:
        crossovers.append(lista)

  # seleciona os melhores indivíduos da lista de crossovers e retorna essa lista
  crossovers = selecionarIndividuos(crossovers)

  return crossovers

def getDados(individuo):
  peso_limite = 20 #peso da bolsa com os itens X
  tempo_limite = 72 #tempo restante da viagem
  valor_total = 0

  peso_atual = 0
  tempo_atual = 0
  valor_atual = 0

  #verifica o peso da mochila e atualiza seu limite
  #soma o tempo dos roubos
  #soma o valor arrecadado nos roubos
  for i in range(0,len(individuo)-1):
    peso, tempo, valor = calcular(individuo[i], individuo[i+1])
    peso_atual += peso
    tempo_atual += tempo
    valor_atual += valor

  peso_limite -= peso_atual
  tempo_limite -= tempo_atual
  valor_total = valor_atual

  #Exibe na tela os resultados
  print("Tamanho da rota -> ", len(individuo))
  print("Tempo restante ->", tempo_limite, "horas")
  print("Peso na bolsa restante ->", peso_limite, "kg")
  print("Valor arrecadado -> $", valor_total)

def selecionarIndividuos(listaIndividuos):
  #Ordenamos a lista de forma decrescente e retornamos os 50 melhores
  selecionados = sorted(listaIndividuos, key=funcao_fitness, reverse=True)
  return selecionados[0:50]

populacao = [inicializacao() for _ in range(0,50)] #Inicializando a população com 50 individuos
geracoes=0 #Contagem das gerações
popIgual=0 #Critério de parada
pontos_fitness=[]
geracoes_aux=[]

print("EP3-IA: ALGORITMOS GENÊTICOS: Joana Sandiego, a Ladra Viajante")

while True: 
  pontos_fitness.append(funcao_fitness(populacao[0]))
  geracoes_aux.append(geracoes)
  
  #Critério de parada: se a população for igual em 100 gerações, aparentemente o individuo não tera geração melhor
  if(popIgual == 100): break

  #Imprime os dados a cada 100 gerações
  if geracoes % 100 == 0:
    print(f'{"Geração ":^8}{str(geracoes):^4}{", Melhor Fitness: ":^11}{str(funcao_fitness(populacao[0])):^5}')

  #Seleciona a populaçãpo antiga
  populacao_antiga = copy.deepcopy(populacao)
  #Chama a função de mutação para mutar cerca de 30% dos individuos daquela população
  populacao_mutada = [mutacao(individuo, 0.3) for individuo in populacao]
  #Chama a funcao de crossover entre individuos mutados e individuos da população original
  populacao_crossover = crossover(populacao_mutada + populacao)
  #Seleciona os melhores individuos entre os originais, mutados e individuos resultantes do crossover
  populacao = selecionarIndividuos(populacao_antiga + populacao_mutada + populacao_crossover)

  #Aqui verificamos se a nova população é igual a anterior para adicionarmos 1 ao contador de gerações iguais ou zeramos
  if populacao_antiga == populacao: popIgual += 1
  else: popIgual=0

  geracoes+=1
  
#Selecionamos os melhores individuos
populacao = selecionarIndividuos(populacao)

print("\n\n~~~~~~~~ Resultados ~~~~~~~\n")
print("Melhor rota encontrada:")
print(populacao[0])
print("\nGerações ->", str(geracoes), "\nFitness ->", str(funcao_fitness(populacao[0])))
getDados(populacao[0])
fig = plt.figure()
plt.plot(geracoes_aux,pontos_fitness)
plt.title("Gerações x Pontuação de Fitness")
plt.xlabel('Gerações')
plt.ylabel('Pontuação de Fitness')
plt.savefig('grafico')  

  
