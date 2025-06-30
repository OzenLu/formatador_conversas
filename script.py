import time
import re
import pandas as pd

inicio = time.time()

# Função para lidar com quebra de linhas nas mensagens
def unir_mensagens(lista):
    
    print("Organizando quebra de linhas.")
    
    dados = lista
    contador = 0
    ultima_data = 0
    lista_exclusao = []
    
    for elemento in dados:
        linha = elemento[0]

        match = regex_padrao_completo.search(linha)

        if match:
            ultima_data = contador
        else:
            lista_exclusao.append(contador)
            mensagem = dados[ultima_data] + elemento
            auxiliar = " "
            auxiliar = auxiliar.join(mensagem)

            dados[ultima_data][0] = auxiliar
        
        contador += 1
    
    for x in sorted(lista_exclusao, reverse=True):
        del dados[x]

    return dados

# Padrão regex para separar data, hora, usuário e mensagem
regex_padrao_completo = re.compile(r"^(\d{2}\/\d{2}\/\d{4})\s(\d{2}:\d{2})\s*(?:-\s*)?(.*?):\s*(.*)")

# Abrindo o arquivo original de conversas
with open("ConversadoWhatsApp.txt", "r", encoding="utf_8") as conversa:
    
    print("Abrindo arquivo de origem.")

    linhas = conversa.readlines()
    dados = [linha.strip().split('\n') for linha in linhas]
    dados = unir_mensagens(dados)

print("Organizando o arquivo em colunas.")

datas = []
horas = []
nomes = []
mensagens = []

# Dividindo cada mensagem em partes e salvando dentro de listas
for x in dados:
    linha = x[0]

    match = regex_padrao_completo.search(linha)

    if match:
        data = match.group(1) 
        hora = match.group(2) 
        nome = match.group(3)
        mensagem = match.group(4)
   
        datas.append(data)
        horas.append(hora)
        nomes.append(nome)
        mensagens.append(mensagem.strip())
    else:
        print(f"Não deu match: {linha}")

# União das listas para criar as colunas
zippados = zip(datas, horas, nomes, mensagens)
conversa_zipada = list(zippados)

colunas = ["data", "hora", "nome", "mensagens"]

df = pd.DataFrame(columns=colunas, data=conversa_zipada)
df['data'] = pd.to_datetime(df['data'], dayfirst=True)
df['hora'] = pd.to_datetime(df['hora'], format='%H:%M').dt.time

# Criando novo arquivo csv para armazenar as mensagens no formato de colunas
try:
    df.to_csv("ConversaDoWhatsAppFormatada.csv", index=False)
    print("Arquivo criado com sucesso.")
except:
    print("Não foi possível criar o arquivo")

fim = time.time()
tempo_total = fim - inicio

print(f"o tempo total de execução foi de {tempo_total: .2f} segundos")