#Tesi 13/03/2020
* Comandi dello studente
    * Già implementati:
        * /question: permette di inviare domande al professore.
        * /report: permette di segnalare un bug allo sviluppatore.
        * /start: apre la guida e avvia il bot.
    * Da implementare (suggeriti da studenti):
        * /revision: permette a uno studente di chiedere al professore una revisione della domanda.
          * pro: permette a uno studente di segnalare eventuali errori al professore.
          * contro: rischia di fare flooding sul professore.
* Comandi del professore:
    * Già implementati:
        * /answer: permette di rispondere a una domanda.
        * /ban: permette di segnalare una domanda come inopportuna e di toglierla dalla lista delle domande in attesa di risposta.
        * /ban_list: mostra tutte le domande segnate come inopportune.
        * /list: mostra tutte le domande a cui si è già risposto.
        * /report: permette di segnalare un bug allo sviluppatore.
        * /start: apre la guida e avvia il bot.
    * Da implementare (suggeriti da studenti):
        * /change: permette di cambiare il responso di una domanda.
          * pro: permette di cambiare la risposta a una domanda senza contattare lo sviluppatore.
          * contro: rischia di fare flooding sullo studente.
        * /sban: permette di rimettere una domanda definita inopportuna nella lista delle domande in attesa di risposta.
* Da fare in un prossimo futuro:
    * Diminuire debito tecnico (anche se basso vorrei ridurlo).
    * Migliorare la struttura dati. (Fatto)
    * Migliorare e velocizzare il riconoscimento della frase. (Fatto)
    * Migliorare le keyboards. (Fatto)
    * Refactoring.
    * Testare la portabilità del multi processing/threading su linux.
* Extra:
    * Aggiunta una modalitá manutenzione nel caso vengano segnalati bug veramente gravi o per rilasciare aggionamenti
* Idee:
    * Possibilità di bannare lo studente dal bot se fa troppi /revision inutili o domande inopportune.
    * Possibilità di avere solo un numero massimo di revision a domanda.
