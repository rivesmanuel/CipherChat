from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import Conversacion
from app.services.agent import Agent
import datetime
import os

bp = Blueprint('Manuel', __name__)

@bp.route('/chat', methods=['POST'])
def enviar_mensaje():
    data = request.get_json()
    message = data.get('message')
    conversation_id = data.get('conversation_id')
    print(f"=== DEBUG 1: Mensaje recibido: {message}")
    print(f"=== DEBUG 2: Conversation ID: {conversation_id}")
    
    if not conversation_id:
        conversacion = Conversacion(mensajes=[])
        db.session.add(conversacion)
        db.session.commit()
        conversation_id = conversacion.id
        print(f"=== DEBUG 3: Nueva conversación creada con ID: {conversation_id}")
    else:
        conversacion = Conversacion.query.get(conversation_id)
        print(f"=== DEBUG 4: Conversación cargada. Mensajes actuales: {conversacion.mensajes}")

    mensajes = conversacion.mensajes or []
    print(f"=== DEBUG 5: Mensajes antes de añadir usuario: {mensajes}")

    mensajes.append({"role": "user", "content": message})
    print(f"=== DEBUG 6: Mensajes después de añadir usuario: {mensajes}")

    agent = Agent()
    print(f"=== DEBUG 7: Llamando al agent...")
    resultado = agent.chat(mensajes)
    if isinstance(resultado, dict):
        respuesta = resultado["response"]
        mensajes = resultado["mensajes"]
        download_data = resultado.get("download")
    else:
        respuesta = resultado
        download_data = None

    conversacion.mensajes = mensajes
    conversacion.actualizado = datetime.datetime.utcnow()
    db.session.commit()

    response_json = {
        "conversation_id": conversation_id,
        "response": respuesta
    }
    if download_data:
        response_json["download"] = download_data
        
    return jsonify (response_json)

@bp.route('/conversaciones', methods=['GET'])
def ver_conversaciones():
    conversaciones = Conversacion.query.all()
    result = []
    for conv in conversaciones:
        result.append({
            "id": conv.id,
            "creado": conv.creado.isoformat(),
            "actualizado": conv.actualizado.isoformat(),
            "mensajes": conv.mensajes
        })
    return jsonify(result)

@bp.route('/conversacion/<int:id>', methods=['GET'])
def ver_conversacion(id):
    conv = Conversacion.query.get_or_404(id)
    return jsonify({
        "id": conv.id,
        "mensajes": conv.mensajes
    })

@bp.route('/conversacion/nueva', methods=['POST'])
def nueva_conversacion():
    conversacion = Conversacion(mensajes=[])
    db.session.add(conversacion)
    db.session.commit()
    return jsonify({"conversation_id": conversacion.id})

@bp.route('/conversacion/<int:id>', methods=['DELETE'])
def eliminar_conversacion(id):
    conv = Conversacion.query.get_or_404(id)
    db.session.delete(conv)
    db.session.commit()
    return jsonify({"message": "Conversación eliminada correctamente"})

@bp.route('/descargar/<filename>', methods=['GET'])
def descargar_wordlist(filename):
    try:
        filepath = os.path.join( 'app','static', 'wordlists', filename)
        filepath= os.getcwd ()+ "\\"+filepath
        if os.path.exists(filepath):
            return send_file(
                filepath,
                mimetype='text/plain',
                as_attachment=True,
                download_name=filename
            )
        else:
            return jsonify({"error": "Archivo no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500