#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QTableWidgetItem, QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
import pandas as pd

pasta_principal = os.path.expanduser("~/")
pasta_layout = os.path.join(os.path.dirname(__file__), "../layout/")


class CriaGrafico(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi(pasta_layout + "main.ui", self)

        self.actionAbrir.triggered.connect(self.carregar_dados)
        self.actionSalvar_2.triggered.connect(self.salvar_dados)
        self.actionFiltrar_dados.triggered.connect(self.selecionar_colunas)
        self.actionConcatenar_dados.triggered.connect(
            self.concatenar_arquivos
        )
        self.actionSair.triggered.connect(self.sair)

        self.initUI()

    def initUI(self):
        self.show()

    def carregar_dados(self):
        arquivo = QFileDialog.getOpenFileName(self, "Abrir arquivo",
                                              pasta_principal, 
                                              ("Arquivo csv (*.csv);;\
                                               Excel 2007–365 (*.xlsx);;\
                                               Excel 97–2003 (*.xls)"))
        if arquivo[0].endswith(".csv"):
            self.dados = pd.read_csv(arquivo[0])
        elif arquivo[0].endswith(".xls"):
            self.dados = pd.read_excel(arquivo[0])
        elif arquivo[0].endswith(".xlsx"):
            self.dados = pd.read_excel(arquivo[0])

        try:
            self.escreve_tabela(self.dados)
        except AttributeError:
            pass

    def escreve_tabela(self, dados):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(dados.shape[0])
        self.tableWidget.setColumnCount(dados.shape[1])

        col_n = 0
        row_n = 0
        for i, col in enumerate(dados.columns):
            self.tableWidget.setHorizontalHeaderItem(i,
                QTableWidgetItem(col)
            )
            for linha in range(dados.shape[0]):
                self.tableWidget.setItem(row_n, col_n,
                    QTableWidgetItem(str(self.dados[col][linha])))
                row_n += 1
            row_n = 0
            col_n += 1

    def salvar_dados(self):
        arquivo = QFileDialog.getSaveFileName(self, "Salvar arquivo",
                                              pasta_principal)
        try:
            if arquivo[0].endswith(".csv"):
                self.dados.to_csv(f"{arquivo[0].split('/')[-1]}",
                                  index=False)
            elif arquivo[0].endswith(".xls"):
                self.dados.to_excel(f"{arquivo[0].split('/')[-1]}",
                                    index=False)
            elif arquivo[0].endswith(".xlsx"):
                self.dados.to_excel(f"{arquivo[0].split('/')[-1]}",
                                    index=False)
            else:
                self.dados.to_csv(f"{arquivo[0].split('/')[-1]}",
                                  index=False)
        except AttributeError:
            print("nada para salvar")

    def selecionar_colunas(self):
        try:
            if not self.dados.empty:
                self.selecao_de_coluna = SelecaoColuna()
                self.selecao_de_coluna.listWidget.addItems(
                    self.dados.columns
                )
                self.selecao_de_coluna.selecao.connect(self.aplicar_mudancas)
                self.selecao_de_coluna.reverter_.connect(self.restaura_bkp)
            else:
                pass
        except AttributeError:
            pass

    def concatenar_arquivos(self):
        lista_de_tabelas = []
        def concatena():
            try:
                lista_de_tabelas.append(self.dados)
                self.dados = pd.concat(lista_de_tabelas, ignore_index=True)
                self.escreve_tabela(self.dados)
            except AttributeError:
                pass

        arquivo = QFileDialog.getOpenFileName(self, "Abrir arquivo",
                                              pasta_principal, 
                                              ("Arquivo csv (*.csv);;\
                                               Excel 2007–365 (*.xlsx);;\
                                               Excel 97–2003 (*.xls)"))
        if arquivo[0].endswith(".csv"):
            lista_de_tabelas.append(pd.read_csv(arquivo[0]))
        elif arquivo[0].endswith(".xls"):
            lista_de_tabelas.append(pd.read_excel(arquivo[0]))
        elif arquivo[0].endswith(".xlsx"):
            lista_de_tabelas.append(pd.read_excel(arquivo[0]))

        concatena()


    def sair(self):
        self.close()

    def aplicar_mudancas(self, colunas):
        self.dados_backup = self.dados
        remover = [col for col in self.dados.columns if col not in colunas]
        self.dados_filtrados = self.dados.drop(remover, axis=1)
        self.atualiza_layout(self.dados_filtrados)

    def atualiza_layout(self, dados):
        self.selecao_de_coluna.listWidget.clear()
        self.selecao_de_coluna.listWidget.addItems(dados.columns)
        self.escreve_tabela(dados)

    def restaura_bkp(self):
        try:
            self.dados = self.dados_backup
            self.atualiza_layout(self.dados)
        except AttributeError:
            pass


class SelecaoColuna(QMainWindow):

    selecao = pyqtSignal(list)
    reverter_ = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        uic.loadUi(pasta_layout + "selecao_de_coluna.ui", self)

        self.listWidget.itemDoubleClicked.connect(self.seleciona_coluna)
        self.listWidget_2.itemDoubleClicked.connect(self.remove_coluna)
        self.pushButton.clicked.connect(self.adiciona_coluna)
        self.pushButton_2.clicked.connect(self.remove_coluna)
        self.pushButton_3.clicked.connect(self.envia_mudancas)
        self.pushButton_4.clicked.connect(self.reverter_.emit)
        self.initUI()

    def initUI(self):
        self.show()

    def adiciona_coluna(self):
        colunas = self.listWidget.selectedItems()
        for col in colunas:
            if col.text() not in self.confere_selecoes():
                self.listWidget_2.addItem(col.text())

    def confere_selecoes(self):
        colunas = [
            self.listWidget_2.item(x).text()
            for x in range(self.listWidget_2.count())
        ]
        return colunas

    def seleciona_coluna(self, val):
        if val.text() not in self.confere_selecoes():
            self.listWidget_2.addItem(val.text())

    def remove_coluna(self):
        coluna = self.listWidget_2.selectedItems()
        for col in coluna:
            self.listWidget_2.takeItem(self.listWidget_2.row(col))

    def envia_mudancas(self):
        colunas = [
                self.listWidget_2.item(x).text()
                for x in range(self.listWidget_2.count())
        ]
        self.selecao.emit(colunas)

    def reverter(self):
        self.reverter_.emit()


def main():
    app = QApplication(sys.argv)
    foo = CriaGrafico()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
