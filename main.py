from pathlib import Path
import pandas as pd

CSV_FILE =Path("habits.csv")

def archivo_existente() -> None:
    if not CSV_FILE.exists():
        print("El archivo no existe. Creando uno nuevo...")
        df = pd.DataFrame(columns=["fecha", "ejercicio", "lectura", "horas_sueno", "estado_animo"])
        df.to_csv(CSV_FILE, index=False)

def agregar_habito():
    fecha = input("Fecha YYYY-MM-DD").strip()
    ejercicio = input("¿Hiciste ejercicio? (sí/no)").strip()
    lectura = input("¿Cuantas paginas leíste?").strip()
    horas_sueno = input("¿Cuantas horas dormiste? (sí/no)").strip()
    estado_animo = input("Estado de animo (1-10)").strip()
    
    nuevo_habito = {
        "fecha": fecha,
        "ejercicio": ejercicio,
        "lectura": int(lectura),
        "horas_sueno": float(horas_sueno),
        "estado_animo": int(estado_animo)
    }
    
    df = pd.read_csv(CSV_FILE)
    df = df.concat([df, pd.DataFrame([nuevo_habito])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    
    print ("Habito agregado exitosamente.")

def ver_habitos():
    df = pd.read_csv(CSV_FILE)
    if df.empty:
        print("No hay hábitos registrados.")
        return
    print(df)

def main():
    archivo_existente()
    
    while True:
        print("\n1. Agregar hábito")
        print("2. Ver hábitos")
        print("3. Salir")
        
        opcion = input("Selecciona una opción: ").strip()
        
        if opcion == "1":
            agregar_habito()
        elif opcion == "2":
            ver_habitos()
        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")
            
if __name__ == "__main__":
    main()