# MANUAL DE USO - FUNDAMENTAL
## SIMULACIÓN Y MITIGACIÓN DE SQL INJECTION
### 1. Requisitos indispensable
- Python instalado
- PyCharm o Visual Studio Code
- Flask instalado en el entorno virtual
- Los archivos de la práctica y la base de datos SQLite

### 2. Ejecutar la aplicación vulnerable
1. Abrir el proyecto en PyCharm
2. Ejecutar el archivo `app_vulnerable.py`
3. Abrir el navegador y entrar al link http://127.0.0.1:5000
4. Probar el formulario de autenticación y la búsqueda de usuarios

### 3. Ejecutar la aplicación segura
1. Abrir una segunda configuración de ejecución en PyCharm
2. Ejecutar `app_segura.py`
3. Abrir el link http://127.0.0.1:5001
4. Comprobar como se comporta el y también la búsqueda

### 4. Ejecutar las pruebas SQL Injection
1. Mantener las dos aplicaciones en funcionamiento
2. Ejecutar el archivo `ataque_sql_i.py`
3. Revisar muy bien los resultados de autenticación y búsqueda
4. Comparar las respuestas de la aplicación vulnerable y la segura

### 5. Escanear los puertos
1. Ejecutar `escaneo_red.py`.
2. Revisar los puertos abiertos y cerrados
3. Identificar los puertos 5000 y 5001 cuando las aplicaciones estén abiertas

### 6. Revisar la base de datos
1. Ejecutar `endurecimiento_db.py`
2. Comprobar que la copia de seguridad se haya creado
3. Verificar que la comprobación de integridad esta debe de mostrar `ok`

### 7. Resultados esperados
- La aplicación vulnerable tiene que permitir alterar consultas SQL
- La aplicación segura tiene que rechazar los intentos de inyección SQL
- El escáner debe de identificar los puertos abiertos
- SQLite debe crear una copia de seguridad y verificar la integridad

### 8. Recomendaciones de seguridad
- Realizar las pruebas únicamente en un entorno autorizado
- No publicar aplicaciones vulnerable en Internet
- Debemos utilizar consultas parametrizadas para evitar la inyección SQL
- Proteger las contraseñas con funciones de hash
- Crear copias de seguridad y limitar el acceso a los archivos