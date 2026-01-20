import numpy as np
import random
import torch
import torch.backends.cudnn as cudnn
from transformers import BertTokenizer, WordpieceTokenizer
from .xbert import BertConfig, BertForMaskedLM
import torch.nn as nn
from rdkit import Chem
from peft import get_peft_model, LoraConfig, TaskType
from aromma.paths import SPMM_DIR


class SPMM(nn.Module):
    def __init__(self, r=4, lora_alpha=8):
        super().__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        seed = 42
        torch.manual_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        cudnn.benchmark = True
        
        self.tokenizer = BertTokenizer(
            vocab_file=str(SPMM_DIR / "vocab_bpe_300.txt"),
            do_lower_case=False,
            do_basic_tokenize=False,
        )
        self.tokenizer.wordpiece_tokenizer = WordpieceTokenizer(
            vocab=self.tokenizer.vocab,
            unk_token=self.tokenizer.unk_token,
            max_input_chars_per_word=250,
        )

        bert_config = BertConfig.from_json_file(str(SPMM_DIR / "config_bert.json"))
        self.text_encoder = BertForMaskedLM(config=bert_config)
        for i in range(bert_config.fusion_layer, bert_config.num_hidden_layers):
            self.text_encoder.bert.encoder.layer[i] = nn.Identity()
        self.text_encoder.cls = nn.Identity()

        lora_config = LoraConfig(
            r=r,
            lora_alpha=lora_alpha,
            target_modules=["query", "key", "value"],
            task_type=TaskType.SEQ_CLS
        )
        self.text_encoder = get_peft_model(self.text_encoder, lora_config)
        self.to(self.device)

        self.output_dim = 768

    def tokenize(self, smiles):
        smiles = ["[CLS]" + Chem.MolToSmiles(
                    Chem.MolFromSmiles(s),
                    isomericSmiles=False,
                    canonical=True,
                ) for s in smiles]

        tok = self.tokenizer(
                smiles,
                padding="longest",
                truncation=True,
                max_length=100,
                return_tensors="pt",
            ).to(self.device)
        
        return tok
    
    def forward(self, smiles):
        tok = self.tokenize(smiles)
        logits = self.text_encoder.bert(
            tok.input_ids[:, 1:],
            attention_mask=tok.attention_mask[:, 1:],
            return_dict=True,
            mode="text",
        ).last_hidden_state[:, 0, :]
        return logits
