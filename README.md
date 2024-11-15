# Web Scraping de Tesis - Cybertesis UNMSM

Este proyecto realiza el scraping de datos de tesis de la plataforma Cybertesis de la Universidad Nacional Mayor de San Marcos (UNMSM), extrayendo metadata relevante de cada tesis y guardándola en un archivo en formato BibTeX.

## Requisitos

Este script requiere los siguientes paquetes:

- `selenium`: Para automatizar la navegación web.
- `beautifulsoup4`: Para parsear el contenido HTML de las páginas.
- `pybtex`: Para generar archivos de bibliografía en formato BibTeX.

Puedes instalar las dependencias usando `pip`:
```bash
pip install selenium beautifulsoup4 pybtex

