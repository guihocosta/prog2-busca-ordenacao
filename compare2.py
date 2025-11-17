import pickle
import time

''' Funcao de Leitura de Arquivos '''
def ler_dados(arquivo):
    with open(arquivo, "rb") as f:
        tipos = pickle.load(f)
        pontos = pickle.load(f)
        alunos = pickle.load(f)
    return tipos, pontos, alunos

''' Funcao para Saída dos Arquivos '''
def gerar_saida(lista_ordenada, alunos, pontos, qtd_tipos, arquivo_saida):
    with open(arquivo_saida, 'w') as f:
        mat_anterior = None
        for mat, ind in lista_ordenada:
            if mat_anterior != mat:
                nome = alunos[mat][0]
                total_pontos = calcular_pontos_aluno(mat, alunos, pontos, qtd_tipos)
                f.write(f"{nome} ({mat}): {total_pontos} pontos\n")
                mat_anterior = mat
        
            tipo, codigo, unidades = alunos[mat][1][ind]
            nome_atividade, pontos_unidade, _ = pontos[(tipo, codigo)]
            pontos_atividade = unidades * pontos_unidade

            f.write(f"  {tipo}.{codigo} {nome_atividade}: {unidades}x{pontos_unidade}={pontos_atividade}\n")

''' Funcao de Criacao da lista de tuplas de matricula e cadastro de atividades '''
def criar_lista_atividades(alunos):
    lista = []
    for mat, (nome, atividades) in alunos.items():
        for i in range(len(atividades)):
            lista.append((mat, i))
    return lista

''' Funcao de Calculo - SEM CACHE (conforme requisito) '''
def calcular_pontos_aluno(matricula, alunos, pontos, qtd_tipos):
    atividades = alunos[matricula][1]
    pontos_tipo = [0] * (qtd_tipos + 1)

    for tipo, codigo, unidades in atividades:
        pontos_unidade = pontos[(tipo, codigo)][1]
        pontos_tipo[tipo] += unidades * pontos_unidade

    total = 0
    for i in range(1, qtd_tipos + 1):
        total += min(pontos_tipo[i], 10)

    return min(total, 15)

def comparar(tupla1, tupla2, alunos, pontos, qtd_tipos):
    mat1, ind1 = tupla1
    mat2, ind2 = tupla2

    # Caso mais comum: mesma matrícula (comparação mais rápida)
    if mat1 == mat2:
        tipo1, cod1, _ = alunos[mat1][1][ind1]
        tipo2, cod2, _ = alunos[mat2][1][ind2]
        
        if tipo1 != tipo2:
            return tipo1 < tipo2
        return cod1 < cod2
    
    # Diferentes matrículas: comparar pontos
    pts1 = calcular_pontos_aluno(mat1, alunos, pontos, qtd_tipos)
    pts2 = calcular_pontos_aluno(mat2, alunos, pontos, qtd_tipos)

    if pts1 != pts2:
        return pts1 > pts2
    
    # Mesmos pontos: comparar nomes
    nome1 = alunos[mat1][0]
    nome2 = alunos[mat2][0]

    if nome1 != nome2:
        return nome1 < nome2
    
    # Mesmos nomes: comparar matrículas
    return mat1 < mat2

''' ============ Merge Sort Otimizado ================== '''

def msort(lista, alunos, pontos, qtd_tipos):
    if len(lista) <= 1:
        return
    
    meio = len(lista) >> 1  # Divisão bit shift (mais rápida)
    lEsq = lista[:meio]
    lDir = lista[meio:]
    
    msort(lEsq, alunos, pontos, qtd_tipos)
    msort(lDir, alunos, pontos, qtd_tipos)
    
    merge(lista, lEsq, lDir, alunos, pontos, qtd_tipos)

def merge(l, lEsq, lDir, alunos, pontos, qtd_tipos):
    i = j = k = 0
    lenEsq = len(lEsq)
    lenDir = len(lDir)
    
    while i < lenEsq and j < lenDir:
        if comparar(lEsq[i], lDir[j], alunos, pontos, qtd_tipos):
            l[k] = lEsq[i]
            i += 1
        else:
            l[k] = lDir[j]
            j += 1
        k += 1
    
    # Copiar elementos restantes
    while i < lenEsq:
        l[k] = lEsq[i]
        i += 1
        k += 1
        
    while j < lenDir:
        l[k] = lDir[j]
        j += 1
        k += 1

''' ============ Função de Comparação de Saídas ============ '''
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
                print(f"✓ Saída {i}: CORRETO")
            else:
                print(f"✗ Saída {i}: DIFERENTE")
                
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
            print(f"✗ Saída {i}: ARQUIVO NÃO ENCONTRADO - {e}")
        except Exception as e:
            print(f"✗ Saída {i}: ERRO - {e}")
    
    print("=" * 60)

''' ============ Funcao Principal ============ '''
def processar_entrada(num_entrada):
    """Processa uma entrada específica"""
    arquivo_entrada = f"entrada{num_entrada}.bin"
    arquivo_saida = f"saida{num_entrada}.txt"
    
    t1 = time.process_time()
    tipos, pontos, alunos = ler_dados(arquivo_entrada)
    
    qtd_tipos = len(tipos)
    
    lista = criar_lista_atividades(alunos)
    msort(lista, alunos, pontos, qtd_tipos)
    
    gerar_saida(lista, alunos, pontos, qtd_tipos, arquivo_saida)
    t2 = time.process_time()
    
    tempo_exec = t2 - t1
    print(f"Entrada {num_entrada}: {tempo_exec:.6f} segundos")
    return tempo_exec

def main():
    """Processa todas as entradas e compara resultados"""
    print("PROCESSANDO ENTRADAS...")
    print("-" * 60)
    
    tempo_total = 0
    for i in range(1, 5):
        try:
            tempo = processar_entrada(i)
            tempo_total += tempo
        except FileNotFoundError:
            print(f"Entrada {i}: ARQUIVO NÃO ENCONTRADO")
        except Exception as e:
            print(f"Entrada {i}: ERRO - {e}")
    
    print("-" * 60)
    print(f"Tempo total: {tempo_total:.6f} segundos")
    print()
    
    # Comparar saídas com ideais
    comparar_saidas()

if __name__ == "__main__":
    main()