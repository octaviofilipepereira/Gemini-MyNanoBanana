# @Author: Octávio Filipe Gonçalves AKA CT7BFV
# @Version: 1.0
# @Last Update: 10 September 2025
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

import sys
import os
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from google import genai
from PIL import Image
from io import BytesIO
import time

# --- CONFIGURAÇÃO INICIAL E CLIENTE DA API ---
load_dotenv()

# Inicializa o cliente da API.
try:
    CLIENTE_GEMINI = genai.Client()
    MODELO_IMAGEM = "gemini-2.5-flash-image"
except Exception:
    CLIENTE_GEMINI = None
    print("❌ Falha na inicialização do Cliente Gemini. Verifique a chave de API.")


# FUNÇÃO DE GERAÇÃO DE IMAGEM ---
def gerar_imagem_com_prompt():
    """
    Função que será acionada pelo botão da interface.
    Lê o prompt, chama a API e salva a imagem.
    """
    if CLIENTE_GEMINI is None:
        messagebox.showerror("Erro de API", "O cliente Gemini não foi inicializado. Verifique sua chave de API.")
        return
    
    prompt = entrada_prompt.get().strip()
    
    if not prompt:
        messagebox.showwarning("ERRO", "Por favor, digite uma descrição para a imagem.")
        return

    # Atualiza o status
    status_var.set("⏳ Gerando imagem... Isso pode levar alguns segundos.")
    janela.update_idletasks() # Força a atualização da interface imediatamente

    try:
        # Chamada à API
        response = CLIENTE_GEMINI.models.generate_content(
            model=MODELO_IMAGEM,
            contents=[prompt],
        )

        # Processa e Salva a Imagem
        imagem_salva = False
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                # Cria um nome de arquivo único com o timestamp
                nome_arquivo = f"my-gnanobanana_{int(time.time())}.png"
                
                image_bytes = BytesIO(part.inline_data.data)
                image = Image.open(image_bytes)
                image.save(nome_arquivo)
                
                status_var.set(f"✅ Sucesso! Imagem salva como: {nome_arquivo}")
                imagem_salva = True
                break
        
        if not imagem_salva:
             status_var.set("⚠️ A API retornou uma resposta sem imagem. Tente de novo.")

    except Exception as e:
        status_var.set(f"❌ Erro na geração: {e}")
        messagebox.showerror("ERRO", f"Ocorreu um erro ao gerar a imagem:\n{e}")

# --- CONFIGURAÇÃO DA INTERFACE TKINTER ---
janela = tk.Tk()
janela.title("My-GnanoBanana v1.0 - Produção de Imagens IA")
janela.geometry("600x250")

# Rótulo de Instrução (Label)
label_prompt = tk.Label(janela, text="Descreva a imagem que pretende gerar:", font=("Arial", 10, "bold"))
label_prompt.pack(pady=10, padx=10, anchor='w')

# Campo de Texto
entrada_prompt = tk.Entry(janela, width=80, font=("Arial", 10))
entrada_prompt.insert(0, "Um astronauta flutuando na via lactea, num quadro a óleo")
entrada_prompt.pack(pady=5, padx=10)

# Botão de Acção
botao_gerar = tk.Button(janela, 
                        text="A gerar imagem com My-GnanoBanana", 
                        command=gerar_imagem_com_prompt, 
                        bg="black", fg="white", 
                        font=("Arial", 10, "bold"))
botao_gerar.pack(pady=15)

# Status
status_var = tk.StringVar()
status_var.set("Ok. Insira a sua descrição e clique em Gerar.")
label_status = tk.Label(janela, textvariable=status_var, fg="blue", font=("Arial", 10))
label_status.pack(pady=10)

# Main Loop
janela.mainloop()
