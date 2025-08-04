import streamlit as st
from datetime import date
import os

from services.turma_service import criar_turma, listar_turmas, deletar_turma
from services.aluno_service import criar_aluno, listar_alunos, listar_por_turma, deletar_aluno
from services.chamada_service import registrar_chamada, historico_por_turma
from utils.validators import validar_telefone, validar_texto

st.set_page_config(page_title="Controle de Chamadas", layout="wide")
st.title("📚 Controle de Chamadas")

menu = st.sidebar.radio("Menu", ["Turmas", "Alunos", "Chamadas"])

# --- CRUD Turmas ---
if menu == "Turmas":
    st.header("Gerenciar Turmas")
    with st.form("form_turma"):
        nome = st.text_input("Nome da Turma", max_chars=100)
        descricao = st.text_area("Descrição", max_chars=500)
        inicio = st.date_input("Data de Início")
        fim = st.date_input("Data de Término")
        submit = st.form_submit_button("Criar Turma")
        if submit:
            if validar_texto(nome, 100) and validar_texto(descricao, 500):
                criar_turma(nome, descricao, inicio, fim)
                st.success("✅ Turma criada com sucesso!")
            else:
                st.error("❌ Verifique os limites de texto.")

    st.subheader("📋 Turmas Cadastradas")
    for turma in listar_turmas():
        st.write(f"**{turma.nome}** - {turma.descricao}")
        st.write(f"Início: {turma.data_inicio} | Término: {turma.data_fim}")
        col1, col2 = st.columns(2)
        if col2.button(f"Deletar Turma {turma.id}"):
            deletar_turma(turma.id)
            st.success("🗑️ Turma excluída.")

# --- CRUD Alunos ---
elif menu == "Alunos":
    st.header("Gerenciar Alunos")
    turmas = listar_turmas()
    turma_opcoes = {t.id: t.nome for t in turmas}
    with st.form("form_aluno"):
        nome = st.text_input("Nome do Aluno", max_chars=100)
        # Limites para data de nascimento: mínimo 95 anos atrás, máximo hoje
        hoje = date.today()
        min_nascimento = date(hoje.year - 95, 1, 1)
        max_nascimento = hoje
        nascimento = st.date_input(
            "Data de Nascimento",
            value=date(2000, 1, 1),
            min_value=min_nascimento,
            max_value=max_nascimento
        )
        telefone = st.text_input("Telefone", placeholder="(XX) XXXXX-XXXX")
        foto = st.file_uploader("Foto", type=["jpg", "png"])
        turma_id = st.selectbox("Turma", options=list(turma_opcoes.keys()), format_func=lambda x: turma_opcoes[x])
        submit = st.form_submit_button("Adicionar Aluno")
        if submit:
            if validar_telefone(telefone):
                foto_path = f"assets/fotos_alunos/{nome.replace(' ', '_')}.png"
                os.makedirs("assets/fotos_alunos", exist_ok=True)
                if foto:
                    with open(foto_path, "wb") as f:
                        f.write(foto.read())
                criar_aluno(nome, nascimento, telefone, foto_path, turma_id)
                st.success("✅ Aluno cadastrado com sucesso!")
            else:
                st.error("❌ Telefone inválido. Use o formato (XX) XXXXX-XXXX.")

    st.subheader("👥 Alunos Cadastrados")
    for aluno in listar_alunos():
        st.image(aluno.foto_path, width=50)
        turma_nome = turma_opcoes.get(aluno.turma_id, "Turma não encontrada")
        st.write(f"**{aluno.nome}** | {aluno.telefone} | Turma: {turma_nome}")
        col1, col2 = st.columns(2)
        if col2.button(f"Deletar Aluno {aluno.id}"):
            deletar_aluno(aluno.id)
            st.success("🗑️ Aluno excluído.")

# --- Registro de Chamadas ---
elif menu == "Chamadas":
    st.header("Registro de Chamadas")
    turmas = listar_turmas()
    turma_opcoes = {t.id: t.nome for t in turmas}
    turma_id = st.selectbox("Selecionar Turma", options=list(turma_opcoes.keys()), format_func=lambda x: turma_opcoes[x])
    data_chamada = st.date_input("Data da Chamada", value=date.today())

    alunos_turma = listar_por_turma(turma_id)
    for aluno in alunos_turma:
        col1, col2, col3 = st.columns([2, 1, 1])
        col1.write(f"👤 {aluno.nome}")
        if col2.button(f"Presente {aluno.id}"):
            registrar_chamada(turma_id, aluno.id, data_chamada, "Presente")
            st.success(f"{aluno.nome} marcado como presente.")
        if col3.button(f"Falta {aluno.id}"):
            registrar_chamada(turma_id, aluno.id, data_chamada, "Falta")
            st.warning(f"{aluno.nome} marcado como ausente.")

    st.subheader("📅 Histórico de Chamadas")
    for chamada in historico_por_turma(turma_id):
        aluno_nome = next((a.nome for a in listar_alunos() if a.id == chamada.aluno_id), "Desconhecido")
        st.write(f"{chamada.data} - {aluno_nome}: {chamada.status}")