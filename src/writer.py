import os
import json
import re
from datetime import datetime
from utils import (
    load_config,
    save_config,
    call_ai_api,
    get_active_genres,
    format_genre_weights,
    load_personajes,
    save_personajes,
    load_cronologia,
    save_cronologia,
    load_hilos,
    save_hilos,
    load_semillas,
    save_semillas,
    load_canon,
)


def read_file(filepath):
    """Lee un archivo si existe, retorna string vacío si no existe."""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def generate_chapter_summary(chapter_content, chapter_num, config):
    """Llama a la IA para resumir el capítulo recién escrito."""
    chapter_content = re.sub(
        r"<think>.*?</think>", "", chapter_content, flags=re.DOTALL
    )

    system_prompt = (
        "Eres un editor literario experto. Resume tramas en máximo 200 palabras. "
        "RESPONDE SOLO CON TEXTO PLANO en español. "
        "PROHIBIDO: bloques <think>, notas al autor, disclaimers, tablas, listas con viñetas, "
        "encabezados markdown, advertencias, preguntas al usuario, o cualquier texto que no sea "
        "parte directa del resumen narrativo."
    )

    prompt = f"""
    Resume el CAPÍTULO {chapter_num} de la novela "{config["story_status"]["title"]}" en un párrafo fluido de máximo 200 palabras.

    EXTRACTO:
    {chapter_content[:2000]}

    Incluye: eventos clave, cambios en relaciones, hilos abiertos.
    Devuelve SOLO el texto del resumen, nada más.
    """

    try:
        response = call_ai_api(prompt, system_prompt, temperature=0.2)
        summary = response.strip()
        summary = re.sub(
            r"<extra_thought>.*?</extra_thought>", "", summary, flags=re.DOTALL
        )
        summary = re.sub(r"<think>.*?</think>", "", summary, flags=re.DOTALL)
        summary = re.sub(r"\(Pensamiento:.*?\)", "", summary, flags=re.DOTALL)
        summary = re.sub(r"\[NOTAS?:.*?\]", "", summary, flags=re.DOTALL)
        summary = re.sub(r"<\|.*?\|>", "", summary, flags=re.DOTALL)
        summary = re.sub(r"\*\*.*?\*\*", "", summary, flags=re.DOTALL)
        summary = summary.strip()
        if len(summary) < 30:
            print(
                f"  WARN: Resumen demasiado corto ({len(summary)} chars), descartado."
            )
            summary = f"(Resumen del capítulo {chapter_num} no disponible)"
        return summary
    except Exception as e:
        print(f"  WARN: Error generando resumen: {e}")
        return f"(Resumen del capítulo {chapter_num} no disponible)"


def update_memory_with_ai(chapter_content, chapter_num, config):
    """Analiza el capítulo para extraer nuevos detalles de personajes y cronología."""
    personajes = load_personajes()
    cronologia = load_cronologia()
    hilos = load_hilos()
    semillas = load_semillas()
    canon = load_canon()

    system_prompt = (
        "Eres un experto en continuidad Narrativa y Lore Master de nivel profesional. "
        "Tu objetivo es mantener una coherencia absoluta, detectando evolución de personajes, "
        "rastreando hilos narrativos abiertos y gestionando el foreshadowing (semillas)."
    )

    prompt = f"""
    Analiza a fondo el CAPÍTULO {chapter_num} para actualizar la arquitectura de la novela.
    
    ESTADO ACTUAL:
    - Personajes: {json.dumps(personajes, indent=2, ensure_ascii=False)}
    - Cronología: {json.dumps(cronologia, indent=2, ensure_ascii=False)}
    - Hilos Narrativos: {json.dumps(hilos, indent=2, ensure_ascii=False)}
    - Semillas (Foreshadowing): {json.dumps(semillas, indent=2, ensure_ascii=False)}
    - Canon: {canon}
    
    TEXTO DEL CAPÍTULO A ANALIZAR:
    {chapter_content}
    
    DEBES GENERAR ÚNICAMENTE UN JSON con cinco claves:
    1. "personajes_actualizados": Personajes con cambios en 'estado_vital', 'relaciones', 'secretos', 'notas_evolucion' o 'metas'.
    2. "nuevo_evento_cronologia": Detalles para la cronología (dia, resumen, eventos_clave, revelaciones, ambiente).
    3. "hilos_actualizados": Evolución de las subtramas (puedes añadir hilos nuevos o actualizar el 'progreso' y 'tension' de los existentes).
    4. "semillas_nuevas": Lista de objetos con 'detalle', 'capitulo_plantado', 'potencial_pago' y 'estado' para foreshadowing plantado ahora.
    5. "hechos_canon_nuevos": Frases cortas de hechos inamovibles.

    REGLA DE EXCELENCIA: Detecta detalles pequeños que puedan servir de semillas futuras. Si una semilla antigua se ha 'cosechado' (usado) en este capítulo, indícalo en el análisis para marcarla como resuelta.
    """

    try:
        response = call_ai_api(prompt, system_prompt, temperature=0.2)

        json_match = re.search(r"\{.*\}", response, re.DOTALL)
        if not json_match:
            print(
                f"  WARN: La IA no devolvió JSON válido en el análisis del capítulo {chapter_num}."
            )
            return

        data = json.loads(json_match.group())

        # Actualizar personajes
        if "personajes_actualizados" in data and data["personajes_actualizados"]:
            personajes = load_personajes()
            for char_name, char_data in data["personajes_actualizados"].items():
                if char_name in personajes:
                    personajes[char_name].update(char_data)
                else:
                    personajes[char_name] = char_data
            save_personajes(personajes)
            print(
                f"  Personajes actualizados: {list(data['personajes_actualizados'].keys())}"
            )

        # Añadir evento de cronología
        if "nuevo_evento_cronologia" in data and data["nuevo_evento_cronologia"]:
            cronologia = load_cronologia()
            cronologia[f"capitulo_{chapter_num}"] = data["nuevo_evento_cronologia"]
            save_cronologia(cronologia)
            print(f"  Cronología actualizada: capítulo {chapter_num}")

        # Actualizar hilos narrativos
        if "hilos_actualizados" in data and data["hilos_actualizados"]:
            hilos = load_hilos()
            hilos.update(data["hilos_actualizados"])
            save_hilos(hilos)
            print(f"  Hilos narrativos actualizados")

        # Añadir nuevas semillas
        if "semillas_nuevas" in data and data["semillas_nuevas"]:
            semillas = load_semillas()
            for i, semilla in enumerate(data["semillas_nuevas"], 1):
                semillas[f"semilla_{chapter_num}_{i:02d}"] = semilla
            save_semillas(semillas)
            print(f"  Nuevas semillas añadidas: {len(data['semillas_nuevas'])}")

        # Actualizar canon
        if "hechos_canon_nuevos" in data and data["hechos_canon_nuevos"]:
            canon = load_canon()
            canon += f"\n\n## Hechos Establecidos (Capítulo {chapter_num})\n"
            for hecho in data["hechos_canon_nuevos"]:
                canon += f"- {hecho}\n"
            with open("../data/canon.md", "w", encoding="utf-8") as f:
                f.write(canon)
            print(
                f"  Canon actualizado: {len(data['hechos_canon_nuevos'])} hechos nuevos"
            )

    except json.JSONDecodeError as e:
        print(f"  WARN: Error parseando JSON de la IA: {e}")
    except Exception as e:
        print(f"  WARN: Error actualizando memoria: {e}")


def validate_chapter_language(chapter_content, chapter_num, config):
    """Valida que el capítulo esté en español puro sin caracteres de otros idiomas."""
    # Detectar caracteres CJK (chino, japonés kanji), cirílico, etc.
    cjk_pattern = re.compile(r"[\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff\uff00-\uffef]")
    cyrillic_pattern = re.compile(r"[\u0400-\u04ff]")
    greek_pattern = re.compile(r"[\u0370-\u03ff]")
    arabic_pattern = re.compile(r"[\u0600-\u06ff]")

    issues = []
    if cjk_pattern.search(chapter_content):
        matches = cjk_pattern.findall(chapter_content)
        issues.append(f"Caracteres CJK detectados: {''.join(matches[:10])}")
    if cyrillic_pattern.search(chapter_content):
        matches = cyrillic_pattern.findall(chapter_content)
        issues.append(f"Caracteres cirílicos detectados: {''.join(matches[:10])}")
    if greek_pattern.search(chapter_content):
        matches = greek_pattern.findall(chapter_content)
        issues.append(f"Caracteres griegos detectados: {''.join(matches[:10])}")
    if arabic_pattern.search(chapter_content):
        matches = arabic_pattern.findall(chapter_content)
        issues.append(f"Caracteres árabes detectados: {''.join(matches[:10])}")

    if issues:
        print(f"VALIDACIÓN FALLIDA Capítulo {chapter_num}:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    return True


def clean_model_output(content):
    """Limpia la salida del modelo de trazas de razonamiento y otros elementos no deseados."""
    content = re.sub(
        r"<extra_thought>.*?</extra_thought>", "", content, flags=re.DOTALL
    )
    content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
    content = re.sub(r"\(Pensamiento:.*?\)", "", content, flags=re.DOTALL)
    content = re.sub(r"\[NOTAS?:.*?\]", "", content, flags=re.DOTALL)
    content = re.sub(r"<\|.*?\|>", "", content, flags=re.DOTALL)

    lines = content.split("\n")
    cleaned_lines = []
    found_start = False

    for line in lines:
        trimmed = line.strip()
        if not found_start:
            if re.match(r"^#?\s*CAP[ÍI]TULO", trimmed, re.IGNORECASE):
                found_start = True
                cleaned_lines.append(line)
            elif trimmed and not trimmed.startswith(("<", "{", "[")):
                found_start = True
                cleaned_lines.append(line)
        else:
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines).strip()


def validate_chapter_completeness(content, chapter_num):
    """Verifica que el capítulo no termine a mitad de frase."""
    content = content.strip()
    if not content:
        return False

    last_lines = content.split("\n")[-5:]
    last_text = " ".join(line.strip() for line in last_lines if line.strip())

    incomplete_indicators = [
        last_text.rstrip().endswith(","),
        last_text.rstrip().endswith("—"),
        last_text.rstrip().endswith("-"),
        last_text.rstrip().endswith("..."),
    ]

    if any(incomplete_indicators):
        print(f"VALIDACIÓN FALLIDA: El capítulo {chapter_num} termina incompletamente.")
        print(f"  Última línea: '{last_lines[-1].strip()}'")
        return False

    if len(last_text) < 20:
        print(
            f"VALIDACIÓN FALLIDA: El capítulo {chapter_num} es demasiado corto o está vacío."
        )
        return False

    return True


def validate_chapter_length(content, min_words=1200, max_words=1800):
    """Verifica que el capítulo tenga entre min_words y max_words palabras."""
    words = content.split()
    word_count = len(words)

    if word_count < min_words:
        print(f"VALIDACIÓN FALLIDA: El capítulo tiene {word_count} palabras, mínimo requerido: {min_words}.")
        return False
    if word_count > max_words:
        print(f"VALIDACIÓN FALLIDA: El capítulo tiene {word_count} palabras, máximo permitido: {max_words}.")
        return False

    print(f"  Longitud validada: {word_count} palabras (rango: {min_words}-{max_words})")
    return True


def truncate(text, max_chars):
    """Truncate text to max_chars, keeping the beginning."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n... [truncado para ahorrar contexto]"


def summarize_personajes(max_chars=800):
    """Return condensed character info, not full JSON."""
    personajes = load_personajes()
    parts = []
    for name, data in personajes.items():
        rol = data.get("rol", "")
        estado = data.get("estado_vital", "")
        secretos = data.get("secretos", "")
        partes = []
        if rol:
            partes.append(f"Rol: {rol}")
        if estado:
            partes.append(f"Estado: {estado}")
        if secretos:
            partes.append(f"Secretos: {secretos}")
        parts.append(f"{name} — {' | '.join(partes)}")
    result = "\n".join(parts)
    return truncate(result, max_chars)


def summarize_cronologia(last_n=3):
    """Return only the last N chronology entries."""
    cronologia = load_cronologia()
    keys = sorted(cronologia.keys())
    recent = keys[-last_n:] if len(keys) > last_n else keys
    parts = []
    for k in recent:
        entry = cronologia[k]
        resumen = entry.get("resumen", "")
        revelaciones = entry.get("revelaciones", [])
        parts.append(f"{k}: {resumen}")
        if revelaciones:
            for r in revelaciones:
                parts.append(f"  - {r}")
    return "\n".join(parts)


def summarize_hilos(max_chars=500):
    """Return only active thread names, tension, and next step."""
    hilos = load_hilos()
    parts = []
    for name, data in hilos.items():
        tension = data.get("tension", "?")
        proximo = data.get("proximo_paso", "")
        parts.append(f"{name} (tension:{tension}) -> {proximo}")
    return truncate("\n".join(parts), max_chars)


def summarize_semillas(max_chars=400):
    """Return only pending seeds."""
    semillas = load_semillas()
    pending = [(k, v) for k, v in semillas.items() if v.get("estado") == "Pendiente"]
    parts = []
    for k, v in pending:
        parts.append(f"{k}: {v.get('detalle', '')}")
    return truncate("\n".join(parts), max_chars)


def run_writing_agent():
    """
    Agente Escritor: compila toda la información y redacta un capítulo.
    Se ejecuta cada 4 horas via GitHub Actions.
    Toma la biblia, resúmenes y notas de investigación para escribir.

    Funciona con cualquier modelo de IA configurado en data/config.json.
    Lee los géneros activos dinámicamente (cualquier género con peso > 0).
    """
    config = load_config()

    # Leer contexto extendido — TRUNCADO para no exceder ventana de contexto
    biblia = truncate(read_file("../data/biblia.md"), 1500)
    resumen = truncate(read_file("../data/resúmenes.md"), 1200)
    research_notes = truncate(read_file("../data/research_log.txt"), 500)
    personajes = summarize_personajes(800)
    cronologia = summarize_cronologia(last_n=3)
    hilos = summarize_hilos(500)
    semillas = summarize_semillas(400)
    canon = truncate(load_canon(), 1000)

    chapter_num = config["story_status"]["last_chapter_number"] + 1
    temp = config["system_settings"]["temperature_writing"]
    max_tokens = config["system_settings"]["max_tokens_output"]
    style = config["dynamic_instructions"]["writing_style_override"]

    # Géneros activos dinámicos
    active_genres = get_active_genres(config)
    genre_text = format_genre_weights(active_genres)

    # Encontrar el género dominante para el system_prompt
    if active_genres:
        top_genres = sorted(active_genres.items(), key=lambda x: x[1], reverse=True)[:3]
        genre_specialties = ", ".join(
            g[0].replace("_", " ").title() for g in top_genres
        )
    else:
        genre_specialties = "ficción general"

    system_prompt = (
        f"Eres un autor profesional de novelas ligeras japonesas traducidas al español, especializado en {genre_specialties}. "
        "ESCRIBE ÚNICAMENTE EN ESPAÑOL. ESTÁ TERMINANTEMENTE PROHIBIDO usar caracteres o palabras en cualquier otro idioma: "
        "ni inglés, ni chino, ni japonés (kanji/kana), ni ruso, ni coreano, ni árabe, ni portugués, ni francés. "
        "Si el modelo intenta insertar caracteres no latinos, el capítulo será RECHAZADO automáticamente. "
        "REGLAS DE CONTINUIDAD OBLIGATORIAS: "
        "1. SOLO usa personajes, lugares y objetos que estén documentados en los archivos de memoria proporcionados. "
        "2. PROHIBIDO inventar: implantes corporales, dispositivos internos, poderes ocultos, tarjetas de acceso especiales, "
        "   profesores nuevos, familiares inexistentes, organizaciones secretas no mencionadas. "
        "3. NO cambies dónde viven los personajes ni su situación vital sin base explícita en los resúmenes anteriores. "
        "4. NO introduzcas personajes nuevos. Los únicos personajes existentes son: Haruto Mizuki, Lyra Vel'Kath, "
        "   Kenji Aoyama, Directora Shirogane, y la madre de Haruto. "
        "5. El capítulo debe continuar exactamente desde donde terminó el anterior. "
        "INSTRUCCIONES DE FORMATO: "
        "1. Narración en primera persona desde la perspectiva de Haruto Mizuki. "
        "2. Monólogos internos en cursiva (*texto*). "
        "3. Diálogos con guion largo (—). "
        '4. Inicia estrictamente con: # Capítulo {chapter_num} — "Título del Capítulo". '
        "REGLAS DEL TÍTULO: "
        "a) Longitud: entre 2 y 6 palabras. "
        "b) El título debe capturar el momento más significativo o evocador del capítulo, no resumirlo. "
        "c) Evita títulos que empiecen con 'El Peso de', 'Límites de', 'La Frecuencia de' repetidamente. "
        "d) Buenos referentes de esta serie: 'La Chica del Cielo', 'Canibalismo Mediático', 'Cuarenta y Siete Suscriptores', 'Zona Muerta', 'Café a las 6 AM'. "
        "e) Sé creativo pero ancla el título en algo concreto del capítulo. "
        "REGLAS DE EXTENSIÓN OBLIGATORIAS: "
        "9. El capítulo debe tener ENTRE 1200 Y 1800 PALABRAS. No menos de 1200. Si escribes menos, el capítulo será rechazado. "
        "10. Desarrolla cada escena con descripción, diálogo y reacción. Cada capítulo debe tener al menos 3-4 escenas bien desarrolladas. "
        "11. El capítulo debe tener un cierre completo con resolución de la escena principal, nunca terminar a mitad de frase o escena."
    )

    mega_prompt = f"""
    Vas a escribir el CAPÍTULO {chapter_num} de la novela "{config["story_status"]["title"]}".

    [PERSONAJES (MEMORIA DETALLADA)]
    {personajes}

    [HECHOS CANÓNICOS (HISTORIAL DE EVENTOS)]
    {canon}

    [CRONOLOGÍA MAESTRA (ORDEN DE LOS HECHOS)]
    {cronologia}

    [HILOS NARRATIVOS ACTIVOS (SUBTRAMAS)]
    {hilos}

    [SEMILLAS DE LORE Y FORESHADOWING (PLANIFICACIÓN)]
    {semillas}

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
    1. El capítulo debe tener aproximadamente {config["story_status"]["target_chapter_words"]} palabras.
    2. Mantén un equilibrio natural entre los géneros según sus pesos de influencia.
    3. Respeta estrictamente los rasgos físicos y personalidades definidos en la MEMORIA DETALLADA.
    4. NO INVENTES NOMBRES DE PERSONAJES NUEVOS para roles principales a menos que sea necesario y justificado por la trama.
    5. CONTINUIDAD: El capítulo anterior fue el {config["story_status"]["last_chapter_number"]}. Continúa la historia desde donde quedó, respetando todos los eventos, relaciones y secretos establecidos.
    6. PROHIBIDO añadir implantes, objetos corporales, poderes ocultos o situaciones de convivencia que no estén documentados en los archivos de memoria proporcionados.

    Escribe el capítulo en formato Markdown. Empieza directamente con el cuerpo del capítulo.
    """

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Redactando Capítulo {chapter_num}...")

    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            chapter_content = call_ai_api(
                mega_prompt, system_prompt, temperature=temp, max_tokens=max_tokens
            )

            cleaned_content = clean_model_output(chapter_content)

            validation_failed = False
            failure_reason = ""

            if not validate_chapter_language(cleaned_content, chapter_num, config):
                failure_reason = "caracteres de otros idiomas"
                validation_failed = True

            if not validate_chapter_completeness(cleaned_content, chapter_num):
                failure_reason = "cierre incompleto o capítulo demasiado corto"
                validation_failed = True

            if not validate_chapter_length(cleaned_content):
                failure_reason = "capítulo fuera del rango de palabras (1200-1800)"
                validation_failed = True

            if validation_failed:
                if attempt < max_attempts:
                    print(f"  Reintentando ({attempt + 1}/{max_attempts})...")
                    mega_prompt += f"\n\nIMPORTANTE: El intento anterior fue rechazado por {failure_reason}. Reescribe el capítulo asegurándote de: (1) usar SOLO caracteres latinos del español, (2) terminar con un cierre completo de escena, no a mitad de frase, (3) el capítulo debe tener entre 1200 y 1800 palabras."
                    continue
                else:
                    print(
                        f"ERROR: Capítulo {chapter_num} rechazado tras {max_attempts} intentos por {failure_reason}."
                    )
                    raise RuntimeError(
                        f"El capítulo {chapter_num} no pasó validación tras {max_attempts} intentos."
                    )

            # Guardar el capítulo
            chapter_filename = f"../chapters/cap_{chapter_num:03d}.md"
            with open(chapter_filename, "w", encoding="utf-8") as f:
                if not cleaned_content.upper().startswith(
                    "# CAPÍTULO"
                ) and not cleaned_content.upper().startswith("CAPÍTULO"):
                    f.write(f'# Capítulo {chapter_num} — "Título del Capítulo"\n\n')
                f.write(cleaned_content)

            print(f"Capítulo {chapter_num} guardado con éxito.")

            # --- GENERAR RESUMEN PARA MEMORIA (Contexto futuro) ---
            print("Generando resumen del capítulo para la memoria de la historia...")
            summary = generate_chapter_summary(chapter_content, chapter_num, config)

            with open("../data/resúmenes.md", "a", encoding="utf-8") as f:
                f.write(f"\n### Capítulo {chapter_num}\n\n{summary}\n\n---\n")

            # --- ACTUALIZAR MEMORIA PROFUNDA (Personajes + Cronología + Canon) ---
            print("Actualizando memoria avanzada de la historia...")
            try:
                update_memory_with_ai(chapter_content, chapter_num, config)
            except Exception as e:
                print(f"  WARN: Error en actualización de memoria: {e}")

            # Actualizar estado en config.json
            config["story_status"]["last_chapter_number"] = chapter_num
            save_config(config)

            # Limpiar el registro de investigación para el siguiente ciclo horario
            with open("../data/research_log.txt", "w", encoding="utf-8") as f:
                f.write("")

            break  # Éxito, salir del loop

        except RuntimeError:
            raise
        except Exception as e:
            print(f"Error durante la escritura del capítulo: {e}")
            raise


if __name__ == "__main__":
    run_writing_agent()
