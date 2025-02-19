# 🎬 **Proyecto Individual Nº1: Machine Learning Operations (MLOps)**

![Logo](https://d31uz8lwfmyn8g.cloudfront.net/Assets/logo-henry-white-lg.png)

---

## 📌 **Descripción del Proyecto**

Bienvenidos al primer proyecto individual de la etapa de Labs de **Henry**, donde asumimos el rol de un ***MLOps Engineer***. El objetivo es desarrollar un **sistema de recomendación de películas** utilizando técnicas de Machine Learning y FastAPI para exponer los datos mediante una API RESTful.

Este proyecto abarca desde la preparación de datos (ETL) hasta el despliegue de un modelo de recomendación, cumpliendo con los principios de MLOps para garantizar que el sistema sea escalable, mantenible y fácil de integrar.

---

## 🛠️ **Requisitos del Proyecto**

### **Transformaciones de Datos**
Para este MVP, se realizaron las siguientes transformaciones en el dataset:

- **Desanidar campos anidados**: Como `belongs_to_collection`, `production_companies` y otros.
- **Rellenar valores nulos**:
  - Los campos `revenue` y `budget` fueron rellenados con `0`.
  - Las filas con valores nulos en `release_date` fueron eliminadas.
- **Formato de fechas**: Se estandarizó el campo `release_date` al formato `AAAA-mm-dd` y se creó la columna `release_year`.
- **Crear columna `return`**: Calculada como `revenue / budget`, rellenando con `0` cuando no hay datos disponibles.
- **Eliminar columnas innecesarias**: `video`, `imdb_id`, `adult`, `original_title`, `poster_path` y `homepage`.

---

### **Endpoints de la API**
La API expone los siguientes endpoints para interactuar con los datos procesados:

| Endpoint                         | Descripción                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `/cantidad_filmaciones_mes/{mes}` | Devuelve la cantidad de películas estrenadas en un mes específico.           |
| `/cantidad_filmaciones_dia/{dia}` | Devuelve la cantidad de películas estrenadas en un día específico.           |
| `/score_titulo/{titulo}`         | Devuelve el título, año de estreno y score/popularidad de una película.      |
| `/votos_titulo/{titulo}`         | Devuelve el título, cantidad de votos y promedio de votos de una película.   |
| `/get_actor/{nombre_actor}`      | Devuelve el éxito medido por retorno, cantidad de películas y promedio.      |
| `/get_director/{nombre_director}`| Devuelve detalles sobre las películas dirigidas por un director específico.  |
| `/recomendacion/{titulo}`        | Devuelve una lista de 5 películas similares basadas en el título ingresado.  |

---

## 🚀 **Cómo Ejecutar el Proyecto**

### **Requisitos Previos**
- Python 3.9 o superior.
- Dependencias instaladas desde `requirements.txt`.

### **Pasos para Ejecutar**
1. Clona este repositorio:
   ```bash
   git clone https://github.com/LemmaUX/SHData.git
   cd proyecto-mlops

   # 📊 Análisis Exploratorio de Datos (EDA)

Se realizó un análisis exploratorio para comprender mejor los datos y detectar patrones interesantes. Algunos hallazgos incluyen:

- Distribución de géneros más populares.
- Relación entre presupuesto (`budget`) y recaudación (`revenue`).
- Palabras más frecuentes en los títulos de las películas (nube de palabras).

# 🤖 Sistema de Recomendación

El sistema de recomendación utiliza similitud de coseno (`cosine_similarity`) para encontrar películas similares basadas en características combinadas como géneros, actores, directores y descripciones. Los pasos clave son:

1. Crear la columna `combined_features` combinando características relevantes.
2. Aplicar `TfidfVectorizer` para vectorizar las características.
3. Calcular la similitud de coseno entre las películas.
4. Devolver las 5 películas más similares.

# 🌐 Despliegue

La API fue desplegada utilizando Render para garantizar su disponibilidad en la web. Puedes acceder al servicio en vivo en el siguiente enlace:  
[https://dashboard.render.com/web/srv-cuqlk7t6l47c73cf4ndg](#)

# 🎥 Video Explicativo

Aquí está el video donde explico el funcionamiento del proyecto, incluyendo una demostración de las consultas requeridas en la API y una breve explicación del modelo utilizado para el sistema de recomendación. También muestro el proceso de ETL, EDA y el desarrollo de la API.

👉 [https://www.loom.com/share/c355c0d257aa4491805227d6cb865359](#)

# 📋 Criterios de Evaluación

El proyecto será evaluado según los siguientes criterios:

- **Código**: Prolijidad, uso de funciones y clases, comentarios claros.
- **Repositorio**: Estructura organizada, nombres de archivos adecuados, README completo.
- **Cumplimiento**: Implementación de todas las funcionalidades requeridas.

# 📂 Estructura del Repositorio
- proyecto-mlops/
    - data/  # Datos procesados y originales
        - movies_processed.csv # Dataset procesado
        - credits.csv # Datos adicionales
    - src/  # Código fuente
        - api.py # API FastAPI
        - utils.py # Funciones auxiliares
        - eda.ipynb # Análisis exploratorio (EDA)
    - notebooks/  # Notebooks para análisis y pruebas
        - recommendation.ipynb # Modelo de recomendación
    - requirements.txt # Dependencias del proyecto
    - README.md # Documentación del proyecto


# 🙏 Agradecimientos

Quiero agradecer a los instructores y mentores de Henry por su apoyo durante el desarrollo de este proyecto. También agradezco a la comunidad de GitHub y Stack Overflow por sus valiosos recursos y ejemplos.

# 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

# 📧 Contacto

Si tienes preguntas o sugerencias, no dudes en contactarme:

- **Nombre**: Terceros Jorge 
- **Email**: optimoter@gmail.com  
- **LinkedIn**: [Perfil de LinkedIn](#)  
- **GitHub**: 
# 🙏 Agradecimientos

Quiero agradecer a los instructores y mentores de Henry por su apoyo durante el desarrollo de este proyecto. También agradezco a la comunidad de GitHub y Stack Overflow por sus valiosos recursos y ejemplos.

# 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

# 📧 Contacto

Si tienes preguntas o sugerencias, no dudes en contactarme:

- **Nombre**: Jorge Terceros 
- **Email**: optimoter.com  
- **LinkedIn**: [https://www.linkedin.com/in/jorge-terceros-273155168/](#)  
- **GitHub**: [https://github.com/LemmaUX/SHData](#)  

Espero que este README cumpla con tus expectativas. Si necesitas ajustes o personalizaciones adicionales, no dudes en pedírmelo. 😊(#)  

