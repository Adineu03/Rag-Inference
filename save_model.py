import tensorflow as tf

class SimpleModel(tf.keras.Model):
    def __init__(self):
        super(SimpleModel,self).__init__()
        self.dense = tf.keras.layers.Dense(10)

    def call(self, inputs):
        return self.dense(inputs)
    
model = SimpleModel()
model.build(input_shape=(None, 10))

tf.saved_model.save(model, "model")