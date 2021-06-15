from  aitextgen import aitextgen

u_input = ''
ai2 = aitextgen(model_folder="trained_model",
                    tokenizer_file="aitextgen.tokenizer.json")


while u_input != '0':
    print(ai2.generate_one(temperature=2., max_length=400, prompt=f'{u_input}',
                       repetition_penalty=3., length_penalty=2., num_beams=500))
    u_input = input(">>> ")
