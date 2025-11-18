
import pickle
import time

''' Funcao de Leitura de Arquivos '''
def ler_dados(arquivo):
    with open(arquivo,"rb") as f:
        tipos = pickle.load(f)
        pontos = pickle.load(f)
        alunos = pickle.load(f)
    return tipos,pontos, alunos

''' Funcao para Gerar o Arquivo de Saida '''
def gerar_saida(lista_ordenada, alunos, pontos, qtd_tipos, arquivo_saida):
    saida = []
    mat_anterior = None
    
    for mat, ind in lista_ordenada:
        if mat_anterior != mat:
            nome = alunos[mat][0]
            total_pontos = calcular_pontos_aluno(mat, alunos, pontos, qtd_tipos)
            saida.append(f"{nome} ({mat}): {total_pontos} pontos\n")
            mat_anterior = mat
        
        tipo, codigo, unidades = alunos[mat][1][ind]
        nome_ativ, pts_unid, _ = pontos[(tipo, codigo)]
        pontos_atividade = unidades * pts_unid
        
        saida.append(f"  {tipo}.{codigo} {nome_ativ}: {unidades}x{pts_unid}={pontos_atividade}\n")

    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        f.writelines(saida)

''' Funcao de Criacao da lista de tuplas de matricula e cadastro de atividades '''
def criar_lista_atividades(alunos):
    l = []
    for mat in alunos:
        atividades = alunos[mat][1]
        for i in range(len(atividades)):
            l.append((mat,i))
    return l

''' Funcao de Calculo'''
def calcular_pontos_por_atividades(atividades, pontos, qtd_tipos):
    total = 0
    pontos_tipo = [0] * (qtd_tipos + 1)

    for tipo, codigo, unidades in atividades:
        pontos_unidade = pontos[(tipo, codigo)][1]
        pontos_tipo[tipo] += unidades * pontos_unidade
    
    for p in pontos_tipo[1:]:
        if p > 10: total += 10
        else: total += p

    return 15 if total > 15 else total

def calcular_pontos_aluno(matricula, alunos, pontos, qtd_tipos):
    atividades = alunos[matricula][1]
    return calcular_pontos_por_atividades(atividades, pontos, qtd_tipos)

def comparar(tupla1,tupla2,alunos,pontos,qtd_tipos):
    mat1, ind1 = tupla1
    mat2, ind2 = tupla2

    if mat1 == mat2:
        tipo1, cod1, _ = alunos[mat1][1][ind1]
        tipo2, cod2, _ = alunos[mat2][1][ind2]

        if tipo1 != tipo2:
            return tipo1 < tipo2
        return cod1 <= cod2
    
    dados1 = alunos[mat1]
    dados2 = alunos[mat2]

    pts1 = calcular_pontos_por_atividades(dados1[1], pontos, qtd_tipos)
    pts2 = calcular_pontos_por_atividades(dados2[1], pontos, qtd_tipos)

    if pts1 != pts2:
         return pts1 > pts2
    
    nome1 = dados1[0]
    nome2 = dados2[0]

    if nome1 != nome2:
        return nome1 < nome2
    
    return mat1 < mat2


''' Merge Sort '''
def merge_sort(lista, aux, esq, dir, alunos, pontos, qtd_tipos):
    if esq >= dir:
        return

    meio = (esq + dir) // 2
    merge_sort(lista, aux, esq, meio, alunos, pontos, qtd_tipos)
    merge_sort(lista, aux, meio + 1, dir, alunos, pontos, qtd_tipos)

    merge(lista, aux, esq, meio, dir, alunos, pontos, qtd_tipos)

def merge(lista, aux, esq, meio, dir, alunos, pontos, qtd_tipos):
    for k in range(esq, dir + 1):
        aux[k] = lista[k]

    i = esq
    j = meio + 1

    for k in range(esq, dir + 1):
        if i > meio:
            lista[k] = aux[j]
            j += 1
        elif j > dir:
            lista[k] = aux[i]
            i += 1
        elif comparar(aux[i], aux[j], alunos, pontos, qtd_tipos):
            lista[k] = aux[i]
            i += 1
        else:
            lista[k] = aux[j]
            j += 1

''' Merge Sort Iterativo '''
def merge_iterativo(src, dest, inicio, meio, fim, alunos, pontos, qtd_tipos):
    i = inicio
    j = meio
    k = inicio

    while i < meio and j < fim:
        if comparar(src[i], src[j], alunos, pontos, qtd_tipos):
            dest[k] = src[i]
            i += 1
        else:
            dest[k] = src[j]
            j += 1
        k += 1

    while i < meio:
        dest[k] = src[i]
        i += 1
        k += 1

    while j < fim:
        dest[k] = src[j]
        j += 1
        k += 1

def msort_iterativo(lista, aux, alunos, pontos, qtd_tipos):
    N = len(lista)
    tamanho_sublista = 1
    
    src = lista
    dest = aux
    
    while tamanho_sublista < N:
        for i in range(0, N, 2 * tamanho_sublista):
            inicio = i
            
            meio_candidato = i + tamanho_sublista
            meio = meio_candidato if meio_candidato < N else N
            
            fim_candidato = i + 2 * tamanho_sublista
            fim = fim_candidato if fim_candidato < N else N
            
            if meio < fim:
                merge_iterativo(src, dest, inicio, meio, fim, alunos, pontos, qtd_tipos)
            else:
                for k in range(inicio, fim):
                    dest[k] = src[k]
            
        src, dest = dest, src
        tamanho_sublista *= 2
        
    if src != lista:
        lista[:] = aux[:]

''' Funcao Principal '''
def main():

    # t1 = time.process_time()
    tipos,pontos,alunos  = ler_dados("entrada.bin")
    
    qtd_tipos = len(tipos)
    
    lista = criar_lista_atividades(alunos)
    
    N = len(lista)
    aux = [0] * N
    
    merge_sort(lista, aux, 0, N - 1, alunos, pontos, qtd_tipos)
    # msort_iterativo(lista, aux, alunos, pontos, qtd_tipos)

    gerar_saida(lista, alunos, pontos, qtd_tipos, 'saida.txt')
    # t2 = time.process_time()

    # print(t2 - t1)

if __name__ == "__main__":
    main()

''' Funcao para Comparar as Saidas com as do Hilario '''
def comparar_saidas():
    """
    Compara saida1.txt até saida4.txt com seus respectivos ideais
    """
    print("=" * 60)
    print("COMPARAÇÃO DE SAÍDAS")
    print("=" * 60)
    
    for i in range(1, 5):
        arquivo_gerado = f"saida{i}.txt"
        arquivo_ideal = f"saida{i}ideal.txt"
        
        try:
            with open(arquivo_gerado, 'r', encoding='utf-8') as f1:
                conteudo_gerado = f1.read().strip()
            
            with open(arquivo_ideal, 'r', encoding='utf-8') as f2:
                conteudo_ideal = f2.read().strip()
            
            if conteudo_gerado == conteudo_ideal:
                print(f"[OK] Saída {i}: CORRETO")
            else:
                print(f"[DIF] Saída {i}: DIFERENTE")
                
                # Mostrar diferenças linha por linha
                linhas_geradas = conteudo_gerado.split('\n')
                linhas_ideais = conteudo_ideal.split('\n')
                
                print(f"  - Linhas geradas: {len(linhas_geradas)}")
                print(f"  - Linhas esperadas: {len(linhas_ideais)}")
                
                # Mostrar primeiras diferenças
                for j, (linha_ger, linha_ideal) in enumerate(zip(linhas_geradas, linhas_ideais), 1):
                    if linha_ger != linha_ideal:
                        print(f"  - Primeira diferença na linha {j}:")
                        print(f"    Gerado:   '{linha_ger}'")
                        print(f"    Esperado: '{linha_ideal}'")
                        break
                        
        except FileNotFoundError as e:
            print(f"[ERR] Saída {i}: ARQUIVO NÃO ENCONTRADO - {e}")
        except Exception as e:
            print(f"[ERR] Saída {i}: ERRO - {e}")
    
    print("=" * 60)

# comparar_saidas()