# Web Scraping de Tesis - Cybertesis UNMSM 

Este proyecto realiza el scraping de datos de tesis de la plataforma Cybertesis de la Universidad Nacional Mayor de San Marcos (UNMSM), extrayendo metadata relevante de cada tesis de la Facultad de Ingeniería de Sistemas e Informática y guardándola en un archivo en formato BibTeX.

## Requisitos

Este script requiere los siguientes paquetes:

- `selenium`: Para automatizar la navegación web.
- `beautifulsoup4`: Para parsear el contenido HTML de las páginas.
- `pybtex`: Para generar archivos de bibliografía en formato BibTeX.

Puedes instalar las dependencias usando `pip`:
```bash
pip install selenium beautifulsoup4 pybtex
```

## Uso del Script

Para ejecutar el script:

1. Clona este repositorio o descarga el archivo `scraper.py`.
2. Asegúrate de que las dependencias están instaladas.
3. Ejecuta el script:
```bash
python bibliofisi.py
```

## Funcionalidades del Script

- Navegación por las páginas de Cybertesis: El script accede automáticamente a las páginas de la colección de tesis y extrae enlaces a tesis individuales.
- Extracción de Metadata: De cada tesis, se extraen los siguientes datos:
  - Autor
  - Asesor
  - Año de emisión
  - Publicador
  - Materias de estudio
  - Nombre del título (grado académico)
- Generación de archivos BibTeX: Toda la metadata se guarda en un archivo llamado `bibliofisi.bib`.

## Parámetros Personalizables

- `max_pages`: Define el número máximo de páginas a procesar. Por defecto, está configurado a 10.
- `filename`: Nombre del archivo de salida para los datos en formato BibTeX. El valor por defecto es `bibliofisi.bib` (si se desea tener más .bib al cambiar el enlace de obtención de tesis es necesario el cambio del archivo de salida).
- `driver.get("https://cybertesis.unmsm.edu.pe/collection/...)`: Si se desea obtener tesis de otro campo solo se cambia el enlace.

## Estructura del Código

1. Funciones principales
  -  `fetch_thesis_metadata() `: Extrae y organiza la metadata de una tesis.
  -  `save_bibtex_file(metadata, filename) `: Guarda la metadata en un archivo BibTeX.
  -  `navigate_to_main_page() `: Navega a la página principal de la colección de tesis.
2. Función principal (`main`)
  - Orquesta el proceso de scraping, incluyendo la navegación entre páginas y la extracción de datos.
3. Manejo de errores
  - El script maneja excepciones para errores comunes como la falta de conexión, fallos en el acceso a enlaces, o tiempo de espera al cargar elementos de la página.

# Ejemplo de entrada BibTex

A continuación, un ejemplo de cómo se vería una entrada BibTeX generada:

```bibtex
@thesis{Juan2021,
  author = {Juan Pérez},
  advisor = {Andrés López},
  year = {2021},
  publisher = {Universidad Nacional Mayor de San Marcos},
  subject = {Redes de Computadoras, Ciencia de Datos},
  degree_name = {Ingeniería de Sistemas}
}
```









