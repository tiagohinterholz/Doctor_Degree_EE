# Vetor = [KVA, L de diesel/(0.25h), steptime autonomia (15 min), steptime reabast. (15 min)]

G = [[20, 1.25, 52, 5], [30, 2.5, 40, 7], [30, 2.5, 40, 7], [66, 3.6, 33, 8], [115, 6.75, 30, 14],
     [180, 9.25, 41, 26], [240, 13.75, 22, 20], [260, 14.75, 20, 20], [360, 20, 12, 16]]

aut = [G[0][2], G[1][2], G[2][2], G[3][2], G[4][2], G[5][2], G[6][2], G[7][2], G[8][2]]
reab = [G[0][3], G[1][3], G[2][3], G[3][3], G[4][3], G[5][3], G[6][3], G[7][3], G[8][3]]

cont_aut = [0, 0, 0, 0, 0, 0, 0, 0, 0]
cont_reab = [0, 0, 0, 0, 0, 0, 0, 0, 0]
bloqueador = [2, 2, 2, 2, 2, 2, 2, 2, 2]
cont_bloc = [0, 0, 0, 0, 0, 0, 0, 0, 0]
cont_desbloc = [4, 4, 4, 4, 4, 4, 4, 4, 4]
dem_ultrap = [0, 195, 349, 455, 532, 578, 606, 431, 374, 331, 199, 158, 21, 0, 89, 73, 138, 272, 757, 973,
              1112, 1128, 1101, 725, 336, 218, 146, 103, 89, 0, 0, 0, 0, 0, 0, 654, 443, 331, 229, 78, 0, 0, 0]

lista_completa = []
despacho = [0, 0, 0, 0, 0, 0, 0, 0, 0]
l_sol = [[0, 0, 0, 0, 0, 0, 0, 0, 0]]
clist = 1

from combinacoes import lista_comb  # importa todas combinações de 9 geradores

for combina in lista_comb:
    dem_GD = G[0][0] * combina[0] + G[1][0] * combina[1] + G[2][0] * combina[2] + G[3][0] * combina[3] + G[4][0] * \
             combina[4] + G[5][0] * combina[5] + G[6][0] * combina[6] + G[7][0] * combina[7] + G[8][0] * combina[8]
    lista_completa.append([combina] + [dem_GD])

tam_list_com = len(lista_completa)  # fixando tamanho da lista completa

for dem in dem_ultrap:
    lista_despacho = []  # sempre zerada na próxima iteração
    for z in range(tam_list_com):
        if lista_completa[z][1] >= dem:
            lista_despacho.append(lista_completa[z])

    for t in range(9):
        lista_index = []
        if bloqueador[t] == 1:
            for comb in lista_despacho:
                if comb[0][t] != 1:
                    index_comb = lista_despacho.index(comb)
                    lista_index.append(index_comb)

        elif bloqueador[t] == 0:
            for comb in lista_despacho:
                if comb[0][t] != 0:
                    index_comb = lista_despacho.index(comb)
                    lista_index.append(index_comb)

        lista_index.sort(reverse=True)

        for index in lista_index:
            if len(lista_index) == 0:
                pass
            else:
                lista_despacho.pop(index)

    tam_list_desp = len(lista_despacho)

    if tam_list_desp == 0:
        despacho = [[0, 0, 0, 0, 0, 0, 0, 0, 0], 0]
        print(despacho, dem, 'Sem solução')
        l_sol.append(despacho[0])
    else:
        lista_diesel = []
        for i in range(tam_list_desp):
            total = 0
            for z in range(9):
                C = lista_despacho[i][0][z] * G[z][1]
                total = C + total
            lista_diesel.append(total)
            melhor_comb = min(lista_diesel)
            index_diesel = lista_diesel.index(melhor_comb)
            despacho = lista_despacho[[index_diesel][0]]
        l_sol.append(despacho[0])

        for h in range(9):
            # variaveis necessárias: contbloc (contar quando ligar) contdesbloc (contar quando desligar/desligado),
            # vetor bloqueador pra indicar se pode ou não ligar
            # o tempo de reabastecimento é sempre metade do tempo de autonomia, ou seja, ele pode estar completamente reabastecido
            # mas nao liberado para entra ainda

            if l_sol[clist][h] - l_sol[clist - 1][h] == -1: # se o gerador desligou
                cont_desbloc[h] = 0 # zera o contador para desbloquear ele
                cont_reab[h] = 0 # zera o contador de reabastecimento pra comecar reabastecer
                bloqueador[h] = 0 # bloqueia ele porque ele desligou (restirção técnica)
                cont_desbloc[h] += 1 # já que desligou começa a contar um step time para liberar de novo
                cont_reab[h] += 1 # ja que desligou, começa a reabastecer ele


            if l_sol[clist][h] - l_sol[clist - 1][h] == 0 and l_sol[clist][h] == 0: # gerador se mantém desligado
                if cont_desbloc[h] < 4: # Se ainda nao ta 4 setps desligado
                    cont_desbloc[h] += 1 # continua contando o tempo desligado
                    bloqueador[h] = 0 # mantem ele fora de operação
                    if aut[h] - cont_aut[h] > 3: # se ele tem autonomia ainda pra quando voltar, vir de cano cheio
                        cont_reab[h] = 0 # nao reabastece
                    else:
                        if cont_reab[h] == reab[h]: # mas ja ta reabastecido
                            cont_aut[h] = 0 # agora tem autonomia
                        else:
                            cont_reab[h] += 1 # Segue reabastecendo

                else: # Se ja ta com 4 step times parado
                    if aut[h] - cont_aut[h] > 3: # Se a autonomia total - o contator atual tiver 4 steps time ainda
                        bloqueador[h] = 2 # libera pra entrar
                    else:
                        cont_reab[h] += 1 # se não segue reabastecendo
                        if cont_reab[h] == reab[h]: # se com a reabastecida na linha em cima completou o tanque
                            bloqueador[h] = 2 # ai libera o gerador ja na proxima
                            cont_reab[h] = 0 # zera o contador de reab
                            cont_aut[h] = 0 # zera o contador de autonomia
                        else:
                            bloqueador[h] = 0 # bloqueia ainda pra continuar reabastecendo
                            cont_reab[h] += 1 # segue reabastecendo

            if l_sol[clist][h] - l_sol[clist-1][h] == 1: # se o gerador ligou
                cont_aut[h] += 1 # conta step tempo de autonomia
                bloqueador[h] = 1 # força ficar ligado
                cont_bloc[h] += 1 # conta o tempo bloqueado

            if l_sol[clist][h] - l_sol[clist - 1][h] == 0 and l_sol[clist][h] == 1: # gerador se mantèm ligado
                cont_aut[h] += 1 # conta a autonomia
                cont_bloc[h] += 1 # segue contando o tempo pra fechar 4 steps
                if cont_bloc[h] < 4: # se não ficou 4 steps ligado
                    bloqueador[h] = 1 # segue ficando
                else:
                    bloqueador[h] = 2 # se não libera para ser desligado ou ligado
                    cont_bloc[h] = 0 # zera o tempo que força ele ficar ligado

        print(despacho, dem)
        clist += 1
