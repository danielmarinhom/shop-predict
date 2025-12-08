import json
import sys
import tensorflow as tf
from tensorflow.keras.layers import Input, Embedding, Dense, Concatenate, Flatten, GlobalAveragePooling1D
from tensorflow.keras.models import Model


if len(sys.argv) > 1:
    input_data = json.loads(sys.argv[1])
else:
    with open('input_data.json') as f:
        input_data = json.load(f)

estado = input_data['estado'] 
genero = input_data['genero'] 
idade = input_data['idade'] 
compras = input_data['compras']
visualizacoes = input_data['visualizacoes']

num_estados = 27
num_generos = 3
num_produtos = 1000

estado_input = Input(shape=(1,), name='estado')
estado_embedding = Embedding(input_dim=num_estados, output_dim=10, name='estado_embedding')(estado_input)
estado_flatten = Flatten()(estado_embedding)

genero_input = Input(shape=(1,), name='genero')
genero_embedding = Embedding(input_dim=num_generos, output_dim=10, name='genero_embedding')(genero_input)
genero_flatten = Flatten()(genero_embedding)

idade_input = Input(shape=(1,), name='idade')

compras_input = Input(shape=(None, 1), name='compras')
compras_embedding = Embedding(input_dim=num_produtos, output_dim=32, name='compras_embedding')(compras_input)
compras_pooled = GlobalAveragePooling1D()(compras_embedding)

visualizacoes_input = Input(shape=(None,), name='visualizacoes')
visualizacoes_embedding = Embedding(input_dim=num_produtos, output_dim=32, name='visualizacoes_embedding')(visualizacoes_input)
visualizacoes_pooled = GlobalAveragePooling1D()(visualizacoes_embedding)

combined_inputs = Concatenate()([estado_flatten, genero_flatten, idade_input, compras_pooled, visualizacoes_pooled])

dense1 = Dense(128, activation='relu')(combined_inputs)
dense2 = Dense(64, activation='relu')(dense1)

output = Dense(num_produtos, activation='softmax', name='predicao')(dense2)

model = Model(inputs=[estado_input, genero_input, idade_input, compras_input, visualizacoes_input], outputs=output)

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()
predictions = model.predict({
    'estado': estado,
    'genero': genero,
    'idade': idade,
    'compras': compras,
    'visualizacoes': visualizacoes
})
top10_indices = tf.math.top_k(predictions, k=10).indices.numpy()
top_10_prob = tf.math.top_k(predictions, k=10).values.numpy()
print("produtos:", top10_indices)
print("probabilidades:", top_10_prob)

