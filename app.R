# Librerías necesarias
library(shiny)
library(ggplot2)
library(plotly)
library(dplyr)
library(stringi)

# Interfaz de usuario
ui <- fluidPage(
  theme = shinythemes::shinytheme("darkly"),
  tags$style(HTML("
      body { background-color: #7B1E24; }
      h1, h2, h3, .title { color: white; }
  ")),
  
  titlePanel("Bibliofisi: Estadísticas Bibliométricas de Tesis"),
  
  sidebarLayout(
    sidebarPanel(
      fileInput("file", "Sube tu archivo .bib", accept = ".bib"),
      width = 3
    ),
    
    mainPanel(
      tabsetPanel(
        tabPanel("Resumen General", tableOutput("summary_table")),
        tabPanel("Tesis por Año", plotlyOutput("year_plot")),
        tabPanel("Autores Destacados", plotlyOutput("top_authors_plot")),
        tabPanel("Asesores Destacados", plotlyOutput("top_advisors_plot")),
        tabPanel("Temas Recurrentes", plotlyOutput("top_subjects_plot"))
      )
    )
  )
)

# Servidor
server <- function(input, output, session) {
  
  # Leer y procesar el archivo .bib
  datos <- reactive({
    req(input$file)
    
    # Leer archivo .bib como texto, asegurando la codificación UTF-8
    bib_text <- readLines(input$file$datapath, warn = FALSE, encoding = "UTF-8")
    
    # Si hay caracteres no válidos, intenta convertirlos
    bib_text <- stri_encode(bib_text, from = "latin1", to = "UTF-8")
    
    # Extraer las entradas de tesis usando una expresión regular
    pattern <- "@thesis\\{([^,]+),\\s*(.*)\\}"
    entries <- regmatches(bib_text, gregexpr(pattern, bib_text))
    entries <- unlist(entries)
    
    # Crear el DataFrame
    data <- data.frame(
      Autor = sapply(entries, function(x) stri_extract_first_regex(x, "author = \"([^\"]+)\"")),
      Asesor = sapply(entries, function(x) stri_extract_first_regex(x, "advisor = \"([^\"]+)\"")),
      Año = as.numeric(sapply(entries, function(x) stri_extract_first_regex(x, "year = \"([^\"]+)\""))),
      Institución = sapply(entries, function(x) stri_extract_first_regex(x, "institution = \"([^\"]+)\"")),
      Asunto = sapply(entries, function(x) stri_extract_first_regex(x, "subject = \"([^\"]+)\"")),
      Grado = sapply(entries, function(x) stri_extract_first_regex(x, "degree_name = \"([^\"]+)\""))
    )
    
    # Eliminar posibles filas con valores no válidos
    data <- na.omit(data)
    
    return(data)
  })
  
  # Estadísticas generales
  output$summary_table <- renderTable({
    data <- datos()
    
    data.frame(
      `Número de Tesis` = nrow(data),
      `Número de Autores` = length(unique(data$Autor)),
      `Número de Asesores` = length(unique(data$Asesor)),
      `Número de Temas` = length(unique(data$Asunto))
    )
  })
  
  # Gráfico de Tesis por Año
  output$year_plot <- renderPlotly({
    data <- datos()
    
    ggplot(data, aes(x = Año)) +
      geom_bar(fill = "skyblue") +
      labs(title = "Número de Tesis por Año", x = "Año", y = "Número de Tesis") +
      theme_minimal() -> p
    
    ggplotly(p)
  })
  
  # Gráfico de Autores Destacados
  output$top_authors_plot <- renderPlotly({
    data <- datos()
    
    top_authors <- data %>%
      count(Autor, sort = TRUE) %>%
      top_n(10)
    
    ggplot(top_authors, aes(x = reorder(Autor, n), y = n)) +
      geom_bar(stat = "identity", fill = "orange") +
      labs(title = "Autores con más Tesis", x = "Autor", y = "Número de Tesis") +
      coord_flip() +
      theme_minimal() -> p
    
    ggplotly(p)
  })
  
  # Gráfico de Asesores Destacados
  output$top_advisors_plot <- renderPlotly({
    data <- datos()
    
    top_advisors <- data %>%
      count(Asesor, sort = TRUE) %>%
      top_n(10)
    
    ggplot(top_advisors, aes(x = reorder(Asesor, n), y = n)) +
      geom_bar(stat = "identity", fill = "purple") +
      labs(title = "Asesores con más Tesis", x = "Asesor", y = "Número de Tesis") +
      coord_flip() +
      theme_minimal() -> p
    
    ggplotly(p)
  })
  
  # Gráfico de Temas Recurrentes
  output$top_subjects_plot <- renderPlotly({
    data <- datos()
    
    top_subjects <- data %>%
      count(Asunto, sort = TRUE) %>%
      top_n(10)
    
    ggplot(top_subjects, aes(x = reorder(Asunto, n), y = n)) +
      geom_bar(stat = "identity", fill = "green") +
      labs(title = "Temas más Recurrentes", x = "Tema", y = "Frecuencia") +
      coord_flip() +
      theme_minimal() -> p
    
    ggplotly(p)
  })
}

# Ejecutar la aplicación
shinyApp(ui = ui, server = server)
