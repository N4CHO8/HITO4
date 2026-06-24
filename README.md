# Hito4 - Asistente RAG de Soporte Tecnico

Proyecto para la evaluacion sumativa de IA Embebida en Sistemas Computacionales.
Implementa un asistente RAG que responde preguntas usando documentacion tecnica
interna sobre Docker, Linux, Git y procedimientos de soporte.

## Integrantes

Equipo de 3 estudiantes de ultimo ano de Ingenieria en Computacion e Informatica.

## Caso seleccionado

Caso 2: Asistente de Soporte Tecnico.

El sistema responde preguntas a partir de documentos locales y muestra las
fuentes utilizadas. Si la respuesta no aparece en el corpus, debe indicar que no
existe informacion suficiente.

## Arquitectura

Usuario -> pregunta -> embedding -> FAISS -> recuperacion de contexto ->
Ollama LLM -> respuesta con fuentes.

Componentes implementados:

- Ingesta documental desde archivos Markdown, TXT y PDF.
- Fragmentacion de documentos en chunks.
- Generacion de embeddings para cada fragmento.
- Almacenamiento vectorial persistente con FAISS.
- Recuperacion semantica de fragmentos relevantes.
- Generacion de respuestas con un LLM local usando el contexto recuperado.
- Visualizacion de fuentes y fragmentos usados.
- Manejo de preguntas fuera del corpus documental.

## Tecnologias

- Python 3.11 o 3.12
- Streamlit
- FAISS
- Ollama
- Modelo de embeddings: `nomic-embed-text`
- Modelo LLM: `llama3.2:3b` (menor a 7B)
- pypdf para lectura de PDF

## Requisitos previos

Instalar Ollama desde <https://ollama.com/> y descargar los modelos:

```bash
ollama pull nomic-embed-text
ollama pull llama3.2:3b
```

Instalar dependencias de Python:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

En Windows se recomienda Python 3.11 o 3.12. Python 3.13 puede causar
problemas con dependencias de bases vectoriales.

Si PowerShell bloquea la activacion del entorno virtual, ejecutar antes:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Luego activar con:

```powershell
.\.venv\Scripts\Activate.ps1
```

En Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecucion

1. Levantar Ollama:

```bash
ollama serve
```

Si Ollama ya esta ejecutandose, puede aparecer un mensaje indicando que el
puerto `11434` ya esta en uso. En ese caso no es necesario iniciar otro
servidor.

2. Indexar los documentos:

```bash
python ingest.py --docs docs --reset
```

3. Ejecutar la aplicacion:

```bash
streamlit run app.py
```

4. Abrir la URL mostrada por Streamlit, normalmente:

```text
http://localhost:8501
```

## Consultas de demostracion

Consulta simple:

```text
Como crear una imagen Docker?
```

Consulta compleja:

```text
Como actualizo un repositorio Git y que debo verificar si el servicio falla despues del despliegue?
```

Consulta sin respuesta documental:

```text
Cual es el protocolo para administrar medicamentos intravenosos?
```

## Ejecucion por consola

Tambien se puede consultar sin interfaz grafica:

```bash
python query.py "Como visualizar procesos en Linux?"
```

## Cumplimiento de requisitos del enunciado

| Requisito | Implementacion |
|---|---|
| Carga documental | `src/document_loader.py` carga Markdown, TXT y PDF. |
| Chunking | `src/chunker.py` divide documentos en chunks de 900 caracteres con overlap de 150. |
| Embeddings | `src/ollama_client.py` usa `nomic-embed-text` mediante Ollama. |
| Base vectorial | `src/vector_store.py` usa FAISS con persistencia local en `data/faiss`. |
| Recuperacion semantica | `src/rag.py` recupera los fragmentos mas cercanos a la pregunta. |
| Integracion con LLM | `src/rag.py` arma el prompt y consulta `llama3.2:3b`. |
| Fuentes recuperadas | La consola y Streamlit muestran documentos fuente y fragmentos recuperados. |
| Preguntas sin respuesta | Se usa `MAX_CONTEXT_DISTANCE` para detectar contexto insuficiente. |

## Estructura del proyecto

```text
.
|-- app.py                  # Interfaz Streamlit
|-- ingest.py               # Indexacion de documentos
|-- query.py                # Consulta por consola
|-- docs/                   # Corpus documental de ejemplo
|-- src/                    # Modulos principales del RAG
|-- tests/                  # Tests del chunking
|-- requirements.txt        # Dependencias
`-- .env.example            # Configuracion opcional
```

## Chunking usado

El proyecto usa fragmentos de 900 caracteres con 150 caracteres de solapamiento.
Ese tamano mantiene suficiente contexto tecnico por fragmento y el solapamiento
reduce la probabilidad de cortar pasos importantes entre dos chunks.

## Variables de entorno opcionales

Copiar `.env.example` a `.env` si se desea cambiar modelos o rutas.

```text
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_EMBED_MODEL=nomic-embed-text
OLLAMA_LLM_MODEL=llama3.2:3b
VECTOR_PATH=data/faiss
MAX_CONTEXT_DISTANCE=0.35
```

`MAX_CONTEXT_DISTANCE` controla cuando una recuperacion se considera demasiado
lejana semanticamente. Si la mejor coincidencia supera ese valor, el asistente
responde que no encontro informacion suficiente.

## Pruebas

```bash
python -m pytest tests -q
```
