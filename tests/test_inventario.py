# test_inventario.py
import unittest
import sqlite3
import os

DB_NAME = "test_inventario.db"

class TestInventario(unittest.TestCase):

    def setUp(self):
        # Cria um banco de testes limpo antes de cada teste
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)
        self.con = sqlite3.connect(DB_NAME)
        cur = self.con.cursor()
        cur.execute("""
            CREATE TABLE materiais (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT,
                descricao TEXT,
                name TEXT,
                d_tecn TEXT,
                quant INTEGER,
                endereco TEXT
            )
        """)
        self.con.commit()

    def tearDown(self):
        # Fecha conexão e remove banco após cada teste
        self.con.close()
        if os.path.exists(DB_NAME):
            os.remove(DB_NAME)

    def test_inserir_dados(self):
        cur = self.con.cursor()
        cur.execute("INSERT INTO materiais (type, descricao, name, d_tecn, quant, endereco) VALUES (?, ?, ?, ?, ?, ?)",
                    ("Ferramenta", "Martelo", "Hammer", "Aço", 10, "A1"))
        self.con.commit()

        cur.execute("SELECT * FROM materiais WHERE name=?", ("Hammer",))
        row = cur.fetchone()
        self.assertIsNotNone(row)
        self.assertEqual(row[2], "Martelo")

    def test_buscar_registro(self):
        cur = self.con.cursor()
        cur.execute("INSERT INTO materiais (type, descricao, name, d_tecn, quant, endereco) VALUES (?, ?, ?, ?, ?, ?)",
                    ("Ferramenta", "Chave de fenda", "Screwdriver", "Metal", 5, "B2"))
        self.con.commit()

        cur.execute("SELECT * FROM materiais WHERE name=?", ("Screwdriver",))
        row = cur.fetchone()
        self.assertEqual(row[2], "Chave de fenda")

    def test_modificar_registro(self):
        cur = self.con.cursor()
        cur.execute("INSERT INTO materiais (type, descricao, name, d_tecn, quant, endereco) VALUES (?, ?, ?, ?, ?, ?)",
                    ("Ferramenta", "Serrote", "Saw", "Aço", 3, "C3"))
        self.con.commit()

        cur.execute("UPDATE materiais SET quant=? WHERE name=?", (7, "Saw"))
        self.con.commit()

        cur.execute("SELECT quant FROM materiais WHERE name=?", ("Saw",))
        row = cur.fetchone()
        self.assertEqual(row[0], 7)

    def test_deletar_registro(self):
        cur = self.con.cursor()
        cur.execute("INSERT INTO materiais (type, descricao, name, d_tecn, quant, endereco) VALUES (?, ?, ?, ?, ?, ?)",
                    ("Ferramenta", "Alicate", "Pliers", "Metal", 2, "D4"))
        self.con.commit()

        cur.execute("DELETE FROM materiais WHERE name=?", ("Pliers",))
        self.con.commit()

        cur.execute("SELECT * FROM materiais WHERE name=?", ("Pliers",))
        row = cur.fetchone()
        self.assertIsNone(row)


if __name__ == "__main__":
    unittest.main()
