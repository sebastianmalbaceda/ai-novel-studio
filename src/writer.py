import os
from datetime import datetime
from utils import load_config, save_config, call_ai_api, get_active_genres, format_genre_weights


def read_file(filepath):
    """Lee un archivo si existe, retorna string vacío si no existe."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


def generate_chapter_summary(chapter_content, chapter_num, config):
    """Llama a la IA para resumir el capítulo recién escrito."""
    system_prompt = "Eres un editor literario experto que sintetiza tramas para mantener la continuidad de la saga."
    
    prompt = f"""
    Resume el CAPÍTULO {chapter_num} de la novela "{config['story_status']['title']}" de forma concisa (máximo 200 palabras).
    
    EXTRACTO DEL CAPÍTULO:
    {chapter_content[:2000]}  # Enviamos solo el inicio y fin si es muy largo, o lo necesario para captar el tono
    
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



def run_writing_agent():
    """
    Agente Escritor: compila toda la información y redacta un capítulo.
    Se ejecuta cada hora via GitHub Actions.
    Toma la biblia, resúmenes y notas de investigación para escribir.

    Funciona con cualquier modelo de IA configurado en data/config.json.
    Lee los géneros activos dinámicamente (cualquier género con peso > 0).
    """
    config = load_config()

    # Leer contexto
    biblia = read_file('../data/biblia.md')
    resumen = read_file('../data/resúmenes.md')
    research_notes = read_file('../data/research_log.txt')

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

    system_prompt = f"Eres un aclamado autor de novelas ligeras especializado en {genre_specialties}."

    mega_prompt = f"""
    Vas a escribir el CAPÍTULO {chapter_num} de la novela "{config['story_status']['title']}".

    [REGLAS DEL MUNDO Y PERSONAJES (BIBLIA)]
    {biblia}

    [RESUMEN DE LA HISTORIA HASTA AHORA]
    {resumen}

    [NOTAS DE INVESTIGACIÓN (USA ESTAS IDEAS PARA EL CAPÍTULO DE HOY)]
    {research_notes}

    [BALANCE DE GÉNEROS ACTIVOS]
    {genre_text}

    [INSTRUCCIONES DE ESTILO]
    {style}
    El capítulo debe tener aproximadamente {config['story_status']['target_chapter_words']} palabras.
    Mantén un equilibrio natural entre los géneros según sus pesos de influencia.

    Escribe directamente el capítulo en formato Markdown.
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Redactando Capítulo {chapter_num}...")

    try:
        chapter_content = call_ai_api(mega_prompt, system_prompt, temperature=temp, max_tokens=max_tokens)

        # Guardar el capítulo
        chapter_filename = f"../chapters/cap_{chapter_num:03d}.md"
        with open(chapter_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Capítulo {chapter_num}\n\n{chapter_content}")

        print(f"Capítulo {chapter_num} guardado con éxito.")

        # --- GENERAR RESUMEN PARA MEMORIA (Contexto futuro) ---
        print("Generando resumen del capítulo para la memoria de la historia...")
        summary = generate_chapter_summary(chapter_content, chapter_num, config)
        
        with open('../data/resúmenes.md', 'a', encoding='utf-8') as f:
            f.write(f"\n### Capítulo {chapter_num}\n\n{summary}\n\n---\n")
        
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
