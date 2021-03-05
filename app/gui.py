#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QTableWidgetItem)
import pandas as pd

pasta_principal = os.path.expanduser("~/")
pasta_layout = os.path.join(os.path.dirname(__file__), "../layout/")


class CriaGrafico(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi(pasta_layout + "main.ui", self)

        self.actionAbrir.triggered.connect(self.carregar_dados)
        self.actionSalvar_2.triggered.connect(self.salvar_dados)
        self.actionSair.triggered.connect(self.sair)

        self.initUI()

    def initUI(self):
        self.show()

    def carregar_dados(self):
        def carregar_tabela():

            col_n = 0
            row_n = 0

            for i, col in enumerate(self.dados.columns):
                self.tableWidget.setHorizontalHeaderItem(i,
                    QTableWidgetItem(col)
                )

                for linha in range(self.dados.shape[0]):
                    self.tableWidget.setItem(row_n, col_n,
                        QTableWidgetItem(str(self.dados[col][linha])))
                    row_n += 1
                row_n = 0
                col_n += 1

        arquivo = QFileDialog.getOpenFileName(self, "Abrir arquivo",
                                              pasta_principal)
        if arquivo[0].endswith(".csv"):
            self.dados = pd.read_csv(arquivo[0])
        elif arquivo[0].endswith(".xls"):
            self.dados = pd.read_excel(arquivo[0])
        elif arquivo[0].endswith(".xlsx"):
            self.dados = pd.read_excel(arquivo[0])

        try:
            self.tableWidget.setRowCount(self.dados.shape[0])
            self.tableWidget.setColumnCount(self.dados.shape[1])

            carregar_tabela()
        except AttributeError:
            pass

    def salvar_dados(self):
        print("salvar")

    def sair(self):
        self.close()


def main():
    app = QApplication(sys.argv)
    foo = CriaGrafico()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
