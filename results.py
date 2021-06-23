import sys
import re

def taxa_entrada(perda, prob, tempo):
    return (perda/prob)/tempo


def populacao_media(probs): # N
    aux = 0
    for i in range(1,len(probs)):
        aux += probs[i] * i
    return aux

def vazao(probs, taxa_saida): #D
    aux = 0
    for i in range(1,len(probs)):
        aux += probs[i] * taxa_saida[i-1]
    return aux

def taxa_saida(k, c, mi): 
    mis = []
    for i in range(1,k+1):
        mis.append(min(c,i)*mi)
    return mis

def mises(k,c):
    mis = []
    for i in range(1,k):
        mis.append(min(c,i))
    return mis

def utilizacao(mises, c, probs): #U
    aux = 0
    for i in range(1, len(probs)):
        aux += probs[i] *(mises[i-1]/c)
    return aux

def tempo_resposta(n, d): #W
    return n/d

#(probs, perda, tempo, tax_entrada, tax_saida, pop_media, vaz, ult, temp_resposta)
def to_string(dic : dict) -> str:
    ret = ""
    for fila in dic:
        ret += "Fila: "+fila+"\n"
        ret += "Probabilidades: "+str(dic[fila][0])+"\n"
        ret += "Perdas: "+str(dic[fila][1])+"\n"
        ret += "Tempo Total: "+str(dic[fila][2])+"\n"
        ret += "Taxa de Entrada: "+str(dic[fila][3])+"\n"
        ret += "Taxa de Saida: "+str(dic[fila][4])+"\n"
        ret += "População Média: "+str(dic[fila][5])+"\n"
        ret += "Vazão: "+str(dic[fila][8])+"\n"
        ret += "Ultilização: "+str(dic[fila][7])+"\n"
        ret += "Tempo de Resposta: "+str(dic[fila][8])+"\n"
        ret += "\n"
    return ret


#          0        1       2      3
#python result.py 
filas = []

probs = []
var_mises = []
k, c, perda = (0,0,0) 
tempo, mi = (0.0, 0.0)
service_average = 0

filas_dict = {}
with open("resultados.txt") as arq:
    linhas  = arq.read()
    _, *rest = re.split(r"#(?:)", linhas)
    filas = [r.split("\n") for r in rest]

    nome  = ""
    for fila in filas:
        first = True
        probs = []
        var_mises = []
        k, c, perda = (0,0,0) 
        tempo, mi = (0.0, 0.0)
        service_average = 0

        for i in fila:
            if i=="":
                continue
            if first:
                nome = i
                first = False
                continue
            i = i.replace("\n","")
            if "losses:" in i:
                i = i.replace("losses:","")
                perda = int(i)
            elif "service:" in i:
                i = i.replace("service:","")
                linha_aux = i.split(" ")
                service_average = (float(linha_aux[0]) + float(linha_aux[1]))/2
            elif "servers:" in i:
                i = i.replace("servers:","")
                c = int(i)
            else:
                linha = i.split(";")
                tempo += float(linha[0].replace(",","."))
                probs.append(float(linha[1].replace(",","."))/100)

        k = len(probs)
        var_mises = mises(k,c)
        mi = var_mises[0]
        #probs, k, c, service_average, perda, tempo, mi

        tax_entrada = taxa_entrada(perda, probs[-1],tempo)
        tax_saida = taxa_saida(k, c, mi)

        pop_media = populacao_media(probs)
        vaz = vazao(probs, tax_saida)
        ult = utilizacao(var_mises, c, probs)
        temp_resposta = tempo_resposta(pop_media,vaz)

        
        filas_dict.update({nome:(probs, perda, tempo, tax_entrada, tax_saida, pop_media, vaz, ult, temp_resposta)})

print(to_string(filas_dict))