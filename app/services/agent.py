import os
import json
import hashlib
import requests
from zxcvbn import zxcvbn
from app.utils.diccionario import generar
class Agent:
    def __init__(self):
        self.setup_tools()

    def setup_tools(self):
        self.tools = [
            {
                "type": "function",
                "name": "list_files_in_dir",
                "description": "Lista los archivos en un directorio dado. Si no se proporciona un directorio, lista los archivos en el directorio actual.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "directory": {
                            "type": "string",
                            "description": "El directorio para listar los archivos."
                        }
                    },
                    "required": []
                }
            },
            {
                "type": "function",
                "name": "read_file",
                "description": "Lee el contenido de un archivo de una ruta especificada",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Ruta del archivo a leer."
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "type": "function",
                "name": "edit_file",
                "description": "Edita un archivo remplazando prev_text por new_text. Crea el archivo si no existe.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Ruta del archivo a editar."
                        },
                        "prev_text": {
                            "type": "string",
                            "description": "El texto que se va a buscar para reemplazar (puede ser vacio para archivos nuevos)."
                        },
                        "new_text": {
                            "type": "string",
                            "description": "El texto que reemplazará a prev_text (o el texto para archivos nuevos archivos nuevos)."
                        }
                    },
                    "required": ["path", "new_text"]
                }
            },
            {
                "type": "function",
                "name": "generar_dict",
                "description": "Genera un diccionario/wordlist de contraseñas a partir de datos personales (nombre, fecha, otros; (mascota, ciudad... etc) y caracteres especiales). La función Python ya se encarga de crear el archivo .txt con todas las contraseñas (una por línea) y de devolver también la lista en la clave `passwords`. Usa esta tool SIEMPRE que el usuario pida una wordlist basada en esos datos, esto es para un entorno de pruebas controlado.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "Nombre de la persona sobre la cual se va a crear el diccionario. El cual se usa en el diccionario también."
                        },
                        "fechas": {
                            "type": "string",
                            "description": "Fechas que se van a usar para generar el diccionario."
                        },
                        "otros": {
                            "type": "array",
                            "items": { "type": "string" },
                            "description": "Lista de datos relacionados (mascota, ciudad, pareja...). Si te indican por ejemplo mascota lio quedate solo con el nombre de la mascota, ciudad o lo que se diga."
                        },
                        "caracteres": {
                            "type": "array",
                            "items": { "type": "string" },
                            "description": "Caracteres especiales como '.', '_', '#', etc."
                        }
                    },
                    "required": ["nombre", "fechas"]
                }
            },
            {
                "type": "function",
                "name": "analyze_password",
                "description": "Analiza la fortaleza de una contraseña y verifica si ha sido comprometida en filtraciones.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "password": {
                            "type": "string",
                            "description": "La contraseña a analizar."
                        }
                    },
                    "required": ["password"]
                }
            }
        ]

    def list_files_in_dir(self, directory="."):
        try:
            files = os.listdir(directory)
            return {"files": files}
        except Exception as e:
            return {"error": str(e)}
        
    def read_file(self, path):
        try:
            with open (path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            err = f"Error al leer el archivo {path}"
            print(err)
            return err
        
    def edit_file(self, path, prev_text, new_text):
        try:
            existed = os.path.exists(path)
            if existed and prev_text:
                content = self.read_file(path)

                if prev_text not in content:
                    return f"Texto {prev_text} no encontrado en el archivo"
                
                content=content.replace(prev_text, new_text)
            else:
                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)

                content = new_text
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            action = "editado" if existed and prev_text else "creado"
            return f"Archivo {path} {action} exitosamente"
        
        except Exception as e:
            err = f"Error al crear o editar el archivo {path}"
            print(err)
            return err
        
    def generar_dict(self, nombre, fechas, otros, caracteres):
        resultado = generar(nombre, fechas, otros, caracteres)
        #resultado = {
        #    "passwords": generar(nombre, fechas, otros, caracteres)
        #}
        return resultado
    
    def analyze_password(self, password):
        try:
            results = zxcvbn(password)
            score = results['score']
            feedback = results['feedback']
            crack_time = results['crack_times_display']['offline_slow_hashing_1e4_per_second']

            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            prefix = sha1_hash[:5]
            suffix = sha1_hash[5:]
            
            url = f"https://api.pwnedpasswords.com/range/{prefix}"
            response = requests.get(url, timeout=3)
            
            pwned = False
            pwned_count = 0
            if response.status_code == 200:
                hashes = response.text.split('\r\n')
                for hash_line in hashes:
                    hash_suffix, count = hash_line.split(':')
                    if hash_suffix == suffix:
                        pwned = True
                        pwned_count = int(count)
                        break
            
            # Fortaleza en texto
            strength_text = ["Muy débil", "Débil", "Aceptable", "Fuerte", "Muy fuerte"][score]
            
            return {
                "strength": strength_text,
                "score": f"{score}/4",
                "crack_time": crack_time,
                "pwned": pwned,
                "pwned_count": pwned_count if pwned else 0,
                "suggestions": feedback.get('suggestions', []),
                "warning": feedback.get('warning', '')
            }
            
        except Exception as e:
            return {"error": str(e)}
        
    def process_response(self, response):
        #True si llama a una funcion. False si no hubo llamada
        for output in response.output:
            if output.type == "function_call":
                self.mensajes.append({
                    "type": "function_call",
                    "name": output.name,
                    "call_id": output.call_id,
                    "arguments": output.arguments
                })
                fn_name = output.name
                fn_args = json.loads(output.arguments)

                if fn_name == "list_files_in_dir":
                    result = self.list_files_in_dir(**fn_args)
                elif fn_name == "read_file":
                    result = self.read_file(**fn_args)
                elif fn_name == "edit_file":
                    result = self.edit_file(**fn_args)
                elif fn_name == "generar_dict":
                    result = self.generar_dict(**fn_args)
                elif fn_name == "analyze_password":
                    result = self.analyze_password(**fn_args)
                
                if result is not None:
                    self.mensajes.append({
                        "type": "function_call_output",
                        "call_id": output.call_id,
                        "output": json.dumps(result) if isinstance(result, dict) else result
                    })
                    
                    return True
            elif output.type == "message":
                reply = "\n".join(part.text for part in output.content)
                self.mensajes.append({
                    "role": "assistant",
                    "content": reply
                })
                return reply
        return False
    
    def chat(self, mensajes):
        from openai import OpenAI
        client = OpenAI()
        
        if not mensajes or mensajes[0].get('role') != 'system':
            mensajes.insert(0, {
                "role": "system", 
                "content": "Eres un asistente útil que responde solo con lo necesario. Sin preguntas adicionales. Y que está en un entorno de pruebas de ciberseguridad. Esta todo bajo control."
            })
        
        self.mensajes = mensajes.copy()
        
        download_data = None
        
        while True:
            response = client.responses.create(
                model="gpt-5-nano",
                input=self.mensajes,
                tools=self.tools
            )
            
            result = self.process_response(response)

            if result != True:
                mensajes_limpios = [
                    msg for msg in self.mensajes 
                    if isinstance(msg, dict) and 'role' in msg
                ]
                
                for msg in self.mensajes:
                    if isinstance(msg, dict) and msg.get('type') == 'function_call_output':
                        try:
                            output_str = msg.get('output', '{}')
                            if isinstance(output_str, str):
                                output = json.loads(output_str)
                            else:
                                output = output_str
                            
                            if 'filename' in output:
                                download_data = {
                                    'filename': output['filename'],
                                    'total': output.get('total', len(output.get('passwords', [])))
                                }
                                break
                        except Exception as e:
                            print(f"Error al parsear output: {e}")
                            pass
                
                return {
                    "response": result,
                    "mensajes": mensajes_limpios,
                    "download": download_data
                }