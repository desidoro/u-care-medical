# u-care-medical

## Struttura del codice 

Sono implementate 4 funzioni:
- load_pdf(f) : riceve come parametro il percorso del file pdf, lo carica, trasforma in formato testuale e suddivide per sezioni. Viene restituita una lista con sezioni e testo associato.
- set_antibiotics_dict(antis, doc_sec_text): riceve come parametro una lista con tutti i farmaci presenti nel pdf e una lista che contiene il testo e la sezione associata. Tale funzione ha lo scopo di creare un nuovo dizionario che abbia come chiave il nome del farmaco e come valore un secondo dizionario che ha come chiave il nome della sezione e come valore il testo associato. 
- assign_bool(p): riceve come parametro un testo e fa una prima operazione di split del testo in frasi e poi una di pulizia per rimuovere frasi inutili. Dopo di che controlla se le frasi sono uguali per verificare successivamente se le misure cambiano per dosaggio e restituisce un booleano.
- list_bold_text(pdf_path): prende il percorso del file come parametro e stampa per ogni riga il font del testo (utile solo per capire come dividere in sezioni).

## Informazioni aggiuntive

Molti controlli sono stati aggiunti per evitare che:

- Nomi di sezioni all'interno di sezioni differenti fossero erroneamente confuse come sezioni stesse. 
- Sezioni che continuano alla pagina successiva fossero concatenate in modo da non perdere informazione.
- Nomi di sezioni su più righe fossero considerati come un unica. 
