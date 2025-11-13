
import pickle
import time

''' Funcao de Leitura de Arquivos '''
def ler_dados(arquivo):
    with open(arquivo,"rb") as f:
        tipos = pickle.load(f)
        pontos = pickle.load(f)
        alunos = pickle.load(f)
    return tipos,pontos, alunos

''' Funcao para Saída dos Arquivos '''
def gerar_saida(lista_ordenada, alunos, pontos, qtd_tipos, arquivo_saida):
    with open(arquivo_saida, 'w') as f:
        mat_anterior = None
        for mat, ind in lista_ordenada:
            if mat_anterior != mat:
                nome = alunos[mat][0]
                total_pontos = calcular_pontos_aluno(mat, alunos, pontos, qtd_tipos)
                f.write(f"{nome} ({mat}) : {total_pontos} pontos \n")
                mat_anterior = mat
        
            tipo, codigo, unidades = alunos[mat][1][ind]
            nome_atividade, pontos_unidade, _ = pontos[(tipo, codigo)]
            pontos_atividade = unidades * pontos_unidade

            f.write(f"{tipo}.{codigo} {nome_atividade} : {unidades}x{pontos_unidade}={pontos_atividade}\n")

''' Funcao de Criacao da lista de tuplas de matricula e cadastro de atividades '''
def criar_lista_atividades(alunos):
    l = []
    for mat in alunos:
        atividades = alunos[mat][1]
        for i in range(len(atividades)):
            l.append((mat,i))
    return l

''' Funcao de Calculo'''
def calcular_pontos_aluno(matricula,alunos,pontos,qtd_tipos):
    atividades = alunos[matricula][1]

    pontos_tipo = [0] * (qtd_tipos + 1)
    for tipo,codigo,unidades in atividades:
        pontos_unidade = pontos[(tipo,codigo)][1]
        pontos_atividade = unidades*pontos_unidade
        pontos_tipo[tipo] += pontos_atividade

    total = sum(min(pts,10) for pts in pontos_tipo[1:])
    return min(total,15)

def quick_sort(lista,alunos,pontos,qtd_tipos):
    if len(lista) <= 1:
        return lista
    
    quick_sort_rec(lista,0,len(lista)-1,alunos,pontos,qtd_tipos)
    return lista

def quick_sort_rec(lista,inicio,fim,alunos,pontos,qtd_tipos):
    if inicio < fim:
        indice_pivo = particionar(lista, inicio, fim, alunos, pontos, qtd_tipos)
        quick_sort_rec(lista, inicio, indice_pivo-1, alunos, pontos, qtd_tipos)
        quick_sort_rec(lista, indice_pivo+1, fim, alunos, pontos, qtd_tipos)

def particionar(lista,inicio,fim,alunos,pontos,qtd_tipos):
    meio = (inicio+fim)//2
    lista[meio], lista[fim] = lista[fim], lista[meio]
    pivo = lista[fim]
    i = inicio - 1
    for j in range(inicio,fim):
        if comparar(lista[j],pivo,alunos,pontos,qtd_tipos) <= 0:
            i += 1
            lista[i], lista[j] = lista[j], lista[i]
    
    lista[i+1], lista[fim] = lista[fim], lista[i+1]

    return i+1

def comparar(tupla1,tupla2,alunos,pontos,qtd_tipos):
    mat1, ind1 = tupla1
    mat2, ind2 = tupla2

    pts1 = calcular_pontos_aluno(mat1, alunos, pontos, qtd_tipos)
    pts2 = calcular_pontos_aluno(mat2, alunos, pontos, qtd_tipos)

    if pts1 != pts2:
        return -1 if pts1 > pts2 else 1
    
    nome1 = alunos[mat1][0]
    nome2 = alunos[mat2][0]

    if nome1 != nome2:
        return -1 if nome1 < nome2 else 1
    
    if mat1 != mat2:
        return -1 if mat1 < mat2 else 1
    
    atividades1 = alunos[mat1][1][ind1]
    atividades2 = alunos[mat1][1][ind2]

    tipo1, cod1, _ = atividades1
    tipo2, cod2, _ = atividades2

    if tipo1 != tipo2:
        return -1 if tipo1 < tipo2 else 1
    
    if cod1 != cod2:
        return -1 if cod1 < cod2 else 1
    
    return 0


''' ============ Merge Sort ================== '''

def merge(esq, dir, alunos, pontos, qtd_tipos):
    resultado = []
    i = j = 0
    
    while i < len(esq) and j < len(dir):
        if comparar(esq[i], dir[j], alunos, pontos, qtd_tipos) <= 0:
            resultado.append(esq[i])
            i += 1
        else:
            resultado.append(dir[j])
            j += 1
    
    resultado.extend(esq[i:])
    
    resultado.extend(dir[j:])
    
    return resultado


def merge_sort(lista, alunos, pontos, qtd_tipos):
    if len(lista) <= 1:
        return lista
    
    meio = len(lista) // 2
    
    esquerda = merge_sort(lista[:meio], alunos, pontos, qtd_tipos)
    direita = merge_sort(lista[meio:], alunos, pontos, qtd_tipos)
    
    return merge(esquerda, direita, alunos, pontos, qtd_tipos)

''' ============ Funcao Principal ============ '''
def main():

    tipos,pontos,alunos  = ler_dados("entrada4.bin")
    
    qtd_tipos = len(tipos)
    
    lista = criar_lista_atividades(alunos)
    lista_ordenada = merge_sort(lista, alunos, pontos, qtd_tipos)

    gerar_saida(lista_ordenada, alunos, pontos, qtd_tipos, 'saida4.txt')

main()