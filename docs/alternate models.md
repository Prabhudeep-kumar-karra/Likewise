# Alternate Models

## Candidates

Use the same labeled span data, split, seed, sequence length, batch size, learning rate, and epoch count for each run:

| Candidate | Backbone name | Main trade-off |
| --- | --- | --- |
| DeBERTa-v3-large | `deberta-v3-large` | Strong token-classification benchmark; 512-token context requires chunking for long filings. |
| Ettin-encoder-400M | `ettin-encoder-400m` | Long context and public training-data provenance; benchmark performance is close to ModernBERT. |
| ModernBERT-large | `modernbert-large` | Long-context control for measuring the value of CaseLawModernBERT domain adaptation. |

The reported generic NER benchmarks are not results on this project. Compare assertion precision, coverage, and guard-case behavior on held-out legal text, in addition to token precision, recall, and F1.

## Install the isolated runtime

These dependencies are intentionally separate from the serving environment. From the repository root on macOS:

```sh
python3 -m venv .venv-extract
.venv-extract/bin/python -m pip install --upgrade pip
.venv-extract/bin/python -m pip install -r extract/requirements.txt
```

PyTorch, Transformers, tokenizers, and safetensors are installed into `.venv-extract`; they are not added to the application's runtime dependencies. The first training run downloads the selected backbone weights from Hugging Face. Each candidate is a large model, so run candidates one at a time and allow several GB of disk space for cached weights and training outputs.

## Run the matched comparison

The training data must be JSONL with one token sequence and BIO label sequence per record:

```json
{"id":"example-001","tokens":["The","court","found","..."],"labels":["O","O","O"]}
```

Keep the training and held-out evaluation files fixed across every run. Example commands (replace the paths with the prepared, identical split):

```sh
.venv-extract/bin/python tools/train_extractor.py \
  --train spans.train.jsonl --eval spans.eval.jsonl \
  --out runs/deberta-v3-large --backbone deberta-v3-large --seed 20260909

.venv-extract/bin/python tools/train_extractor.py \
  --train spans.train.jsonl --eval spans.eval.jsonl \
  --out runs/ettin-encoder-400m --backbone ettin-encoder-400m --seed 20260909

.venv-extract/bin/python tools/train_extractor.py \
  --train spans.train.jsonl --eval spans.eval.jsonl \
  --out runs/modernbert-large --backbone modernbert-large --seed 20260909
```

The trainer prints token precision, recall, and F1 after each run. For a fair model decision, also run each saved checkpoint through the same calibrated extraction and round-trip evaluation, with evaluation styles held out from training. Do not choose a model by token F1 alone: the operational target is high precision at useful coverage, with no assertions on guard records.

## Current data limitation

No labeled legal-prose span train/evaluation JSONL files are currently present in this workspace. The example filings and HMDA tables are not substitutes for adjudicated BIO labels. Until those files are prepared, these commands install and document the experiment but cannot produce a meaningful three-model comparison.
