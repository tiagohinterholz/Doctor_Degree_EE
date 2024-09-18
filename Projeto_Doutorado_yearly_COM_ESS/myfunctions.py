def verifica_bloqueador_ultrap(l_sol,i,cont_desbloc,cont_reab,bloqueador,aut,cont_aut,cont_bloc,reab):
    for h in range(9):
        if l_sol[i - 1][h] == 1 and l_sol[i][h] == 0:  # se o gerador desligou
            cont_desbloc[h] = 0  # zera o contador para desbloquear ele
            cont_reab[h] = 0  # zera o contador de reabastecimento pra comecar reabastecer
            bloqueador[h] = 0  # bloqueia ele porque ele desligou (restirção técnica)
            cont_desbloc[h] += 1  # já que desligou começa a contar um step time para liberar de novo
            if aut[h] - cont_aut[h] < 4:
                cont_reab[h] += 1  # ja que desligou, começa a reabastecer ele
            cont_bloc[h] = 0

        if l_sol[i][h] - l_sol[i - 1][h] == 0 and l_sol[i][h] == 0:  # gerador se mantém desligado
            if cont_desbloc[h] < 4:  # Se ainda nao ta 4 setps desligado
                cont_desbloc[h] += 1  # continua contando o tempo desligado
                bloqueador[h] = 0  # mantem ele fora de operação
                if aut[h] - cont_aut[h] > 3:  # se ele tem autonomia ainda pra quando voltar, vir de cano cheio
                    cont_reab[h] = 0  # nao reabastece
                else:
                    if cont_reab[h] == reab[h]:  # mas ja ta reabastecido
                        cont_aut[h] = 0  # agora tem autonomia
                    else:
                        cont_reab[h] += 1  # Segue reabastecendo

            else:  # Se ja ta com 4 step times parado
                if aut[h] - cont_aut[h] > 3:  # Se a autonomia total - o contator atual tiver 4 steps time ainda
                    bloqueador[h] = 2  # libera pra entrar
                else:
                    cont_reab[h] += 1  # se não segue reabastecendo
                    if cont_reab[h] == reab[h]:  # se com a reabastecida na linha em cima completou o tanque
                        bloqueador[h] = 2  # ai libera o gerador ja na proxima
                        cont_reab[h] = 0  # zera o contador de reab
                        cont_aut[h] = 0  # zera o contador de autonomia
                    else:
                        bloqueador[h] = 0  # bloqueia ainda pra continuar reabastecendo

        if  l_sol[i - 1][h] == 0 and l_sol[i][h] == 1:  # se o gerador ligou
            cont_aut[h] += 1  # conta step tempo de autonomia
            bloqueador[h] = 1  # força ficar ligado
            cont_bloc[h] += 1  # conta o tempo bloqueado

        if l_sol[i - 1][h] == 1 and l_sol[i][h] == 1:  # gerador se mantèm ligado
            if cont_bloc[h] < 4 and cont_aut[h] <= aut[h]:  # se não ficou 4 steps ligado
                cont_aut[h] += 1  # conta a autonomia
                cont_bloc[h] += 1  # conta os steps de tempo
                bloqueador[h] = 1  # segue ficando
            elif cont_bloc[h] >= 4 and cont_aut[h] + 4 >= aut[h]:
                cont_aut[h] += 1  # conta a autonomia
                cont_bloc[h] += 1  # conta os steps de tempo
                bloqueador[h] = 2  # se não libera para ser desligado ou ligado
            else:
                bloqueador[h] = 0  # bloqueia pra ele começar a reabastecer



    return bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc

def verifica_bloqueador_nao_ultrap(l_sol,i,cont_desbloc,cont_reab,bloqueador,aut,cont_aut,cont_bloc,reab):

    for h in range(9):
        # se o gerador desligou
        if l_sol[i - 1][h] == 0 and l_sol[i - 2][h] == 1:
            bloqueador[h] = 0  # bloqueia ele porque ele desligou (restrição técnica)

        # G mantém desligado
        if l_sol[i - 2][h] == 0 and l_sol[i - 1][h] == 0:
            if cont_desbloc[h] < 4:  # Se ainda nao ta 4 setps desligado
                bloqueador[h] = 0  # mantem ele fora de operação
            else:  # Se ja ta com 4 step times parado
               bloqueador[h] = 2  # libera pra entrar

        if l_sol[i - 1][h] == 1 and l_sol[i - 2][h] == 0:  # se o gerador ligou
            bloqueador[h] = 1  # força ficar ligado

        if l_sol[i - 1][h] == 1 and l_sol[i - 2][h] == 1:  # gerador se mantèm ligado
            if cont_bloc[h] < 4:  # se não ficou 4 steps ligado
                bloqueador[h] = 1  # segue ficando

            else:
                bloqueador[h] = 2  # se não libera para ser desligado ou ligado

        despacho = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for k in range(9):  # aqui eu verifico o bloqueador. Se ele for 0 ou 2 significa que o gerador tem que
            # estar fora ou liberado. Como a demanda vai ser 0, se ele ta liberado, cai fora. Se não, segue 1
            if bloqueador[k] == 0 or bloqueador[k] == 2:
                despacho[k] = 0
            else:
                despacho[k] = 1

    return despacho

def create_lista_despacho(tam_list_com, lista_completa, dem_fault, bloqueador):
    lista_despacho = []  # sempre zerada na próxima iteração
    dec_dem_ultrap = 1
    while len(lista_despacho) == 0:
        for z in range(tam_list_com):  # procuro na lista completa todas combinações que atendem a ultrap
            if lista_completa[z][1] >= dec_dem_ultrap * dem_fault:
                lista_despacho.append(lista_completa[z])  # armazena na lista_despacho todas que atendem
        for t in range(9):  # aqui eu pego o vetor bloqueador pra ver quais entram quais sai e quais são indiferentes
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
            lista_index.sort(reverse=True)  # armazeno todos os index para sair e ordeno para deletar
            for index in lista_index:  # rotina para limpar a lista despacho que serve como base para o proximo passo
                if len(lista_index) == 0:
                    pass
                else:
                    lista_despacho.pop(index)
        dec_dem_ultrap = dec_dem_ultrap - 0.05

    return lista_despacho

def create_lista_diesel(tam_list_desp, lista_despacho, G):  # gera uma lista com as 3 soluções mais barats no gasto
    lista_diesel = []
    for w in range(tam_list_desp):
        total = 0
        for z in range(9):
            C = lista_despacho[w][0][z] * G[z][1]
            total = C + total
        lista_diesel.append([total, lista_despacho[w]])
    lista_diesel.sort()
    for k in range(tam_list_desp):
        if k > tam_list_desp - 4:
            pass
        else:
            lista_diesel.pop()

    return lista_diesel

def prev_dem(i, tempo, dem_lida):
    x1 = i - 2
    x2 = i - 1
    y1 = dem_lida[i - 2]
    y2 = dem_lida[i - 1]

    xmedia = (x2 + x1) / 2
    ymedia = (y2 + y1) / 2

    Sxy = ((x2 - xmedia) * (y2 - ymedia)) + ((x1 - xmedia) * (y1 - ymedia))
    Sxx = ((x2 - xmedia) * (x2 - xmedia)) +((x1 - xmedia) * (x1 - xmedia))


    beta = Sxy/Sxx
    alfa = ymedia - (beta * xmedia)

    dem = alfa + beta * i

    return dem

def plot_general(dem_lida_GD, dem_lida, Gptotal_GMG, Gptotal_UFV, Gptotal_ESS, SoC1):

    import matplotlib.pyplot as plt

    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(dem_lida_GD, color='r', label='P1')
    ax1.legend()
    ax1.set_ylabel("Demand (kW)")
    ax2.plot(SoC1, color='r', label='V1')
    ax2.set_ylabel("SoC1")

    plt.title("Circuit Power kW Total")
    plt.plot(range(1, len(dem_lida_GD) + 1), dem_lida_GD, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(-1000, 6500)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(dem_lida_GD) + 1)
    #grid(True)
    plt.show()

    plt.title("Circuit Power kW Total with no Generator")
    plt.plot(range(1, len(dem_lida) + 1), dem_lida, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 6500)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(dem_lida) + 1)
    # grid(True)
    plt.show()

    plt.title("GD GMC Power kW Total")
    plt.plot(range(1, len(Gptotal_GMG) + 1), Gptotal_GMG, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 1300)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(Gptotal_GMG) + 1)
    # grid(True)
    plt.show()

    #plt.title("GD UFV Power kW Total")
    #plt.plot(range(1, len(Gptotal_UFV) + 1), Gptotal_UFV, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    #plt.legend()
    #plt.ylim(0, 1500)
    #plt.ylabel("kW")
    #plt.xlabel("Hour")
    #plt.xlim(1, len(Gptotal_GMC) + 1)
    # grid(True)
    #plt.show()

    plt.title("ESS Power kW Total")
    plt.plot(range(1, len(Gptotal_ESS) + 1), Gptotal_ESS, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 750)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(Gptotal_ESS) + 1)
    # grid(True)
    plt.show()

def plot_kwhstored(kWhrated1, kWhrated2, kWhrated3, kWhrated4):

    import matplotlib.pyplot as plt

    plt.title("kWhStored ESS1 Total")
    plt.plot(range(1, len(kWhrated1) + 1), kWhrated1, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 1500)
    plt.ylabel("kWh")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWhrated1) + 1)
    #grid(True)
    plt.show()

    plt.title("kWhStored ESS2 Total")
    plt.plot(range(1, len(kWhrated2) + 1), kWhrated2, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 5000)
    plt.ylabel("kWh")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWhrated2) + 1)
    # grid(True)
    plt.show()

    plt.title("kWhStored ESS3 Total")
    plt.plot(range(1, len(kWhrated3) + 1), kWhrated3, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 600)
    plt.ylabel("kWh")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWhrated3) + 1)
    # grid(True)
    plt.show()

    plt.title("kwhStored ESS4 Total")
    plt.plot(range(1, len(kWhrated4) + 1), kWhrated4, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 400)
    plt.ylabel("kWh")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWhrated4) + 1)
    # grid(True)
    plt.show()

def plot_kwstored(kWratedin1, kWratedin2, kWratedin3, kWratedin4):

    import matplotlib.pyplot as plt

    plt.title("kWStored ESS1 Total")
    plt.plot(range(1, len(kWratedin1) + 1), kWratedin1, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 150)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWratedin1) + 1)
    #grid(True)
    plt.show()

    plt.title("kWStored ESS2 Total")
    plt.plot(range(1, len(kWratedin2) + 1), kWratedin2, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 500)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWratedin2) + 1)
    # grid(True)
    plt.show()

    plt.title("kwStored ESS3 Total")
    plt.plot(range(1, len(kWratedin3) + 1), kWratedin3, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 60)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWratedin3) + 1)
    # grid(True)
    plt.show()

    plt.title("kwStored ESS4 Total")
    plt.plot(range(1, len(kWratedin4) + 1), kWratedin4, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0, 45)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(kWratedin4) + 1)
    # grid(True)
    plt.show()

def plot_SoC(SoC1, SoC2, SoC3, SoC4):

    import matplotlib.pyplot as plt

    plt.title("SoC 1")
    plt.plot(range(1, len(SoC1) + 1), SoC1, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(-1, 1)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(SoC1) + 1)
    #grid(True)
    plt.show()

    plt.title("SoC 2")
    plt.plot(range(1, len(SoC2) + 1), SoC2, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(-1, 1)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(SoC2) + 1)
    # grid(True)
    plt.show()

    plt.title("SoC 3")
    plt.plot(range(1, len(SoC3) + 1), SoC3, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(-1, 1)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(SoC3) + 1)
    # grid(True)
    plt.show()

    plt.title("SoC 4")
    plt.plot(range(1, len(SoC4) + 1), SoC4, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(-1, 1)
    plt.ylabel("kW")
    plt.xlabel("Hour")
    plt.xlim(1, len(SoC4) + 1)
    # grid(True)
    plt.show()

def plot_voltage_bus(Voltages_219d):

    import matplotlib.pyplot as plt

    plt.title("Voltage Bus 219d")
    plt.plot(range(1, len(Voltages_219d) + 1), Voltages_219d, "g", label="P")
    # plt.plot(range(1, len(qt) + 1), qt, "b", label="Q")
    plt.legend()
    plt.ylim(0.93, 1.03)
    plt.ylabel("PU")
    plt.xlabel("Hour")
    plt.xlim(1, len(Voltages_219d) + 1)
    # grid(True)
    plt.show()