dem_ess = dem_ultrap - sum_gen_ufv

if dem_ess <= 0:
    for ess_name in ess_names:
        self.dssText.command = '{}.State = Idling'.format(ess_name)

    dem_fault = dem_ess

else:
    pu_soc_total = 0
    for ess_name in ess_names:
        self.dssCircuit.SetActiveElement(ess_name)
        pu_soc = float(self.dssCktElement.Properties('%stored').val)


