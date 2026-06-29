def run_tp05(self):
    ea_0 = 13865.0
    l_val = 400.0
    h_val = 20.0
    y_val = np.arange(40.0, 19.0, -1.0)
    
    beta_0 = np.arctan(h_val / l_val)
    delta_v = h_val - y_val
    beta = np.arctan(y_val / l_val)
    
    f_val = 2 * ea_0 * np.tan(beta) * (np.cos(beta_0) - np.cos(beta))
    n_val = f_val / (2 * np.sin(beta))
    
    self._plotter.create_plot("TP05")
    self._plotter.add_curve(delta_v, f_val, label=r"$F$")
    self._plotter.add_curve(delta_v, n_val, label=r"$N$")
    self._plotter.configure(
        r"$\delta_v$ (cm)", r"Esforco (N)", 
        r"TP05: $F, N \times \delta_v$"
    )