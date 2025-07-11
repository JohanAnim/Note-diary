# -*- coding: utf-8 -*-

import re
import os

def main():
    """
    Función principal para generar el archivo de cambios de la última versión.
    """
    try:
        # 1. Leer la versión desde buildVars.py
        with open("buildVars.py", "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'addon_version":\s*"([^"]+)"', content)
            if not match:
                raise ValueError("No se pudo encontrar la versión en buildVars.py")
            current_version = match.group(1)

        # 2. Leer CHANGELOG.md
        with open("CHANGELOG.md", "r", encoding="utf-8") as f:
            changelog_content = f.read()

        # 3. Extraer los cambios para la versión actual
        pattern = re.compile(
            r"(##\s+" + re.escape(current_version) + r".*?)(?=##\s+\d|\Z)",
            re.DOTALL | re.IGNORECASE
        )
        match = pattern.search(changelog_content)

        if not match:
            raise ValueError(f"No se encontraron cambios para la versión {current_version} en CHANGELOG.md")

        version_changes = match.group(1).strip()

        # 4. Escribir en cambios.txt
        output_path = os.path.join("addon", "globalPlugins", "note diary", "cambios.txt")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(version_changes)

        print(f"Archivo de cambios generado exitosamente para la versión {current_version} en {output_path}")

    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
