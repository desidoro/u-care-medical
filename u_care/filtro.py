import openpyxl
from PyPDF2 import PdfReader
import fitz
import re
doc = list()
sections = ['Clinical use', 'Dose in normal renal function', 'Pharmacokinetics', 'Metabolism', 'Dose in renal impairment GFR (mL/min)','Dose in patients undergoing renal \nreplacement therapies', 'Important drug interactions', 'Administration', 'Other information']  
section_dict = {}
antibiotics = ['Abacavir','Abatacept', 'Abciximab', 'Abiraterone acetate', 'Acamprosate calcium','Acarbose', 'Acebutolol', 'Aceclofenac', 'Acenocoumarol (nicoumalone)']

#print(sections)


"""
## QUESTA FUNZIONE HA DEI PROBLEMI PERCHE RILEVA ANCHE LE PAROLE UGUALI AL NOME DI UNA SEZIONE
APPARTENENTE A UNA SEZIONE DIFFERENTE COME UNA SEZIONE SEPARATA ##

def load_pdf(f):
    #print("Sono entratata nella fun")
    doc = []  ## LISTA PER CONSERVARE I TESTI DELLE SEZIONI
    pdf = fitz.open(f)
    
    text = ""
    ## CONCATENO PIU PAGINE
    for page in pdf:
        text += page.get_text()  

    
    for section in sections:
    ## GESTIONE PER SEZIONE 'Dose in patients undergoing renal \nreplacement therapies' PERCHE SU DUE RIGHE DIVERSE
            if section == 'Dose in patients undergoing renal \nreplacement therapies':
                text = text.replace(section, f"\nDose in patients undergoing renal replacement therapies\n")
            else:
                text = text.replace(section, f"\n{section}\n")
    
    ## PULIZIA 
    for antibiotic in antibiotics:
        antibiotic_escaped = re.escape(antibiotic)
        pattern = fr"\b\d+\s*{antibiotic_escaped}\b|\b{antibiotic_escaped}\s*\d+\b|\b{antibiotic_escaped}\b"
        if re.search(pattern, text):
           text = re.sub(pattern, "", text)
        elif antibiotic in text:
            text = text.replace(antibiotic, "")
        else:
            print(f"'{antibiotic}' non trovato nel testo.")
    text = re.sub("\sA\s{2}|\s{2}A\s"," ",text)
    
    ## DIVIDI TESTO PER SEZIONI
    pieces = text.split('\n')
    #print(pieces)
    current_section = None
    section_text = ""

    for piece in pieces:
        if piece in sections or piece == "Dose in patients undergoing renal replacement therapies":
            if current_section is not None:
                doc.append((current_section, section_text.strip()))
            current_section = piece
            section_text = ""
        else:
            section_text += piece + " "

    ## GESTIONE ULTIMA SEZIONE
    if current_section is not None:
        doc.append((current_section, section_text.strip()))

    pdf.close()
    return doc

    """
def list_bold_text(pdf_path):
    pdf = fitz.open(pdf_path)
    bold_texts = []

    for page_number in range(len(pdf)):
        page = pdf[page_number]
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" in b:
                for line in b["lines"]:
                    for span in line["spans"]:
                        print(span["font"])
                        print(span["text"])
                        #bold_texts.append()

    pdf.close()
    
def load_pdf(f):
    #print("Sono entratata nella fun")
    doc = []  ## LISTA PER CONSERVARE I TESTI DELLE SEZIONI
    pdf = fitz.open(f) ## APRO FILE PDF
    
    current_section = None
    section_text = "" 
    previous_drug = "" ## FARMACO DELLA PAGINA PRECEDENTE
    continueSection = False ## VARIABILE CHE MI DICE SE IL FARMACO SI ESTENDE SU PIù PAGINE
    
    for page_number,page in enumerate(pdf):
        i = 0 ##TENGO CONTO DEL NUMERO DI RIGHE
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if i == 0 and span["font"] == "AJensonPro-Regular":
                            curr_drug = re.sub(r'\d+(\.\d+)?', '', span["text"]).strip()
                            #print("cd ", curr_drug)
                            ## CONTROLLO SE IL FARMACO DELLA PAGINA PRECEDENTE E LO STESSO
                            if(curr_drug == previous_drug):
                                ## RECUPERO IL TESTO DELLA SEZIONE PRECEDENTE 
                                section_1, text_1 = doc[-1]   
                                print(section_1, text_1)
                                print(page_number)
                                continueSection = True
                            previous_drug = curr_drug
                            #print("pd ", previous_drug)
                        i+=1
                        ## CONTROLLO SE HO UNA NUOVA SEZIONE
                        if span["font"] == "HelveticaLTStd-Bold":
                            if current_section is not None:
                                doc.append((current_section, section_text.strip()))
                                section_text = ""
                            current_section = text
                        ## CONTROLLO SE LA PAGINA è LA CONTINUA DELLA SEZIONE ALLA PAGINA PRECEDENTE E APPENDO IL TESTO DELLA SEZIONE
                        elif continueSection == True:
                            current_section = section_1
                            section_text = text_1 + " "
                            continueSection = False
                        else:
                            # PULIZIA
                            for antibiotic in antibiotics:
                                antibiotic_escaped = re.escape(antibiotic)
                                pattern = fr"\b\d+\s*{antibiotic_escaped}\b|\b{antibiotic_escaped}\s*\d+\b|\b{antibiotic_escaped}\b"
                                if re.search(pattern, text):
                                    text = re.sub(pattern, "", text)
                                elif antibiotic in text:
                                    text = text.replace(antibiotic, "")
                            section_text += text + " "

    # ULTIMA SEZIONE
    if current_section is not None:
        doc.append((current_section, section_text.strip()))

    pdf.close()
    return doc

## SETTO UN DIZIONARIO CHE HA PER CHIAVE IL NOME DEL FARMACO E PER VALORE UN SECONDO DIZIONARIO CON CHIAVE SEZIONE E VALORE TESTO
def set_antibiotics_dict(antis, doc_sec_text):
    count = 0
    i = 0
    count_dict = 0
    antibiotics_dict = {antibiotic: {} for antibiotic in antis}

    for antibiotic in antibiotics_dict:
        #print(antibiotic)
        section_dict = {}
        count_dict += 1
        ## IL CICLO SERVE SOLO PER SCORRERE LA FINESTRA DELLE SEZIONI IN MODO CHE NON RIPARTA DAL PRIMO FARMACO
        while i < len(doc_sec_text):
            section, text = doc_sec_text[i]
            #print(f"Section: {section}\nText: {text}\n\n")
            ## QUANDO ARRIVA A CLINICAL USE VUOL DIRE CHE LE SEZIONI DEL FARMACO CORRENTE SONO TERMINATE
            if section == "Clinical use" and count >= 2:
                antibiotics_dict[antibiotic] = section_dict
                count = 0
                break
            section_dict[section] = text
            i += 1
            #print(section_dict[section])
            count+=1
            ## ULTIMO FARMACO
            if count_dict == len(antibiotics_dict):
                antibiotics_dict[antibiotic] = section_dict  
    return antibiotics_dict

## FUNZIONE PER CONTROLLO CAMBIO DOSE
def assign_bool(p):
    phrases = p.split('.')
    filtered_phrases = [e for e in phrases if e not in [" See 'Other information'", ' Use with caution', '', " See ‘Other information’"]]       
    #print(filtered_phrases)
    second_parts = [phrase.split(maxsplit=1)[1] if len(phrase.split(maxsplit=1)) > 1 else None for phrase in filtered_phrases]
    all_equal = all(part == second_parts[0] for part in second_parts if part is not None)
    return 1 if all_equal == True else 0

if __name__ == '__main__':
    
    pdf_path = "./The_Renal_Drug_Handbook_The_Ultimate 1-20-30 (1).pdf"
    sections_text = load_pdf(pdf_path)
    antibiotics = set_antibiotics_dict(antibiotics, sections_text)
    ##list_bold_text(pdf_path) questa mi serve solo a vedere quale font usare
    ## STAMPO PER OGNI ANTIBIOTICO LE SEZIONI CHE MI INTERESSANO
    for antibiotic in antibiotics:
        #print(antibiotic)
        print(f"Antibiotic: ", antibiotic)
        print(f"Clinical use: ", antibiotics[antibiotic]['Clinical use'] )
        print(f"Dose in normal renal function: ", antibiotics[antibiotic]['Dose in normal renal function'])
        print(f"Dose in renal impairment GFR (mL/min): ", antibiotics[antibiotic]['Dose in renal impairment GFR (mL/min)'])
        print(f"Administration: ", antibiotics[antibiotic]['Administration'])
    
    #print(antibiotics_dict['Acenocoumarol (nicoumalone)']['Other information'])
    #print(f"Other Information: ",antibiotics_dict[antibiotic]['Other information'])


    ## SALVATAGGIO SU EXCEL
    
    my_exc = openpyxl.Workbook()
    sheet = my_exc.active
    sheet.title = 'The Renal Drug Handbook'
    ## PRIMA RIGA
    sheet.append(["Renal Drug", "Clinical use", "Dose in normal renal function", "Dose in renal impairment GFR (mL/min)", "Administration", "Change"])
    for antibiotic in antibiotics:
        ## RIGHE SUCCESSIVE
        row = [antibiotic]  # Inizia la riga con il nome dell'antibiotico
        row.append(antibiotics[antibiotic]['Clinical use'])
        row.append(antibiotics[antibiotic]['Dose in normal renal function'])
        row.append(antibiotics[antibiotic]['Dose in renal impairment GFR (mL/min)'])
        row.append(antibiotics[antibiotic]['Administration'])
        val = assign_bool(antibiotics[antibiotic]['Dose in renal impairment GFR (mL/min)'])
        row.append(val)
        sheet.append(row)

    my_exc.save("The_Renal_Antibiotics.xlsx")
