import os
import json
from datetime import datetime
from utils import load_config, save_config, call_ai_api, get_active_genres, format_genre_weights, load_personajes, save_personajes, load_canon


def read_file(filepath):
    """Lee un archivo si existe, retorna string vacío si no existe."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def generate_chapter_summary(chapter_content, chapter_num, config):
    """Llama a la IA para resumir el capítulo recién escrito."""
    # Limpiamos el contenido por si acaso para el resumen también
    import re
    chapter_content = re.sub(r'<think>.*?</think>', '', chapter_content, flags=re.DOTALL)
    
    system_prompt = "Eres un editor literario experto que sintetiza tramas para mantener la continuidad de la saga."
    
    prompt = f"""
    Resume el CAPÍTULO {chapter_num} de la novela "{config['story_status']['title']}" de forma concisa (máximo 200 palabras).
    
    EXTRACTO DEL CAPÍTULO:
    {chapter_content[:2000]}
    
    DEBES INCLUIR:
    1. Eventos clave de la trama.
    2. Cambios en las relaciones o estado de los personajes.
    3. Hilos de trama abiertos o misterios sin resolver.
    
    Utiliza un tono objetivo y enfocado en la utilidad para el autor en futuras entregas.
    """
    
    try:
        summary = call_ai_api(prompt, system_prompt, temperature=0.5)
        return summary.strip()
    except Exception as e:
        print(f"Aviso: Falló la generación del resumen, pero el capítulo se guardó: {e}")
        return "Resumen no disponible debido a error técnico."


def update_memory_with_ai(chapter_content, config):
    """Analiza el capítulo para extraer nuevos detalles de personajes y canon."""
    personajes = load_personajes()
    canon = load_canon()
    
    system_prompt = "Eres un analista de continuidad literaria. Tu misión es extraer hechos nuevos y rasgos de personajes de un texto narrativo."
    
    prompt = f"""
    Basado en este capítulo, ¿hay nuevos detalles sobre los personajes o hechos inamovibles (canon)?
    
    ACTUALES PERSONAJES:
    {json.dumps(personajes, indent=2, ensure_ascii=False)}
    
    ACTUAL CANON:
    {canon}
    
    CAPÍTULO:
    {chapter_content}
    
    RESPONDE ÚNICAMENTE CON UN JSON que contenga dos claves: "personajes_actualizados" (el objeto completo de personajes con cambios) y "hechos_canon_nuevos" (una lista de strings con frases cortas de hechos nuevos). 
    Si no hay cambios, devuelve los datos actuales.
    """
    
    try:
        # Usamos temperature baja para precisión
        response = call_ai_api(prompt, system_prompt, temperature=0.2)
        # Extraer JSON de la respuesta (a veces la IA añade texto extra)
        import re
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            if "personajes_actualizados" in data:
                save_personajes(data["personajes_actualizados"])
            if "hechos_canon_nuevos" in data and data["hechos_canon_nuevos"]:
                with open('../data/canon.md', 'a', encoding='utf-8') as f:
                    for hecho in data["hechos_canon_nuevos"]:
                        f.write(f"\n- {hecho}")
            print("Memoria de personajes y canon actualizada.")
    except Exception as e:
        print(f"No se pudo actualizar la memoria automática: {e}")
def clean_model_output(content):
    """Limpia la salida del modelo de trazas de razonamiento y otros elementos no deseados."""
    import re
    # Eliminar bloques <think>...</think>
    content = re.sub(r'<think>.*?</think>', '', content, flags=re.DOTALL)
    # Eliminar bloques (Pensamiento: ...) si existieran
    content = re.sub(r'\(Pensamiento:.*?\)', '', content, flags=re.DOTALL)
    
    lines = content.split('\n')
    cleaned_lines = []
    found_start = False
    
    for line in lines:
        trimmed = line.strip()
        if not found_start:
            # Buscamos el inicio real del capítulo (título o primer párrafo sustancial)
            if trimmed.upper().startswith('CAPÍTULO') or trimmed.startswith('#'):
                found_start = True
                cleaned_lines.append(line)
            elif trimmed and not trimmed.startswith(('<', '{', '[')):
                # Si encontramos texto que no es un tag ni un header, asumimos que es el inicio
                found_start = True
                cleaned_lines.append(line)
        else:
             cleaned_lines.append(line)
             
    return '\n'.join(cleaned_lines).strip()


def run_writing_agent():
    """
    Agente Escritor: compila toda la información y redacta un capítulo.
    Se ejecuta cada hora via GitHub Actions.
    Toma la biblia, resúmenes y notas de investigación para escribir.

    Funciona con cualquier modelo de IA configurado en data/config.json.
    Lee los géneros activos dinámicamente (cualquier género con peso > 0).
    """
    config = load_config()

    # Leer contexto extendido
    biblia = read_file('../data/biblia.md')
    resumen = read_file('../data/resúmenes.md')
    research_notes = read_file('../data/research_log.txt')
    personajes = json.dumps(load_personajes(), indent=2, ensure_ascii=False)
    canon = load_canon()

    chapter_num = config['story_status']['last_chapter_number'] + 1
    temp = config['system_settings']['temperature_writing']
    max_tokens = config['system_settings']['max_tokens_output']
    style = config['dynamic_instructions']['writing_style_override']

    # Géneros activos dinámicos
    active_genres = get_active_genres(config)
    genre_text = format_genre_weights(active_genres)

    # Encontrar el género dominante para el system_prompt
    if active_genres:
        top_genres = sorted(active_genres.items(), key=lambda x: x[1], reverse=True)[:3]
        genre_specialties = ", ".join(g[0].replace('_', ' ').title() for g in top_genres)
    else:
        genre_specialties = "ficción general"

    system_prompt = (
        f"Eres un aclamado autor de novelas ligeras especializado en {genre_specialties}. "
        "REGLA CRÍTICA DE IDIOMA: Escribe EXCLUSIVAMENTE en ESPAÑOL. Prohibido usar Spanglish o términos técnicos en inglés (como 'Noted', 'atmospheres', 'programming', 'duty'). "
        "No uses caracteres chinos o japoneses en el cuerpo del texto fuera de nombres propios. "
        "REGLA CRÍTICA DE FORMATO: Escribe SOLO el contenido de la historia. ABSOLUTAMENTE NINGÚN rastro de pensamientos, razonamientos (<think>) o notas del modelo. "
        "Empieza directamente con el título del capítulo siguiendo el formato: # CAPÍTULO X: [TÍTULO]."
    )

    mega_prompt = f"""
    Vas a escribir el CAPÍTULO {chapter_num} de la novela "{config['story_status']['title']}".

    [PERSONAJES (MEMORIA DETALLADA)]
    {personajes}

    [HECHOS CANÓNICOS (HISTORIAL DE EVENTOS)]
    {canon}

    [REGLAS ADICIONALES DEL MUNDO (BIBLIA)]
    {biblia}

    [RESUMEN DE LA HISTORIA HASTA AHORA]
    {resumen}

    [NOTAS DE INVESTIGACIÓN (USA ESTAS IDEAS PARA EL CAPÍTULO DE HOY)]
    {research_notes}

    [BALANCE DE GÉNEROS ACTIVOS]
    {genre_text}

    [INSTRUCCIONES DE ESTILO]
    {style}
    
    OBJETIVOS:
    1. El capítulo debe tener aproximadamente {config['story_status']['target_chapter_words']} palabras.
    2. Mantén un equilibrio natural entre los géneros según sus pesos de influencia.
    3. Respeta estrictamente los rasgos físicos y personalidades definidos en la MEMORIA DETALLADA.
    4. NO INVENTES NOMBRES DE PERSONAJES NUEVOS para roles principales a menos que sea necesario y justificado por la trama.

    Escribe el capítulo en formato Markdown. Empieza directamente con el cuerpo del capítulo.
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Redactando Capítulo {chapter_num}...")

    try:
        chapter_content = call_ai_api(mega_prompt, system_prompt, temperature=temp, max_tokens=max_tokens)

        # Nueva limpieza profunda del output del modelo
        cleaned_content = clean_model_output(chapter_content)

        # Guardar el capítulo
        chapter_filename = f"../chapters/cap_{chapter_num:03d}.md"
        with open(chapter_filename, 'w', encoding='utf-8') as f:
            # Si el contenido ya trae su propio header de Capítulo, lo respetamos. 
            # Si no, lo añadimos nosotros con el formato correcto.
            if not cleaned_content.upper().startswith('# CAPÍTULO') and not cleaned_content.upper().startswith('CAPÍTULO'):
                 f.write(f"# CAPÍTULO {chapter_num}\n\n")
            f.write(cleaned_content)

        print(f"Capítulo {chapter_num} guardado con éxito.")

        # --- GENERAR RESUMEN PARA MEMORIA (Contexto futuro) ---
        print("Generando resumen del capítulo para la memoria de la historia...")
        summary = generate_chapter_summary(chapter_content, chapter_num, config)
        
        with open('../data/resúmenes.md', 'a', encoding='utf-8') as f:
            f.write(f"\n### Capítulo {chapter_num}\n\n{summary}\n\n---\n")
        
        # --- ACTUALIZAR MEMORIA DE PERSONAJES Y CANON ---
        print("Actualizando memoria de personajes y canon...")
        update_memory_with_ai(chapter_content, config)
        
        # Actualizar estado en config.json
        config['story_status']['last_chapter_number'] = chapter_num
        save_config(config)

        # Limpiar el registro de investigación para el siguiente ciclo horario
        with open('../data/research_log.txt', 'w', encoding='utf-8') as f:
            f.write("")

    except Exception as e:
        print(f"Error durante la escritura del capítulo: {e}")
        raise


if __name__ == "__main__":
    run_writing_agent()
