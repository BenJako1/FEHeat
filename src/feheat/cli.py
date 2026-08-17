import argparse
import os
from pathlib import Path
from .case import Case

def main():
    parser = argparse.ArgumentParser(description="Run an FEHeat heat-transfer simulation.")

    parser.add_argument("case", type=Path, nargs="?", default=Path.cwd(), help="Path to the case directory (default: current directory)")

    args = parser.parse_args()

    case = Case(args.case)

    case = Case(os.getcwd())

    case.load_element()

    case.load_mesh()

    case.apply_properties()

    case.assemble()

    case.apply_boundary_conditions()

    case.solve()

    case.output()


if __name__ == "__main__":
    main()