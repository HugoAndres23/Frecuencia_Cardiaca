# ❤️ Heart Rate Modeling & Simulation API

## 📌 Descripción del Proyecto

Este sistema permite:

* Cargar datos experimentales de frecuencia cardíaca en formato CSV.
* Modelar los datos utilizando distintos algoritmos de regresión.
* Comparar valores reales vs valores predichos.
* Visualizar resultados mediante gráficos.
* Generar reportes automáticos en PDF.

El backend está desarrollado como una API REST usando FastAPI.

---

## ⚙️ Tecnologías Utilizadas

### Backend

* Python 3.10+
* FastAPI
* Uvicorn
* Pandas
* NumPy
* Scikit-learn
* Matplotlib
* ReportLab

---

## ✅ Requisitos Previos

Antes de ejecutar el proyecto asegúrese de tener instalado:

* Python 3.10 o superior
* pip
* Git (opcional)

Verificar instalación:

```bash
python --version
```

---

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend
```

---

### 2️⃣ Crear entorno virtual

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

Si todo funciona correctamente verá algo similar a:

```
Uvicorn running on http://127.0.0.1:8000
```


## 📥 Formato del Archivo CSV

El sistema espera un archivo CSV con la siguiente estructura:

```
tiempo,actividad,fc
0,Reposo,72
10,Reposo,73
20,Caminata,85
30,Trote,110
```

### Columnas requeridas

| Columna   | Descripción               |
| --------- | ------------------------- |
| tiempo    | Tiempo en segundos        |
| actividad | Nivel de actividad física |
| fc        | Frecuencia cardíaca (BPM) |

---

## 👤 Autor

Proyecto académico desarrollado por:

**Hugo Andrés Casas**
**Juan Esteban Velez**
**Carolina Londoño**
**Santiago Solis**

---