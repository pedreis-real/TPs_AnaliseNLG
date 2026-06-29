def run_tp08(self):
    ea_0 = 133.865
    h_val = 2.0
    l_val = 2.0
    
    y_val = np.arange(2.0, -4.01, -0.02)
    lamb = np.sqrt((l_val**2 + y_val**2) / (l_val**2 + h_val**2))
    cos_alpha = y_val / np.sqrt(y_val**2 + l_val**2)
    
    k_const = 3 * ea_0 * cos_alpha
    
    p_green = -k_const * 0.5 * lamb * (lamb**2 - 1)
    p_biot = -k_const * (lamb - 1)
    p_log = -k_const * (np.log(lamb) / lamb)
    p_hyp = -k_const * ((lamb - 1) / lamb**3)
    p_alm = -k_const * ((lamb**2 - 1) / lamb**5)
    
    idx1 = np.where(y_val >= -1e-5)[0]                            
    idx2 = np.where((y_val <= 1e-5) & (y_val >= -2.0 - 1e-5))[0]  
    idx3 = np.where(y_val <= -2.0 + 1e-5)[0]                      
    
    curves = [
        (p_green, r"Green"),
        (p_biot, r"Biot"),
        (p_log, r"Logaritmica"),
        (p_hyp, r"Hiperbolica"),
        (p_alm, r"Almansi")
    ]

    self._plotter.create_plot("TP08")
    for p_curve, label in curves:
        # 1. Ramo inferior
        c, m = self._plotter.add_curve(
            lamb[idx2], p_curve[idx2], label=label, linestyle="-"
        )
        # 2. Ramo superior (tracejado e sem marcador)
        self._plotter.add_curve(
            lamb[idx1], p_curve[idx1], color=c, marker="None", linestyle="--", no_legend=True
        )
        # 3. Ramo de tracao
        self._plotter.add_curve(
            lamb[idx3], p_curve[idx3], color=c, marker=m, linestyle="-", no_legend=True
        )
        
    self._plotter.configure(
        r"$\lambda$", r"$P$ (kN)", r"TP08: $P \times \lambda$"
    )