import urwid
import sqlite3

class InventarioApp:
    def __init__(self):
        self.header = urwid.Text("INVENTARIO 2026", align='center')
        self.con = None

        botoes = [
            urwid.Button("Criar Inventário"),
            urwid.Button("Abrir Inventário"),
            urwid.Button("Inserir Dados"),
            urwid.Button("Buscar"),
            urwid.Button("Modificar"),
            urwid.Button("Deletar"),
            urwid.Button("Sair"),
        ]
        for btn in botoes:
            urwid.connect_signal(btn, 'click', self.on_button_click)

        self.body = urwid.ListBox(urwid.SimpleFocusListWalker([
            urwid.AttrMap(btn, None, focus_map='reversed') for btn in botoes
        ]))
        self.footer = urwid.Text("Barra de status")

        self.frame = urwid.Frame(header=self.header, body=self.body, footer=self.footer)

        palette = [
            ('header', 'white', 'dark blue'),
            ('footer', 'white', 'dark red'),
            ('body', 'black', 'light gray'),
            ('reversed', 'standout', ''),
        ]
        self.frame.header = urwid.AttrMap(self.header, 'header')
        self.frame.body = urwid.AttrMap(self.body, 'body')
        self.frame.footer = urwid.AttrMap(self.footer, 'footer')

        self.loop = urwid.MainLoop(self.frame, palette=palette, unhandled_input=self.handle_input)

    # =========================
    # EVENTOS DE BOTÕES
    # =========================
    def on_button_click(self, button):
        label = button.get_label()
        if label == "Sair":
            raise urwid.ExitMainLoop()
        elif label == "Criar Inventário":
            self.show_dialog_criar()
        elif label == "Abrir Inventário":
            self.show_dialog_abrir()
        elif label == "Inserir Dados":
            self.show_dialog_inserir()
        elif label == "Buscar":
            self.show_dialog_buscar()
        elif label == "Modificar":
            self.show_dialog_modificar()
        elif label == "Deletar":
            self.show_dialog_deletar()

    def handle_input(self, key):
        if key in ('q', 'Q', 'esc'):
            raise urwid.ExitMainLoop()

    # =========================
    # DIÁLOGOS
    # =========================
    def show_dialog_criar(self):
        edit = urwid.Edit("Nome do inventário: ")
        ok = urwid.Button("OK")
        cancel = urwid.Button("Cancelar")

        def salvar(_):
            nome = edit.get_edit_text()
            try:
                self.con = sqlite3.connect(f"{nome}.db")
                cur = self.con.cursor()
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS materiais (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        type TEXT,
                        descricao TEXT,
                        name TEXT,
                        d_tecn TEXT,
                        quant INTEGER,
                        endereco TEXT
                    )
                """)
                self.footer.set_text(f"Inventário '{nome}.db' criado com sucesso!")
            except Exception as e:
                self.footer.set_text(f"Erro: {e}")
            self.loop.widget = self.frame

        urwid.connect_signal(ok, 'click', salvar)
        urwid.connect_signal(cancel, 'click', lambda _: self.loop.widget == self.frame)

        self._show_overlay(edit, ok, cancel, "Criar Inventário")

    def show_dialog_abrir(self):
        edit = urwid.Edit("Nome do inventário: ")
        ok = urwid.Button("OK")
        cancel = urwid.Button("Cancelar")

        def abrir(_):
            nome = edit.get_edit_text()
            try:
                self.con = sqlite3.connect(f"{nome}.db")
                self.footer.set_text(f"Inventário '{nome}.db' aberto com sucesso!")
            except Exception as e:
                self.footer.set_text(f"Erro: {e}")
            self.loop.widget = self.frame

        urwid.connect_signal(ok, 'click', abrir)
        urwid.connect_signal(cancel, 'click', lambda _: self.loop.widget == self.frame)

        self._show_overlay(edit, ok, cancel, "Abrir Inventário")

    def show_dialog_inserir(self):
        """Inserir novo registro na tabela"""
        type_edit = urwid.Edit("Tipo: ")
        desc_edit = urwid.Edit("Descrição: ")
        name_edit = urwid.Edit("Nome: ")
        dtecn_edit = urwid.Edit("Dados Técnicos: ")
        quant_edit = urwid.Edit("Quantidade: ")
        end_edit = urwid.Edit("Endereço: ")
        ok = urwid.Button("OK")
        cancel = urwid.Button("Cancelar")

        def inserir(_):
            try:
                cur = self.con.cursor()
                cur.execute("""
                    INSERT INTO materiais (type, descricao, name, d_tecn, quant, endereco)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    type_edit.get_edit_text(),
                    desc_edit.get_edit_text(),
                    name_edit.get_edit_text(),
                    dtecn_edit.get_edit_text(),
                    int(quant_edit.get_edit_text()),
                    end_edit.get_edit_text()
                ))
                self.con.commit()
                self.footer.set_text("Registro inserido com sucesso!")
            except Exception as e:
                self.footer.set_text(f"Erro: {e}")
            self.loop.widget = self.frame

        urwid.connect_signal(ok, 'click', inserir)
        urwid.connect_signal(cancel, 'click', lambda _: self.loop.widget == self.frame)

        self._show_overlay([type_edit, desc_edit, name_edit, dtecn_edit, quant_edit, end_edit], ok, cancel, "Inserir Dados")

    def show_dialog_buscar(self):
        edit = urwid.Edit("ID do registro: ")
        ok = urwid.Button("OK")
        cancel = urwid.Button("Cancelar")

        def buscar(_):
            try:
                cur = self.con.cursor()
                res = cur.execute("SELECT * FROM materiais WHERE id=?", (edit.get_edit_text(),))
                linha = res.fetchone()
                self.footer.set_text(f"Resultado: {linha}")
            except Exception as e:
                self.footer.set_text(f"Erro: {e}")
            self.loop.widget = self.frame

        urwid.connect_signal(ok, 'click', buscar)
        urwid.connect_signal(cancel, 'click', lambda _: self.loop.widget == self.frame)

        self._show_overlay(edit, ok, cancel, "Buscar Registro")

    def show_dialog_modificar(self):
        id_edit = urwid.Edit("ID: ")
        campo_edit = urwid.Edit("Campo: ")
        valor_edit = urwid.Edit("Novo valor: ")
        ok = urwid.Button("OK")
        cancel = urwid.Button("Cancelar")

        def modificar(_):
            try:
                cur = self.con.cursor()
                sql = f"UPDATE materiais SET {campo_edit.get_edit_text()}=? WHERE id=?"
                cur.execute(sql, (valor_edit.get_edit_text(), id_edit.get_edit_text()))
                self.con.commit()
                self.footer.set_text("Registro atualizado com sucesso!")
            except Exception as e:
                self.footer.set_text(f"Erro: {e}")
            self.loop.widget = self.frame

        urwid.connect_signal(ok, 'click', modificar)
        urwid.connect_signal(cancel, 'click', lambda _: self.loop.widget == self.frame)

        self._show_overlay([id_edit, campo_edit, valor_edit], ok, cancel, "Modificar Registro")

    def show_dialog_deletar(self):
        edit = urwid.Edit("ID do registro: ")
        ok = urwid.Button("OK")
        cancel = urwid.Button("Cancelar")

        def deletar(_):
            try:
                cur = self.con.cursor()
                cur.execute("DELETE FROM materiais WHERE id=?", (edit.get_edit_text(),))
                self.con.commit()
                self.footer.set_text("Registro deletado com sucesso!")
            except Exception as e:
                self.footer.set_text(f"Erro: {e}")
            self.loop.widget = self.frame

        urwid.connect_signal(ok, 'click', deletar)
        urwid.connect_signal(cancel, 'click', lambda _: self.loop.widget == self.frame)

        self._show_overlay(edit, ok, cancel, "Deletar Registro")

    # =========================
    # FUNÇÃO AUXILIAR
    # =========================
    def _show_overlay(self, edits, ok, cancel, titulo):
        if not isinstance(edits, list):
            edits = [edits]
        dialog = urwid.LineBox(
            urwid.ListBox(urwid.SimpleFocusListWalker(
                edits + [urwid.Divider(), urwid.Columns([ok, cancel], dividechars=2)]
            )),
            title=titulo
        )
        overlay = urwid.Overlay(dialog, self.frame,
                                align='center', width=('relative', 50),
                                valign='middle', height=('relative', 60),
                                min_width=20, min_height=5)
        self.loop.widget = overlay

    def run(self):
        self.loop.run()


if __name__ == "__main__":
    app = InventarioApp()
    app.run()
