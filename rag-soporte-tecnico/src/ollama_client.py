import requests


class OllamaClient:
    def __init__(self, base_url: str, embedding_model: str, llm_model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.embedding_model = embedding_model
        self.llm_model = llm_model

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings: list[list[float]] = []
        for text in texts:
            embeddings.append(self.embed_one(text))
        return embeddings

    def embed_one(self, text: str) -> list[float]:
        url = f"{self.base_url}/api/embed"
        response = requests.post(
            url,
            json={"model": self.embedding_model, "input": text},
            timeout=120,
        )
        if response.status_code == 404:
            return self._embed_one_legacy(text)
        response.raise_for_status()
        data = response.json()
        if "embeddings" in data:
            return data["embeddings"][0]
        if "embedding" in data:
            return data["embedding"]
        raise RuntimeError(f"Respuesta de embeddings no reconocida: {data}")

    def _embed_one_legacy(self, text: str) -> list[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.embedding_model, "prompt": text},
            timeout=120,
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def generate_answer(self, prompt: str) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.llm_model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0.2},
            },
            timeout=180,
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"].strip()

