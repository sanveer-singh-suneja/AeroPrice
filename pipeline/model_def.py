import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.applications import ResNet50

def build_multimodal_model(num_tab_features: int = 0) -> tf.keras.Model:
    """Satellite image → price model (optional numeric features)."""

    # Image branch
    image_input = layers.Input(shape=(128, 128, 3), name="image_input")
    resnet = ResNet50(include_top=False, weights="imagenet", input_shape=(128, 128, 3))
    resnet._name = "resnet_backbone"
    resnet.trainable = False
    x_img = resnet(image_input)
    x_img = layers.Flatten()(x_img)
    x_img = layers.Dense(256, activation='relu')(x_img)
    x_img = layers.Dropout(0.3)(x_img)
    x_img = layers.BatchNormalization()(x_img)

    # Numeric branch (optional)
    if num_tab_features > 0:
        tabular_input = layers.Input(shape=(num_tab_features,), name="tabular_input")
        x_num = layers.Dense(128, activation='relu')(tabular_input)
        x_num = layers.Dropout(0.2)(x_num)
        x_num = layers.BatchNormalization()(x_num)
        fused = layers.Concatenate()([x_img, x_num])
        inputs = [image_input, tabular_input]
    else:
        fused = x_img
        inputs = image_input

    fused = layers.Dense(128, activation='relu')(fused)
    fused = layers.Dropout(0.3)(fused)
    output = layers.Dense(1, activation='linear', name='price')(fused)

    model = Model(inputs=inputs, outputs=output, name='satellite_price_model')
    model.compile(optimizer=tf.keras.optimizers.Adam(), loss='mse', metrics=['mae'])
    return model
