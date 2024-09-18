# -*- coding: utf-8 -*-

import win32com.client
from pylab import *
import myfunctions

class DSS():

    def __init__(self, dssFileName):

        self.dssFileName = dssFileName
        self.dssObj = win32com.client.Dispatch('OpenDSSEngine.DSS')

        if self.dssObj.Start(0) == False:
            print("DSS failed to start")

        else:
            self.dssText = self.dssObj.Text
            self.dssCircuit = self.dssObj.ActiveCircuit
            self.dssSolution = self.dssCircuit.Solution
            self.dssCktElement = self.dssCircuit.ActiveCktElement
            self.dssBus = self.dssCircuit.ActiveBus
            self.dssSwtControls = self.dssCircuit.SwtControls
            self.dssPDElement = self.dssCircuit.PDElements
            self.dssGenerators = self.dssCircuit.Generators
            self.dssLines = self.dssCircuit.Lines
            self.dssMonitors = self.dssCircuit.Monitors
            self.dssMeters = self.dssCircuit.Meters
            self.dssObj.Allowforms = False

    def compile_DSS(self):

        self.dssObj.ClearAll()
        self.dssText.Command = "compile " + self.dssFileName

    def solve_DSS_snapshot(self, mult_carga):

        self.dssText.Command = "Set Mode = Snapshot"
        self.dssText.Command = "Set ControlMode = Static"
        self.dssSolution.LoadMult = mult_carga

        self.dssSolution.Solve()

    def solve_Yearly(self):
        from combinacoes import lista_comb  # importa todas combinações de 9 geradores

        myObject.compile_DSS()
        self.dssText.Command = "Set Mode = yearly"
        self.dssText.Command = "Set number = 1"
        self.dssText.Command = "Set stepsize = 1h"
        self.dssText.Command = "Set ControlMode = static"
        self.dssText.Command = "Set Hour = 0"
        self.dssText.Command = "set AllowDuplicates = yes"

        self.dssText.command = "New Energymeter.SE element = Line.Sub terminal = 1"
        self.dssText.command = "New Monitor.SE element = Line.Sub Terminal = 1 mode = 1 ppolar = no"

        self.dssText.command = "New Monitor.G1 element = Line.G1 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G2 element = Line.G2 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G3 element = Line.G3 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G4 element = Line.G4 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G5 element = Line.G5 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G6 element = Line.G6 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G7 element = Line.G7 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G8 element = Line.G8 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G9 element = Line.G9 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G10 element = Line.G10 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G11 element = Line.G11 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G12 element = Line.G12 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G13 element = Line.G13 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G14 element = Line.G14 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G15 element = Line.G15 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G16 element = Line.G16 terminal = 1 mode = 1 ppolar = false "
        self.dssText.command = "New Monitor.G17 element = Line.G17 terminal = 1 mode = 1 ppolar = false "

        self.dssText.command = "New Monitor.State1 element = Storage.S_Predio9F   terminal = 1 mode = 3 "
        self.dssText.command = "New Monitor.State2 element = Storage.S_Parque_Exp terminal = 1 mode = 3 "
        self.dssText.command = "New Monitor.State3 element = Storage.S_CTISM      terminal = 1 mode = 3 "
        self.dssText.command = "New Monitor.State4 element = Storage.S_CEU60      terminal = 1 mode = 3 "


        # informações Geradores  (kW, L Diesel/15 min, Aut (15min), Reab (15Min))
        #G = [[18, 1.25, 52, 5], [27, 2.5, 40, 7], [27, 2.5, 40, 7], [59.4, 3.6, 33, 8], [103.5, 6.75, 30, 14],
             #[162, 9.25, 41, 26], [216, 13.75, 22, 20], [234, 14.75, 20, 20], [324, 20, 12, 16]]
        G = [[18, 1.25, 60, 5], [27, 2.5, 45, 7], [27, 2.5, 45, 7], [59.4, 3.6, 40, 8], [103.5, 6.75, 35, 14],
             [162, 9.25, 47, 26], [216, 13.75, 25, 20], [234, 14.75, 25, 20], [324, 20, 18, 16]]
        # vetores contadores
        aut = [G[0][2], G[1][2], G[2][2], G[3][2], G[4][2], G[5][2], G[6][2], G[7][2], G[8][2]]
        reab = [G[0][3], G[1][3], G[2][3], G[3][3], G[4][3], G[5][3], G[6][3], G[7][3], G[8][3]]
        cont_aut = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        cont_reab = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        bloqueador = [2, 2, 2, 2, 2, 2, 2, 2, 2]
        cont_bloc = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        cont_desbloc = [4, 4, 4, 4, 4, 4, 4, 4, 4]
        lista_completa = []
        l_sol = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]
        despacho = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        tempo = []
        tSinterval = 2880
        dia = 1
        semana = 1
        # vetores de armazenamento de dados
        dem_lida = []
        dem_lida_GD = []
        dem_prev = [0, 0]
        dem_ultrap = 0
        Gptotal_GMG = [0, 0]
        Gptotal_UFV = [0, 0]
        Gptotal_ESS = [0, 0]
        Voltages_219d = []
        energy_consumed = 0
        buses = self.dssCircuit.AllBusNames
        swt_lines = ['Line.G1', 'Line.G2', 'Line.G3', 'Line.G4', 'Line.G5', 'Line.G6', 'Line.G7', 'Line.G8', 'Line.G9']
        ess_names = ['Storage.S_Predio9F', 'Storage.S_Parque_Exp', 'Storage.S_CTISM', 'Storage.S_CEU60']
        monitors_names = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12', 'G13', 'G14', 'G15',
                          'G16', 'G17', 'State1', 'State2', 'State3', 'State4']

        for combina in lista_comb:
            dem_GD = G[0][0] * combina[0] + G[1][0] * combina[1] + G[2][0] * combina[2] + G[3][0] * combina[3] + G[4][
                0] * \
                     combina[4] + G[5][0] * combina[5] + G[6][0] * combina[6] + G[7][0] * combina[7] + G[8][0] * \
                     combina[8]
            lista_completa.append([combina] + [dem_GD])
        tam_list_com = len(lista_completa)  # fixando tamanho da lista completa

        for i in range(tSinterval):
            # ajustar dia, semana e enquandrar nos horários de ponta e fora ponta
            if i == dia * 96:
                dia = dia + 1
            if i == semana * 672:
                semana = semana + 1
            Sab = 96 + ((semana - 1) * 672)
            Seg = 288 + ((semana - 1) * 672)
            dezoitoh = 72 + ((dia - 1) * 96)
            vinteumah = 84 + ((dia - 1) * 96)
            vinteduash = 88 + ((dia - 1) * 96)
            seish = 25 + ((dia - 1) * 96)


            if i < 2:  # as primeiras duas iterações não tenho dados para fazer a regressão linear
                self.dssSolution.Solve()
                dem_lida_GD.append(round(-1 * self.dssCircuit.TotalPower[0], 2))
                dem_lida.append(round(-1 * self.dssCircuit.TotalPower[0], 2))
                tempo.append(self.dssSolution.dblHour)
                self.dssCircuit.SetActiveBus('219dBT')
                Voltages_219d.append(self.dssBus.puVoltages[0])

                #generator_data = [dem_ultrap, "Solucao: ", l_sol[i], "autonomia: ", cont_aut, "reabastecimento: ",
                                  #cont_reab,
                                  #"Conta_block: ", cont_bloc, "Cont_desblock: ", cont_desbloc, "bloqueadr: ", bloqueador]
                #with open('dados_geradores_restricao.txt', 'a') as arquivo:
                    #arquivo.write("\n")
                    #arquivo.write(str(generator_data))

                resultado = [i, l_sol[i], "G(kW):", round(Gptotal_GMG[i], 1), "ESS (kW):", round(Gptotal_ESS[i], 1),
                             "UFV(kW):", round(Gptotal_UFV[i], 1), "Dem_lida_GD: ", round(dem_lida_GD[i], 1),
                             "Dem_Prev: ", round(dem_prev[i], 1), "Tensão: ", round(Voltages_219d[i], 4)]
                #with open('dados_rede_GMG+UFV+ESS.txt', 'a') as arquivo:
                    #arquivo.write("\n")
                    #arquivo.write(str(resultado))
                #print(resultado)

            else:
                dem = myfunctions.prev_dem(i, tempo, dem_lida)
                dem_prev.append(dem)
                time_sim = self.dssSolution.dblHour
                Voltages_bus = []
                for b in buses:
                    self.dssCircuit.SetActiveBus(b)
                    Voltages_bus.append(self.dssBus.puVoltages[0])


                #monitores para GD UFV
                self.dssLines.name = 'G10'
                power_kw = self.dssCktElement.Powers
                p10_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G11'
                power_kw = self.dssCktElement.Powers
                p11_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G12'
                power_kw = self.dssCktElement.Powers
                p12_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G13'
                power_kw = self.dssCktElement.Powers
                p13_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                sum_gen_ufv = -1 * (p10_total_kw + p11_total_kw + p12_total_kw + p13_total_kw)

                # verifica horario PONTA
                if i >= dezoitoh and i < vinteumah:  # se tiver no horario de PONTA a demanda contratada = 3 MW
                    dem_ultrap = dem_prev[i] - 3000
                    dem_ess = dem_ultrap - sum_gen_ufv

                    soc_ess = []
                    kw_ess = []
                    soma_ess = 0
                    cont_ess = 0

                    if dem_ess <= 0: #se nao precisar das baterias e consequentemente dos GMG = NAO CARREGA NEM DESCARREGA
                        for ess_name in ess_names:
                            self.dssCircuit.SetActiveElement(ess_name)
                            self.dssText.command = '{}.State = Idling'.format(ess_name)


                    else: #seprecisar das baterias VAMOS VER QUAIS TAO DISPONÍVEIS e despachar tudo que da
                        for ess_name in ess_names:
                            self.dssCircuit.SetActiveElement(ess_name)
                            soc_ess.append(float(self.dssCktElement.Properties('%stored').val))
                            kw_ess.append(float(self.dssCktElement.Properties('kWrated').val))
                            if soc_ess[cont_ess] > 25:
                                self.dssText.command = '{}.State = Discharging'.format(ess_name)
                                soma = kw_ess[cont_ess]
                            else:
                                self.dssCircuit.SetActiveElement(ess_name)
                                self.dssText.command = '{}.State = Idling'.format(ess_name)
                                soma = 0

                            soma_ess = soma_ess + soma
                            cont_ess = cont_ess + 1

                    Gptotal_ESS.append(soma_ess)
                    dem_fault = dem_ultrap - sum_gen_ufv - soma_ess

                    if dem_fault >= 0:
                        lista_despacho = myfunctions.create_lista_despacho(tam_list_com, lista_completa, dem_fault,
                                                                           bloqueador)
                        tam_list_desp = len(lista_despacho)  # lista final com tamanho para calculo do diesel

                        if tam_list_desp == 0:
                            despacho = myfunctions.verifica_bloqueador_nao_ultrap(l_sol, i, cont_desbloc,
                                                                                  cont_reab,
                                                                                  bloqueador, aut, cont_aut, cont_bloc,
                                                                                  reab)
                            l_sol.append(despacho)
                            bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc = myfunctions.verifica_bloqueador_ultrap \
                                (l_sol, i, cont_desbloc, cont_reab, bloqueador, aut, cont_aut, cont_bloc, reab)

                        else:
                            lista_diesel = myfunctions.create_lista_diesel(tam_list_desp, lista_despacho, G)
                            voltage_tests = []
                            solutions = []
                            dif_voltages = []
                            cost_kwh = 1.2
                            cost_v = 1000
                            cost_fp = 500
                            cost_kw = 30
                            cost_diesel = 5.5
                            for lista in lista_diesel:
                                #self.dssObj.ClearAll()
                                #self.dssText.Command = "compile " + self.dssFileName
                                self.dssText.Command = "Set Hour = {}".format(time_sim)

                                diesel = lista[0]
                                for w in range(9):
                                    switchname = swt_lines[w]
                                    self.dssCircuit.Lines.Name = switchname.split(".")[1]
                                    if lista[1][0][w] == 0:
                                        oldBusName = self.dssCircuit.Lines.Bus2
                                        self.dssCircuit.Lines.Bus2 = "__opened__" + oldBusName
                                    else:
                                        self.dssCircuit.Lines.Bus2 = switchname.split(".")[1]

                                self.dssText.Command = 'Set maxiterations = 10'
                                self.dssSolution.Solve()

                                kwh_consumed = self.dssMeters.RegisterValues[0] / 4

                                buses = self.dssCircuit.AllBusNames
                                for b in buses:
                                    self.dssCircuit.SetActiveBus(b)
                                    voltage_tests.append(self.dssBus.puVoltages[0])

                                tam1 = len(voltage_tests)
                                tam2 = len(Voltages_bus)

                                if tam1 >= tam2:
                                    delta = tam2
                                else:
                                    delta = tam1

                                for n in range(delta):
                                    dif_voltages.append((abs(voltage_tests[n] - Voltages_bus[n])))

                                power_circuit = self.dssCircuit.TotalPower
                                kw = -1 * power_circuit[0]
                                kvar = -1 * power_circuit[1]
                                kva = pow((kw * kw + kvar * kvar), 0.5)
                                PF_test = kw / kva

                                dif_voltages.sort(reverse=True)

                                for v in dif_voltages:  # apaga as tensões dos geradores que entram e causam mais de 0.9 pu de variação
                                    if v > 0.5:
                                        index = dif_voltages.index(v)
                                        dif_voltages.pop(index)

                                v_test = 0
                                for vmax in dif_voltages:  # pegar o maior desvio de tensão para mensurar ele
                                    if vmax > v_test:
                                        v_test = vmax

                                if v_test > 0.05:
                                    max_v = v_test - 0.05
                                else:
                                    max_v = 0

                                if lista[1][1] - dem_fault >= 0:
                                    demand = 0
                                else:
                                    if dem_fault - lista[1][1] <= 250:
                                        demand = 0
                                    else:
                                        demand = dem_fault - lista[1][1]

                                total_cost = round((cost_diesel * diesel + cost_fp * (abs(PF_test - 0.92)) + cost_kwh *
                                                    kwh_consumed + cost_v * max_v + demand * 3 * cost_kw), 2)

                                solutions.append([total_cost, lista])

                            solutions.sort(reverse=False)
                            despacho = solutions[0][1][1][0]

                        l_sol.append(despacho)
                        bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc = myfunctions.verifica_bloqueador_ultrap(
                            l_sol, i, cont_desbloc, cont_reab, bloqueador, aut, cont_aut, cont_bloc, reab)

                    else:
                        despacho = myfunctions.verifica_bloqueador_nao_ultrap(l_sol,i,cont_desbloc,cont_reab,bloqueador,
                                                                              aut,cont_aut,cont_bloc,reab)
                        l_sol.append(despacho)
                        bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc = myfunctions.verifica_bloqueador_ultrap(
                            l_sol,i,cont_desbloc,cont_reab,bloqueador,aut,cont_aut,cont_bloc,reab)


                else:  # aqui horario fora ponta com demanda de 5 MW

                    dem_ultrap = dem_prev[i] - 5000
                    dem_ess = dem_ultrap - sum_gen_ufv

                    soc_ess = []
                    kw_ess = []
                    soma_ess_charging = 0
                    soma_ess_discharging = 0
                    cont_ess = 0
                    soma = 0

                    if i >= vinteduash or i <= seish:
                        for ess_name in ess_names:
                            self.dssCircuit.SetActiveElement(ess_name)
                            soc_ess.append(float(self.dssCktElement.Properties('%stored').val))
                            kw_ess.append(float(self.dssCktElement.Properties('kWrated').val))
                            if soc_ess[cont_ess] < 95:
                                self.dssText.command = '{}.State = Charging'.format(ess_name)
                                soma = kw_ess[cont_ess]
                            soma_ess_charging = soma + soma_ess_charging
                            cont_ess = cont_ess + 1


                    else:
                        if dem_ess <= 0:  # se nao precisar das baterias e consequentemente dos GMG = NAO CARREGA NEM DESCARREGA
                            for ess_name in ess_names:
                                self.dssCircuit.SetActiveElement(ess_name)
                                self.dssText.command = '{}.State = Idling'.format(ess_name)


                        else:  # seprecisar das baterias VAMOS VER QUAIS TAO DISPONÍVEIS e despachar tudo que da
                            for ess_name in ess_names:
                                self.dssCircuit.SetActiveElement(ess_name)
                                soc_ess.append(float(self.dssCktElement.Properties('%stored').val))
                                kw_ess.append(float(self.dssCktElement.Properties('kWrated').val))
                                if soc_ess[cont_ess] > 25:
                                    self.dssText.command = '{}.State = Discharging'.format(ess_name)
                                    soma = kw_ess[cont_ess]
                                else:
                                    self.dssCircuit.SetActiveElement(ess_name)
                                    self.dssText.command = '{}.State = Idling'.format(ess_name)
                                    soma = 0

                                soma_ess_discharging = soma + soma_ess_discharging
                                cont_ess = cont_ess + 1

                    Gptotal_ESS.append(soma_ess_discharging - soma_ess_charging)


                    dem_fault = dem_ultrap - sum_gen_ufv - soma_ess_discharging + soma_ess_charging
                    if dem_fault >= 0:
                        lista_despacho = myfunctions.create_lista_despacho(tam_list_com, lista_completa, dem_fault,
                                                                           bloqueador)
                        tam_list_desp = len(lista_despacho)  # lista despacho final completa para do diesel

                        if tam_list_desp == 0:
                            despacho = myfunctions.verifica_bloqueador_nao_ultrap(l_sol, i, cont_desbloc,
                                                                                  cont_reab,
                                                                                  bloqueador, aut, cont_aut, cont_bloc,
                                                                                  reab)
                            l_sol.append(despacho)
                            bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc = myfunctions.verifica_bloqueador_ultrap(
                                l_sol, i, cont_desbloc, cont_reab, bloqueador, aut, cont_aut, cont_bloc, reab)

                        else:
                            lista_diesel = myfunctions.create_lista_diesel(tam_list_desp, lista_despacho, G)
                            voltage_tests = []
                            solutions = []
                            dif_voltages = []
                            cost_kwh = 0.35
                            cost_v = 1000
                            cost_fp = 500
                            cost_kw = 30
                            cost_diesel = 5.5
                            for lista in lista_diesel:
                                #self.dssObj.ClearAll()
                                #self.dssText.Command = "compile " + self.dssFileName
                                self.dssText.Command = "Set Hour = {}".format(time_sim)

                                diesel = lista[0]
                                for w in range(9):
                                    switchname = swt_lines[w]
                                    self.dssCircuit.Lines.Name = switchname.split(".")[1]
                                    if lista[1][0][w] == 0:
                                        oldBusName = self.dssCircuit.Lines.Bus2
                                        self.dssCircuit.Lines.Bus2 = "__opened__" + oldBusName
                                    else:
                                        self.dssCircuit.Lines.Bus2 = switchname.split(".")[1]

                                self.dssText.Command = 'Set maxiterations = 10'
                                self.dssSolution.Solve()

                                kwh_consumed = self.dssMeters.RegisterValues[0]/4

                                buses = self.dssCircuit.AllBusNames
                                for b in buses:
                                    self.dssCircuit.SetActiveBus(b)
                                    voltage_tests.append(self.dssBus.puVoltages[0])

                                tam1 = len(voltage_tests)
                                tam2 = len(Voltages_bus)

                                if tam1 >= tam2:
                                    delta = tam2
                                else:
                                    delta = tam1

                                for n in range(delta):
                                    dif_voltages.append((abs(voltage_tests[n] - Voltages_bus[n])))

                                power_circuit = self.dssCircuit.TotalPower
                                kw = -1 * power_circuit[0]
                                kvar = -1 * power_circuit[1]
                                kva = pow((kw * kw + kvar * kvar), 0.5)
                                PF_test = kw / kva

                                for v in dif_voltages:  # apaga as tensões dos geradores que entram e causam mais de 0.9 pu de variação
                                    if v > 0.5:
                                        index = dif_voltages.index(v)
                                        dif_voltages.pop(index)

                                v_test = 0
                                for vmax in dif_voltages:  # pegar o maior desvio de tensão para mensurar ele
                                    if vmax > v_test:
                                        v_test = vmax

                                if v_test > 0.05:
                                    max_v = v_test - 0.05
                                else:
                                    max_v = 0

                                if lista[1][1] - dem_fault >= 0:
                                    demand = 0
                                else:
                                    if dem_fault - lista[1][1] <= 250:
                                        demand = 0
                                    else:
                                        demand = dem_fault - lista[1][1]

                                total_cost = round((cost_diesel * diesel + cost_fp * (abs(PF_test - 0.92)) + cost_kwh *
                                                    kwh_consumed + cost_v * max_v + demand * 3 * cost_kw), 2)

                                solutions.append([total_cost, lista])

                            solutions.sort(reverse=False)
                            despacho = solutions[0][1][1][0]

                        l_sol.append(despacho)
                        bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc = myfunctions.verifica_bloqueador_ultrap(
                            l_sol, i, cont_desbloc, cont_reab, bloqueador, aut, cont_aut, cont_bloc, reab)


                    else:
                        despacho = myfunctions.verifica_bloqueador_nao_ultrap(l_sol, i, cont_desbloc, cont_reab,
                                                                              bloqueador,
                                                                              aut, cont_aut, cont_bloc, reab)
                        l_sol.append(despacho)
                        bloqueador, cont_aut, cont_reab, cont_bloc, cont_desbloc = myfunctions.verifica_bloqueador_ultrap(
                            l_sol, i, cont_desbloc, cont_reab, bloqueador, aut, cont_aut, cont_bloc, reab)


                self.dssText.Command = "Set Hour = {}".format(time_sim)

                for sw in range(9):
                    switchname = swt_lines[sw]
                    self.dssCircuit.Lines.Name = switchname.split(".")[1]
                    if l_sol[i][sw] == 0:
                        oldBusName = self.dssCircuit.Lines.Bus2
                        self.dssCircuit.Lines.Bus2 = "__opened__" + oldBusName
                    else:
                        self.dssCircuit.Lines.Bus2 = switchname.split(".")[1]

                self.dssSolution.Solve()
                tempo.append(self.dssSolution.dblHour)

                self.dssCircuit.SetActiveBus('219dBT')
                Voltages_219d.append(self.dssBus.puVoltages[0])


                self.dssMonitors.name = 'State1'  # channel 1 kWh medido
                kWhrated1 = self.dssMonitors.Channel(1)
                self.dssMonitors.name = 'State2'
                kWhrated2 = self.dssMonitors.Channel(1)
                self.dssMonitors.name = 'State3'
                kWhrated3 = self.dssMonitors.Channel(1)
                self.dssMonitors.name = 'State4'
                kWhrated4 = self.dssMonitors.Channel(1)

                self.dssMonitors.name = 'State1'  # channel 2 é -1 0 e 1
                SoC1 = self.dssMonitors.Channel(2)
                self.dssMonitors.name = 'State2'
                SoC2 = self.dssMonitors.Channel(2)
                self.dssMonitors.name = 'State3'
                SoC3 = self.dssMonitors.Channel(2)
                self.dssMonitors.name = 'State4'
                SoC4 = self.dssMonitors.Channel(2)

                self.dssMonitors.name = 'State1'  # channel 3 kW out
                kWratedin1 = self.dssMonitors.Channel(3)
                self.dssMonitors.name = 'State2'
                kWratedin2 = self.dssMonitors.Channel(3)
                self.dssMonitors.name = 'State3'
                kWratedin3 = self.dssMonitors.Channel(3)
                self.dssMonitors.name = 'State4'
                kWratedin4 = self.dssMonitors.Channel(3)
                sum_ess_discharging = float(kWratedin4[i] + kWratedin3[i] + kWratedin2[i] + kWratedin1[i])

                self.dssMonitors.name = 'State1'  # channel 4 kW in ou idling
                kWratedout1 = self.dssMonitors.Channel(4)
                self.dssMonitors.name = 'State2'
                kWratedout2 = self.dssMonitors.Channel(4)
                self.dssMonitors.name = 'State3'
                kWratedout3 = self.dssMonitors.Channel(4)
                self.dssMonitors.name = 'State4'
                kWratedout4 = self.dssMonitors.Channel(4)
                sum_ess_charging = float(kWratedout4[i] + kWratedout3[i] + kWratedout2[i] + kWratedout1[i])


                self.dssLines.name = 'G1'
                power_kw = self.dssCktElement.Powers
                p1_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G2'
                power_kw = self.dssCktElement.Powers
                p2_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G3'
                power_kw = self.dssCktElement.Powers
                p3_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G4'
                power_kw = self.dssCktElement.Powers
                p4_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G5'
                power_kw = self.dssCktElement.Powers
                p5_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G6'
                power_kw = self.dssCktElement.Powers
                p6_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G7'
                power_kw = self.dssCktElement.Powers
                p7_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G8'
                power_kw = self.dssCktElement.Powers
                p8_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                self.dssLines.name = 'G9'
                power_kw = self.dssCktElement.Powers
                p9_total_kw = power_kw[0] + power_kw[2] + power_kw[4]
                Gptotal_GMG.append(-1 * (p1_total_kw + p2_total_kw + p3_total_kw + p4_total_kw + p5_total_kw +
                                         p6_total_kw + p7_total_kw + p8_total_kw + p9_total_kw))

                Gptotal_UFV.append(sum_gen_ufv)

                dem_lida_GD.append(round(-1 * self.dssCircuit.TotalPower[0], 2))
                dem_lida.append(dem_lida_GD[i] + Gptotal_GMG[i] + Gptotal_UFV[i] + Gptotal_ESS[i])

                #generator_data = [dem_ultrap, "Solucao: ", l_sol[i], "autonomia: ", cont_aut, "reabastecimento: ", cont_reab,
                      #"Conta_block: ", cont_bloc, "Cont_desblock: ", cont_desbloc, "bloqueadr: ", bloqueador]

                #with open('dados_geradores_restricao.txt', 'a') as arquivo:
                    #arquivo.write("\n")
                    #arquivo.write(str(generator_data))

                #print(i, l_sol[i], "|", "G(kW):", round(Gptotal_GMG[i], 1), "|", "ESS (kW):", round(Gptotal_ESS[i], 1),
                      #"|", "UFV(kW):", round(Gptotal_UFV[i], 1), "|", "Ultrap:", round(dem_ultrap, 1), "|", "Dem_lida_GD: ",
                      #round(dem_lida_GD[i], 1), "|", "Dem_Prev: ", round(dem_prev[i], 1), "|",
                      #"Dem_Lida_Total(No_GD/ESS): ", round(dem_lida[i]), 1, "|", "Tensão: ", round(Voltages_219d [i], 4))

                resultado = [i, l_sol[i], "G(kW):", round(Gptotal_GMG[i], 1), "ESS (kW):", round(Gptotal_ESS[i], 1),
                             "UFV(kW):", round(Gptotal_UFV[i], 1), "Dem_lida_GD: ", round(dem_lida_GD[i], 1),
                             "Dem_Prev: ", round(dem_prev[i], 1), "Tensão: ", round(Voltages_219d[i], 4)]

                #with open('dados_rede_GMG+UFV+ESS.txt', 'a') as arquivo:
                    #arquivo.write("\n")
                    #arquivo.write(str(resultado))

                #print(resultado)

        energy_consumed = self.dssMeters.RegisterValues[0]/4

        print(energy_consumed)
        #myfunctions.plot_general(dem_lida_GD, dem_lida, Gptotal_GMG, Gptotal_UFV, Gptotal_ESS, SoC1)
        #myfunctions.plot_kwhstored(kWhrated1, kWhrated2, kWhrated3, kWhrated4)
        #myfunctions.plot_kwstored(kWratedin1, kWratedin2, kWratedin3, kWratedin4)
        #myfunctions.plot_SoC(SoC1, SoC2, SoC3, SoC4)
        #myfunctions.plot_voltage_bus(Voltages_219d)

        l_diesel = 0
        for solution in l_sol:
            for zz in range(9):
                l_diesel = l_diesel + solution[zz] * G[zz][1]

        reais = (l_diesel) * 6
        print(l_diesel,  "R$ ", reais)

        #self.dssText.command = "Export monitors SE"



if __name__ == '__main__':

    myObject = DSS(r"T:\Doctor_Degree_EE\Projeto_Doutorado_yearly_COM_ESS\Mestre.dss")
    myObject.solve_Yearly()


