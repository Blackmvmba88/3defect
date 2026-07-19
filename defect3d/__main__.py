"""
Punto de entrada del módulo / Module entry point.

Uso / Usage:
  python -m defect3d              # descripción completa / full description
  python -m defect3d --version    # sólo la versión / version only
  python -m defect3d --list       # clases disponibles / available classes
"""

import argparse
import sys


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m defect3d",
        description=(
            "3defect — Sistema de Modelado 3D / 3D Modeling System\n"
            "Ejecuta sin argumentos para ver la descripción completa.\n"
            "Run without arguments to see the full description."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--version", "-v",
        action="store_true",
        help="Muestra la versión del paquete / Show package version",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Lista todas las clases públicas disponibles / List all public classes",
    )
    return parser


def main() -> None:
    import defect3d

    parser = _build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"defect3d {defect3d.__version__}")
        sys.exit(0)

    if args.list:
        print(f"defect3d {defect3d.__version__} — clases disponibles / available classes:\n")
        for name in sorted(defect3d.__all__):
            obj = getattr(defect3d, name, None)
            doc = (getattr(obj, "__doc__", None) or "").strip().splitlines()[0] if obj else ""
            print(f"  {name:<20} {doc}")
        sys.exit(0)

    # default: full description
    defect3d.describe()


if __name__ == "__main__":
    main()
