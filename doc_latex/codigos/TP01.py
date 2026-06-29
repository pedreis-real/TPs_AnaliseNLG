def run_tp01(self):
    k_mola = 1000.0
    l_val = 100.0
    
    theta = np.linspace(1e-5, np.pi/2, 200)
    delta_v = l_val * (1 - np.cos(theta))
    delta_h = l_val * np.sin(theta)
    p_val = (k_mola / l_val) * (theta / np.sin(theta))
    
    self._plotter.create_plot("TP01")
    self._plotter.add_curve(delta_v, p_val, label=r"$\delta_v$")
    self._plotter.add_curve(delta_h, p_val, label=r"$\delta_h$")
    self._plotter.add_curve(theta, p_val, label=r"$\theta$", sec_x=True)
    self._plotter.configure(
        r"$\delta$ (cm)", r"$P$ (kN)", 
        r"TP01: $P \times \delta$ e $P \times \theta$",
        sec_x_lab=r"$\theta$ (rad)",
        is_theta_sec_x=True, max_theta=np.pi/2
    )