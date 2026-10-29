# Estado atual do laboratório OCR

Revisão: 13/10/2026. Git inicial limpo. Última etapa comprovada: inspeção estática de CLI, processamento e métricas. Nenhuma imagem pessoal foi lida, nenhum OCR/teste foi executado.

## Componentes e regras observadas

[cli.py](../ocr_lab/cli.py) recebe caminho da imagem, `--lang` (padrão `eng`) e `--tesseract-cmd`, também obtido de `TESSERACT_CMD`; chama `extract_text`. [preprocess.py](../ocr_lab/preprocess.py) lê com OpenCV, sinaliza arquivo não carregável, converte BGR para cinza, redimensiona (padrão 2x), aplica mediana 3 e limiar Otsu. Escala deve ser positiva.

[metrics.py](../ocr_lab/metrics.py) calcula distância de edição, erros de caracteres/palavras e igualdade normalizada. `normalize_text` usa apenas `[a-z0-9 ]`; letras acentuadas não são preservadas. Isso é comportamento observado, não definição universal de qualidade em português. Não se transcreveram valores de benchmark como resultado desta revisão.

## Operação existente

A fonte é o [README](../README.md): ambiente Python, `python -m pip install -r requirements.txt`, Tesseract local e idioma `por` para OCR em português, `python -m ocr_lab.cli sample_images/sample-text.pbm --lang eng`, `pytest` e `python scripts/run_demo_benchmark.py`. Todos: **não executado nesta tarefa**. A suíte é documentada como processamento sem necessidade do binário; OCR real depende dele. [requirements.txt](../requirements.txt) declara numpy, OpenCV headless, Pillow, pytesseract e pytest.

## Plano e lacunas

Não foi identificado roadmap aprovado ou decisão histórica adicional. Sugestões: (1) confirmar se a normalização de métricas é adequada ao conjunto português; (2) revisar suíte e benchmark sintético quando autorizado; (3) registrar versão/idiomas do Tesseract efetivamente usados. Presença de screenshots e CI não certifica execução atual.

[Índice](INDEX.md).
