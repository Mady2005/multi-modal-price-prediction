from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments

import pandas as pd

# 1. Prepare Data
df = pd.read_csv('train.csv')
dataset = Dataset.from_pandas(df[['catalog_content', 'price']])
dataset = dataset.train_test_split(test_size=0.2)

# 2. Tokenizer
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
def tokenize_function(examples):
    return tokenizer(examples["catalog_content"], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# 3. Model (Num_labels=1 means Regression!)
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=1)

# 4. Training Args
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
)

# 5. Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
)

trainer.train()
model.save_pretrained("./fine_tuned_price_model")