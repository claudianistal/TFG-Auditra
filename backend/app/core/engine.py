class ForensicEngine:
    def __init__(self):
        # Aquí puedes cargar tus estrategias (podrías leerlas del JSON)
        self.strategies = [
            PaddingStrategy("Análisis de Padding", 30),
            # MetadataStrategy("Metadatos Críticos", 50),
        ]

    def analyze_file(self, file_path: str):
        results = []
        total_score = 0
        
        for strategy in self.strategies:
            res = strategy.run(file_path)
            results.append(res)
            total_score += res["score_impact"]
            
        return {"total_score": total_score, "details": results}