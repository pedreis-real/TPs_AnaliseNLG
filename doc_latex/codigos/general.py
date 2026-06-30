import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from pathlib import Path

# Cores estritamente escuras e distintas
_GLOBAL_COLORS = [
    "#000080", # Azul Marinho
    "#008000", # Verde Escuro
    "#f58231", # Laranja Queimado
    "#911eb4", # Roxo Escuro
    "#00002D", # Preto Azulado
    "#469990", # Cerceta / Azul Petroleo
    "#e6194b", # Vermelho Carmesim
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

# Pasta de output
_ROOT = Path(__file__).parent
_DOC_DIR = _ROOT / "doc_latex"
_FIG_DIR = _DOC_DIR / "figuras"
OUT_DIR = _FIG_DIR / "resultados"

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

    def create_plot(self, tp_name, aspect_equal=False, fig = None):
        """Inicializa uma nova figura com a cor de fundo solicitada."""
        fig, ax = plt.subplots(figsize=(8, 6) if fig == None else fig)
        
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

    def add_curve(
        self,
        x, y,
        label=None,
        sec_x=False,
        linestyle="-", color=None, marker=None,
        no_legend=False
    ):
        """Adiciona uma curva, permitindo sobreposicao de cor e marcador."""
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
            
            filepath = Path(OUT_DIR / filename).resolve()
            # Garante a manutencao da cor de fundo ao salvar o PDF
            fig.savefig(filepath, facecolor='#f9f9f9')
            print(f"Salvo localmente: {filepath}")
            
        plt.show()


class GeometricNonLinearAnalysis:
    """Classe principal com metodos para cada TP da disciplina."""

    def __init__(self):
        self._plotter = Plotter()
        self._helpers = _Helpers()