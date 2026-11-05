# Alternate Model Comparison

## Matched Pilot Results

English WikiANN named-entity recognition pilot. All three runs used the same fixed sample and recipe.

| Model | Precision | Recall | F1 | Validation loss |
|:--|--:|--:|--:|--:|
| ModernBERT-large | 0.301 | 0.256 | **0.277** | 1.206 |
| Ettin-encoder-400M | 0.238 | 0.147 | 0.181 | 1.398 |
| DeBERTa-v3-large | 0.283 | 0.078 | 0.122 | 1.346 |

## Run Settings

| Setting | Value |
|:--|:--|
| Training sample | 240 sentences |
| Validation sample | 120 sentences |
| Epochs | 1 |
| Batch size | 8 |
| Maximum sequence length | 128 tokens |
| Learning rate | 1e-5 |
| Random seed | 20261022 |
| Weight precision | float32 |

## Interpretation

ModernBERT had the highest F1 and recall in this pilot. DeBERTa's precision was close to ModernBERT's, but its recall was substantially lower. All validation losses were finite after loading every backbone in float32.

The dataset is Wikipedia text, the sample is small, and training lasted one epoch. These metrics do not establish performance on Likewise fields, legal prose, negation, attribution, hedging, assertion precision, or coverage.

**This is a small general-NER pilot. The dataset card does not declare a license and these score are not an official benchmark results.**