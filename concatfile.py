import csv
import sys
import pandas as pd

#inicialização com listas vazias
desmama = []
sobreano = []
todos = []


# region [leitura do arquivo desmama]
with open("Desmama_2018_ajustado_v5_final.csv", 'r') as desmama_csv_file:
    
    #DictReader cria um leitor para o arquivo. Quando DiscReader lê, ele constrói um dicionário com o que está sendo lido     
    desmama_reader = csv.DictReader(desmama_csv_file, delimiter=' ')

    #para cada linha no arquivo lido
    for line in desmama_reader:
        #alimenta a lista de desmama
        desmama.append(line)
#        
desmamaDF = pd.DataFrame(desmama)
# print(desmamaDF.loc[desmamaDF["safra"] == "2010"])
# endregion

# region [leitura do arquivo sobreano]
with open("novo_sobreano_v6_final.csv", 'r') as sobreano_csv_file:

    #DictReader cria um leitor para o arquivo. Quando DiscReader lê, ele constrói um dicionário com o que está sendo lido     
    sobreano_reader = csv.DictReader(sobreano_csv_file, delimiter=' ')

    #para cada linha no arquivo lido
    for line in sobreano_reader:
        #alimenta a lista de desmama
        sobreano.append(line)

sobreanoDF = pd.DataFrame(sobreano)
# endregion


comumDF = desmamaDF.loc[desmamaDF['REGISTRO_ANIMAL'].isin(sobreanoDF["REGISTRO_ANIMAL"])]
apenasDesmamaDF = desmamaDF.loc[~desmamaDF['REGISTRO_ANIMAL'].isin(sobreanoDF["REGISTRO_ANIMAL"])]
apenasSobreanoDF = sobreanoDF.loc[~sobreanoDF['REGISTRO_ANIMAL'].isin(desmamaDF["REGISTRO_ANIMAL"])]

header = list(desmamaDF.columns) + list(sobreanoDF.columns)[3:]

todos.append(header)
print(f"Iniciando!!!")
print()

# PERCORRE A LISTA. INTERROWS É O iterador da biblioteca 
# region [Itens em comum]
size = len(comumDF) + len(apenasDesmamaDF) + len(apenasSobreanoDF)
for idx, reg in comumDF.iterrows():
    sobreano_aux = list(sobreanoDF.loc[sobreanoDF['REGISTRO_ANIMAL'] == reg['REGISTRO_ANIMAL']].iloc[0])
    desmama_aux = list(reg)
    # print(sobreano_aux)

    del sobreano_aux[0:3]
    todos.append(desmama_aux + sobreano_aux)
    sys.stdout.write('\r'+f"{idx}/{size}")
# endregion

#region apenasDesmamaDF
size = len(apenasDesmamaDF)
for idx, reg in apenasDesmamaDF.iterrows():
    sobreano_aux = list("" for i in range(len(sobreano_aux)))
    desmama_aux = list(reg)

    todos.append(desmama_aux + sobreano_aux)
    sys.stdout.write('\r'+f"{idx}/{size}")

#endregion

# region apenasSobreano
size = len(apenasSobreanoDF)
for idx, reg in apenasSobreanoDF.iterrows():
    sobreano_aux = list(reg)
    desmama_aux = list("" for i in range(len(desmama_aux)))

    desmama_aux[0] = sobreano_aux[0]
    desmama_aux[1] = sobreano_aux[1]
    desmama_aux[2] = sobreano_aux[2]

    del sobreano_aux[0:3]
    todos.append(desmama_aux + sobreano_aux)
    sys.stdout.write('\r'+f"{idx}/{size}")
# endregion

with open('Desmama_Sobreano_final', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(todos)