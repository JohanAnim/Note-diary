# Note Diary per NVDA

Un componente aggiuntivo per NVDA che ti consente di creare, modificare, importare ed esportare note in modo rapido ed efficiente.

## Caratteristiche

*   **Gestione di Diari e Capitoli**: Organizza le tue note in diari e capitoli per una migliore struttura.
*   **Modifica Rapida**: Apri e modifica i capitoli con facilità.
*   **Importazione ed Esportazione**: Salva e ripristina i tuoi diari e capitoli in file `.ndn`.
*   **Ricerca Integrata**: Trova rapidamente diari e capitoli per nome.
*   **Accessibilità Migliorata**: Progettato pensando all'accessibilità per gli utenti NVDA.
*   **Suoni Personalizzabili**: Configura i suoni per gli eventi chiave del componente aggiuntivo.

## Installazione

1.  Scarica l'ultima versione del componente aggiuntivo dal link di download.
2.  Apri il file `.nvda-addon` scaricato.
3.  Conferma l'installazione quando richiesto da NVDA.
4.  Riavvia NVDA affinché le modifiche abbiano effetto.

## Come usare il componente aggiuntivo

Per utilizzare il componente aggiuntivo, segui questi passaggi:

1.  **Apri il componente aggiuntivo**: Accedi a Note Diary dal menu NVDA, in `Strumenti` > `Note Diary`. Puoi assegnare una scorciatoia da tastiera in `Preferenze` > `Gesti di input` nella categoria `Note Diary`.
2.  **Crea un diario**: Premi il pulsante del menu `Altre opzioni` e seleziona `Nuovo diario`, oppure usa `CTRL+N` nell'albero dei diari. Inserisci il nome del diario (es., "Il mio diario personale", "Corso di Python").
3.  **Crea capitoli**: Con il diario selezionato, premi `Altre opzioni` > `Nuovo capitolo`, oppure usa `CTRL+P`. Dai un nome al capitolo (es., "Lezione 01 Ciao mondo", "05/07/2025").
4.  **Scrivi in un capitolo**: Seleziona un capitolo e premi `Invio`, oppure `Applicazioni` / `Shift+F10` e seleziona `Modifica`. Inizia a scrivere nel campo di testo multilinea.
5.  **Salva il capitolo**: Premi `Alt+G` o naviga con `Tab` fino al pulsante `Salva` e premilo. Se ci sono modifiche e chiudi la finestra, ti verrà chiesto se desideri salvare.

## Spiegazione dell'interfaccia

### L'elenco dei diari

È una visualizzazione ad albero che ti consente di navigare tra diari e capitoli. I diari sono al livello 0. Usa le frecce su/giù per spostarti, `Invio` o le frecce sinistra/destra per espandere/comprimere i diari. Puoi anche navigare con le lettere dell'alfabeto.

### Il pulsante Altre opzioni

Quando premi questo pulsante o lo metti a fuoco e premi la freccia giù, appaiono le seguenti opzioni:

*   **Nuovo diario**: Crea un nuovo diario.
*   **Nuovo capitolo**: Crea un nuovo capitolo nel diario selezionato.
*   **Importa diari**: Ripristina i diari da un file `.ndn`.
*   **Esporta diari**: Salva tutti i tuoi diari e capitoli in un file `.ndn` per il backup o la condivisione.
*   **Aiuto**: Contiene `Informazioni su...` (informazioni di base sul componente aggiuntivo) e `Documentazione` (apre questo file nel browser).

### Casella informazioni di sola lettura

Dopo l'elenco dei diari, troverai una casella di modifica di sola lettura con informazioni di base sul diario o capitolo selezionato.

*   **Diari**: Mostra nome, data di creazione, data di modifica e numero di capitoli.
*   **Capitoli**: Mostra nome del capitolo, diario a cui appartiene, data di creazione, data di modifica e numero di pagine.

### Il pulsante Chiudi

Chiude la finestra del componente aggiuntivo. Puoi anche usare il tasto `Esc`.

## Elenco delle scorciatoie da tastiera

### Finestra principale

*   `Ctrl+N`: Crea un nuovo diario.
*   `Ctrl+P`: Crea un nuovo capitolo nel diario selezionato.
*   `Canc`: Elimina un diario (con tutti i suoi capitoli) o un capitolo.
*   `Invio`: Apre/chiude un diario; apre la finestra di modifica di un capitolo.
*   `F5`: Aggiorna la finestra.
*   `F2`: Rinomina il diario o capitolo selezionato.
*   `F1`: Apre questo documento.
*   `Applicazioni` o `Shift+F10`: Apre un menu contestuale per il diario o capitolo selezionato.

### Scorciatoie utili nella finestra principale

*   `Alt+M`: Apre il menu `Altre opzioni`.
*   `Alt+D`: Mette a fuoco l'elenco dei diari.
*   `Alt+I`: Mette a fuoco la casella di modifica delle informazioni.
*   `Alt+C`: Chiude la finestra del componente aggiuntivo.

### Scorciatoie utili all'interno della finestra di modifica di un capitolo

*   `Alt+N`: Mette a fuoco il campo di modifica.
*   `Alt+P`: Copia tutto il contenuto del capitolo negli appunti.
*   `Alt+G`: Salva il capitolo.
*   `Alt+C`: Chiude la finestra di dialogo del capitolo.

## Configurazione del componente aggiuntivo

Nelle opzioni NVDA, sotto `Note Diary`, puoi abilitare o disabilitare i suoni del componente aggiuntivo. Quando attivati, i suoni verranno riprodotti in eventi come il cambio di diario o capitolo.

## Download

Puoi scaricare l'ultima versione del componente aggiuntivo dal seguente link:
[Scarica Note Diary per NVDA](https://github.com/JohanAnim/Note-diary/releases/latest/download/Note.diary.for.NVDA.nvda-addon)

## Collaboratori

Crediti ai seguenti utenti per aver collaborato con parte del codice sorgente e con alcune funzionalità:

*   [Héctor J. Benítez Corredera](https://github.com/hxebolax/): Ha implementato la parte iniziale di questo componente aggiuntivo.
*   [metalalchemist](https://github.com/metalalchemist/): Implementazione di alcune delle funzionalità del componente aggiuntivo.

---

© 2023-2025 Johan G

## Cronologia delle modifiche

Puoi vedere tutte le modifiche e le versioni del componente aggiuntivo nella [Cronologia delle modifiche](CHANGELOG.md).