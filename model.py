import json
import sys
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Concatenate, Flatten, GlobalAveragePooling1D
from tensorflow.keras.models import Model



# Ler os dados de entrada do JSON passado como argumento ou de um arquivo local
if len(sys.argv) > 1:
    input_data = json.loads(sys.argv[1])
else:
    with open('input_data.json') as f:
        input_data = json.load(f)

estado = input_data['estado']  # Exemplo: estado codificado
genero = input_data['genero']  # Exemplo: gênero codificado (0: M, 1: F, 2: N)
idade = input_data['idade']    # Exemplo: idade do usuário
compras = input_data['compras']  # Histórico de compras (N produtos)
visualizacoes = input_data['visualizacoes']  # Histórico de visualizações (N produtos)

# número de estados (assumindo 27 estados do Brasil)
num_estados = 27
num_generos = 3
num_produtos = 1000

# Entrada para o estado
estado_input = Input(shape=(1,), name='estado')
# Embedding para transformar o estado em uma representação densa
estado_embedding = Embedding(input_dim=num_estados, output_dim=10, name='estado_embedding')(estado_input)
estado_flatten = Flatten()(estado_embedding)

# Embedding para o gênero (3 categorias: Masculino - M, Feminino - F, Não-binário - N)
genero_input = Input(shape=(1,), name='genero')
genero_embedding = Embedding(input_dim=num_generos, output_dim=10, name='genero_embedding')(genero_input)
genero_flatten = Flatten()(genero_embedding)

# Input para a idade (contínuo, sem embedding)
idade_input = Input(shape=(1,), name='idade')

compras_input = Input(shape=(None, 1), name='compras')
compras_embedding = Embedding(input_dim=num_produtos, output_dim=32, name='compras_embedding')(compras_input)
compras_pooled = GlobalAveragePooling1D()(compras_embedding)

visualizacoes_input = Input(shape=(None,), name='visualizacoes')
visualizacoes_embedding = Embedding(input_dim=num_produtos, output_dim=32, name='visualizacoes_embedding')(visualizacoes_input)
visualizacoes_pooled = GlobalAveragePooling1D()(visualizacoes_embedding)

# Combinar todas as entradas processadas
combined_inputs = Concatenate()([estado_flatten, genero_flatten, idade_input, compras_pooled, visualizacoes_pooled])

# Camadas densas subsequentes para processar as combinações
dense1 = Dense(128, activation='relu')(combined_inputs)
dense2 = Dense(64, activation='relu')(dense1)

# Camada de saída (100 produtos no catálogo, predição com softmax)
output = Dense(num_produtos, activation='softmax', name='predicao')(dense2)

# Definir o modelo completo
model = Model(inputs=[estado_input, genero_input, idade_input, compras_input, visualizacoes_input], outputs=output)

# Compilar o modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Exibir o resumo do modelo
model.summary()

# Exemplo de dados para previsão, retirados do JSON

# Fazer a previsão com base nos dados fornecidos
predictions = model.predict({
    'estado': estado,
    'genero': genero,
    'idade': idade,
    'compras': compras,
    'visualizacoes': visualizacoes
})
top10_indices = tf.math.top_k(predictions, k=10).indices.numpy()
top_10_prob = tf.math.top_k(predictions, k=10).values.numpy()
# Imprimir a predição dos produtos recomendados
print("Top 10 produtos recomendados (ID):", top10_indices)
print("Top 10 probabilidades:", top_10_prob)
