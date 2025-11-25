from search import search

chain = search()

if not chain:
    print("Não foi possível iniciar o chat. Verifique os erros de inicialização.")
else:
    print("Chat iniciado! Faça sua pergunta ou digite 'sair' para terminar.")
    print("-" * 30)

    while True:
        try:
            question = input("Pergunta: ")
            if question.lower().strip() == 'sair':
                print("Encerrando o chat. Até logo!")
                break

            if not question:
                continue

            answer = chain.invoke(question)

            print(f"Resposta: {answer}")
            print("-" * 30)

        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando o chat. Até logo!")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")
            break