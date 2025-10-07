# @Author: MagicBrain Simple CMS
# @Version: 0.1
# @Last Update: 07 September 2025
# @Developer: Octávio Filipe Gonçalves @ octavio.filipe.pereira at gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/gpl-3.0.html

import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
from io import BytesIO

# Incluir GEMINI_API_KEY
load_dotenv()

try:
    client = genai.Client()
except Exception as e:
    print("❌ Erro ao inicializar a API. Verifique sua GEMINI_API_KEY")
    print(f"Detalhes do erro: {e}")
    exit()

# Descrição pretendida da imagem
prompt_descricao = "Uma estação de radio amador, com morse e vários rádios e antenas, no  campo, num dia de sol, num quadro a óleo"

# Nome do output (png, jpg, wepp, tif, etc...)
NOME_DO_ARQUIVO = "hampt.png"

print(f"🚀 A enviar o pedido para o Gemini - Modelo Nano Banana: '{prompt_descricao}'")

# A aguardar resposta da API
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=[prompt_descricao],
)

# A processar a resposta e salva a imagem recorrendo ao BytesIO e PIL.Image
for part in response.candidates[0].content.parts:
    if part.inline_data is not None:

        image_bytes = BytesIO(part.inline_data.data)
        
        image = Image.open(image_bytes)
        
        image.save(NOME_DO_ARQUIVO)
        
        print(f"✅ A imagem foi gerada com sucesso!")
        print(f"💾 A imagem foi guardada com sucesso: {NOME_DO_ARQUIVO}")
        
    elif part.text is not None:
        # Caso a API devolva apenas texto, faz o display ao utilizador (Exemplo: caso a resposta for bloqueada ou inválida)
        print(f"⚠️ A API retornou uma resposta de texto (erro ou aviso): {part.text}")
