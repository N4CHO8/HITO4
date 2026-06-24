import argparse

from src.rag import RagAssistant


def main() -> None:
    parser = argparse.ArgumentParser(description="Consulta el asistente RAG por consola.")
    parser.add_argument("question", help="Pregunta para el asistente.")
    args = parser.parse_args()

    assistant = RagAssistant()
    result = assistant.ask(args.question)
    print("\nRespuesta:\n")
    print(result["answer"])
    print("\nFuentes recuperadas:")
    for source in result["sources"]:
        print(f"- {source}")


if __name__ == "__main__":
    main()

