from datasets import load_dataset
from transformers import BartTokenizer, BartForSequenceClassification
from transformers import TrainingArguments, Trainer, DataCollatorWithPadding

def tokenize_function(examples):
  return tokenizer(examples['cleaned_reviews'], padding='max_length', truncation=True)

dataset = load_dataset('csv', data_files={'train':'training_data.csv'})

model_name = 'facebook/bart-large-mnli'
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForSequenceClassification.from_pretrained(model_name, num_labels=4, problem_type="multi_label_classification", ignore_mismatched_sizes=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

trainin_args = TrainingArguments(
  output_dir='./result',
  evaluation_strategy='no',
  learning_rate=2e-5,
  per_device_eval_batch_size=16,
  num_train_epochs=3,
  weight_decay=0.01
)

data_collator = DataCollatorWithPadding(tokenizer=tokenizer)

trainer = Trainer(
  model = model,
  args = trainin_args,
  train_dataset = tokenized_datasets['train'],
  tokenizer = tokenizer,
  data_collator = data_collator
)

trainer.train()
trainer.evaluate()

model.save_pretrained('./fine-tuned-model')
tokenizer.save_pretrained('./fine-tuned-model')