def run_tp09(self):
    e_val = 20000.0
    l_val = 150.0
    h_val = 10.0
    a_0 = 5.0
    p_ext = 20.0
    
    c_0 = np.sqrt(h_val**2 + l_val**2)
    k_nr = (e_val * a_0) / (c_0**3)
    
    def _res_func(v):
        return k_nr * (v**3 + 3 * h_val * v**2 + 2 * h_val**2 * v) - p_ext

    def _hess_func(v):
        return k_nr * (3 * v**2 + 6 * h_val * v + 2 * h_val**2)

    v_0 = (p_ext * l_val / (2 * e_val * a_0)) * (1 + (l_val / h_val)**2)
    
    try:
        v_sol, iters = self._helpers.solve_newton_raphson(
            _res_func, _hess_func, v_0, tol=0.001
        )
        print("TP09 - Metodo de Newton-Raphson:")
        print(f" -> Convergiu em {iters} iteracoes.")
        
        v_0_str = f"{v_0:.4f}".replace('.', ',')
        v_sol_str = f"{v_sol:.4f}".replace('.', ',')
        pct_str = f"{(v_sol / v_0) * 100:.2f}".replace('.', ',')
        
        print(f" -> Chute inicial (linear): {v_0_str} cm")
        print(f" -> Deslocamento vertical final v: {v_sol_str} cm")
        print(f" -> v / v_linear: {pct_str} %")
        
    except ValueError as e:
        print(f"TP09 - Erro: {e}")