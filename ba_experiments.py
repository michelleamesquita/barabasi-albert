import os
from dataclasses import dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


@dataclass
class BAParams:
    num_nodes: int = 10_000
    m: int = 4
    snapshot_sizes: Tuple[int, int, int] = (100, 1_000, 10_000)
    seed: int = 42


def build_ba_graph(params: BAParams) -> nx.Graph:
    """
    Build a BA graph with n=num_nodes, m, starting from a clique of size m.
    NetworkX uses a complete graph K_m as initial graph by default for BA.
    """
    return nx.barabasi_albert_graph(n=params.num_nodes, m=params.m, seed=params.seed)


def degrees_to_ccdf(degrees: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    if degrees.size == 0:
        return np.array([]), np.array([])
    k_min = int(np.min(degrees))
    k_max = int(np.max(degrees))
    k_vals = np.arange(k_min, k_max + 1)
    counts = np.bincount(degrees, minlength=k_max + 1)
    tail_counts = counts[k_vals[::-1]].cumsum()[::-1]
    ccdf = tail_counts / float(degrees.size)
    return k_vals, ccdf


def run_experiment(params: BAParams, out_dir: str) -> None:
    os.makedirs(out_dir, exist_ok=True)

    # Build single BA graph then slice snapshots by first N nodes
    g_full = build_ba_graph(params)

    # Ensure requested snapshots are valid
    snaps = sorted(set(params.snapshot_sizes))
    if snaps[-1] != params.num_nodes:
        raise ValueError("Largest snapshot must equal num_nodes")

    # Plot CCDFs
    fig, ax = plt.subplots(figsize=(6, 4))
    for n in snaps:
        nodes = list(range(n))
        g_n = g_full.subgraph(nodes)
        degs = np.array([d for _, d in g_n.degree()], dtype=int)
        k, ccdf = degrees_to_ccdf(degs)
        mask = k >= 1
        k = k[mask]
        ccdf = ccdf[mask]
        ax.loglog(k, ccdf, 'o', ms=3, linestyle='', label=f"N={n}")

    ax.set_xlabel("k (grau)")
    ax.set_ylabel("P(K ≥ k)")
    ax.set_title("BA – CCDF da distribuição de grau")
    ax.legend()
    fig.tight_layout()
    fig.savefig(os.path.join(out_dir, "ba_degree_ccdf.png"), dpi=160)
    plt.close(fig)

    # Top-20 and ratios per snapshot
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    for n in snaps:
        nodes = list(range(n))
        g_n = g_full.subgraph(nodes)
        deg_items = sorted(g_n.degree(), key=lambda t: (-t[1], t[0]))
        top20 = deg_items[:20]
        df = pd.DataFrame({
            "rank": [i + 1 for i in range(len(top20))],
            "node": [node for node, _ in top20],
            "degree": [deg for _, deg in top20],
        })
        df.to_csv(os.path.join(out_dir, f"top20_deg_N{n}.csv"), index=False)

        if len(top20) >= 2:
            dmax = float(top20[0][1])
            ratios = [dmax / float(deg) for _, deg in top20[1:]]
            pd.DataFrame({
                "rank": list(range(2, len(top20) + 1)),
                "ratio_dmax_over_d": ratios,
            }).to_csv(os.path.join(out_dir, f"top20_ratios_N{n}.csv"), index=False)

            ax2.plot(range(2, len(top20) + 1), ratios, 'o-', label=f"N={n}")

    ax2.set_xlabel("rank (2..20)")
    ax2.set_ylabel("d_max / d_rank")
    ax2.set_title("Razão entre maior grau e demais top-20")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig(os.path.join(out_dir, "top20_ratio_vs_rank.png"), dpi=160)
    plt.close(fig2)


def main() -> None:
    out_dir = os.path.join(os.path.dirname(__file__), "out")
    params = BAParams()
    run_experiment(params, out_dir)


if __name__ == "__main__":
    main()


