from crew import OrionCrew

if __name__ == "__main__":
    orion = OrionCrew()

    result = orion.run("Preciso mandar um e-mail para o professor agradecendo pela orientação do TCC.")

    print("\n===== RESULTADO FINAL =====\n")
    print(result)
