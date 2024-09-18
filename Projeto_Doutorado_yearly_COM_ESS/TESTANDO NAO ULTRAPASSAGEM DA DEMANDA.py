if l_sol[clist-1][h] - l_sol[clist - 2][h] == -1:  # se o gerador desligou
    cont_desbloc[h] = 0  # zera o contador para desbloquear ele
    cont_reab[h] = 0  # zera o contador de reabastecimento pra comecar reabastecer
    bloqueador[h] = 0  # bloqueia ele porque ele desligou (restirção técnica)
    cont_desbloc[h] += 1  # já que desligou começa a contar um step time para liberar de novo
    cont_reab[h] += 1  # ja que desligou, começa a reabastecer ele

if l_sol[clist-1][h] - l_sol[clist - 2][h] == 0 and l_sol[clist-1][
    h] == 0:  # gerador se mantém desligado
    if cont_desbloc[h] < 4:  # Se ainda nao ta 4 setps desligado
        cont_desbloc[h] += 1  # continua contando o tempo desligado
        bloqueador[h] = 0  # mantem ele fora de operação
        if aut[h] - cont_aut[
            h] > 3:  # se ele tem autonomia ainda pra quando voltar, vir de cano cheio
            cont_reab[h] = 0  # nao reabastece
        else:
            if cont_reab[h] == reab[h]:  # mas ja ta reabastecido
                cont_aut[h] = 0  # agora tem autonomia
            else:
                cont_reab[h] += 1  # Segue reabastecendo

    else:  # Se ja ta com 4 step times parado
        if aut[h] - cont_aut[
            h] > 3:  # Se a autonomia total - o contator atual tiver 4 steps time ainda
            bloqueador[h] = 2  # libera pra entrar
        else:
            cont_reab[h] += 1  # se não segue reabastecendo
            if cont_reab[h] == reab[
                h]:  # se com a reabastecida na linha em cima completou o tanque
                bloqueador[h] = 2  # ai libera o gerador ja na proxima
                cont_reab[h] = 0  # zera o contador de reab
                cont_aut[h] = 0  # zera o contador de autonomia
            else:
                bloqueador[h] = 0  # bloqueia ainda pra continuar reabastecendo
                cont_reab[h] += 1  # segue reabastecendo

if l_sol[clist-1][h] - l_sol[clist - 2][h] == 1:  # se o gerador ligou
    cont_aut[h] += 1  # conta step tempo de autonomia
    bloqueador[h] = 1  # força ficar ligado
    cont_bloc[h] += 1  # conta o tempo bloqueado

if l_sol[clist-1][h] - l_sol[clist - 2][h] == 0 and l_sol[clist][
    h] == 1:  # gerador se mantèm ligado
    cont_aut[h] += 1  # conta a autonomia
    cont_bloc[h] += 1  # segue contando o tempo pra fechar 4 steps
    if cont_bloc[h] < 4:  # se não ficou 4 steps ligado
        bloqueador[h] = 1  # segue ficando
    else:
        bloqueador[h] = 2  # se não libera para ser desligado ou ligado
        cont_bloc[h] = 0  # zera o tempo que força ele ficar ligado