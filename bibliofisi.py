from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from pybtex.database import BibliographyData, Entry
import time

def fetch_thesis_metadata():
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'MuiTableCell-root')))

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('tr')
    
    # Datos de interés
    author = advisor = year = title = type_field = institution = degree_name = None
    subject = []
    
    # Extraer la metadata
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            field = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            if field == "dc.contributor.author":
                author = value
            elif field == "dc.contributor.advisor":
                advisor = value
            elif field == "dc.date.issued":
                year = value
            elif field == "dc.title":
                title = value
            elif field == "dc.type":
                type_field = value
            elif field == "dc.subject":
                subject.append(value)
            elif field == "dc.publisher":
                institution = value
            elif field == "thesis.degree.name":
                degree_name = value
    
    # Crear la entrada BibTeX
    thesis_entry = {
        'ENTRYTYPE': 'thesis',
        'ID': f"{author.split()[0]}{year}" if author and year else 'NoID',
        'author': author or 'No Author',
        'advisor': advisor or 'No Advisor',
        'year': year or 'No Year',
        'title': title or 'No Title',
        'type': type_field or 'No Type',
        'institution': institution or 'No Institution',
        'subject': ', '.join(subject) or 'No Subject',
        'degree_name': degree_name or 'No Degree Name'
    }
    return thesis_entry

def save_bibtex_file(metadata, filename="tesis.bib"):
    # Crear el objeto BibliographyData y añadir la entrada
    bib_data = BibliographyData()
    entry = Entry(
        metadata['ENTRYTYPE'],
        fields={
            'author': metadata['author'],
            'advisor': metadata['advisor'],
            'year': metadata['year'],
            'title': metadata['title'],         
            'type': metadata['type'],           
            'institution': metadata['institution'],  
            'subject': metadata['subject'],
            'degree_name': metadata['degree_name']
        }
    )
    bib_data.add_entry(metadata['ID'], entry)
    
    # Guardar la metadata en el archivo .bib
    with open(filename, 'a') as bib_file:
        bib_data.to_file(bib_file)

def navigate_to_main_page():
    """Función para volver a la página principal."""
    driver.get("https://cybertesis.unmsm.edu.pe/collection/8c7c6dc5-2beb-4b23-a722-50012376769e")
    print("Volvió a la página principal.")
    time.sleep(3)

def main():
    global driver
    driver = webdriver.Chrome()

    navigate_to_main_page()
    
    try:
        fecha_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/browse/dateissued/']"))
        )
        fecha_button.click()
        print("Hizo clic en el botón de 'Fecha'.")
        time.sleep(3)
    except Exception as e:
        print("Error al hacer clic en el botón de 'Fecha':", e)
        driver.quit()
        return

    page_number = 1
    max_pages = 10  # O el número de páginas que consideres que pueden existir
    while page_number <= max_pages:
        print(f"Procesando página {page_number}...")
        
        # Extraer enlaces de tesis en la página actual
        try:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            thesis_links = [a['href'] for a in soup.find_all('a', class_='MuiTypography-root MuiTypography-h5 MuiLink-root MuiLink-underlineNone css-mr5w6s', href=True)]
            
            if not thesis_links:
                print("No se encontraron enlaces de tesis en esta página.")
                break 
            
            print(f"Se encontraron {len(thesis_links)} enlaces de tesis en esta página.")
            
            # Acceder a la metadata de cada tesis
            for i, link in enumerate(thesis_links):
                try:
                    full_link = "https://cybertesis.unmsm.edu.pe" + link + "/full"
                    driver.get(full_link)
                    print(f"Accedió a la tesis {i+1}: {full_link}")
                    
                    # Extraer y guardar metadata
                    metadata = fetch_thesis_metadata()
                    save_bibtex_file(metadata, filename="bibliofisi.bib")
                    print(f"Metadata de {link} guardada.")
                
                except Exception as e:
                    print(f"No se pudo extraer metadata de la tesis {i+1} ({link}):", e)
                    continue 

        except Exception as e:
            print("Error durante la navegación o extracción de tesis:", e)
            break  
        
        try:
            if page_number < max_pages:
                navigate_to_main_page()
                
                fecha_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='/browse/dateissued/']"))
                )
                fecha_button.click()
                print(f"Hizo clic en el botón 'Fecha' nuevamente para la página {page_number + 1}.")
                time.sleep(3)

                for _ in range(page_number):
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Go to next page']"))
                    )
                    next_button.click()
                    print(f"Hizo clic en el botón 'Next Page'.")
                    time.sleep(3)
                
                page_number += 1  
            else:
                print("Ya se han procesado todas las páginas.")
                break
        
        except Exception as e:
            print("Error durante la navegación a la siguiente página:", e)
            break 
    
    driver.quit()

main()