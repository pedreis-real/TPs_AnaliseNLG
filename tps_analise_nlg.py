import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Cores estritamente escuras e distintas, sem vermelhos confusos
_GLOBAL_COLORS = [
    "#000080", # Azul Marinho
    "#008000", # Verde Escuro
    "#f58231", # Laranja Queimado
    "#911eb4", # Roxo Escuro
    "#000000", # Preto
    "#469990", # Cerceta / Azul Petroleo
    "#e6194b", # Vermelho Carmesim (Unico vermelho principal)
    "#9a6324", # Marrom
    "#808000", # Oliva
    "#1976d2", # Azul Forte
    "#388e3c", # Verde Floresta
    "#7b1fa2", # Violeta Profundo
    "#f57c00", # Laranja Escuro
    "#5d4037", # Marrom Cafe
    "#006064"  # Ciano Escuro
]
_global_color_idx = 0

# Marcadores para as curvas
_MARKERS = ["o", "s", "d", "+", "*"]

def _get_next_color():
    """Retorna a proxima cor garantindo a exclusividade no ciclo."""
    global _global_color_idx
    color = _GLOBAL_COLORS[_global_color_idx % len(_GLOBAL_COLORS)]
    _global_color_idx += 1
    return color

def _comma_fmt(x, pos):
    """Formata os rotulos dos eixos com virgula."""
    return f"{x:g}".replace('.', ',')

def _apply_pi_ticks(ax, max_theta):
    """Mapeia os eixos com fracoes notaveis de pi."""
    if max_theta <= np.pi/2 + 0.1:
        # Fracoes notaveis incluindo pi/12 e 5pi/12
        ticks = [0, np.pi/12, np.pi/6, np.pi/4, np.pi/3, 5*np.pi/12, np.pi/2]
        labels = ["0", r"$\pi/12$", r"$\pi/6$", r"$\pi/4$", r"$\pi/3$", r"$5\pi/12$", r"$\pi/2$"]
    elif max_theta <= np.pi + 0.1:
        ticks = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        labels = ["0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$"]
    else:
        ticks = [
            0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 
            5*np.pi/4, 3*np.pi/2, 7*np.pi/4, 2*np.pi
        ]
        labels = [
            "0", r"$\pi/4$", r"$\pi/2$", r"$3\pi/4$", r"$\pi$",
            r"$5\pi/4$", r"$3\pi/2$", r"$7\pi/4$", r"$2\pi$"
        ]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)


class _Helpers:
    """Classe contendo ferramentas numericas comuns."""

    @staticmethod
    def solve_newton_raphson(res_func, hess_func, x0, tol=1e-3, max_it=50):
        """Metodo de Newton-Raphson para equacoes nao lineares 1D."""
        x = float(x0)
        for i in range(max_it):
            res = res_func(x)
            if abs(res) <= tol:
                return x, i
            hess = hess_func(x)
            dx = -res / hess
            x = x + dx
        raise ValueError("Newton-Raphson nao convergiu.")


class Plotter:
    """Classe especifica para gerenciar todos os graficos solicitados."""

    def __init__(self):
        self._fig_list = []
        self._fig_names = []
        self._curr_ax = None
        self._twin_ax = None
        self._marker_idx = 0

    def create_plot(self, tp_name, aspect_equal=False):
        """Inicializa uma nova figura com a cor de fundo solicitada."""
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Aplicando a cor de fundo requerida para a figura e o eixo
        fig.patch.set_facecolor('#f9f9f9')
        ax.set_facecolor('#f9f9f9')
        
        if aspect_equal:
            ax.set_aspect('equal')
        self._curr_ax = ax
        self._twin_ax = None
        self._marker_idx = 0
        self._fig_list.append(fig)
        self._fig_names.append(tp_name)
        return ax

    def add_curve(self, x, y, label=None, sec_x=False, linestyle="-", color=None, marker=None, no_legend=False):
        """Adiciona uma curva, permitindo sobreposicao manual de cor e marcador."""
        if self._curr_ax is None:
            return None, None

        if color is None:
            color = _get_next_color()
        if marker is None:
            marker = _MARKERS[self._marker_idx % len(_MARKERS)]
            self._marker_idx += 1
        
        mk_ev = max(1, int(len(x) / 12.0))
        
        if sec_x:
            if self._twin_ax is None:
                self._twin_ax = self._curr_ax.twiny()
            ax = self._twin_ax
        else:
            ax = self._curr_ax
            
        ax.plot(
            x, y, color=color, marker=marker, markersize=4,
            markevery=mk_ev, label=label if not no_legend else None, 
            linestyle=linestyle
        )
        return color, marker

    def configure(self, x_lab, y_lab, title, sec_x_lab=None, 
                  log_y=False, is_theta_x=False, is_theta_sec_x=False, 
                  max_theta=np.pi/2, legend_loc='best', y_min=None):
        """Configura rotulos, legendas unificadas, grid e formatacao."""
        if self._curr_ax is None:
            return

        self._curr_ax.set_xlabel(x_lab)
        self._curr_ax.set_ylabel(y_lab)
        self._curr_ax.set_title(title)
        
        if sec_x_lab and self._twin_ax:
            self._twin_ax.set_xlabel(sec_x_lab)

        if log_y:
            self._curr_ax.set_yscale('symlog', linthresh=0.1)
            
        if y_min is not None:
            self._curr_ax.set_ylim(bottom=y_min)

        self._curr_ax.minorticks_on()
        self._curr_ax.grid(True, which='both', alpha=0.3)

        for ax in [self._curr_ax, self._twin_ax]:
            if ax is not None:
                ax.xaxis.set_major_formatter(ticker.FuncFormatter(_comma_fmt))
                ax.yaxis.set_major_formatter(ticker.FuncFormatter(_comma_fmt))

        if is_theta_x:
            _apply_pi_ticks(self._curr_ax, max_theta)
        if is_theta_sec_x and self._twin_ax:
            _apply_pi_ticks(self._twin_ax, max_theta)

        ln_1, lab_1 = self._curr_ax.get_legend_handles_labels()
        ln_2, lab_2 = [], []
        if self._twin_ax is not None:
            ln_2, lab_2 = self._twin_ax.get_legend_handles_labels()
            
        lns = ln_1 + ln_2
        labs = lab_1 + lab_2
        
        if lns:
            self._curr_ax.legend(lns, labs, loc=legend_loc)

    def save_all_and_show(self):
        """Salva todos os graficos em disco e os exibe no console/tela."""
        name_counts = {}
        for fig, name in zip(self._fig_list, self._fig_names):
            if name not in name_counts:
                name_counts[name] = 1
            else:
                name_counts[name] += 1
                
        current_counts = {name: 0 for name in name_counts}
        
        for fig, name in zip(self._fig_list, self._fig_names):
            fig.tight_layout()
            current_counts[name] += 1
            
            if name_counts[name] > 1:
                filename = f"{name}-result{current_counts[name]}.pdf"
            else:
                filename = f"{name}-result.pdf"
                
            # Garante a manutencao da cor de fundo ao salvar o PDF
            fig.savefig(filename, facecolor='#f9f9f9')
            print(f"Salvo localmente: {filename}")
            
        plt.show()


class GeometricNonLinearAnalysis:
    """Classe principal com metodos para cada TP da disciplina."""

    def __init__(self):
        self._plotter = Plotter()
        self._helpers = _Helpers()

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

    def run_tp03(self):
        k_mola = 1000.0
        l_val = 100.0
        theta = np.linspace(1e-5, np.pi/2 - 0.01, 200)
        
        delta_h = l_val * (1 - np.cos(theta))
        delta_v = l_val * np.sin(theta)
        p_val = (4 * k_mola / l_val) * (theta / np.cos(theta))
        
        self._plotter.create_plot("TP03")
        self._plotter.add_curve(delta_v, p_val, label=r"$\delta_v$")
        self._plotter.add_curve(delta_h, p_val, label=r"$\delta_h$")
        self._plotter.add_curve(theta, p_val, label=r"$\theta$", sec_x=True)
        self._plotter.configure(
            r"$\delta$ (cm)", r"$P$ (kN)", 
            r"TP03: $P \times \delta$ e $P \times \theta$",
            sec_x_lab=r"$\theta$ (rad)",
            log_y=True,
            is_theta_sec_x=True, max_theta=np.pi/2
        )

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
            r"$\delta_v$ (cm)", r"Esforço (N)", 
            r"TP05: $F, N \times \delta_v$"
        )

    def run_tp06(self):
        lamb = np.linspace(0.1, 2.0, 200)
        
        eps_alm = 0.5 * (1 - 1 / lamb**2)
        eps_hyp = 1 - 1 / lamb
        eps_log = np.log(lamb)
        eps_biot = lamb - 1
        eps_green = 0.5 * (lamb**2 - 1)
        
        self._plotter.create_plot("TP06")
        self._plotter.add_curve(lamb, eps_alm, label=r"Almansi")
        self._plotter.add_curve(lamb, eps_hyp, label=r"Hiperbólica")
        self._plotter.add_curve(lamb, eps_log, label=r"Logarítmica")
        self._plotter.add_curve(lamb, eps_biot, label=r"Biot")
        self._plotter.add_curve(lamb, eps_green, label=r"Green")
        self._plotter.configure(
            r"$\lambda$", r"$\epsilon^*$", 
            r"TP06: Medidas de Deformação", 
            log_y=False, y_min=-10.0
        )
        
        self._plotter.create_plot("TP06")
        self._plotter.add_curve(lamb, lamb**3, label=r"Almansi")
        self._plotter.add_curve(lamb, lamb**2, label=r"Hiperbólica")
        self._plotter.add_curve(lamb, lamb, label=r"Logarítmica")
        self._plotter.add_curve(lamb, np.ones_like(lamb), label=r"Biot")
        self._plotter.add_curve(lamb, 1 / lamb, label=r"Green")
        self._plotter.configure(
            r"$\lambda$", r"$\frac{\sigma^*}{\sigma_B}$", 
            r"TP06: Tensões Normalizadas"
        )

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
            (p_log, r"Logarítmica"),
            (p_hyp, r"Hiperbólica"),
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

    def save_and_display(self):
        """Salva todas as figuras criadas na chamada final e as exibe."""
        self._plotter.save_all_and_show()


if __name__ == '__main__':
    analysis = GeometricNonLinearAnalysis()
    
    analysis.run_tp01()
    analysis.run_tp02()
    analysis.run_tp03()
    analysis.run_tp04()
    analysis.run_tp05()
    analysis.run_tp06()
    analysis.run_tp08()
    analysis.run_tp09()
    
    analysis.save_and_display()