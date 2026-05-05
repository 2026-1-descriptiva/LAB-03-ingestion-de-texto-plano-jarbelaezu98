import re
import pandas as pd
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", encoding="utf-8") as f:
        lines = f.readlines()

    data = []
    current = None

    for line in lines:
        line = line.rstrip()

        match = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+\s*%)\s+(.*)", line)

        if match:
            if current:
                data.append(current)

            current = {
                "cluster": int(match.group(1)),
                "cantidad_de_palabras_clave": int(match.group(2)),
                "porcentaje_de_palabras_clave": match.group(3),
                "principales_palabras_clave": match.group(4).strip(),
            }

        elif current and line.strip() != "" and not line.startswith("-"):
            current["principales_palabras_clave"] += " " + line.strip()

    if current:
        data.append(current)

    df = pd.DataFrame(data)

    # Limpiar porcentaje → float
    df["porcentaje_de_palabras_clave"] = (
        df["porcentaje_de_palabras_clave"]
        .str.replace("%", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
        .astype(float)
    )

    # Limpiar keywords
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .replace(r"\s+", " ", regex=True)
        .replace(r"\s*,\s*", ", ", regex=True)
        .str.strip()
        .str.rstrip(".")
    )

    return df
    
