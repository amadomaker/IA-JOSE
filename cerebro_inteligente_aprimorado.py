# ==================================================================================
# PROJETO: ROBÔ HUMANOIDE NEURAL (NIED - UNICAMP)
# DOCUMENTAÇÃO DE DEPENDÊNCIAS E BIBLIOTECAS
# ==================================================================================

# 1. speech_recognition (as sr):
#    Serventia: É o "ouvido" do robô. Utiliza a API do Google para converter o áudio 
#    captado pelo microfone em texto (Speech-to-Text).

# 2. edge_tts:
#    Serventia: É a "garganta" de alta fidelidade. Conecta-se aos servidores da Microsoft 
#    para gerar uma voz natural (como a do Antonio), transformando texto em áudio.

# 3. pygame (módulo mixer):
#    Serventia: Responsável por gerenciar e reproduzir os arquivos de som (.mp3) 
#    gerados. Foi escolhido por sua estabilidade ao lidar com áudio em tempo real.

# 4. asyncio:
#    Serventia: Gerencia tarefas que ocorrem em paralelo. Essencial para o edge_tts 
#    funcionar sem "travar" o resto do código enquanto baixa o áudio da voz.

# 5. os:
#    Serventia: Permite que o Python interaja com o Sistema Operacional. Aqui, usamos 
#    principalmente para apagar os arquivos temporários de áudio após a fala do robô.

# 6. serial:
#    Serventia: Realiza a comunicação USB entre o computador e o Arduino Uno. 
#    Envia os sinais que coordenam o movimento dos motores (boca) em sincronia com a voz.

# 7. time:
#    Serventia: Controla o tempo de execução, pausas e sincronia. É fundamental para 
#    garantir que a boca não feche antes do áudio terminar.

# 8. json:
#    Serventia: Gerencia o "cérebro" persistente do robô. Permite ler e salvar o 
#    aprendizado no arquivo 'cerebro_nied.json', garantindo que o robô não esqueça o que aprendeu.

# ==================================================================================

import speech_recognition as sr
import edge_tts
import pygame
import asyncio
import os
import serial
import time
import json 

# --- CONFIGURAÇÕES DE HARDWARE ---
arduino_conectado = False
try:
    arduino = serial.Serial('COM3', 9600, timeout=0.1) 
    time.sleep(2)
    arduino_conectado = True
    print("✓ Sistema Nervoso (Arduino) Online.")
except:
    print("! Modo Simulação: Atuadores de boca offline.")

# --- CONFIGURAÇÕES DE VOZ ---
pygame.mixer.init()
VOZ_MASCULINA = "pt-BR-AntonioNeural"
PALAVRA_CHAVE = "josé"  # J.O.S.E - Jovem Orientador de Soluções Educacionais
VARIANTES_NOME = ["josé", "jose", "j.o.s.e", "j o s e"]  # Variações de pronúncia
ARQUIVO_MEMORIA = "cerebro_nied.json"

# --- BANCO DE DADOS INICIAL ---
FAQ_INICIAL = [
    # Mantenha vazio ou coloque o básico se for resetar o JSON
]

# --- FUNÇÕES UTILITÁRIAS DE TEXTO ---

def formatar_texto_inteligente(texto):
    """
    Transforma 'o nied é legal' em 'O NIED é legal.'
    """
    if not texto: return ""
    
    # 1. Primeira letra maiúscula
    texto = texto.strip().capitalize()
    
    # 2. Correção de Termos do NIED (O Google escreve tudo minúsculo)
    substituicoes = {
        "nied": "NIED",
        "unicamp": "Unicamp",
        "arduino": "Arduino",
        "maker": "Maker",
        "fe": "FE",
        "pibic": "PIBIC",
        "bas": "BAS",
        "creality": "Creality",
        "gideone": "Gideone",
        "gideoni": "Gideone"
    }
    
    palavras = texto.split()
    # Substitui palavras isoladas mantendo a pontuação se houver (lógica simples)
    novas_palavras = []
    for p in palavras:
        # Remove pontuação temporária para checar a palavra
        p_limpa = p.lower().strip(".,?!")
        if p_limpa in substituicoes:
            # Reconstrói a palavra com a grafia correta (Ex: nied -> NIED)
            novas_palavras.append(substituicoes[p_limpa])
        else:
            novas_palavras.append(p)
            
    texto = " ".join(novas_palavras)
    
    # 3. Adiciona Ponto Final se não tiver pontuação no fim
    if texto[-1] not in ['.', '!', '?', ':']:
        texto += "."
        
    return texto

# --- FUNÇÕES DE MEMÓRIA (JSON) ---

#função que busca a resposta para a pergunta conforme o arquivo de memória .json

def carregar_memoria():
    if not os.path.exists(ARQUIVO_MEMORIA):
        with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
            json.dump(FAQ_INICIAL, f, ensure_ascii=False, indent=4)
        return FAQ_INICIAL
    try:
        with open(ARQUIVO_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return FAQ_INICIAL

#função que faz o salvamento do aprendizado de algo pelo usuário diretamente no arquivo .json

def salvar_aprendizado(nova_pergunta, nova_resposta):
    memoria = carregar_memoria()
    nova_entrada = {
        "gatilhos": [nova_pergunta],
        "resposta": nova_resposta
    }
    memoria.append(nova_entrada)
    with open(ARQUIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=4)
    print(f"✓ Aprendido: '{nova_pergunta}' -> '{nova_resposta}'")

# --- FUNÇÕES DE INTERAÇÃO ---

async def gerar_voz(texto):
    arquivo_audio = "resposta.mp3"
    try:
        # MUDANÇA IMPORTANTE: Rate alterado de +15% para 0%
        # Isso faz ele falar com mais calma, disfarçando a falta de vírgulas
        comunicador = edge_tts.Communicate(texto, VOZ_MASCULINA, rate="+0%")
        await comunicador.save(arquivo_audio)
        return arquivo_audio
    except Exception as e:
        print(f"Erro no TTS: {e}")
        return None

def falar(texto):
    print(f"\n[J.O.S.E]: {texto}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    arquivo_audio = loop.run_until_complete(gerar_voz(texto))
    loop.close()

    if not arquivo_audio: return

    if arduino_conectado:
        try: arduino.write(b'1')
        except: pass

    try:
        pygame.mixer.music.load(arquivo_audio)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.05)
    except: pass
    
    if arduino_conectado:
        try: arduino.write(b'0')
        except: pass
    
    pygame.mixer.music.unload()
    if os.path.exists(arquivo_audio):
        try: os.remove(arquivo_audio)
        except: pass

def buscar_resposta(pergunta):
    memoria = carregar_memoria()
    pergunta = pergunta.lower().strip()
    for item in memoria:
        if any(gatilho in pergunta for gatilho in item["gatilhos"]):
            return item["resposta"]
    return None

def ouvir_natural():
    rec = sr.Recognizer()
    rec.pause_threshold = 1.0 
    rec.energy_threshold = 300 
    rec.dynamic_energy_threshold = True 
    
    with sr.Microphone() as fonte:
        print("\n[Ouvindo...]")
        rec.adjust_for_ambient_noise(fonte, duration=0.5)
        try:
            audio = rec.listen(fonte, timeout=None, phrase_time_limit=8) # Aumentei para 8s para frases longas
            texto = rec.recognize_google(audio, language='pt-BR').lower()
            print(f"-> Você: {texto}")
            return texto
        except:
            return None

# --- MODO APRENDIZADO APRIMORADO ---
def modo_aprendizado(pergunta_desconhecida):
    falar(f"Eu não sei sobre '{pergunta_desconhecida}'. O que devo responder? (Diga 'cancelar' para sair)")
    
    while True:
        resposta_ensino = ouvir_natural()
        
        # 1. Cancelamento
        if resposta_ensino and any(x in resposta_ensino for x in ["cancelar", "esquece", "sair"]):
            falar("Operação cancelada.")
            return

        if resposta_ensino and len(resposta_ensino) > 2:
            
            # --- AQUI ACONTECE A MÁGICA ---
            # Formatamos o texto antes de confirmar
            resposta_formatada = formatar_texto_inteligente(resposta_ensino)
            
            falar(f"Entendi. A resposta será: '{resposta_formatada}'. Posso salvar?")
            
            confirmacao = ouvir_natural()
            
            # 2. Cancelamento na confirmação
            if confirmacao and any(x in confirmacao for x in ["cancelar", "esquece", "não"]):
                if "não" in confirmacao and "cancelar" not in confirmacao:
                    falar("Ok, diga a resposta correta novamente.")
                    continue 
                else:
                    falar("Entendido. Cancelei.")
                    return 
            
            # 3. Sucesso
            if confirmacao and any(x in confirmacao for x in ["sim", "pode", "ok", "claro", "isso"]):
                salvar_aprendizado(pergunta_desconhecida, resposta_formatada)
                falar("Perfeito! Informação salva.")
                return 
            
            falar("Diga 'sim' para gravar ou 'cancelar' para desistir.")
        
        else:
            falar("Não ouvi a resposta. Repita ou diga 'cancelar'.")

# --- LOOP PRINCIPAL ---

falar("Olá! Sou o José, Jovem Orientador de Soluções Educacionais. Estou pronto para ajudar!")
carregar_memoria()

while True:
    entrada_usuario = ouvir_natural()
    
    if entrada_usuario:
        # Verifica se alguma variação do nome foi dita
        nome_detectado = any(variante in entrada_usuario for variante in VARIANTES_NOME)
        
        if nome_detectado:
            # Remove todas as variações do nome da pergunta
            pergunta_limpa = entrada_usuario
            for variante in VARIANTES_NOME:
                pergunta_limpa = pergunta_limpa.replace(variante, "")
            pergunta_limpa = pergunta_limpa.strip()
            
            if len(pergunta_limpa) < 2:
                falar("Estou ouvindo.")
                continue

            if any(x in entrada_usuario for x in ["sair", "tchau", "desligar", "até logo", "falo josé", "falou josé", "encerrar josé"]):
                falar("Até logo! Foi um prazer ajudar!")
                break
                
            resposta = buscar_resposta(pergunta_limpa)
            
            if resposta:
                falar(resposta)
            else:
                modo_aprendizado(pergunta_limpa)