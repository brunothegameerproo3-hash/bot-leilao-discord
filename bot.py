# -*- coding: utf-8 -*-
import discord
from discord.ext import tasks, commands
import pandas as pd
import asyncio
import aiohttp
import io
from datetime import datetime, timedelta
import random
import gspread
import os

# CONFIGURAÇÃO DO BOT
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']


# Configuracoes
ITEMS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSREA4EiAWWgU3jR1u3h4WfPYosHgd5Qo7425-6UxAbFXF8TrPC6a_KcrWHzX8URFZcQ4Dk_-Wx4MSR/pub?gid=0&single=true&output=tsv"
PONTOS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR2plzZgfqRFp3F3q7hZtCznsag8PymIDXxbq9pUWGAX48g6YabrdmZ_Yfsod3RkVuhoiYPMkF-zLDu/pub?gid=0&single=true&output=csv"

# Configuracao de STAFF - Adicione os IDs dos usuarios staff aqui
STAFF_IDS = [
    880587847218905119,  # ID Squall 
    381898660213948418,  # ID Jone
    366997454882865194   # ID Isac
]

# Configurações do Google Sheets API
GOOGLE_SHEETS_CREDENTIALS = {
  "type": "service_account",
  "project_id": "squall-project",
  "private_key_id": "8f81bb7fb1c234e8a8ef7468ea39ac16a1dd803d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC2p6BJuAU2PVzb\nGalKPnR5TIbLB6sPwV14zOeNqBVLp71PCa5E/jVL1Z7nyy7oD35zthndNhbyQf8U\nllRIE8/wJssOCiWMo+JkOLuh+TfyqxYEaM5nccruZnGwJrLHUI61IqmzgfigQvUL\nQ/zswAtxgt0PNcg8RQlQfnfiu0vV1Tc6wyE/z7P3VOws+EVwJkW/zoqeX/GpP5yA\nGWUumI22v5IoS8lXtEhyh9sNGktVRp7aL/XTCaUJunB/plhteyyExOTJvaQoHCSb\nE0mOrWNIeNGSgqiMAL+XjD+MqWgdJVo6B0t6qcmKgyFDZJn2yCV/gEHKXIcP8uzo\nNaCghB+HAgMBAAECggEAIOy/bnpu6hOOmOobw4fVjAX46EE2Gy1ycXOSK81IJW6T\np9spYENojQZxUfwktO0SEL6bE+6LnVi7J9VfVOzJV1NO1/WJRjxGc2VsoSpg5Ovl\nGJ9h0XDIMUgjJysan+YMC2e3qmV70TuwmzrCrVSC24/I1FSQBxk0sB9T8flsFpu9\nyALU8k2vrLoh06W/rg8PZb0YOTWxcsEAoOAzcopAiTbu8/951L6/FOsrMWCOwGcK\nakWzC++9u7FU9YnMvGtN/OW8f3o7uHyfgz1wiLgKO22HE4ALcgtGyafv/6Jkd9nx\n1JLeZ7VhucU81QiIyj15++LLxxhIdyfqymdEez5+rQKBgQDsWoQcOwcTsfChgkui\nuotD2ZaMkAiyr2R6FROGwDavQ5I02/5A6yBZq5JnhHXy735Uw3DuoOTF9QY/GfRo\nViCjjAmK12cYOqdNBpbDLcB9MvYMnqbDINAj5J4fVjeP2avcPoTOzruWNLfx8ADT\nOEPWljBXSpalruyCsXoBko7/SwKBgQDF1m1Z61cQcsXvoqITPFWTyXOpcwLb7xC6\nKm2Qci5bf4IXS1GDWTmKIHCtESL7kxENATxyp7K99aNqwAKyS0vKYOUwE0hQ3GI9\nAo+T7gokxsGGo7hhSICFOn5b266HnOi4jnCOMLJ1GcSrt5srRBXv/Qaii7vKqMF2\nM4ZC2Q+vNQKBgQDoVgY91gyb4LQhn/qH6YZS2UazwDa8p8tGcwdx0+stmGfVzFgA\nKuHvI8hUOBLWD3UJD+IowUKCEd3lE7d9BQUqn9MVh68RUz74abyz+nqY2Aqk1yQo\n9k2EqwyA03jk0F2vsElPHkuqWQJlMr8s4sdU3uiANpMmJXDa/GlpuE8XRwKBgBUT\noRbBUcc40wmSo/20odFa1u2oiRdxQrDysDWBVJr+3JcquQZrTQwAJMDrYHS42Eow\nZYY5g3tlXgGTbzYbe3mWFRSoGT40HGsviKhT5dTBMADuFEiY9sg60RdsMg3Uk56F\n3kvnuDttgVxh9TAI0uV8aWaLyHfwvpufJaCdi2Q5AoGAYwqDRij2gcUvfHJOvVkR\n4RTnyY2I8nCQtdM8EcP36ECnz3wV16uo1FDzsqQUlcebB8R1Gh/Xj1tuNRDuvsBn\n/UpkwFFRd9/l12evbziV3/ws8Ibvg0z1FkejX9QeXZJr14nj4koX+nAjSCtb2mia\nsXYo+PF8NYz38vRXtFmxlsY=\n-----END PRIVATE KEY-----\n",
  "client_email": "discord-squall-bot-leilao@squall-project.iam.gserviceaccount.com",
  "client_id": "105961118874981793167",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/discord-squall-bot-leilao%40squall-project.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# ID da planilha de pontos (encontre na URL da planilha)
SPREADSHEET_ID = "1-aPR_RImZLlAes-p1zluHtsCTmedpf-6e6BbCV6prlc"
# ID da planilha de itens (substitua pelo ID real da planilha de itens)
ITEMS_SPREADSHEET_ID = "1H5Xd2ZlGEHGI1aYntwdUOQt0JCeq8g-BtXbe7JMIkf4"

# INTENTS COMPLETOS (COM PRIVILÉGIOS ATIVADOS)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

class BidBot:
    def __init__(self):
        self.dados_pontos = None
        self.itens_leilao = None
        self.saldo_disponivel = 0
        self.leilao_ativo = False
        self.tempo_restante = 0
        self.lance_atual = 0
        self.lance_inicial = 0
        self.vencedor_atual = None
        self.item_atual = None
        self.historico_lances = []
        self.pontuacoes_jogadores = {}
        self.lances_reservados = {}
        self.coluna_nome = None
        self.coluna_pontos = None
        self.gc = None
        self.quantidade_leilao = 1
        
        # Inicializar Google Sheets
        self.inicializar_google_sheets()
    
    def inicializar_google_sheets(self):
        """Inicializa a conexão com o Google Sheets"""
        try:
            self.gc = gspread.service_account_from_dict(GOOGLE_SHEETS_CREDENTIALS)
            print("✅ Google Sheets API conectada com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao conectar com Google Sheets: {e}")
            self.gc = None
    
    async def atualizar_planilha_pontos(self, nome_jogador, novos_pontos):
        """Atualiza os pontos do jogador na planilha do Google Sheets"""
        try:
            if self.gc is None:
                print("❌ Cliente do Google Sheets não inicializado")
                return False
            
            # Abre a planilha
            worksheet = self.gc.open_by_key(SPREADSHEET_ID).sheet1
            
            # Encontra a linha do jogador
            todas_celulas = worksheet.get_all_records()
            
            for i, linha in enumerate(todas_celulas, start=2):
                nome_na_planilha = str(list(linha.values())[0]).strip()
                if nome_jogador.lower() == nome_na_planilha.lower():
                    # Atualiza os pontos na coluna correta
                    coluna_pontos_idx = 2
                    if self.coluna_pontos:
                        cabecalho = worksheet.row_values(1)
                        if self.coluna_pontos in cabecalho:
                            coluna_pontos_idx = cabecalho.index(self.coluna_pontos) + 1
                    
                    worksheet.update_cell(i, coluna_pontos_idx, novos_pontos)
                    print(f"✅ Planilha atualizada: {nome_jogador} -> {novos_pontos} pontos")
                    return True
            
            print(f"❌ Jogador {nome_jogador} não encontrado na planilha")
            return False
            
        except Exception as e:
            print(f"❌ Erro ao atualizar planilha: {e}")
            return False

    async def atualizar_planilha_itens(self, numero_item, nova_quantidade):
        """Atualiza a quantidade do item na planilha do Google Sheets"""
        try:
            if self.gc is None:
                print("❌ Cliente do Google Sheets não inicializado")
                return False
            
            # Abre a planilha de itens
            worksheet = self.gc.open_by_key(ITEMS_SPREADSHEET_ID).sheet1
            
            # Encontra a linha do item (linha = numero_item + 1 porque a primeira linha é cabeçalho)
            linha_item = numero_item + 1
            
            # Atualiza a quantidade na terceira coluna (coluna C)
            worksheet.update_cell(linha_item, 3, nova_quantidade)
            print(f"✅ Planilha de itens atualizada: Item {numero_item} -> {nova_quantidade} unidades")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao atualizar planilha de itens: {e}")
            return False
    
    def obter_nome_jogador(self, member):
        """Obtém o nome do jogador removendo prefixos como [Æsir]"""
        nome_original = member.display_name
        
        prefixos = ["[Æsir] ", "[Aesir] ", "[ASIR] ", "[ÆSIR] "]
        
        nome_limpo = nome_original
        for prefixo in prefixos:
            if nome_limpo.startswith(prefixo):
                nome_limpo = nome_limpo.replace(prefixo, "", 1)
                break
        
        return nome_limpo, nome_original
        
    async def carregar_dados(self):
        """Carrega tanto os itens quanto os pontos"""
        print("🔄 Carregando dados...")
        
        if await self.carregar_pontos():
            print("✅ Pontos carregados com sucesso!")
        else:
            print("❌ Erro ao carregar pontos")
            
        if await self.carregar_itens():
            print("✅ Itens carregados com sucesso!")
        else:
            print("❌ Erro ao carregar itens")
            
    async def carregar_pontos(self):
        """Carrega os pontos dos personagens"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(PONTOS_URL) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.dados_pontos = pd.read_csv(io.StringIO(content))
                        await self.processar_pontuacoes()
                        return True
                    else:
                        print(f"❌ Erro ao acessar pontos: {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Erro ao carregar pontos: {e}")
            return False
    
    async def processar_pontuacoes(self):
        """Processa as pontuações individuais de cada jogador"""
        if self.dados_pontos is None:
            return
            
        try:
            self.pontuacoes_jogadores = {}
            
            self.coluna_nome = None
            self.coluna_pontos = None
            
            for col in self.dados_pontos.columns:
                col_lower = col.lower()
                if any(word in col_lower for word in ['nome', 'name', 'jogador', 'player', 'personagem']):
                    self.coluna_nome = col
                    break
            
            for col in self.dados_pontos.columns:
                col_lower = col.lower()
                if any(word in col_lower for word in ['pontos', 'points', 'saldo', 'score', 'total']):
                    self.coluna_pontos = col
                    break
            
            if self.coluna_nome is None and len(self.dados_pontos.columns) >= 1:
                self.coluna_nome = self.dados_pontos.columns[0]
            
            if self.coluna_pontos is None and len(self.dados_pontos.columns) >= 2:
                self.coluna_pontos = self.dados_pontos.columns[1]
            
            print(f"📝 Coluna de nomes: {self.coluna_nome}")
            print(f"📝 Coluna de pontos: {self.coluna_pontos}")
            
            for index, row in self.dados_pontos.iterrows():
                if self.coluna_nome in row and self.coluna_pontos in row:
                    nome = str(row[self.coluna_nome]).strip()
                    try:
                        pontos = int(float(row[self.coluna_pontos]))
                        self.pontuacoes_jogadores[nome] = pontos
                        print(f"👤 {nome}: {pontos} pontos")
                    except (ValueError, TypeError):
                        print(f"⚠️ Pontos inválidos para {nome}: {row[self.coluna_pontos]}")
            
            print(f"✅ {len(self.pontuacoes_jogadores)} jogadores carregados")
            
        except Exception as e:
            print(f"❌ Erro ao processar pontuações: {e}")
    
    def obter_pontuacao_jogador(self, member):
        """Obtém a pontuação específica de um jogador (considerando lances reservados)"""
        nome_limpo, nome_original = self.obter_nome_jogador(member)
        
        chaves_possiveis = [
            nome_limpo,
            nome_original,
            nome_limpo.lower(),
            nome_original.lower(),
            nome_limpo.upper(),
            nome_original.upper()
        ]
        
        pontuacao_base = 0
        for chave in chaves_possiveis:
            if chave in self.pontuacoes_jogadores:
                pontuacao_base = self.pontuacoes_jogadores[chave]
                break
        
        if pontuacao_base == 0:
            for chave_planilha in self.pontuacoes_jogadores.keys():
                if nome_limpo.lower() in chave_planilha.lower() or nome_original.lower() in chave_planilha.lower():
                    pontuacao_base = self.pontuacoes_jogadores[chave_planilha]
                    break
        
        lance_reservado = self.lances_reservados.get(member.id, 0)
        return max(0, pontuacao_base - lance_reservado)
    
    def obter_pontuacao_base_jogador(self, member):
        """Obtém a pontuação base do jogador (sem considerar lances reservados)"""
        nome_limpo, nome_original = self.obter_nome_jogador(member)
        
        chaves_possiveis = [
            nome_limpo,
            nome_original,
            nome_limpo.lower(),
            nome_original.lower(),
            nome_limpo.upper(),
            nome_original.upper()
        ]
        
        for chave in chaves_possiveis:
            if chave in self.pontuacoes_jogadores:
                return self.pontuacoes_jogadores[chave]
        
        for chave_planilha in self.pontuacoes_jogadores.keys():
            if nome_limpo.lower() in chave_planilha.lower() or nome_original.lower() in chave_planilha.lower():
                return self.pontuacoes_jogadores[chave_planilha]
        
        return 0
    
    def listar_pontuacoes_formatadas(self):
        """Retorna uma mensagem formatada com todas as pontuações"""
        if not self.pontuacoes_jogadores:
            return "❓ Nenhum dado de pontos carregado."
        
        jogadores_ordenados = sorted(
            self.pontuacoes_jogadores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        mensagem = "📊 **RANKING DE PONTUAÇÕES** 📊\n\n"
        
        for i, (nome, pontos) in enumerate(jogadores_ordenados, 1):
            medalha = ""
            if i == 1:
                medalha = "🥇 "
            elif i == 2:
                medalha = "🥈 "
            elif i == 3:
                medalha = "🥉 "
            
            mensagem += f"{medalha}**{i}º.** {nome}: **{pontos} pontos**\n"
        
        mensagem += f"\n👥 **Total de jogadores:** {len(self.pontuacoes_jogadores)}"
        
        return mensagem
    
    async def carregar_itens(self):
        """Carrega a lista de itens para leilão incluindo quantidades"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(ITEMS_URL) as response:
                    if response.status == 200:
                        content = await response.text()
                        self.itens_leilao = pd.read_csv(io.StringIO(content), sep='\t')
                        print(f"🎁 Itens carregados: {len(self.itens_leilao)} itens disponíveis")
                        
                        # Verifica a estrutura da planilha
                        if len(self.itens_leilao.columns) >= 3:
                            print("✅ Planilha com quantidade detectada")
                        else:
                            print("⚠️ Planilha sem coluna de quantidade")
                        
                        return True
                    else:
                        print(f"❌ Erro ao acessar itens: {response.status}")
                        return False
        except Exception as e:
            print(f"❌ Erro ao carregar itens: {e}")
            return False
    
    def listar_itens(self):
        """Retorna lista formatada de itens disponíveis com quantidades"""
        if self.itens_leilao is None or len(self.itens_leilao) == 0:
            return "❓ Nenhum item disponível para leilão"
        
        mensagem = "🎁 **ITENS DISPONÍVEIS PARA LEILÃO:**\n"
        
        for index, row in self.itens_leilao.iterrows():
            item_id = index + 1
            nome = row.iloc[0] if len(row) > 0 else "Item sem nome"
            descricao = row.iloc[1] if len(row) > 1 else ""
            quantidade = row.iloc[2] if len(row) > 2 else "1"
            
            mensagem += f"**{item_id}.** {nome}"
            if descricao and str(descricao) != 'nan':
                mensagem += f" - {descricao}"
            if quantidade and str(quantidade) != 'nan':
                mensagem += f" | **Quantidade disponível: {quantidade}**"
            mensagem += "\n"
        
        mensagem += f"\n**Staff use:** `!escolher <número> [quantidade]` para escolher um item!"
        return mensagem
    
    def escolher_item(self, numero_item, quantidade=1):
        """Escolhe um item para leilão com quantidade específica"""
        if self.itens_leilao is None:
            return None, "❓ Lista de itens não carregada"
        
        if numero_item < 1 or numero_item > len(self.itens_leilao):
            return None, f"❓ Item deve estar entre 1 e {len(self.itens_leilao)}"
        
        item_escolhido = self.itens_leilao.iloc[numero_item - 1]
        nome_item = item_escolhido.iloc[0] if len(item_escolhido) > 0 else "Item sem nome"
        descricao = item_escolhido.iloc[1] if len(item_escolhido) > 1 else ""
        quantidade_disponivel = item_escolhido.iloc[2] if len(item_escolhido) > 2 else 1
        
        # Converte quantidade disponível para inteiro
        try:
            quantidade_disponivel = int(quantidade_disponivel)
        except (ValueError, TypeError):
            quantidade_disponivel = 1
        
        # Verifica se a quantidade solicitada está disponível
        if quantidade > quantidade_disponivel:
            return None, f"❌ Quantidade indisponível! Disponível: {quantidade_disponivel}"
        
        if quantidade < 1:
            return None, "❌ Quantidade deve ser pelo menos 1"
        
        self.item_atual = {
            'id': numero_item,
            'nome': nome_item,
            'descricao': descricao,
            'quantidade_total': quantidade_disponivel,
            'quantidade_leilao': quantidade,
            'quantidade_restante': quantidade_disponivel - quantidade
        }
        
        # Reseta o lance inicial quando escolhe novo item
        self.lance_inicial = 0
        self.quantidade_leilao = quantidade
    
        mensagem = f"✅ **Item selecionado:** {nome_item}"
        if descricao and str(descricao) != 'nan':
            mensagem += f" - {descricao}"
        
        mensagem += f"\n📦 **Quantidade no leilão:** {quantidade}"
        mensagem += f"\n🎯 **Lance inicial atual:** {self.lance_inicial} pontos"
        mensagem += f"\n⚡ **Staff use:** `!lance_inicial <valor>` para definir um lance inicial"
            
        return self.item_atual, mensagem
    
    async def fazer_lance(self, valor, autor):
        """Faz um lance se o jogador tiver saldo suficiente (apenas reserva)"""
        pontuacao_base = self.obter_pontuacao_base_jogador(autor)
        lance_anterior = self.lances_reservados.get(autor.id, 0)
        
        # Verifica se o lance é maior que o lance inicial E maior que o lance atual
        lance_minimo = max(self.lance_inicial, self.lance_atual)
        
        if valor <= pontuacao_base and valor > lance_minimo:
            self.lance_atual = valor
            self.vencedor_atual = autor
            
            self.lances_reservados[autor.id] = valor
            
            nome_limpo, nome_original = self.obter_nome_jogador(autor)
            
            self.historico_lances.append({
                'autor': autor,
                'nome_limpo': nome_limpo,
                'nome_original': nome_original,
                'valor': valor,
                'timestamp': datetime.now(),
                'saldo_restante': pontuacao_base - valor
            })
            
            return True
        return False
    
    async def atualizar_pontos_vencedor(self, vencedor, valor_lance):
        """Atualiza os pontos do vencedor na planilha - COM DIAGNÓSTICO"""
        try:
            nome_limpo, nome_original = self.obter_nome_jogador(vencedor)
            
            print(f"🔍 DIAGNÓSTICO: Tentando atualizar pontos para {nome_limpo}")
            
            if self.gc is None:
                print("❌ Google Sheets não conectado")
                return False
            
            jogador_encontrado = None
            pontuacao_original = 0
            
            for nome_planilha, pontos_atuais in self.pontuacoes_jogadores.items():
                if (nome_limpo.lower() in nome_planilha.lower() or 
                    nome_original.lower() in nome_planilha.lower()):
                    jogador_encontrado = nome_planilha
                    pontuacao_original = pontos_atuais
                    break
            
            if not jogador_encontrado:
                print(f"❌ Jogador {nome_limpo} não encontrado na planilha")
                print("👥 Jogadores na planilha:", list(self.pontuacoes_jogadores.keys()))
                return False
            
            novos_pontos = max(0, pontuacao_original - valor_lance)
            
            print(f"🔍 DIAGNÓSTICO: {jogador_encontrado} - {pontuacao_original} -> {novos_pontos} pontos")
            
            self.pontuacoes_jogadores[jogador_encontrado] = novos_pontos
            
            sucesso_planilha = await self.atualizar_planilha_pontos(jogador_encontrado, novos_pontos)
            
            if sucesso_planilha:
                print(f"✅ Pontos atualizados na planilha: {jogador_encontrado} -> {novos_pontos} pontos")
                return True
            else:
                print(f"⚠️ Pontos atualizados localmente, mas erro ao atualizar planilha")
                return False
                    
        except Exception as e:
            print(f"❌ Erro ao atualizar pontos do vencedor: {e}")
            return False

    async def atualizar_pontos_e_itens(self, vencedor, valor_lance, numero_item, quantidade_usada):
        """Atualiza os pontos do vencedor E a quantidade de itens na planilha"""
        try:
            # Atualiza pontos do vencedor (código existente)
            nome_limpo, nome_original = self.obter_nome_jogador(vencedor)
            
            print(f"🔍 DIAGNÓSTICO: Tentando atualizar pontos para {nome_limpo}")
            
            if self.gc is None:
                print("❌ Google Sheets não conectado")
                return False
            
            jogador_encontrado = None
            pontuacao_original = 0
            
            for nome_planilha, pontos_atuais in self.pontuacoes_jogadores.items():
                if (nome_limpo.lower() in nome_planilha.lower() or 
                    nome_original.lower() in nome_planilha.lower()):
                    jogador_encontrado = nome_planilha
                    pontuacao_original = pontos_atuais
                    break
            
            if not jogador_encontrado:
                print(f"❌ Jogador {nome_limpo} não encontrado na planilha")
                return False
            
            novos_pontos = max(0, pontuacao_original - valor_lance)
            
            print(f"🔍 DIAGNÓSTICO: {jogador_encontrado} - {pontuacao_original} -> {novos_pontos} pontos")
            
            self.pontuacoes_jogadores[jogador_encontrado] = novos_pontos
            
            sucesso_pontos = await self.atualizar_planilha_pontos(jogador_encontrado, novos_pontos)
            
            # NOVO: Atualiza a quantidade de itens
            sucesso_itens = await self.atualizar_planilha_itens(numero_item, quantidade_usada)
            
            if sucesso_pontos and sucesso_itens:
                print(f"✅ Pontos e itens atualizados na planilha!")
                return True
            else:
                print(f"⚠️ Alguma atualização falhou - Pontos: {sucesso_pontos}, Itens: {sucesso_itens}")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao atualizar pontos e itens: {e}")
            return False

# Instância do bot de leilão
bid_bot = BidBot()

def eh_staff(ctx):
    """Verifica se o usuário é staff"""
    return ctx.author.id in STAFF_IDS

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    print('✅ Comandos disponíveis:')
    print('   ⚡ STAFF: !itens, !escolher, !lance_inicial, !iniciar_leilao, !parar_leilao')
    print('   👥 TODOS: !pontos, !meuspontos, !lance, !status, !historico, !atualizar, !quem_sou_eu, !ajuda')
    await bid_bot.carregar_dados()
    verificar_leiloes.start()

# COMANDOS PARA TODOS OS USUÁRIOS

@bot.command()
async def pontos(ctx):
    """Mostra o ranking completo de pontuações de todos os jogadores"""
    mensagem = bid_bot.listar_pontuacoes_formatadas()
    
    if len(mensagem) > 1900:
        partes = [mensagem[i:i+1900] for i in range(0, len(mensagem), 1900)]
        for parte in partes:
            await ctx.send(parte)
    else:
        await ctx.send(mensagem)

@bot.command()
async def ranking(ctx):
    """Alias para o comando pontos - mostra o ranking"""
    await pontos(ctx)

@bot.command()
async def meuspontos(ctx):
    """Mostra os pontos do jogador que executou o comando"""
    pontuacao_base = bid_bot.obter_pontuacao_base_jogador(ctx.author)
    pontuacao_atual = bid_bot.obter_pontuacao_jogador(ctx.author)
    nome_limpo, nome_original = bid_bot.obter_nome_jogador(ctx.author)
    
    lance_reservado = bid_bot.lances_reservados.get(ctx.author.id, 0)
    
    if bid_bot.pontuacoes_jogadores:
        jogadores_ordenados = sorted(
            bid_bot.pontuacoes_jogadores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        posicao = None
        for i, (nome, pontos) in enumerate(jogadores_ordenados, 1):
            if nome_limpo.lower() in nome.lower() or nome_original.lower() in nome.lower():
                posicao = i
                break
    else:
        posicao = None
    
    mensagem = (
        f"📊 **SUA PONTUAÇÃO**\n"
        f"👤 **Jogador:** {nome_limpo}\n"
        f"💰 **Pontos totais:** **{pontuacao_base}**\n"
    )
    
    if lance_reservado > 0:
        mensagem += f"🎯 **Lance reservado:** {lance_reservado} pontos\n"
        mensagem += f"✅ **Pontos disponíveis:** **{pontuacao_atual}**\n"
    else:
        mensagem += f"✅ **Pontos disponíveis:** **{pontuacao_atual}**\n"
    
    if posicao:
        mensagem += f"🏆 **Posição no ranking:** {posicao}º\n"
    
    if bid_bot.leilao_ativo and bid_bot.item_atual:
        mensagem += f"🎁 **Item em leilão:** {bid_bot.item_atual['nome']}\n"
        if bid_bot.quantidade_leilao > 1:
            mensagem += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
        mensagem += f"💵 **Lance atual:** {bid_bot.lance_atual} pontos"
        if bid_bot.lance_inicial > 0:
            mensagem += f"\n🎯 **Lance inicial:** {bid_bot.lance_inicial} pontos"
        if bid_bot.vencedor_atual and bid_bot.vencedor_atual.id == ctx.author.id:
            mensagem += f"\n👑 **Você está na liderança!**"
    elif bid_bot.item_atual:
        mensagem += f"🎁 **Item selecionado:** {bid_bot.item_atual['nome']}\n"
        if bid_bot.quantidade_leilao > 1:
            mensagem += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
        if bid_bot.lance_inicial > 0:
            mensagem += f"🎯 **Lance inicial definido:** {bid_bot.lance_inicial} pontos\n"
        mensagem += f"⏳ **Aguardando início do leilão**"
    
    await ctx.send(mensagem)

@bot.command()
async def lance(ctx, valor: int):
    """Faz um lance no leilão atual - TODOS PODEM USAR"""
    if not bid_bot.leilao_ativo:
        await ctx.send("❌ Não há leilão ativo no momento!")
        return
    
    if bid_bot.item_atual is None:
        await ctx.send("❌ Nenhum item selecionado para leilão!")
        return
    
    pontuacao_atual = bid_bot.obter_pontuacao_jogador(ctx.author)
    pontuacao_base = bid_bot.obter_pontuacao_base_jogador(ctx.author)
    nome_limpo, nome_original = bid_bot.obter_nome_jogador(ctx.author)
    
    # Calcula o lance mínimo necessário
    lance_minimo = max(bid_bot.lance_inicial, bid_bot.lance_atual)
    
    if await bid_bot.fazer_lance(valor, ctx.author):
        saldo_restante = pontuacao_base - valor
        
        mensagem_lance = (
            f"✅ **Lance aceito!** {ctx.author.mention} ({nome_limpo}) fez um lance de **{valor} pontos**!\n"
            f"🎁 **Item:** {bid_bot.item_atual['nome']}\n"
        )
        
        if bid_bot.quantidade_leilao > 1:
            mensagem_lance += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
            
        mensagem_lance += (
            f"💵 **Lance atual:** {valor} pontos\n"
            f"💰 **Seus pontos totais:** {pontuacao_base} pontos\n"
            f"🎯 **Lance reservado:** {valor} pontos\n"
            f"✅ **Pontos disponíveis:** {saldo_restante} pontos\n"
            f"👑 **Líder atual:** {nome_limpo}"
        )
        
        # Mensagem especial se foi o primeiro lance
        if bid_bot.lance_atual == bid_bot.lance_inicial and bid_bot.lance_inicial > 0:
            mensagem_lance += f"\n🎉 **Primeiro lance do leilão!**"
            
        await ctx.send(mensagem_lance)
    else:
        if valor > pontuacao_base:
            await ctx.send(f"❌ Saldo insuficiente! Você tem {pontuacao_base} pontos totais. Use `!meuspontos` para verificar.")
        elif valor <= lance_minimo:
            if bid_bot.lance_inicial > 0 and bid_bot.lance_atual == bid_bot.lance_inicial:
                await ctx.send(f"❌ O primeiro lance deve ser maior que {bid_bot.lance_inicial} pontos!")
            else:
                await ctx.send(f"❌ Lance deve ser maior que o atual ({bid_bot.lance_atual} pontos)")
        else:
            await ctx.send("❌ Erro ao processar lance")

@bot.command()
async def status(ctx):
    """Mostra status do leilão atual"""
    status_msg = "📊 **STATUS DO LEILÃO**\n"
    
    if bid_bot.leilao_ativo and bid_bot.item_atual:
        minutos = bid_bot.tempo_restante // 60
        segundos = bid_bot.tempo_restante % 60
        
        status_msg += (
            f"🔥 **LEILÃO ATIVO!** 🔥\n"
            f"🎁 **Item:** {bid_bot.item_atual['nome']}\n"
        )
        
        if bid_bot.quantidade_leilao > 1:
            status_msg += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
            
        status_msg += (
            f"🎯 **Lance inicial:** {bid_bot.lance_inicial} pontos\n"
            f"💵 **Lance atual:** {bid_bot.lance_atual} pontos\n"
            f"⏰ **Tempo restante:** {minutos:02d}:{segundos:02d}\n"
        )
        
        if bid_bot.vencedor_atual:
            nome_limpo, nome_original = bid_bot.obter_nome_jogador(bid_bot.vencedor_atual)
            status_msg += f"👑 **Líder atual:** {nome_limpo}\n"
        
        status_msg += f"📈 **Total de lances:** {len(bid_bot.historico_lances)}\n"
        status_msg += f"👥 **Jogadores com lances:** {len(bid_bot.lances_reservados)}"
        
    elif bid_bot.item_atual:
        status_msg += (
            f"🎁 **Item selecionado:** {bid_bot.item_atual['nome']}\n"
        )
        
        if bid_bot.quantidade_leilao > 1:
            status_msg += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
            
        status_msg += (
            f"🎯 **Lance inicial definido:** {bid_bot.lance_inicial} pontos\n"
            f"⏳ **Aguardando início do leilão**\n"
            f"⚡ **Staff use:** `!iniciar_leilao [minutos]` para começar!"
        )
    else:
        status_msg += "❓ **Nenhum item selecionado**\n⚡ **Aguardando staff selecionar um item**"
    
    await ctx.send(status_msg)

@bot.command()
async def historico(ctx):
    """Mostra o histórico de lances do leilão atual"""
    if not bid_bot.leilao_ativo or len(bid_bot.historico_lances) == 0:
        await ctx.send("📜 Nenhum lance realizado neste leilão.")
        return
    
    mensagem = "📜 **HISTÓRICO DE LANCES:**\n"
    
    for i, lance in enumerate(bid_bot.historico_lances[-10:], 1):
        tempo = lance['timestamp'].strftime("%H:%M:%S")
        saldo_info = f" (Saldo: {lance['saldo_restante']})" if 'saldo_restante' in lance else ""
        mensagem += f"{i}. **{lance['nome_limpo']}**: {lance['valor']} pontos{saldo_info} ({tempo})\n"
    
    await ctx.send(mensagem)

@bot.command()
async def atualizar(ctx):
    """Atualiza os dados dos pontos e itens"""
    await bid_bot.carregar_dados()
    await ctx.send("✅ Dados atualizados! Use `!pontos` para ver o ranking completo.")

@bot.command()
async def quem_sou_eu(ctx):
    """Mostra informações sobre quem está usando o comando"""
    nome_limpo, nome_original = bid_bot.obter_nome_jogador(ctx.author)
    pontuacao_base = bid_bot.obter_pontuacao_base_jogador(ctx.author)
    pontuacao_atual = bid_bot.obter_pontuacao_jogador(ctx.author)
    
    is_staff = eh_staff(ctx)
    lance_reservado = bid_bot.lances_reservados.get(ctx.author.id, 0)
    
    if bid_bot.pontuacoes_jogadores:
        jogadores_ordenados = sorted(
            bid_bot.pontuacoes_jogadores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        posicao = None
        for i, (nome, pontos) in enumerate(jogadores_ordenados, 1):
            if nome_limpo.lower() in nome.lower() or nome_original.lower() in nome.lower():
                posicao = i
                break
    else:
        posicao = None
    
    mensagem = (
        f"👤 **SUAS INFORMAÇÕES:**\n"
        f"**Nome original:** {nome_original}\n"
        f"**Nome limpo:** {nome_limpo}\n"
        f"**Pontuação total:** {pontuacao_base} pontos\n"
    )
    
    if lance_reservado > 0:
        mensagem += f"**Lance reservado:** {lance_reservado} pontos\n"
        mensagem += f"**Pontos disponíveis:** {pontuacao_atual} pontos\n"
    
    if posicao:
        mensagem += f"**Posição no ranking:** {posicao}º\n"
    
    if is_staff:
        mensagem += "**⚡ Staff:** ✅ Sim\n"
    else:
        mensagem += "**⚡ Staff:** ❌ Não\n"
    
    mensagem += (
        f"**Menção:** {ctx.author.mention}\n"
        f"**ID:** {ctx.author.id}"
    )
    
    await ctx.send(mensagem)

@bot.command()
async def ajuda(ctx):
    """Mostra apenas os comandos que o usuário tem permissão para usar"""
    is_staff = eh_staff(ctx)
    
    mensagem = "❓ **COMANDOS DISPONÍVEIS**\n\n"
    
    if is_staff:
        mensagem += "⚡ **VOCÊ É STAFF - TODOS OS COMANDOS:**\n"
        mensagem += "• `!itens` - Lista todos os itens disponíveis para leilão\n"
        mensagem += "• `!escolher <número> [quantidade]` - Escolhe um item para leilão\n"
        mensagem += "• `!lance_inicial <valor>` - Define o lance inicial do leilão\n"
        mensagem += "• `!iniciar_leilao [minutos]` - Inicia leilão do item selecionado\n"
        mensagem += "• `!parar_leilao` - Para o leilão atual manualmente\n"
        mensagem += "• `!pontos` / `!ranking` - Mostra o ranking completo de pontos\n"
        mensagem += "• `!meuspontos` - Mostra seus pontos e posição no ranking\n"
        mensagem += "• `!lance <valor>` - Faz um lance no leilão atual\n"
        mensagem += "• `!status` - Mostra status do leilão atual\n"
        mensagem += "• `!historico` - Mostra histórico de lances do leilão\n"
        mensagem += "• `!atualizar` - Atualiza dados dos pontos\n"
        mensagem += "• `!quem_sou_eu` - Mostra suas informações\n"
        mensagem += "• `!ajuda` - Mostra esta mensagem de ajuda\n\n"
        
    else:
        mensagem += "👥 **SEUS COMANDOS DISPONÍVEIS:**\n"
        mensagem += "• `!pontos` / `!ranking` - Mostra o ranking completo de pontos\n"
        mensagem += "• `!meuspontos` - Mostra seus pontos e posição no ranking\n"
        mensagem += "• `!lance <valor>` - Faz um lance no leilão atual\n"
        mensagem += "• `!status` - Mostra status do leilão atual\n"
        mensagem += "• `!historico` - Mostra histórico de lances do leilão\n"
        mensagem += "• `!atualizar` - Atualiza dados dos pontos\n"
        mensagem += "• `!quem_sou_eu` - Mostra suas informações\n"
        mensagem += "• `!ajuda` - Mostra esta mensagem de ajuda\n\n"
        
        mensagem += "⚠️ *Comandos de staff não estão disponíveis para você*\n\n"
    
    if bid_bot.leilao_ativo and bid_bot.item_atual:
        minutos = bid_bot.tempo_restante // 60
        segundos = bid_bot.tempo_restante % 60
        mensagem += f"🔥 **LEILÃO ATIVO:** {bid_bot.item_atual['nome']} (⏰ {minutos:02d}:{segundos:02d})\n"
        mensagem += f"💵 **Lance atual:** {bid_bot.lance_atual} pontos\n"
        if bid_bot.quantidade_leilao > 1:
            mensagem += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
        if bid_bot.lance_inicial > 0:
            mensagem += f"🎯 **Lance inicial:** {bid_bot.lance_inicial} pontos\n"
        if bid_bot.vencedor_atual:
            nome_limpo, nome_original = bid_bot.obter_nome_jogador(bid_bot.vencedor_atual)
            mensagem += f"👑 **Líder atual:** {nome_limpo}\n"
    elif bid_bot.item_atual:
        mensagem += f"🎁 **ITEM SELECIONADO:** {bid_bot.item_atual['nome']} (⏳ Aguardando início)\n"
        if bid_bot.quantidade_leilao > 1:
            mensagem += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
        if bid_bot.lance_inicial > 0:
            mensagem += f"🎯 **Lance inicial definido:** {bid_bot.lance_inicial} pontos\n"
    else:
        mensagem += "❓ **NENHUM ITEM SELECIONADO** (Aguardando staff)\n"
    
    await ctx.send(mensagem)

# COMANDOS EXCLUSIVOS DA STAFF

@bot.command()
@commands.check(eh_staff)
async def itens(ctx):
    """Lista todos os itens disponíveis para leilão - APENAS STAFF"""
    mensagem = bid_bot.listar_itens()
    await ctx.send(mensagem)

@itens.error
async def itens_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **Acesso negado!** Apenas membros da staff podem ver a lista de itens.")
    else:
        await ctx.send(f"❌ Erro ao listar itens: {error}")

@bot.command()
@commands.check(eh_staff)
async def escolher(ctx, numero_item: int, quantidade: int = 1):
    """Escolhe um item para leilão - APENAS STAFF"""
    if bid_bot.leilao_ativo:
        await ctx.send("❌ Há um leilão em andamento! Finalize o leilão atual antes de escolher outro item.")
        return
    
    item, mensagem = bid_bot.escolher_item(numero_item, quantidade)
    await ctx.send(mensagem)
    
    if item:
        await ctx.send(f"✅ **Item pronto para leilão!** Staff use `!iniciar_leilao [minutos]` para começar!")

@escolher.error
async def escolher_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **Acesso negado!** Apenas membros da staff podem escolher itens para leilão.")
    else:
        await ctx.send(f"❌ Erro ao escolher item: {error}")

@bot.command()
@commands.check(eh_staff)
async def lance_inicial(ctx, valor: int):
    """Define o lance inicial para o leilão - APENAS STAFF"""
    if bid_bot.leilao_ativo:
        await ctx.send("❌ Não é possível alterar o lance inicial durante um leilão ativo!")
        return
    
    if bid_bot.item_atual is None:
        await ctx.send("❌ Nenhum item selecionado! Use `!escolher <número>` primeiro.")
        return
    
    if valor < 0:
        await ctx.send("❌ O lance inicial não pode ser negativo!")
        return
    
    bid_bot.lance_inicial = valor
    
    mensagem = (
        f"✅ **Lance inicial definido!**\n"
        f"🎁 **Item:** {bid_bot.item_atual['nome']}\n"
    )
    
    if bid_bot.quantidade_leilao > 1:
        mensagem += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
        
    mensagem += (
        f"🎯 **Lance inicial:** {valor} pontos\n"
        f"⚡ **Agora use:** `!iniciar_leilao [minutos]` para começar o leilão!"
    )
    
    await ctx.send(mensagem)

@lance_inicial.error
async def lance_inicial_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **Acesso negado!** Apenas membros da staff podem definir o lance inicial.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ **Uso correto:** `!lance_inicial <valor>`")
    else:
        await ctx.send(f"❌ Erro ao definir lance inicial: {error}")

@bot.command()
@commands.check(eh_staff)
async def iniciar_leilao(ctx, duracao_minutos: int = 5):
    """Inicia um novo leilão para o item selecionado - APENAS STAFF"""
    if bid_bot.leilao_ativo:
        await ctx.send("❌ Já existe um leilão em andamento!")
        return
    
    if bid_bot.item_atual is None:
        await ctx.send("❌ Nenhum item selecionado! Use `!itens` para ver a lista e `!escolher <número>` para escolher um item.")
        return
    
    # Limpa lances anteriores
    bid_bot.lances_reservados = {}
    bid_bot.historico_lances = []
    
    await bid_bot.carregar_dados()
    
    bid_bot.leilao_ativo = True
    bid_bot.tempo_restante = duracao_minutos * 60
    bid_bot.lance_atual = bid_bot.lance_inicial
    bid_bot.vencedor_atual = None
    
    mensagem_inicio = (
        f"🔥 **LEILÃO INICIADO!** 🔥\n"
        f"⚡ **Iniciado por:** {ctx.author.mention}\n"
        f"🎁 **Item:** {bid_bot.item_atual['nome']}\n"
    )
    
    if bid_bot.quantidade_leilao > 1:
        mensagem_inicio += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
    
    if bid_bot.item_atual['descricao'] and str(bid_bot.item_atual['descricao']) != 'nan':
        mensagem_inicio += f"📝 **Descrição:** {bid_bot.item_atual['descricao']}\n"
    
    mensagem_inicio += (
        f"⏰ **Duração:** {duracao_minutos} minutos\n"
        f"🎯 **Lance inicial:** {bid_bot.lance_inicial} pontos\n"
        f"💵 **Use:** `!lance <valor>` para participar!\n"
        f"📊 **Verifique seus pontos com:** `!meuspontos`\n"
        f"🏆 **Veja o ranking completo com:** `!pontos`\n"
    )
    
    # Informações adicionais sobre o lance inicial
    if bid_bot.lance_inicial > 0:
        mensagem_inicio += f"⚠️ **ATENÇÃO:** O primeiro lance deve ser maior que {bid_bot.lance_inicial} pontos!\n"
    else:
        mensagem_inicio += f"ℹ️ **Sistema de lances:** Os pontos são apenas **reservados** durante o leilão e serão **debitados apenas do vencedor**"
    
    await ctx.send(mensagem_inicio)
    
    # 🔔 ANÚNCIO PARA TODOS OS MEMBROS QUE O LEILÃO COMEÇOU
    anuncio_global = (
        f"🎉 @everyone **LEILÃO INICIADO!** 🎉\n"
        f"🔥 **Item:** {bid_bot.item_atual['nome']}\n"
    )
    
    if bid_bot.quantidade_leilao > 1:
        anuncio_global += f"📦 **Quantidade:** {bid_bot.quantidade_leilao} itens\n"
        
    anuncio_global += (
        f"⏰ **Duração:** {duracao_minutos} minutos\n"
        f"💵 **Lance inicial:** {bid_bot.lance_inicial} pontos\n"
        f"📊 **Verifique seus pontos:** `!meuspontos`\n"
        f"🏆 **Faça seu lance:** `!lance <valor>`\n"
        f"🎁 **Boa sorte a todos!** 🎁"
    )
    
    # Envia o anúncio para todos os canais de texto
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:
                    await channel.send(anuncio_global)
                    break
                except:
                    continue

@iniciar_leilao.error
async def iniciar_leilao_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **Acesso negado!** Apenas membros da staff podem iniciar leilões.")
    else:
        await ctx.send(f"❌ Erro ao iniciar leilão: {error}")

@bot.command()
@commands.check(eh_staff)
async def parar_leilao(ctx):
    """Para o leilão atual manualmente - APENAS STAFF"""
    if not bid_bot.leilao_ativo:
        await ctx.send("❌ Não há leilão ativo no momento!")
        return
    
    bid_bot.leilao_ativo = False
    await ctx.send("🛑 **Leilão interrompido manualmente pela staff!**")
    await finalizar_leilao()

@parar_leilao.error
async def parar_leilao_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("❌ **Acesso negado!** Apenas membros da staff podem parar leilões.")

# ADICIONANDO VERIFICAÇÃO DE PERMISSÃO PARA COMANDOS DE STAFF
@bot.check
async def bloqueio_comandos_staff(ctx):
    """Bloqueia comandos de staff para não-staff"""
    comandos_staff = ['itens', 'escolher', 'lance_inicial', 'iniciar_leilao', 'parar_leilao']
    
    if ctx.command.name in comandos_staff and not eh_staff(ctx):
        await ctx.send("❌ **Acesso negado!** Este comando é exclusivo para membros da staff.")
        return False
    
    return True

@tasks.loop(seconds=1)
async def verificar_leiloes():
    """Verifica e atualiza o tempo dos leilões"""
    if bid_bot.leilao_ativo:
        bid_bot.tempo_restante -= 1
        
        if bid_bot.tempo_restante == 300:
            await enviar_aviso("⏰ **5 minutos restantes no leilão!**")
        elif bid_bot.tempo_restante == 60:
            await enviar_aviso("⏰ **1 minuto restante!**")
        elif bid_bot.tempo_restante == 30:
            await enviar_aviso("⏰ **30 segundos restantes!**")
        elif bid_bot.tempo_restante == 10:
            await enviar_aviso("⏰ **10 segundos!**")
        
        if bid_bot.tempo_restante <= 0:
            await finalizar_leilao()

async def enviar_aviso(mensagem):
    """Envia aviso para todos os canais que o bot tem acesso"""
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                if bid_bot.item_atual:
                    mensagem = f"🎁 **{bid_bot.item_atual['nome']}** - {mensagem}"
                await channel.send(mensagem)
                break

async def finalizar_leilao():
    """Finaliza o leilão atual e limpa o chat"""
    bid_bot.leilao_ativo = False
    
    if bid_bot.item_atual:
        mensagem_final = (
            f"🏁 **LEILÃO FINALIZADO!** 🏁\n"
            f"🎁 **Item:** {bid_bot.item_atual['nome']}\n"
            f"📦 **Quantidade:** {bid_bot.quantidade_leilao}\n"
        )
        
        if bid_bot.vencedor_atual:
            nome_limpo, nome_original = bid_bot.obter_nome_jogador(bid_bot.vencedor_atual)
            pontuacao_vencedor = bid_bot.obter_pontuacao_base_jogador(bid_bot.vencedor_atual)
            saldo_restante = pontuacao_vencedor - bid_bot.lance_atual
            
            # ATUALIZADO: Agora atualiza pontos E itens
            sucesso = await bid_bot.atualizar_pontos_e_itens(
                bid_bot.vencedor_atual, 
                bid_bot.lance_atual,
                bid_bot.item_atual['id'],
                bid_bot.item_atual['quantidade_restante']
            )
            
            mensagem_final += (
                f"👑 **Vencedor:** {bid_bot.vencedor_atual.mention} ({nome_limpo})\n"
                f"💵 **Lance vencedor:** {bid_bot.lance_atual} pontos\n"
                f"💰 **Saldo restante do vencedor:** {saldo_restante} pontos\n"
                f"📦 **Quantidade adquirida:** {bid_bot.quantidade_leilao}\n"
                f"📈 **Total de lances:** {len(bid_bot.historico_lances)}"
            )
            
            if sucesso:
                mensagem_final += f"\n✅ **Pontos debitados e quantidade atualizada na planilha!**"
            else:
                mensagem_final += f"\n⚠️ **Erro ao atualizar planilhas**"
        else:
            mensagem_final += "❌ Nenhum lance foi realizado."
        
        # MENSAGEM DE AGUARDO PARA O PRÓXIMO LEILÃO
        mensagem_aguardo = (
            f"\n\n⏳ **📢 COMUNICADO IMPORTANTE** ⏳\n"
            f"🔔 **Você será notificado quando o próximo leilão for iniciado!** 🔔\n"
            f"🎯 **Fique atento às notificações do bot para não perder a próxima oportunidade!** 🎯\n"
            f"📊 **Enquanto isso, verifique seus pontos com:** `!meuspontos`"
        )
        
        mensagem_completa = mensagem_final + mensagem_aguardo
        
        # LIMPAR O CHAT ANTES DE ENVIAR A MENSAGEM FINAL
        await limpar_chat_leilao()
        
        # Enviar mensagem final limpa
        await enviar_aviso(mensagem_completa)
        
        bid_bot.lances_reservados = {}
        bid_bot.item_atual = None
        bid_bot.lance_inicial = 0
        bid_bot.quantidade_leilao = 1

async def limpar_chat_leilao():
    """Limpa o chat completamente desde o início"""
    try:
        CANAL_LEILAO_ID = 1443392788388511909
        canal_leilao = bot.get_channel(CANAL_LEILAO_ID)
        
        if canal_leilao:
            print(f"🎯 Canal de leilão encontrado: #{canal_leilao.name}")
            
            try:
                # Método para limpar TODAS as mensagens (em lotes)
                mensagens_limpas_total = 0
                continuar_limpando = True
                
                while continuar_limpando:
                    # Limpa em lotes de 100 mensagens por vez
                    deletadas = await canal_leilao.purge(limit=100, check=lambda m: not m.pinned)
                    mensagens_limpas_total += len(deletadas)
                    
                    print(f"🧹 Lote limpo: {len(deletadas)} mensagens (Total: {mensagens_limpas_total})")
                    
                    # Se foram deletadas menos de 100 mensagens, chegamos ao fim
                    if len(deletadas) < 100:
                        continuar_limpando = False
                    
                    # Pequena pausa para não sobrecarregar a API do Discord
                    await asyncio.sleep(1)
                
                print(f"✅ Chat completamente limpo! Total de {mensagens_limpas_total} mensagens removidas de #{canal_leilao.name}")
                return True
                
            except discord.Forbidden:
                print("❌ Bot não tem permissão para limpar mensagens neste canal")
                print("💡 Configure as permissões: Gerenciar Mensagens + Ler Histórico de Mensagens")
                return False
                
            except discord.HTTPException as e:
                print(f"❌ Erro da API do Discord: {e}")
                return False
                
            except Exception as e:
                print(f"❌ Erro ao limpar canal: {e}")
                return False
                
        else:
            print("❌ Canal de leilão não encontrado! Verifique o ID.")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
