# Juntando diversos arquivos
import pandas as pd
import glob
import os

# Caminho da pasta onde estão os arquivos
pasta = r"C:\Reneg_baixas"

# Encontra todos os arquivos .xlsx na pasta
arquivos = glob.glob(os.path.join(pasta, "*.xlsx"))

# Verifica se há arquivos encontrados
if not arquivos:
    print("Nenhum arquivo .xlsx encontrado na pasta especificada.")
else:
    # Lê e junta todos os arquivos Excel
    df = pd.concat(
        (pd.read_excel(f) for f in arquivos),
        ignore_index=True
    )

    # Caminho completo do arquivo consolidado
    arquivo_saida = os.path.join(pasta, "consolidado.xlsx")

    # Salva o DataFrame em um novo arquivo Excel
    df.to_excel(arquivo_saida, index=False)

    print(f"✅ {len(arquivos)} arquivos foram consolidados em:")
    print(f"➡️  {arquivo_saida}")

