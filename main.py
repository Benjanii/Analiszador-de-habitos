from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE =Path("habits.csv")


def agregar_habito():
    fecha = input("Fecha YYYY-MM-DD" ).strip()
    ejercicio = input("¿Hiciste ejercicio? (s/n): ").lower()
    lectura = input("¿Cuantas paginas leíste?: ").strip()
    horas_sueno = input("¿Cuantas horas dormiste?: ").strip()
    agua = input("¿Tomaste al menos 2.5L de agua? (s/n): ").lower()
    consumo = input("¿Te medicaste? (s/n): ").lower()
    productividad = input("Productividad (1-10): ").strip()
    estado_animo = input("Estado de animo (1-10): ").strip()

    nuevo_habito = {
        "fecha": fecha,
        "ejercicio": ejercicio,
        "lectura": lectura,
        "horas_sueno": horas_sueno,
        "agua": agua,
        "consumo": consumo,
        "productividad": productividad,
        "estado_animo": int(estado_animo)
    }

    # Si el archivo existe, leerlo y agregar columnas si faltan
    try:
        df = pd.read_csv(CSV_FILE)
    except Exception:
        df = pd.DataFrame()
    for col in ["agua", "consumo", "productividad"]:
        if col not in df.columns:
            df[col] = None
    df = pd.concat([df, pd.DataFrame([nuevo_habito])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    print ("Habito agregado exitosamente.")
    
def grafico_animo() -> None:
    """Grafica el estado de ánimo por fecha."""
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No hay datos para graficar.")
        return

    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    plt.figure(figsize=(10, 5))
    plt.plot(df["fecha"], df["estado_animo"], marker="o")
    plt.title("Estado de ánimo por fecha")
    plt.xlabel("Fecha")
    plt.ylabel("Estado de ánimo")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def graficos_ejercicio_lectura():
    """Genera gráficos y estadísticas de ejercicio, lectura y estado de ánimo por mes y día."""
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No hay datos para analizar.")
        return
    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    # Estado de ánimo
    plt.figure(figsize=(10, 5))
    plt.plot(df["fecha"], df["estado_animo"], marker="o")
    plt.title("Estado de ánimo por fecha")
    plt.xlabel("Fecha")
    plt.ylabel("Estado de ánimo")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # EJERCICIO
    df_ej = df.copy()
    df_ej["ejercicio"] = df_ej["ejercicio"].str.lower().map({"s": 1, "n": 0})
    df_ej["mes"] = df_ej["fecha"].dt.to_period("M")
    mes_actual = pd.Timestamp.now().to_period("M")
    df_mes = df_ej[df_ej["mes"] == mes_actual]
    total_dias_mes = df_mes.shape[0]
    dias_ejercicio = df_mes["ejercicio"].sum()
    porcentaje_ejercicio = (dias_ejercicio / total_dias_mes * 100) if total_dias_mes > 0 else 0
    print(f"\nPorcentaje de días con ejercicio este mes: {porcentaje_ejercicio:.2f}%")

    # Probabilidad de hacer ejercicio hoy (basado en historial del mismo día de la semana)
    hoy = pd.Timestamp.now()
    dia_semana = hoy.dayofweek
    df_ej["dia_semana"] = df_ej["fecha"].dt.dayofweek
    historial_dia = df_ej[df_ej["dia_semana"] == dia_semana]
    prob_ejercicio = historial_dia["ejercicio"].mean() if not historial_dia.empty else 0
    print(f"Probabilidad de hacer ejercicio hoy ({hoy.strftime('%A')}): {prob_ejercicio*100:.2f}%")

    # Gráfico de ejercicio mensual
    plt.figure(figsize=(8,4))
    df_ej.groupby("mes")["ejercicio"].mean().plot(kind="bar", color="skyblue")
    plt.title("Porcentaje de días con ejercicio por mes")
    plt.ylabel("Porcentaje de ejercicio")
    plt.xlabel("Mes")
    plt.ylim(0,1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # LECTURA
    df["lectura"] = pd.to_numeric(df["lectura"], errors="coerce")
    df["mes"] = df["fecha"].dt.to_period("M")
    df["dia_semana"] = df["fecha"].dt.dayofweek
    df_mes_lectura = df[df["mes"] == mes_actual]
    total_dias_lectura = df_mes_lectura.shape[0]
    dias_leyendo = df_mes_lectura[df_mes_lectura["lectura"] > 0].shape[0]
    porcentaje_lectura = (dias_leyendo / total_dias_lectura * 100) if total_dias_lectura > 0 else 0
    print(f"\nPorcentaje de días con lectura este mes: {porcentaje_lectura:.2f}%")

    # Probabilidad de leer hoy (basado en historial del mismo día de la semana)
    historial_lectura = df[(df["dia_semana"] == dia_semana)]
    prob_lectura = (historial_lectura["lectura"] > 0).mean() if not historial_lectura.empty else 0
    print(f"Probabilidad de leer hoy ({hoy.strftime('%A')}): {prob_lectura*100:.2f}%")

    # Gráfico de días con lectura por mes
    plt.figure(figsize=(8,4))
    df.groupby("mes")["lectura"].apply(lambda x: (x>0).mean()).plot(kind="bar", color="orange")
    plt.title("Porcentaje de días con lectura por mes")
    plt.ylabel("Porcentaje de lectura")
    plt.xlabel("Mes")
    plt.ylim(0,1)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # AGUA
    if "agua" in df.columns:
        df["agua"] = df["agua"].str.lower().map({"s": 1, "n": 0})
        df_mes_agua = df[df["mes"] == mes_actual]
        total_dias_agua = df_mes_agua.shape[0]
        dias_agua = df_mes_agua[df_mes_agua["agua"] == 1].shape[0]
        porcentaje_agua = (dias_agua / total_dias_agua * 100) if total_dias_agua > 0 else 0
        print(f"\nPorcentaje de días con 2.5L de agua este mes: {porcentaje_agua:.2f}%")
        historial_agua = df[(df["dia_semana"] == dia_semana)]
        prob_agua = historial_agua["agua"].mean() if not historial_agua.empty else 0
        print(f"Probabilidad de tomar 2.5L de agua hoy ({hoy.strftime('%A')}): {prob_agua*100:.2f}%")
        plt.figure(figsize=(8,4))
        df.groupby("mes")["agua"].mean().plot(kind="bar", color="deepskyblue")
        plt.title("Porcentaje de días con 2.5L de agua por mes")
        plt.ylabel("Porcentaje de agua")
        plt.xlabel("Mes")
        plt.ylim(0,1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # CONSUMO
    if "consumo" in df.columns:
        df["consumo"] = df["consumo"].str.lower().map({"s": 1, "n": 0})
        df_mes_consumo = df[df["mes"] == mes_actual]
        total_dias_consumo = df_mes_consumo.shape[0]
        dias_consumo = df_mes_consumo[df_mes_consumo["consumo"] == 1].shape[0]
        porcentaje_consumo = (dias_consumo / total_dias_consumo * 100) if total_dias_consumo > 0 else 0
        print(f"\nPorcentaje de días con consumo este mes: {porcentaje_consumo:.2f}%")
        historial_consumo = df[(df["dia_semana"] == dia_semana)]
        prob_consumo = historial_consumo["consumo"].mean() if not historial_consumo.empty else 0
        print(f"Probabilidad de consumo hoy ({hoy.strftime('%A')}): {prob_consumo*100:.2f}%")
        plt.figure(figsize=(8,4))
        df.groupby("mes")["consumo"].mean().plot(kind="bar", color="red")
        plt.title("Porcentaje de días con consumo por mes")
        plt.ylabel("Porcentaje de consumo")
        plt.xlabel("Mes")
        plt.ylim(0,1)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # PRODUCTIVIDAD
    if "productividad" in df.columns:
        df["productividad"] = pd.to_numeric(df["productividad"], errors="coerce")
        plt.figure(figsize=(10, 5))
        plt.plot(df["fecha"], df["productividad"], marker="o", color="green")
        plt.title("Productividad por fecha")
        plt.xlabel("Fecha")
        plt.ylabel("Productividad (1-10)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        # Probabilidad de alta productividad (>=8)
        historial_prod = df[(df["dia_semana"] == dia_semana)]
        prob_prod = (historial_prod["productividad"] >= 8).mean() if not historial_prod.empty else 0
        print(f"Probabilidad de productividad alta hoy ({hoy.strftime('%A')}): {prob_prod*100:.2f}%")

    # HORAS DE SUEÑO
    df["horas_sueno"] = pd.to_numeric(df["horas_sueno"], errors="coerce")
    plt.figure(figsize=(10, 5))
    plt.plot(df["fecha"], df["horas_sueno"], marker="o", color="purple")
    plt.title("Horas de sueño por fecha")
    plt.xlabel("Fecha")
    plt.ylabel("Horas de sueño")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def ver_habitos():
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No hay hábitos registrados.")
        return
    print(df)

def mostrar_resumen() -> None:
    #Muestra estadísticas de los hábitos.
    df = pd.read_csv(CSV_FILE)
    df.columns = df.columns.str.strip()
    df["lectura"] = pd.to_numeric(df["lectura"], errors="coerce")
    df["horas_sueno"] = pd.to_numeric(df["horas_sueno"], errors="coerce")
    df["estado_animo"] = pd.to_numeric(df["estado_animo"], errors="coerce")
    print("Columnas en el CSV:", df.columns.tolist())# <-- línea para depurar
    if df.empty:
        print("No hay datos para analizar.")
        return

    total_registros = len(df)
    dias_con_ejercicio = len(df[df["ejercicio"] == "s"])
    dias_sin_ejercicio = len(df[df["ejercicio"] == "n"])
    promedio_lectura = df["lectura"].mean()
    promedio_sueno = df["horas_sueno"].mean()
    promedio_animo = df["estado_animo"].mean()

    print("\n=== RESUMEN ===")
    print(f"Total de registros: {total_registros}")
    print(f"Días con ejercicio: {dias_con_ejercicio}")
    print(f"Días sin ejercicio: {dias_sin_ejercicio}")
    print(f"Promedio de páginas leídas: {promedio_lectura:.2f}")
    print(f"Promedio de horas de sueño: {promedio_sueno:.2f}")
    print(f"Promedio de estado de ánimo: {promedio_animo:.2f}")

def editar_habito():
    df = pd.read_csv(CSV_FILE)
    df.columns = df.columns.str.strip()

    if df.empty:
        print("No hay hábitos registrados para editar.")
        return

    print("\n=== Hábitos registrados ===")
    print(df)

    try:
        idx = int(input("\nIngresa el índice del hábito que quieres editar: "))
        if idx not in df.index:
            print("Índice inválido.")
            return
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return

    # Columnas que se pueden editar (todas menos 'ejercicio')
    columnas_editables = [col for col in df.columns]

    print("\nColumnas que puedes editar:")
    for i, col in enumerate(columnas_editables):
        print(f"{i + 1}. {col} (valor actual: {df.at[idx, col]})")

    try:
        col_opcion = int(input("Selecciona la columna que quieres editar (número): "))
        if not 1 <= col_opcion <= len(columnas_editables):
            print("Opción inválida.")
            return
    except ValueError:
        print("Por favor, ingresa un número válido.")
        return

    columna_seleccionada = columnas_editables[col_opcion - 1]
    nuevo_valor = input(f"Ingresa el nuevo valor para '{columna_seleccionada}': ").strip()

    # Actualizar el valor en el DataFrame
    df.at[idx, columna_seleccionada] = nuevo_valor

    # Guardar cambios en el CSV
    df.to_csv(CSV_FILE, index=False)
    print(f"Registro actualizado correctamente en la columna '{columna_seleccionada}'.")
#_______________________________________________________________________________________________________
def main():
    while True:

        print("\n1. Agregar hábito")
        print("2. Ver hábitos")
        print("3. Ver resumen de habitos")
        print("4. Editar hábito")
        print("5. Gráficos y estadísticas (ánimo, ejercicio, lectura y sueño)")
        print("6. Salir")


        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            agregar_habito()
        elif opcion == "2":
            ver_habitos()
        elif opcion == "3":
            mostrar_resumen()
        elif opcion == "4":
            editar_habito()
        elif opcion == "5":
            graficos_ejercicio_lectura()
        elif opcion == "6":
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            
if __name__ == "__main__":
    main()
    
