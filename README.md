# Report Atualização ObservaSampa

Automatização do relatório de atualização dos indicadores do ObservaSampa.

Os cálculos são feitos da seguinte forma:
* Para cada indicador, obter a ficha do indicador;
* Na ficha do indicador, identificar sua periodicidade;
* Realizar calcular o ano ideal de disponibilização dos dados a partir da periodicidade:
    * Por exemplo, "anual" = ano_atual - 1, "descenal" = ano_atual - 10 etc.
* Cruzar o ano obtido com o último valor disponível para o indicador na planilha de download de dados abertos do indicador.

Gerar assim o relatório com os indicadores desatualizados e produzir visualizações.
