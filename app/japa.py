#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog,
     QTableWidgetItem, QMessageBox, QDialog, QMenu, QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QFont
from PyQt5.QtCore import pyqtSignal
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pandas as pd

from testes import teste_kappa_fleiss, teste_t_ind


pasta_principal = os.path.expanduser("~/")
pasta_layout = os.path.join(os.path.dirname(__file__), "../layout/")
pasta_assets = os.path.join(os.path.dirname(__file__), "../assets/")


class CriaGrafico(QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi(pasta_layout + "main.ui", self)

        self.setMinimumSize(480, 320)
        self.actionAbrir.triggered.connect(self.carregar_dados)
        self.actionSalvar_2.triggered.connect(self.salvar_dados)
        self.actionConcatenar_dados.triggered.connect(
            self.concatenar_arquivos
        )
        self.actionSair.triggered.connect(self.sair)
        self.actionTipos_de_gr_fico.triggered.connect(self.lista_grafico)
        self.actionPlotar_gr_fico.triggered.connect(self.cria_grafico)
        self.menuTratar_dados.triggered.connect(self.remove_na)
        self.actionKappa_Fleiss.triggered.connect(self.executa_teste)
        self.actionTeste_T.triggered.connect(self.executa_teste)
        # self.actionDesenvolvimento.triggered.connect(self.infor)

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
            self.dados = pd.read_csv(arquivo[0], low_memory=False)
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

        for i, col in enumerate(dados.columns):
            self.tableWidget.setHorizontalHeaderItem(i,
                QTableWidgetItem(col)
            )

        for indice_coluna, col in enumerate(dados.columns.to_list()):
            for indice_linha, linha in enumerate(dados[col]):
                self.tableWidget.setItem(indice_linha, indice_coluna,
                    QTableWidgetItem(str(linha)))

    def salvar_dados(self):
        arquivo = QFileDialog.getSaveFileName(self, "Salvar arquivo",
                                              pasta_principal)
        try:
            if arquivo[0].endswith(".csv"):
                self.dados.to_csv(f"{arquivo[0]}", index=False)
            elif arquivo[0].endswith(".xls"):
                self.dados.to_excel(f"{arquivo[0]}", index=False)
            elif arquivo[0].endswith(".xlsx"):
                self.dados.to_excel(f"{arquivo[0]}", index=False)
            else:
                self.dados.to_csv(f"{arquivo[0]}", index=False)
        except AttributeError:
            try:
                if arquivo[0].endswith(".csv"):
                    pd.DataFrame().to_csv(f"{arquivo[0]}", index=False)
                elif arquivo[0].endswith(".xls"):
                    pd.DataFrame().to_excel(f"{arquivo[0]}", index=False)
                elif arquivo[0].endswith(".xlsx"):
                    pd.DataFrame().to_excel(f"{arquivo[0]}", index=False)
                else:
                    pd.DataFrame().to_csv(f"{arquivo[0]}", index=False)
            except FileNotFoundError:
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

    def atualiza_layout(self, dados):
        self.selecao_de_coluna.listWidget.clear()
        self.selecao_de_coluna.listWidget.addItems(dados.columns)
        self.escreve_tabela(dados)

    def executa_teste(self):
        try:
            if self.sender().text() == "Kappa Fleiss":
                self.escreve_relatorio(
                    teste_kappa_fleiss(
                        self.dados, self.pega_colunas_selecionadas()
                    )
                )
            elif self.sender().text() == "Teste T":
                if len(self.pega_colunas_selecionadas()) == 2:
                    self.escreve_relatorio(
                        teste_t_ind(
                            self.dados, self.pega_colunas_selecionadas()
                        )
                    )
                else:
                    pass
        except AttributeError:
            pass

    def pega_colunas_selecionadas(self):
        rows = set(
            cell.column() for cell in self.tableWidget.selectedIndexes()
        )
        headers = [
            self.tableWidget.horizontalHeaderItem(r) for r in rows
        ]
        return [x.text() for x in headers if x is not None]

    def escreve_relatorio(self, informacao):
        self.plainTextEdit.clear()
        self.plainTextEdit.insertPlainText(informacao)

    def remove_na(self):
        try:
            self.dados.dropna(inplace=True)
            self.escreve_tabela(self.dados)
        except AttributeError:
            pass
            # self.erro = MensagemErro()
            # self.erro.setText("Arquivo não foi carregado ou não existe")
            # self.erro.buttonClicked.connect(lambda: self.destroy)
            # self.erro.show()

    def lista_grafico(self):
        self.janelagrafico = JanelaGrafico()

    def cria_grafico(self):
        self.janelagrafico.cria_grafico(
            self.dados[self.pega_colunas_selecionadas()[0]],
            self.dados[self.pega_colunas_selecionadas()[1]]
        )

        # if 'self.dados_filtrados' in locals():
        #     print('testou locals')
        # elif 'self.dados_filtrados' in globals():
        #     print('testou globals')

    def infor(self):
        self.sobre = Sobre()
        self.sobre.setFixedSize(365, 81)
        self.sobre.show()

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)

        sair = contextMenu.addAction("Sair")
        action = contextMenu.exec_(self.mapToGlobal(event.pos()))

        if action == sair: self.sair()


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


class JanelaGrafico(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.args = args
        self.kwargs = kwargs

        self.grafico = pg.PlotWidget()
        self.setCentralWidget(self.grafico)

    def seletor_de_colunas(self):
        pass

    def cria_grafico(self, *dados):
        self.grafico.plot(*dados)
        self.show()

    def lista_de_graficos(self):
        pass

    def salvar_grafico(self):
        pass


class Sobre(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(pasta_layout + "sobre.ui", self)


class MensagemErro(QMessageBox):
    def __init__(self):
        super().__init__()

        self.configuracao_basica()

    def configuracao_basica(self):
        self.setFont(QFont("Arial", 15))
        self.setWindowTitle("Erro!")
        self.setStandardButtons(self.Ok)


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(pasta_assets + "cat_ico.png"))
    foo = CriaGrafico()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
