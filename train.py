from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

if __name__ == '__main__':
    file_name = "input.txt"

    train_tokenizer(file_name)
    tokenizer_file = "aitextgen.tokenizer.json"

    config = GPT2ConfigCPU()

    print("\nInstantiate aitextgen")
    ai = aitextgen(tokenizer_file=tokenizer_file, config=config)

    print("\nToken Dataset")
    data = TokenDataset(file_name, tokenizer_file=tokenizer_file, block_size=64)

    print("\nTrain")
    ai.train(data, batch_size=8, num_steps=100000, generate_every=5000, save_every=5000)

    print("\nGenerate")
    ai.generate()
