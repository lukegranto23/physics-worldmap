"""Figure: noise-attribution curves f_noise(sigma) for the speed-persistence coupling, with lab 51's lower bound.

Reads saved results only (labs 49, 50, 51); no data access needed.
    python 52_speed_persistence_figure.py
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
R = HERE / "results"


def main():
    iv = {r["label"]: r for r in json.loads((R / "speed_persistence_noise/celltrackR/results.json").read_text())["runs"]}
    vt = {r["label"]: r for r in json.loads((R / "in_vitro_speed_persistence/zenodo_8420011/results.json").read_text())["runs"]}
    br = json.loads((R / "in_vitro_speed_persistence/noise_bracket_post_hoc.json").read_text())["groups"]
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for r, col, ls, lab in [(vt["ICAM"], "C0", "-", "in vitro T cells, ICAM-1"), (vt["VCAM"], "C1", "-", "in vitro T cells, VCAM-1"),
                            (iv["BCells"], "C2", "--", "in vivo B cells (lymph node)")]:
        g = np.array(r["sigma_grid"])
        ax.plot(g, np.array(r["f_noise_curve"], float), ls, color=col, label=f"{lab} (gap {r['G_raw']:.2f})")
        ax.fill_between(g, np.array(r["f_noise_16"], float), np.array(r["f_noise_84"], float), color=col, alpha=0.15)
    for k, col in (("ICAM", "C0"), ("VCAM", "C1")):
        ax.axvline(br[k]["sigma_lo"], color=col, lw=1.2, ls="-.")
    ax.text(0.665, 0.22, "dash-dot: conservative lower bounds\non σ from near-immobile in vitro\ntracks; the true σ lies to the right", fontsize=7)
    ax.axvline(0.645, color="k", lw=0.7, ls=":"); ax.text(0.655, 0.05, "1 pixel", fontsize=7)
    ax.axhline(0.5, color="k", lw=0.5)
    ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.2)
    ax.set_xlabel("assumed localization error σ (µm)")
    ax.set_ylabel("fraction of speed–persistence gap due to noise")
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    fig.savefig(R / "in_vitro_speed_persistence/sensitivity_curves.png", dpi=160)


if __name__ == "__main__":
    main()
