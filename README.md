# 📦 Inventário 2026

Um sistema de inventário retrô feito em **Python**, utilizando **Urwid** para a interface de terminal e **SQLite** para persistência dos dados.  
O projeto oferece uma interface simples e interativa para gerenciar materiais, permitindo criar, abrir, inserir, buscar, modificar e deletar registros.

---

## 🚀 Funcionalidades

- **Criar Inventário**: Cria um novo banco de dados SQLite com a tabela `materiais`.
- **Abrir Inventário**: Abre um inventário existente (`.db`).
- **Inserir Dados**: Adiciona novos registros com campos como tipo, descrição, nome, dados técnicos, quantidade e endereço.
- **Buscar**: Localiza registros pelo ID.
- **Modificar**: Atualiza campos de registros existentes.
- **Deletar**: Remove registros pelo ID.
- **Interface Retrô**: Menu com botões e diálogos em estilo retrô usando Urwid.

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Urwid](http://urwid.org/) — biblioteca para interfaces de terminal.
- [SQLite3](https://www.sqlite.org/) — banco de dados leve e embutido.

---

## 📂 Estrutura da Tabela

A tabela `materiais` é criada automaticamente com os seguintes campos:

| Campo      | Tipo        | Descrição                  |
|------------|-------------|----------------------------|
| id         | INTEGER PK  | Identificador único        |
| type       | TEXT        | Tipo do material           |
| descricao  | TEXT        | Descrição breve            |
| name       | TEXT        | Nome do material           |
| d_tecn     | TEXT        | Dados técnicos             |
| quant      | INTEGER     | Quantidade disponível      |
| endereco   | TEXT        | Localização/Endereço       |

---

## Instalar dependencias

pip install urwid

## Executar programa

python inventario.py

🎮 Atalhos
- q ou esc → sair do programa

- F2 → salvar

- F5 → executar

📜 Licença
Este projeto é distribuído sob a licença MIT.
Sinta-se livre para usar, modificar e compartilhar.

👨‍💻 Desenvolvido por Marco


