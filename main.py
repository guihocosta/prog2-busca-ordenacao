
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
                f.write(f"{nome} ({mat}): {total_pontos} pontos \n")
                mat_anterior = mat
        
            tipo, codigo, unidades = alunos[mat][1][ind]
            nome_atividade, pontos_unidade, _ = pontos[(tipo, codigo)]
            pontos_atividade = unidades * pontos_unidade

            f.write(f"\t {tipo}.{codigo} {nome_atividade}: {unidades}x{pontos_unidade}={pontos_atividade}\n")

''' Funcao de Criacao da lista de tuplas de matricula e cadastro de atividades '''
def criar_lista_atividades(alunos):
    l = []
    for mat in alunos:
        atividades = alunos[mat][1]
        for i in range(len(atividades)):
            l.append((mat,i))
    return l

''' Funcao de Calculo'''
def calcular_pontos_aluno(matricula, alunos, pontos, qtd_tipos):
    atividades = alunos[matricula][1]
    total = 0
    pontos_tipo = [0] * (qtd_tipos + 1)

    for tipo,codigo,unidades in atividades:
        pontos_unidade = pontos[(tipo,codigo)][1]
        pontos_tipo[tipo] += unidades * pontos_unidade

    for i in range(1, len(pontos_tipo)):
        if pontos_tipo[i] > 10: pontos_tipo[i] = 10
        total += pontos_tipo[i]

    return 15 if total > 15 else total

def comparar(tupla1,tupla2,alunos,pontos,qtd_tipos):
    mat1, ind1 = tupla1
    mat2, ind2 = tupla2

    if mat1 == mat2:
        tipo1, cod1, _ = alunos[mat1][1][ind1]
        tipo2, cod2, _ = alunos[mat2][1][ind2]

        if tipo1 != tipo2:
            return tipo1 < tipo2
        return cod1 <= cod2

    pts1 = calcular_pontos_aluno(mat1, alunos, pontos, qtd_tipos)
    pts2 = calcular_pontos_aluno(mat2, alunos, pontos, qtd_tipos)

    if pts1 != pts2:
         return pts1 > pts2
    
    nome1 = alunos[mat1][0]
    nome2 = alunos[mat2][0]

    if nome1 != nome2:
        return nome1 < nome2
    
    if mat1 != mat2:
        return mat1 < mat2
    
    atividades1 = alunos[mat1][1][ind1]
    atividades2 = alunos[mat2][1][ind2]

    tipo1, cod1, _ = atividades1
    tipo2, cod2, _ = atividades2

    if tipo1 != tipo2:
        return tipo1 < tipo2
    
    return cod1 <= cod2


''' ============ Merge Sort ================== '''

def msort(lista, alunos, pontos, qtd_tipos):
    if len(lista) > 1:
        meio = len(lista) // 2
        lEsq = lista[:meio]
        lDir = lista[meio:]
        
        msort(lEsq, alunos, pontos, qtd_tipos)
        msort(lDir, alunos, pontos, qtd_tipos)
        
        merge(lista, lEsq, lDir, alunos, pontos, qtd_tipos)	

def merge(l, lEsq, lDir, alunos, pontos, qtd_tipos):
    i = 0
    j = 0
    k = 0
    
    while i<len(lEsq) and j<len(lDir):
        if comparar(lEsq[i], lDir[j], alunos, pontos, qtd_tipos):
            l[k] = lEsq[i]
            i += 1
        else:
            l[k] = lDir[j]
            j += 1
        k += 1
    
    while i < len(lEsq):
        l[k] = lEsq[i]
        i += 1
        k += 1
        
    while j < len(lDir):
        l[k] = lDir[j]
        j += 1
        k += 1

''' ============ Funcao Principal ============ '''
def main():

    t1 = time.process_time()
    tipos,pontos,alunos  = ler_dados("entrada1.bin")
    
    qtd_tipos = len(tipos)
    
    lista = criar_lista_atividades(alunos)
    msort(lista, alunos, pontos, qtd_tipos)

    gerar_saida(lista, alunos, pontos, qtd_tipos, 'saida1.txt')
    t2 = time.process_time()

    print(t2 - t1)

main()