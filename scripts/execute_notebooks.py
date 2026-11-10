"""
Notebook Pre-rendering and Execution Engine.

Executes code cells in the 4 research notebooks and embeds formatted stdout
and base64-encoded PNG figures directly into the .ipynb JSON structures.
"""

import base64
import contextlib
import io
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR / "src"))
NOTEBOOKS_DIR = ROOT_DIR / "notebooks"


def execute_notebook_in_place(nb_path: Path):
    with open(nb_path, "r", encoding="utf-8") as f:
        nb_data = json.load(f)

    # Execution namespace shared across cells in this notebook
    exec_scope = {
        "__name__": "__main__",
        "__file__": str(nb_path),
    }

    cell_counter = 1

    for cell in nb_data.get("cells", []):
        if cell.get("cell_type") != "code":
            continue

        source_code = "".join(cell.get("source", []))
        cell["execution_count"] = cell_counter
        cell["outputs"] = []

        # Intercept stdout and plt figures
        stdout_buf = io.StringIO()
        plt.close("all")

        try:
            with contextlib.redirect_stdout(stdout_buf):
                # Replace plt.show() with a pass or figure capture hook
                exec(source_code, exec_scope)

            # Check for any active matplotlib figures
            fig_nums = plt.get_fignums()
            for fnum in fig_nums:
                fig = plt.figure(fnum)
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format="png", bbox_inches="tight", dpi=130)
                img_buf.seek(0)
                img_b64 = base64.b64encode(img_buf.getvalue()).decode("utf-8")

                cell["outputs"].append({
                    "data": {
                        "image/png": img_b64,
                        "text/plain": ["<Figure size ...>"]
                    },
                    "metadata": {},
                    "output_type": "display_data"
                })
                plt.close(fig)

            stdout_text = stdout_buf.getvalue()
            if stdout_text.strip():
                cell["outputs"].append({
                    "name": "stdout",
                    "output_type": "stream",
                    "text": [line + "\n" for line in stdout_text.splitlines()]
                })

        except Exception as e:
            cell["outputs"].append({
                "ename": type(e).__name__,
                "evalue": str(e),
                "output_type": "error",
                "traceback": [f"{type(e).__name__}: {str(e)}"]
            })

        cell_counter += 1

    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb_data, f, indent=1)

    print(f"[+] Successfully executed and pre-rendered: {nb_path.name}")


def main():
    print("=" * 70)
    print("  PRE-RENDERING AND EXECUTING 4 JUPYTER RESEARCH NOTEBOOKS")
    print("=" * 70)

    notebooks = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))
    for nb in notebooks:
        execute_notebook_in_place(nb)

    print("\nAll 4 notebooks pre-rendered with pre-computed outputs and charts!")


if __name__ == "__main__":
    main()
