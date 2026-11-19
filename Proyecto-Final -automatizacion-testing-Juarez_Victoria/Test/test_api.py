import json
import urllib.request
import urllib.error

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_api_get_posts_exitoso():
    """Caso 1 (GET - Éxito): Obtener listado de publicaciones y validar código 200 y estructura JSON"""
    url = f"{BASE_URL}/posts"
    
    with urllib.request.urlopen(url) as response:
        # Validamos código de estado HTTP
        assert response.status == 200
        
        # Leemos y decodificamos la respuesta JSON
        datos = json.loads(response.read().decode("utf-8"))
        
        assert isinstance(datos, list)
        assert len(datos) > 0
        assert "userId" in datos[0]
        assert "title" in datos[0]

def test_api_post_crear_recurso():
    """Caso 2 (POST - Éxito): Crear un nuevo recurso y validar código 201 y datos devueltos"""
    url = f"{BASE_URL}/posts"
    nuevo_post = {
        "title": "Prueba automatizada QA",
        "body": "Contenido de prueba creado con Pytest y urllib",
        "userId": 1
    }
    
    data_bytes = json.dumps(nuevo_post).encode("utf-8")
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json; charset=UTF-8"}, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            # Validamos código 201 
            assert response.status == 201
            
            datos = json.loads(response.read().decode("utf-8"))
            assert datos["title"] == nuevo_post["title"]
            assert datos["body"] == nuevo_post["body"]
            assert "id" in datos
    except urllib.error.HTTPError as e:
        # Por si el servidor de pruebas devuelve 201 de forma estricta que urllib a veces interpreta
        assert e.code == 201

def test_api_delete_eliminar_recurso():
    """Caso 3 (DELETE - Éxito): Eliminar un recurso existente y validar código 200"""
    url = f"{BASE_URL}/posts/1"
    req = urllib.request.Request(url, method="DELETE")
    
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        datos = json.loads(response.read().decode("utf-8"))
        assert datos == {}

def test_api_get_recurso_inexistente_error():
    """Caso 4 (GET - Escenario Negativo): Buscar un ID inexistente y validar código 404"""
    url = f"{BASE_URL}/posts/999999"
    
    try:
        urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        # Validamos que el servidor devuelva el error 404 esperado
        assert e.code == 404