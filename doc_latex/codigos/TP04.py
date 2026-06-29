def run_tp04(self):
    ei_val = 4e4
    l_val = 500.0
    
    theta = np.linspace(1e-5, 2 * np.pi, 200)
    m_val = (ei_val * theta) / l_val
    rho = l_val / theta
    
    u_val = l_val - rho * np.sin(theta)
    v_val = rho * (1 - np.cos(theta))
    
    self._plotter.create_plot("TP04")
    self._plotter.add_curve(u_val, m_val, label=r"$u$")
    self._plotter.add_curve(v_val, m_val, label=r"$v$")
    self._plotter.add_curve(theta, m_val, label=r"$\theta$", sec_x=True, linestyle="--")
    self._plotter.configure(
        r"Deslocamento (cm)", r"$M$ (N.cm)", 
        r"TP04: $M \times u$, $M \times v$ e $M \times \theta$",
        sec_x_lab=r"$\theta$ (rad)",
        is_theta_sec_x=True, max_theta=2*np.pi,
        legend_loc='lower right'
    )
    
    self._plotter.create_plot("TP04", aspect_equal=True)
    s = np.linspace(0, l_val, 11) 
    
    for t_val, t_label in zip([np.pi, 2 * np.pi], [r"\pi", r"2\pi"]):
        rho_s = l_val / t_val
        x_line = rho_s * np.sin(s / rho_s)
        v_line = rho_s * (1 - np.cos(s / rho_s))
        self._plotter.add_curve(
            x_line, v_line, label=rf"$\theta = {t_label}$"
        )
        
    self._plotter.configure(
        r"$x$ (cm)", r"$v$ (cm)", r"TP04: Linha Neutra",
        legend_loc='lower right'
    )