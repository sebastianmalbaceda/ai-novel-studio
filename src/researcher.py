import os
from utils import load_config, call_ai_api, get_active_genres, format_genre_weights


def run_research_agent():
    """
    Agente Investigador: genera ideas y tropos literarios.
    Se ejecuta cada 15 minutos via GitHub Actions.
    Los resultados se añaden en modo append a research_log.txt.

    Funciona con cualquier modelo de IA configurado en data/config.json.
    Lee los géneros activos dinámicamente (cualquier género con peso > 0).
    """
    config = load_config()
    research_focus = config['dynamic_instructions']['current_research_focus']
    temp = config['system_settings']['temperature_research']

    # Obtener géneros activos dinámicamente
    active_genres = get_active_genres(config)
    genre_text = format_genre_weights(active_genres)

    system_prompt = "Eres un investigador experto en tropos literarios, ciencia ficción y manga."

    prompt = f"""
    Realiza una investigación y lluvia de ideas sobre el siguiente tema:
    "{research_focus}"

    Busca formas originales de integrar estos elementos en una historia que combina los siguientes géneros con sus pesos de influencia:
    {genre_text}

    Genera 3 ideas concretas (eventos, revelaciones de misterio o interacciones entre personajes).
    Devuelve solo el texto de tus ideas, estructurado en puntos.
    """

    calls_per_run = config['system_settings'].get('researcher_calls_per_run', 1)

    print(f"Iniciando ciclo de investigación profunda ({calls_per_run} iteraciones)...")

    try:
        current_knowledge = ""
        
        with open('../data/research_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"\n\n============= NUEVA SESIÓN DE INVESTIGACIÓN ({calls_per_run} ITERACIONES) =============\n")

            for i in range(1, calls_per_run + 1):
                print(f"-> Ejecutando iteración {i}/{calls_per_run}...")
                
                if i == 1:
                    actual_prompt = prompt
                else:
                    actual_prompt = f"""
                    Aquí está la investigación y lluvia de ideas que generamos en la iteración anterior:
                    ---
                    {current_knowledge}
                    ---
                    Como investigador experto, tómate esta iteración para refinar, expandir y profundizar en esas ideas.
                    Enfócate en mejorar la consistencia, el atractivo de los personajes y llevar las ideas un paso más allá basándote en los géneros objetivo.
                    No te repitas textualmente, sino evoluciona el concepto.
                    """

                # Llamada al modelo
                research_output = call_ai_api(actual_prompt, system_prompt, temperature=temp)
                current_knowledge = research_output

                # Añadir el resultado interactivo de esta ronda al log, para que quede registro
                f.write(f"\n--- ITERACIÓN {i} ---\n{research_output}\n")
                
                print(f"   [Iteración {i} completada]")

        print("Investigación completada y guardada evolutivamente en research_log.txt")
    except Exception as e:
        print(f"Error durante la investigación iterativa: {e}")
        raise


if __name__ == "__main__":
    run_research_agent()
