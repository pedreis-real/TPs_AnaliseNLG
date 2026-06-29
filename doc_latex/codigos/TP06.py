def run_tp06(self):
    lamb = np.linspace(0.1, 2.0, 200)
    
    eps_alm = 0.5 * (1 - 1 / lamb**2)
    eps_hyp = 1 - 1 / lamb
    eps_log = np.log(lamb)
    eps_biot = lamb - 1
    eps_green = 0.5 * (lamb**2 - 1)
    
    self._plotter.create_plot("TP06")
    self._plotter.add_curve(lamb, eps_alm, label=r"Almansi")
    self._plotter.add_curve(lamb, eps_hyp, label=r"Hiperbolica")
    self._plotter.add_curve(lamb, eps_log, label=r"Logaritmica")
    self._plotter.add_curve(lamb, eps_biot, label=r"Biot")
    self._plotter.add_curve(lamb, eps_green, label=r"Green")
    self._plotter.configure(
        r"$\lambda$", r"$\epsilon^*$", 
        r"TP06: Medidas de Deformacao", 
        log_y=False, y_min=-10.0
    )
    
    self._plotter.create_plot("TP06")
    self._plotter.add_curve(lamb, lamb**3, label=r"Almansi")
    self._plotter.add_curve(lamb, lamb**2, label=r"Hiperbolica")
    self._plotter.add_curve(lamb, lamb, label=r"Logaritmica")
    self._plotter.add_curve(lamb, np.ones_like(lamb), label=r"Biot")
    self._plotter.add_curve(lamb, 1 / lamb, label=r"Green")
    self._plotter.configure(
        r"$\lambda$", r"$\frac{\sigma^*}{\sigma_B}$", 
        r"TP06: Tensoes Normalizadas"
    )