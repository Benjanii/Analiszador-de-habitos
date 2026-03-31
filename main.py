from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE =Path("habits.csv")


def agregar_habito():
    fecha = input("Fecha YYYY-MM-DD" ).strip()
    ejercicio = input("¿Hiciste ejercicio? (s/n:) ").lower()
    lectura = input("¿Cuantas paginas leíste?: ").strip()
    horas_sueno = input("¿Cuantas horas dormiste?: ").strip()
    estado_animo = input("Estado de animo (1-10): ").strip()
    
    nuevo_habito = {
        "fecha": fecha,
        "ejercicio": ejercicio,
        "lectura": (lectura),
        "horas_sueno": (horas_sueno),
        "estado_animo": int(estado_animo)
    }
    
    df = pd.read_csv(CSV_FILE)
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
    promedio_lectura = df["lectura"].mean()
    promedio_sueno = df["horas_sueno"].mean()
    promedio_animo = df["estado_animo"].mean()

    print("\n=== RESUMEN ===")
    print(f"Total de registros: {total_registros}")
    print(f"Días con ejercicio: {dias_con_ejercicio}")
    print(f"Promedio de páginas leídas: {promedio_lectura:.2f}")
    print(f"Promedio de horas de sueño: {promedio_sueno:.2f}")
    print(f"Promedio de estado de ánimo: {promedio_animo:.2f}")

def editar_habito():
    import pandas as pd

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

def main():
    while True:
        print("\n1. Agregar hábito")
        print("2. Ver hábitos")
        print("3. Ver resumen de habitos")
        print("4. Ver gráfico de estado de ánimo")
        print("5. Editar hábito")
        print("6. Salir")
        
        opcion = input("Selecciona una opción: ")
        
        if opcion == "1":
            agregar_habito()
        elif opcion == "2":
            ver_habitos()
        elif opcion == "3":
            mostrar_resumen()
            break
        elif opcion == "4":
            grafico_animo()
        elif opcion == "5":
            editar_habito()
        elif opcion == "6":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            
if __name__ == "__main__":
    main()
    
