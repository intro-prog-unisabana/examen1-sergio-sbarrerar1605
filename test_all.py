# NO MODIFICAR
import subprocess
import sys
import ast
import os
import tempfile


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def run_program(filename, inputs):
    """Ejecuta un archivo .py con inputs simulados por stdin."""
    process = subprocess.Popen(
        [sys.executable, filename],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, _ = process.communicate(input="\n".join(inputs))
    return stdout


def run_program_with_vars(filename, replacements):
    """
    Lee el archivo .py, reemplaza líneas de asignación de variables
    según el dict replacements {"var": valor}, y ejecuta el resultado.
    Ejemplo: replacements={"nums": [1,2,3]} reemplaza la línea 'nums = ...'
    """
    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()

    lines = source.splitlines()
    new_lines = []
    for line in lines:
        replaced = False
        for var, value in replacements.items():
            # Reemplaza líneas que asignan exactamente esa variable
            if line.strip().startswith(f"{var} =") or line.strip().startswith(f"{var}="):
                new_lines.append(f"{var} = {repr(value)}")
                replaced = True
                break
        if not replaced:
            new_lines.append(line)

    modified_source = "\n".join(new_lines)

    # Escribe en un archivo temporal y ejecútalo
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as tmp:
        tmp.write(modified_source)
        tmp_path = tmp.name

    try:
        process = subprocess.Popen(
            [sys.executable, tmp_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, _ = process.communicate()
    finally:
        os.unlink(tmp_path)

    return stdout


# ─────────────────────────────────────────────
# Pregunta 1: Beca
# ─────────────────────────────────────────────

class TestBeca:

    def test_bi_otorga_beca_sin_importar_nada(self):
        output = run_program("beca.py", ["0.0", "0", "0", "1"])
        assert "True" in output

    def test_bi_otorga_beca_con_pa_bajo(self):
        output = run_program("beca.py", ["2.0", "50", "200", "1"])
        assert "True" in output

    def test_cumple_todos_requisitos(self):
        output = run_program("beca.py", ["3.5", "100", "260", "0"])
        assert "True" in output

    def test_cumple_holgado(self):
        output = run_program("beca.py", ["4.5", "200", "350", "0"])
        assert "True" in output

    def test_pa_insuficiente(self):
        output = run_program("beca.py", ["3.4", "150", "300", "0"])
        assert "False" in output

    def test_pa_cero(self):
        output = run_program("beca.py", ["0.0", "150", "300", "0"])
        assert "False" in output

    def test_horas_insuficientes(self):
        output = run_program("beca.py", ["3.8", "99", "300", "0"])
        assert "False" in output

    def test_horas_cero(self):
        output = run_program("beca.py", ["3.8", "0", "300", "0"])
        assert "False" in output

    def test_saber_pro_insuficiente(self):
        output = run_program("beca.py", ["3.8", "150", "259", "0"])
        assert "False" in output

    def test_saber_pro_cero(self):
        output = run_program("beca.py", ["3.8", "150", "0", "0"])
        assert "False" in output

    def test_falla_pa_y_horas(self):
        output = run_program("beca.py", ["3.0", "80", "300", "0"])
        assert "False" in output

    def test_falla_todo(self):
        output = run_program("beca.py", ["1.0", "10", "100", "0"])
        assert "False" in output

    def test_borde_pa_exactamente_35(self):
        output = run_program("beca.py", ["3.5", "100", "260", "0"])
        assert "True" in output

    def test_borde_horas_exactamente_100(self):
        output = run_program("beca.py", ["3.5", "100", "260", "0"])
        assert "True" in output

    def test_borde_saber_pro_exactamente_260(self):
        output = run_program("beca.py", ["3.5", "100", "260", "0"])
        assert "True" in output


# ─────────────────────────────────────────────
# Pregunta 2: Encontrando la "s"
# ─────────────────────────────────────────────

class TestEncontrandoS_Parte1:

    def test_contiene_s_minuscula(self):
        output = run_program("s_parte1.py", ["Estoy bajo demasiada presión"])
        assert "True" in output

    def test_no_contiene_s(self):
        output = run_program("s_parte1.py", ["Voy a la reunión"])
        assert "False" in output

    def test_S_mayuscula_en_frase(self):
        output = run_program("s_parte1.py", ["Solo necesito un café"])
        assert "True" in output

    def test_solo_S_mayuscula(self):
        output = run_program("s_parte1.py", ["SALIDA"])
        assert "True" in output

    def test_mensaje_vacio(self):
        output = run_program("s_parte1.py", [""])
        assert "True" not in output

    def test_mensaje_sin_letras(self):
        output = run_program("s_parte1.py", ["1234 !!"])
        assert "False" in output

    def test_s_unica_letra(self):
        output = run_program("s_parte1.py", ["s"])
        assert "True" in output

    def test_S_unica_letra_mayuscula(self):
        output = run_program("s_parte1.py", ["S"])
        assert "True" in output


class TestEncontrandoS_Parte2:

    def test_tres_mensajes_con_s(self):
        mensajes = [
            "Estoy bajo demasiada presión",
            "Voy a la reunión",
            "necesito ayuda",
            "Voy al baño",
            "todo bien por aquí",
            "Sin duda",
            "Voy a comer",
            "el clima hoy",
            "Reunión a mediodía",
            "Llegaré tarde",
        ]
        output = run_program("s_parte2.py", mensajes)
        assert '3/10 mensajes contenían la letra "s"' in output

    def test_ninguno_con_s(self):
        mensajes = [
            "Voy a la reunión", "Voy al baño", "todo bien",
            "el clima hoy", "Llegaré tarde", "Tengo una cita",
            "Voy a comer", "Hoy llueve", "La reunión fue bien", "Regrego pronto",
        ]
        output = run_program("s_parte2.py", mensajes)
        assert '0/10 mensajes contenían la letra "s"' in output

    def test_todos_con_s(self):
        output = run_program("s_parte2.py", ["sí"] * 10)
        assert '10/10 mensajes contenían la letra "s"' in output

    def test_solo_mayusculas_S(self):
        mensajes = [
            "SALIDA", "TRABAJO", "SISTEMA", "REUNIÓN", "SOL",
            "CAFÉ", "SILLA", "MESA", "LIBRO", "PUERTA",
        ]
        output = run_program("s_parte2.py", mensajes)
        assert '5/10 mensajes contenían la letra "s"' in output

    def test_imprime_10_booleanos(self):
        output = run_program("s_parte2.py", ["sí"] + ["no"] * 9)
        lines = [l.strip() for l in output.strip().splitlines() if l.strip()]
        bool_lines = [l for l in lines if l in ("True", "False")]
        assert len(bool_lines) == 10


# ─────────────────────────────────────────────
# Pregunta 3: Sumas Únicas
# ─────────────────────────────────────────────

class TestSumasUnicas:

    def test_ejemplo_1_positivos(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [0, 2, 4, 6]})
        result = sorted(ast.literal_eval(output.strip()))
        assert result == sorted([2, 4, 6, 8, 10])

    def test_ejemplo_2_mixtos(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [-1, 2, 5, -3]})
        result = sorted(ast.literal_eval(output.strip()))
        assert result == sorted([-4, -1, 1, 2, 4, 7])

    def test_dos_elementos(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [3, 7]})
        result = sorted(ast.literal_eval(output.strip()))
        assert result == [10]

    def test_solo_negativos(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [-1, -2, -3]})
        result = sorted(ast.literal_eval(output.strip()))
        assert result == sorted([-5, -4, -3])

    def test_con_cero(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [0, 1, 2]})
        result = sorted(ast.literal_eval(output.strip()))
        assert result == sorted([1, 2, 3])

    def test_sin_duplicados_en_resultado(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [0, 1, 2, 3]})
        result = ast.literal_eval(output.strip())
        assert len(result) == len(set(result))

    def test_duplicado_suma_aparece_una_vez(self):
        # 0+3=3 y 1+2=3, el 3 debe aparecer solo una vez
        output = run_program_with_vars("sumas_unicas.py", {"nums": [0, 1, 2, 3]})
        result = ast.literal_eval(output.strip())
        assert result.count(3) == 1

    def test_cinco_elementos(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [1, 2, 3, 4, 5]})
        result = sorted(ast.literal_eval(output.strip()))
        esperado = sorted(set(
            i + j for idx, i in enumerate([1, 2, 3, 4, 5]) for j in [1, 2, 3, 4, 5][idx + 1:]
        ))
        assert result == esperado

    def test_grandes_negativos_y_positivos(self):
        output = run_program_with_vars("sumas_unicas.py", {"nums": [-10, 0, 10]})
        result = sorted(ast.literal_eval(output.strip()))
        assert result == sorted([-10, 0, 10])


# ─────────────────────────────────────────────
# Pregunta 4: Cálculos de Ingeniería
# ─────────────────────────────────────────────

class TestTempValida:

    def test_entrada_valida_directa(self):
        output = run_program("temp_valida.py", ["76"])
        assert "Entrada válida." in output

    def test_entrada_valida_borde_inferior(self):
        output = run_program("temp_valida.py", ["55"])
        assert "Entrada válida." in output

    def test_entrada_valida_borde_superior(self):
        output = run_program("temp_valida.py", ["100"])
        assert "Entrada válida." in output

    def test_texto_invalido_luego_valido(self):
        output = run_program("temp_valida.py", ["hola", "76"])
        assert "Entrada inválida, intenta de nuevo." in output
        assert "Entrada válida." in output

    def test_fuera_de_rango_luego_valido(self):
        output = run_program("temp_valida.py", ["900", "76"])
        assert "Entrada inválida, intenta de nuevo." in output
        assert "Entrada válida." in output

    def test_multiples_invalidos_luego_valido(self):
        output = run_program("temp_valida.py", ["abc", "900", "-5", "80"])
        assert output.count("Entrada inválida, intenta de nuevo.") == 3
        assert "Entrada válida." in output

    def test_decimal_es_invalido(self):
        # "76.5" no es entero, isdecimal() lo rechaza por el punto
        output = run_program("temp_valida.py", ["76.5", "80"])
        assert "Entrada inválida, intenta de nuevo." in output
        assert "Entrada válida." in output

    def test_texto_con_numeros_es_invalido(self):
        # "76abc" no es decimal puro
        output = run_program("temp_valida.py", ["76abc", "80"])
        assert "Entrada inválida, intenta de nuevo." in output
        assert "Entrada válida." in output

    def test_borde_inferior_invalido(self):
        output = run_program("temp_valida.py", ["54", "55"])
        assert "Entrada inválida, intenta de nuevo." in output

    def test_borde_superior_invalido(self):
        output = run_program("temp_valida.py", ["101", "100"])
        assert "Entrada inválida, intenta de nuevo." in output

        
class TestPromedioSenales:

    def test_ejemplo_base(self):
        output = run_program_with_vars("promedio.py", {"signals": (3.3, 5.0, 4.2, 3.8)})
        assert float(output.strip()) == 4.075

    def test_valores_iguales(self):
        output = run_program_with_vars("promedio.py", {"signals": (5.0, 5.0, 5.0)})
        assert float(output.strip()) == 5.0

    def test_dos_elementos(self):
        output = run_program_with_vars("promedio.py", {"signals": (2.0, 4.0)})
        assert float(output.strip()) == 3.0

    def test_con_cero(self):
        output = run_program_with_vars("promedio.py", {"signals": (0.0, 10.0)})
        assert float(output.strip()) == 5.0

    def test_cinco_elementos(self):
        output = run_program_with_vars("promedio.py", {"signals": (1.0, 2.0, 3.0, 4.0, 5.0)})
        assert float(output.strip()) == 3.0


class TestRegistroMaterial:

    def test_ejemplo_acero(self):
        output = run_program_with_vars("registro_material.py", {"temp": 1200, "material": "Acero"})
        assert output.strip() == "Temperatura registrada: 1200 grados Celsius para el material: Acero"

    def test_ejemplo_aluminio(self):
        output = run_program_with_vars("registro_material.py", {"temp": 850, "material": "Aluminio"})
        assert output.strip() == "Temperatura registrada: 850 grados Celsius para el material: Aluminio"

    def test_temp_cero(self):
        output = run_program_with_vars("registro_material.py", {"temp": 0, "material": "Cobre"})
        assert output.strip() == "Temperatura registrada: 0 grados Celsius para el material: Cobre"

    def test_temp_negativa(self):
        output = run_program_with_vars("registro_material.py", {"temp": -40, "material": "Titanio"})
        assert output.strip() == "Temperatura registrada: -40 grados Celsius para el material: Titanio"

    def test_material_con_espacio(self):
        output = run_program_with_vars("registro_material.py", {"temp": 300, "material": "Acero inoxidable"})
        assert output.strip() == "Temperatura registrada: 300 grados Celsius para el material: Acero inoxidable"