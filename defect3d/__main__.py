"""
Punto de entrada del módulo / Module entry point.

Uso / Usage:
  python -m defect3d                         # descripción completa
  python -m defect3d --version               # versión
  python -m defect3d --list                  # clases públicas
  python -m defect3d --ecosystem             # proveedores/capacidades 3D
  python -m defect3d --validate-asset FILE   # valida contrato Mamba3D
  python -m defect3d --plan-asset FILE       # plan integrado cross-repo
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m defect3d",
        description=(
            "3defect / Mamba3D — Sistema integrado de modelado 3D\n"
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
        help="Lista todas las clases públicas disponibles / List public classes",
    )
    parser.add_argument(
        "--ecosystem",
        action="store_true",
        help="Muestra el registro integrado de repositorios/capacidades Mamba3D",
    )
    parser.add_argument(
        "--validate-asset",
        metavar="FILE",
        help="Valida un manifest JSON contra el contrato Mamba3D",
    )
    parser.add_argument(
        "--plan-asset",
        metavar="FILE",
        help="Genera el plan cross-repository para un manifest Mamba3D",
    )
    return parser


def _load_json(path_value: str) -> Mapping[str, Any]:
    path = Path(path_value)
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load JSON asset manifest: {exc}") from exc

    if not isinstance(data, dict):
        raise ValueError("asset manifest root must be a JSON object")
    return data


def _print_json(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))


def main() -> None:
    import defect3d

    parser = _build_parser()
    args = parser.parse_args()

    if args.version:
        print(f"defect3d {defect3d.__version__}")
        sys.exit(0)

    if args.list:
        print(
            f"defect3d {defect3d.__version__} — "
            "clases disponibles / available classes:\n"
        )
        for name in sorted(defect3d.__all__):
            obj = getattr(defect3d, name, None)
            doc = (
                (getattr(obj, "__doc__", None) or "").strip().splitlines()[0]
                if obj else ""
            )
            print(f"  {name:<20} {doc}")
        sys.exit(0)

    if args.ecosystem:
        from defect3d.integrations import ecosystem_summary

        _print_json(ecosystem_summary())
        sys.exit(0)

    if args.validate_asset:
        from defect3d.asset_contract import validate_asset_contract

        try:
            data = _load_json(args.validate_asset)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(2)

        errors = validate_asset_contract(data)
        result = {
            "asset_id": data.get("asset_id"),
            "valid": not errors,
            "errors": errors,
        }
        _print_json(result)
        sys.exit(0 if not errors else 1)

    if args.plan_asset:
        from defect3d.pipeline import plan_asset_pipeline

        try:
            data = _load_json(args.plan_asset)
        except ValueError as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            sys.exit(2)

        plan = plan_asset_pipeline(data)
        _print_json(plan)
        sys.exit(0 if plan["contract_valid"] else 1)

    defect3d.describe()


if __name__ == "__main__":
    main()
