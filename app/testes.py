from nltk import agreement


def teste_kappa_fleiss(tabela, colunas):
    count = 0
    valor_coluna = []
    # for coluna in tabela.columns.to_list():
    for coluna in colunas:
        valor_coluna += [
            [count, str(i), str(tabela[coluna][i])]
            for i in range(0, len(tabela[coluna]))
        ]
        count += 1
    resultado = agreement.AnnotationTask(data=valor_coluna)

    resultado_final = 'Kappa: {}\nFleiss: {}\nAlpha: {}\nScotts: {}'.format(
        resultado.kappa(),
        resultado.multi_kappa(), resultado.alpha(), resultado.pi()
    )

    return resultado_final
