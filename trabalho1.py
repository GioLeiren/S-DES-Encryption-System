def permutacao(bits, ordem):
    """Aplica uma permutação a uma lista de bits."""
    return [bits[i - 1] for i in ordem]

def deslocar_circular(parte_esquerda, parte_direita, passos):
    """Realiza o deslocamento circular em duas partes."""
    esquerda_deslocada = parte_esquerda[passos:] + parte_esquerda[:passos]
    direita_deslocada = parte_direita[passos:] + parte_direita[:passos]
    return esquerda_deslocada, direita_deslocada

def gerar_subchaves(chave):
    """Gera as subchaves K1 e K2 a partir de uma chave de 10 bits."""
    # Permutação P10
    p10_ordem = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    chave_permutada = permutacao(chave, p10_ordem)
    
    # Divisão em duas metades
    metade_esquerda = chave_permutada[:5]
    metade_direita = chave_permutada[5:]
    
    # Deslocamento Circular Simples
    metade_esquerda, metade_direita = deslocar_circular(metade_esquerda, metade_direita, 1)
    
    # Permutação P8 para gerar K1
    p8_ordem = [6, 3, 7, 4, 8, 5, 10, 9]
    k1 = permutacao(metade_esquerda + metade_direita, p8_ordem)
    
    # Deslocamento Circular Duplo
    metade_esquerda, metade_direita = deslocar_circular(metade_esquerda, metade_direita, 2)
    
    # Permutação P8 para gerar K2
    k2 = permutacao(metade_esquerda + metade_direita, p8_ordem)
    
    return k1, k2

def funcao_feistel(parte_direita, subchave):
    """Aplica a função Feistel na metade direita usando a subchave."""
    # Expansão/Permutação (E/P)
    ep_ordem = [4, 1, 2, 3, 2, 3, 4, 1]
    expandido = permutacao(parte_direita, ep_ordem)
    
    # XOR com a subchave
    xor_result = [expandido[i] ^ subchave[i] for i in range(len(expandido))]
    
    # S-Boxes (S0 e S1)
    s0 = [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ]
    s1 = [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]
    esquerda = xor_result[:4]
    direita = xor_result[4:]
    
    # Calcula os índices para as S-Boxes
    s0_linha = 2 * esquerda[0] + esquerda[3]
    s0_coluna = 2 * esquerda[1] + esquerda[2]
    s1_linha = 2 * direita[0] + direita[3]
    s1_coluna = 2 * direita[1] + direita[2]
    
    s0_saida = format(s0[s0_linha][s0_coluna], "02b")
    s1_saida = format(s1[s1_linha][s1_coluna], "02b")
    
    # Combina as saídas das S-Boxes e aplica P4
    combinacao = [int(bit) for bit in s0_saida + s1_saida]
    p4_ordem = [2, 4, 3, 1]
    return permutacao(combinacao, p4_ordem)

def sdes_encriptar(bloco, k1, k2):
    """Realiza a encriptação usando S-DES."""
    # Permutação Inicial (IP)
    ip_ordem = [2, 6, 3, 1, 4, 8, 5, 7]
    bloco_permutado = permutacao(bloco, ip_ordem)
    bloco_permutado = [1, 0, 1, 1, 1, 1, 0, 1]
    
    # Divisão em L e R
    l, r = bloco_permutado[:4], bloco_permutado[4:]
    
    # Primeira rodada de Feistel
    f1 = funcao_feistel(r, k1)
    l = [l[i] ^ f1[i] for i in range(4)]  # Resultado de F1(L,R)

    # Troca L e R
    l, r = r, l
    
    # Segunda rodada de Feistel
    f2 = funcao_feistel(r, k2)
    l = [l[i] ^ f2[i] for i in range(4)]
    
    # Combina L e R e aplica Permutação Final (IP⁻¹)
    bloco_final = l + r
    ip_inversa_ordem = [4, 1, 3, 5, 7, 2, 8, 6]
    return permutacao(bloco_final, ip_inversa_ordem)

# Teste
chave_10_bits = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]  # Chave fornecida
bloco = [1, 1, 0, 1, 0, 1, 1, 1]  # Bloco fornecido
k1, k2 = gerar_subchaves(chave_10_bits)
cifrado = sdes_encriptar(bloco, k1, k2)
print("K1:", k1)
print("K2:", k2)
print("Bloco cifrado:", cifrado)
