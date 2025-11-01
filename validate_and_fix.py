#!/usr/bin/env python3
"""
Script de Validación y Reparación / Validation and Repair Script

Este script valida el código Python, detecta errores y aplica reparaciones automáticas.
This script validates Python code, detects errors, and applies automatic repairs.

Funcionalidad / Functionality:
- Validación de sintaxis / Syntax validation
- Análisis de estilo (flake8, pylint) / Style analysis
- Reparación automática de problemas comunes / Auto-fix common issues
- Reporte detallado de errores / Detailed error reporting
- Optimización de código / Code optimization

Uso / Usage:
    python validate_and_fix.py [opciones]

Opciones / Options:
    --fix             Aplicar reparaciones automáticas / Apply automatic fixes
    --check-only      Solo verificar sin reparar / Only check without fixing
    --verbose         Modo verboso / Verbose mode
    --report FILE     Guardar reporte en archivo / Save report to file
"""

import os
import sys
import subprocess
import re
import ast
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import argparse


class CodeValidator:
    """Validador y reparador de código / Code validator and repairer."""

    def __init__(self, project_root: str, verbose: bool = False):
        """
        Inicializa el validador.
        Initialize the validator.

        Args:
            project_root: Ruta raíz del proyecto / Project root path
            verbose: Modo verboso / Verbose mode
        """
        self.project_root = Path(project_root)
        self.verbose = verbose
        self.issues_found = []
        self.fixes_applied = []
        self.colors = {
            'RED': '\033[91m',
            'GREEN': '\033[92m',
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'RESET': '\033[0m',
            'BOLD': '\033[1m'
        }

    def log(self, message: str, color: str = 'RESET', bold: bool = False):
        """Registra un mensaje con color / Log a message with color."""
        if self.verbose or color in ['RED', 'GREEN', 'YELLOW']:
            prefix = self.colors['BOLD'] if bold else ''
            print(f"{prefix}{self.colors[color]}{message}{self.colors['RESET']}")

    def run_command(self, cmd: List[str]) -> Tuple[int, str, str]:
        """
        Ejecuta un comando y retorna el resultado.
        Run a command and return the result.
        """
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
                check=False
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)

    def find_python_files(self) -> List[Path]:
        """
        Encuentra todos los archivos Python en el proyecto.
        Find all Python files in the project.
        """
        python_files = []
        exclude_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', '.venv'}

        for root, dirs, files in os.walk(self.project_root):
            # Remove excluded directories from search
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)

        return python_files

    def validate_syntax(self, file_path: Path) -> List[str]:
        """
        Valida la sintaxis de un archivo Python.
        Validate Python file syntax.
        """
        errors = []
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            ast.parse(code)
            self.log(f"✓ Sintaxis válida / Valid syntax: {file_path.name}", 'GREEN')
        except SyntaxError as e:
            error_msg = f"Error de sintaxis / Syntax error in {file_path}: {e}"
            errors.append(error_msg)
            self.log(f"✗ {error_msg}", 'RED')
            self.issues_found.append({
                'file': str(file_path),
                'type': 'syntax_error',
                'message': str(e),
                'line': e.lineno
            })
        except Exception as e:
            error_msg = f"Error al leer / Error reading {file_path}: {e}"
            errors.append(error_msg)
            self.log(f"✗ {error_msg}", 'RED')

        return errors

    def fix_whitespace_issues(self, file_path: Path) -> int:
        """
        Repara problemas de espacios en blanco.
        Fix whitespace issues.
        """
        fixes = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            modified = False
            new_lines = []

            for line in lines:
                original_line = line
                # Remove trailing whitespace
                line = line.rstrip() + '\n' if line.endswith('\n') else line.rstrip()

                if line != original_line:
                    fixes += 1
                    modified = True

                new_lines.append(line)

            # Remove trailing newlines but keep one
            while len(new_lines) > 1 and new_lines[-1].strip() == '':
                new_lines.pop()
                modified = True

            if new_lines and not new_lines[-1].endswith('\n'):
                new_lines[-1] += '\n'
                modified = True

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)

                self.log(f"  → Reparados {fixes} problemas de espacios / Fixed {fixes} whitespace issues", 'CYAN')
                self.fixes_applied.append({
                    'file': str(file_path),
                    'type': 'whitespace',
                    'count': fixes
                })

        except Exception as e:
            self.log(f"  ✗ Error al reparar espacios / Error fixing whitespace: {e}", 'RED')

        return fixes

    def remove_unused_imports(self, file_path: Path) -> int:
        """
        Elimina imports no utilizados.
        Remove unused imports.
        """
        # This is a simple implementation
        # For production, consider using autoflake or similar
        fixes = 0

        try:
            # Run autoflake if available
            cmd = ['python', '-m', 'autoflake', '--remove-all-unused-imports', '--in-place', str(file_path)]
            returncode, stdout, stderr = self.run_command(cmd)

            if returncode == 0:
                # Count fixes from output
                if "imports removed" in stdout.lower() or stderr:
                    fixes = 1
                    self.log(f"  → Imports no utilizados eliminados / Unused imports removed", 'CYAN')
                    self.fixes_applied.append({
                        'file': str(file_path),
                        'type': 'unused_imports',
                        'count': 1
                    })
        except Exception as e:
            self.log(f"  ⓘ autoflake no disponible / autoflake not available: {e}", 'YELLOW')

        return fixes

    def fix_encoding_issues(self, file_path: Path) -> int:
        """
        Agrega especificación de encoding explícita a open().
        Add explicit encoding specification to open().
        """
        fixes = 0
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Pattern to match open() without encoding
            pattern = r'\bopen\s*\([^)]*\)'

            def add_encoding(match):
                call = match.group(0)
                # Check if encoding is already specified
                if 'encoding=' in call:
                    return call
                # Add encoding before the closing parenthesis
                if call.endswith(')'):
                    return call[:-1] + ", encoding='utf-8')"
                return call

            new_content = re.sub(pattern, add_encoding, content)

            if new_content != content:
                fixes = content.count('open(') - new_content.count("encoding='utf-8'")
                # Don't actually modify - this is complex and needs manual review
                self.log(f"  ⓘ {fixes} llamadas a open() sin encoding / open() calls without encoding found", 'YELLOW')
                self.issues_found.append({
                    'file': str(file_path),
                    'type': 'encoding_warning',
                    'message': f'{fixes} open() calls without explicit encoding',
                    'severity': 'warning'
                })

        except Exception as e:
            self.log(f"  ✗ Error al verificar encoding / Error checking encoding: {e}", 'RED')

        return 0  # Don't auto-fix this

    def run_flake8(self) -> Dict:
        """
        Ejecuta flake8 en el proyecto.
        Run flake8 on the project.
        """
        self.log("\n" + "="*60, 'BLUE', True)
        self.log("Ejecutando flake8 / Running flake8...", 'BLUE', True)
        self.log("="*60, 'BLUE', True)

        cmd = [
            'python', '-m', 'flake8',
            'defect3d/',
            '--count',
            '--max-line-length=120',
            '--statistics'
        ]

        returncode, stdout, stderr = self.run_command(cmd)

        results = {
            'success': returncode == 0,
            'output': stdout,
            'errors': stderr,
            'issues': []
        }

        if stdout:
            # Parse flake8 output
            for line in stdout.split('\n'):
                if ':' in line and line.strip():
                    self.log(f"  {line}", 'YELLOW')
                    results['issues'].append(line)

        if returncode == 0:
            self.log("\n✓ flake8: Sin problemas / No issues found!", 'GREEN', True)
        else:
            self.log(f"\n⚠ flake8: {len(results['issues'])} problemas encontrados / issues found", 'YELLOW', True)

        return results

    def run_pylint(self) -> Dict:
        """
        Ejecuta pylint en el proyecto.
        Run pylint on the project.
        """
        self.log("\n" + "="*60, 'BLUE', True)
        self.log("Ejecutando pylint / Running pylint...", 'BLUE', True)
        self.log("="*60, 'BLUE', True)

        cmd = [
            'python', '-m', 'pylint',
            'defect3d/',
            '--disable=C,R',  # Disable convention and refactor messages
            '--max-line-length=120'
        ]

        returncode, stdout, stderr = self.run_command(cmd)

        results = {
            'success': returncode == 0,
            'output': stdout,
            'errors': stderr,
            'score': None
        }

        if stdout:
            # Extract score
            score_match = re.search(r'rated at ([\d.]+)/10', stdout)
            if score_match:
                results['score'] = float(score_match.group(1))

            # Show only important messages
            lines = stdout.split('\n')
            for line in lines:
                if any(marker in line for marker in ['*****', 'E0', 'W0', 'F0', 'rated at']):
                    self.log(f"  {line}", 'CYAN')

        if results['score']:
            score = results['score']
            if score >= 9.0:
                self.log(f"\n✓ pylint: Puntuación excelente / Excellent score: {score}/10", 'GREEN', True)
            elif score >= 7.0:
                self.log(f"\n⚠ pylint: Puntuación buena / Good score: {score}/10", 'YELLOW', True)
            else:
                self.log(f"\n✗ pylint: Puntuación baja / Low score: {score}/10", 'RED', True)

        return results

    def check_security_issues(self) -> List[Dict]:
        """
        Verifica problemas de seguridad comunes.
        Check for common security issues.
        """
        self.log("\n" + "="*60, 'BLUE', True)
        self.log("Verificando seguridad / Checking security...", 'BLUE', True)
        self.log("="*60, 'BLUE', True)

        security_issues = []
        python_files = self.find_python_files()

        # Patterns to check
        patterns = {
            'eval': r'\beval\s*\(',
            'exec': r'\bexec\s*\(',
            'pickle': r'import\s+pickle',
            'shell': r'shell\s*=\s*True',
            'hardcoded_password': r'password\s*=\s*["\'][^"\']+["\']'
        }

        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                for issue_type, pattern in patterns.items():
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # Count line number
                        line_num = content[:match.start()].count('\n') + 1

                        security_issues.append({
                            'file': str(file_path),
                            'type': issue_type,
                            'line': line_num,
                            'match': match.group(0)
                        })

                        self.log(
                            f"  ⚠ {file_path.name}:{line_num} - "
                            f"Posible problema de seguridad / Possible security issue: {issue_type}",
                            'YELLOW'
                        )

            except Exception as e:
                self.log(f"  ✗ Error al verificar {file_path}: {e}", 'RED')

        if not security_issues:
            self.log("\n✓ Sin problemas de seguridad obvios / No obvious security issues!", 'GREEN', True)
        else:
            self.log(
                f"\n⚠ {len(security_issues)} posibles problemas de seguridad encontrados / "
                f"possible security issues found",
                'YELLOW',
                True
            )

        return security_issues

    def validate_project(self, fix: bool = False) -> Dict:
        """
        Valida el proyecto completo.
        Validate the entire project.

        Args:
            fix: Si es True, aplica reparaciones automáticas / If True, apply automatic fixes
        """
        self.log("\n" + "="*60, 'MAGENTA', True)
        self.log("INICIANDO VALIDACIÓN / STARTING VALIDATION", 'MAGENTA', True)
        self.log("="*60 + "\n", 'MAGENTA', True)

        results = {
            'timestamp': datetime.now().isoformat(),
            'syntax_errors': [],
            'flake8': {},
            'pylint': {},
            'security_issues': [],
            'fixes_applied': [],
            'summary': {}
        }

        # Find all Python files
        python_files = self.find_python_files()
        self.log(f"Encontrados {len(python_files)} archivos Python / Found {len(python_files)} Python files\n", 'CYAN')

        # Validate syntax
        self.log("="*60, 'BLUE', True)
        self.log("Validando sintaxis / Validating syntax...", 'BLUE', True)
        self.log("="*60, 'BLUE', True)

        for file_path in python_files:
            errors = self.validate_syntax(file_path)
            if errors:
                results['syntax_errors'].extend(errors)

        # Apply fixes if requested
        if fix:
            self.log("\n" + "="*60, 'BLUE', True)
            self.log("Aplicando reparaciones / Applying fixes...", 'BLUE', True)
            self.log("="*60, 'BLUE', True)

            for file_path in python_files:
                self.log(f"\nProcesando / Processing: {file_path.name}", 'CYAN')

                # Fix whitespace
                self.fix_whitespace_issues(file_path)

                # Check encoding (warning only)
                self.fix_encoding_issues(file_path)

            results['fixes_applied'] = self.fixes_applied

        # Run linters
        results['flake8'] = self.run_flake8()
        results['pylint'] = self.run_pylint()

        # Check security
        results['security_issues'] = self.check_security_issues()

        # Generate summary
        results['summary'] = {
            'total_files': len(python_files),
            'syntax_errors': len(results['syntax_errors']),
            'flake8_issues': len(results['flake8'].get('issues', [])),
            'pylint_score': results['pylint'].get('score'),
            'security_issues': len(results['security_issues']),
            'fixes_applied': len(self.fixes_applied),
            'overall_health': 'good' if len(results['syntax_errors']) == 0 else 'needs_attention'
        }

        return results

    def print_summary(self, results: Dict):
        """
        Imprime un resumen de los resultados.
        Print a summary of results.
        """
        self.log("\n" + "="*60, 'MAGENTA', True)
        self.log("RESUMEN / SUMMARY", 'MAGENTA', True)
        self.log("="*60, 'MAGENTA', True)

        summary = results['summary']

        self.log(f"\n📊 Archivos analizados / Files analyzed: {summary['total_files']}", 'CYAN', True)

        if summary['syntax_errors'] == 0:
            self.log(f"✓ Errores de sintaxis / Syntax errors: 0", 'GREEN', True)
        else:
            self.log(f"✗ Errores de sintaxis / Syntax errors: {summary['syntax_errors']}", 'RED', True)

        if summary['flake8_issues'] == 0:
            self.log(f"✓ Problemas de estilo (flake8): 0", 'GREEN', True)
        else:
            self.log(f"⚠ Problemas de estilo (flake8): {summary['flake8_issues']}", 'YELLOW', True)

        if summary['pylint_score']:
            score = summary['pylint_score']
            color = 'GREEN' if score >= 9.0 else 'YELLOW' if score >= 7.0 else 'RED'
            self.log(f"📈 Puntuación pylint / pylint score: {score}/10", color, True)

        if summary['security_issues'] == 0:
            self.log(f"✓ Problemas de seguridad / Security issues: 0", 'GREEN', True)
        else:
            self.log(f"⚠ Posibles problemas de seguridad / Possible security issues: {summary['security_issues']}", 'YELLOW', True)

        if summary['fixes_applied'] > 0:
            self.log(f"\n🔧 Reparaciones aplicadas / Fixes applied: {summary['fixes_applied']}", 'CYAN', True)

        # Overall health
        self.log("\n" + "="*60, 'MAGENTA', True)
        if summary['overall_health'] == 'good' and summary['syntax_errors'] == 0:
            self.log("✓ ESTADO: SALUDABLE / STATUS: HEALTHY", 'GREEN', True)
        else:
            self.log("⚠ ESTADO: REQUIERE ATENCIÓN / STATUS: NEEDS ATTENTION", 'YELLOW', True)
        self.log("="*60 + "\n", 'MAGENTA', True)

    def save_report(self, results: Dict, output_file: str):
        """
        Guarda el reporte en un archivo.
        Save report to a file.
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("REPORTE DE VALIDACIÓN / VALIDATION REPORT\n")
                f.write("="*60 + "\n\n")
                f.write(f"Fecha / Date: {results['timestamp']}\n\n")

                f.write("RESUMEN / SUMMARY\n")
                f.write("-"*60 + "\n")
                for key, value in results['summary'].items():
                    f.write(f"{key}: {value}\n")

                f.write("\n" + "="*60 + "\n")
                f.write("DETALLES / DETAILS\n")
                f.write("="*60 + "\n\n")

                if results['syntax_errors']:
                    f.write("Errores de Sintaxis / Syntax Errors:\n")
                    for error in results['syntax_errors']:
                        f.write(f"  - {error}\n")
                    f.write("\n")

                if results['security_issues']:
                    f.write("Problemas de Seguridad / Security Issues:\n")
                    for issue in results['security_issues']:
                        f.write(f"  - {issue['file']}:{issue['line']} - {issue['type']}\n")
                    f.write("\n")

                if results['fixes_applied']:
                    f.write("Reparaciones Aplicadas / Fixes Applied:\n")
                    for fix in results['fixes_applied']:
                        f.write(f"  - {fix['file']}: {fix['type']} ({fix['count']} fixes)\n")
                    f.write("\n")

            self.log(f"\n✓ Reporte guardado en / Report saved to: {output_file}", 'GREEN', True)

        except Exception as e:
            self.log(f"\n✗ Error al guardar reporte / Error saving report: {e}", 'RED', True)


def main():
    """Función principal / Main function."""
    parser = argparse.ArgumentParser(
        description='Valida y repara código Python / Validate and fix Python code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos / Examples:
  python validate_and_fix.py --check-only              # Solo verificar / Check only
  python validate_and_fix.py --fix                     # Verificar y reparar / Check and fix
  python validate_and_fix.py --fix --verbose           # Modo verboso / Verbose mode
  python validate_and_fix.py --fix --report report.txt # Guardar reporte / Save report
        """
    )

    parser.add_argument(
        '--fix',
        action='store_true',
        help='Aplicar reparaciones automáticas / Apply automatic fixes'
    )

    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Solo verificar sin reparar / Only check without fixing'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Modo verboso / Verbose mode'
    )

    parser.add_argument(
        '--report',
        type=str,
        metavar='FILE',
        help='Guardar reporte en archivo / Save report to file'
    )

    args = parser.parse_args()

    # Determine project root
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Create validator
    validator = CodeValidator(project_root, verbose=args.verbose or not args.check_only)

    # Run validation
    apply_fixes = args.fix and not args.check_only
    results = validator.validate_project(fix=apply_fixes)

    # Print summary
    validator.print_summary(results)

    # Save report if requested
    if args.report:
        validator.save_report(results, args.report)

    # Exit with appropriate code
    if results['summary']['syntax_errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
