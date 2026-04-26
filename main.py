# libreria que lee datos del sistema operativo (intalado en el servidor)
import psutil
from fastapi import FastAPI  # Es el framework, crea mi servidor de datos
from fastapi.middleware.cors import CORSMiddleware  # Componente de seguridad
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Instancio el objeto de tipo fastAPI y lo guardo en la variable app. Basicamente instancio mi servidor
app = FastAPI(title="Mi Dashboard")


# CORS - Configuracion de reglas de seguridad por que mi front va a estar en un dominio y mi backend en otro, y normalmente el navegador lo bloquea.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Declaro donde esta mi directorio de Estaticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# EndPoint - Es las instrucciones a fastAPI de que hacer con cada solicitud del tipo decorador


@app.get("/")  # Decorador de /
def frontend():  # Declara el objeto frontend para cargar la respuesta de mis estaticos (estaticos son los archivos de frontend como css html js)
    # indica que en vez de mandar un json me mande el archivo index.html
    return FileResponse("static/index.html")

# Decorador - Indica que al abrir /api/health se ejecute lo de abajo.


@app.get("/api/health")
def health():
    return {"estado": "ok"}


# Decorador de sistema, nos da un resumen del uso de cpu, memoria y almacenamiento
@app.get("/api/sistema")
def sistema():
    cpu = psutil.cpu_percent(interval=1)  # porcentaje de uso de cpu
    ram = psutil.virtual_memory()  # Cantidad en bits (?) de Memoria
    disco = psutil.disk_usage("/")  # Cantidad en bits (?) de Almacenamiento

    return {
        "cpu": cpu,
        "ram": {
            # cargado de la ram total en gb redondeado a 2 decimales
            "total_gb": round(ram.total / (1024**3), 2),
            # cargado de la ram usada en gb redondeado a 2 decimales
            "usado_gb": round(ram.used / (1024**3), 2),
            "porcentaje": ram.percent  # Porcentaje de usado
        },
        "disco": {
            # cargado del almacenamiento total en gb redondeado a 2 decimales
            "total_gb": round(disco.total / (1024**3), 2),
            # cargado del almacenamiento usada en gb redondeado a 2 decimales
            "usado_gb": round(disco.used / (1024**3), 2),
            "porcentaje": disco.percent  # Porcentaje de usado
        }
    }
