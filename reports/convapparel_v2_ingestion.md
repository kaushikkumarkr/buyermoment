# ConvApparel V2 status

The official Google ConvApparel dataset card currently exposes both `ConvApparel.zip` and `ConvApparel_V2.zip` and declares CC BY 4.0. The repository now archives and normalizes V2 separately: `3,534` conversations and `141,168` turn-recommendation rows. V1 remains `4,146` conversations, `14,736` turns, and `175,751` turn-recommendation rows.

V2 is evaluation-only and is not mixed into the CCB-1 v0.1 train/validation/hidden split. The rights registry marks V2 `REVIEW_REQUIRED` because it is human conversation data and the current card/publication/version terms must be reconciled before training or commercial reuse. No V2 performance metrics are claimed yet; ingestion is the durable asset in this checkpoint.

Archive SHA-256: `14001121fa81149ae20cc5b2aa962b5e5077af55b3ac14657211007b75ca8fa4`.

Source: <https://huggingface.co/datasets/google/ConvApparel>. The V1 checksum is preserved in `data/ccb1/source_manifest.json`.
