def run_tp02(self):
    k_mola = 1.0
    l_val = 100.0
    theta = np.linspace(0, np.pi/2, 200)
    
    delta_h = l_val * np.sin(theta)
    delta_v = l_val * (1 - np.cos(theta))
    p_val = k_mola * l_val * np.cos(theta)
    
    self._plotter.create_plot("TP02")
    self._plotter.add_curve(delta_v, p_val, label=r"$\delta_v$")
    self._plotter.add_curve(delta_h, p_val, label=r"$\delta_h$")
    self._plotter.add_curve(theta, p_val, label=r"$\theta$", sec_x=True)
    self._plotter.configure(
        r"$\delta$ (cm)", r"$P$ (kN)", 
        r"TP02: $P \times \delta$ e $P \times \theta$",
        sec_x_lab=r"$\theta$ (rad)",
        is_theta_sec_x=True, max_theta=np.pi/2
    )