import argparse

from src.rag import RagAssistant


def main() -> None:
    parser = argparse.ArgumentParser(description="Indexa documentos para el asistente RAG.")
    parser.add_argument("--docs", default="docs", help="Directorio con PDF, TXT o Markdown.")
    parser.add_argument("--reset", action="store_true", help="Recrear la coleccion vectorial.")
    args = parser.parse_args()

    assistant = RagAssistant()
    total = assistant.ingest(args.docs, reset=args.reset)
    print(f"Documentos indexados correctamente. Chunks generados: {total}")
    print(f"Total almacenado en FAISS: {assistant.store.count()}")


if __name__ == "__main__":
    main()
