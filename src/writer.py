import os
from utils import load_config, save_config, call_ai_api, get_active_genres, format_genre_weights


def read_file(filepath):
    """Lee un archivo si existe, retorna string vacío si no existe."""
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ""


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

    print(f"Redactando Capítulo {chapter_num}...")

    try:
        chapter_content = call_ai_api(mega_prompt, system_prompt, temperature=temp, max_tokens=max_tokens)

        # Guardar el capítulo
        chapter_filename = f"../chapters/cap_{chapter_num:03d}.md"
        with open(chapter_filename, 'w', encoding='utf-8') as f:
            f.write(f"# Capítulo {chapter_num}\n\n{chapter_content}")

        print(f"Capítulo {chapter_num} guardado con éxito.")

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
