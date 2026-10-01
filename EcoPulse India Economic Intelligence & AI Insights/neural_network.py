"""
EcoPulse India Economic Intelligence
Neural Network using TensorFlow
"""

import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import tensorflow as tf
    from tensorflow.keras import layers, models, callbacks
    from tensorflow.keras.utils import to_categorical
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, LabelEncoder
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False

from helpers import setup_logging, load_data

logger = setup_logging()


if TF_AVAILABLE:

    class EconomicNN:
        """Deep neural network classifier for growth category."""

        def __init__(self):
            self.scaler = StandardScaler()
            self.encoder = LabelEncoder()
            self.model = None

        def build(self, input_dim, num_classes):
            """Construct feedforward network."""
            model = models.Sequential([
                layers.Input(shape=(input_dim,)),
                layers.Dense(128, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(64, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.2),
                layers.Dense(32, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(num_classes, activation='softmax')
            ])

            model.compile(
                optimizer=tf.keras.optimizers.Adam(0.001),
                loss='sparse_categorical_crossentropy',
                metrics=['accuracy']
            )
            return model

        def train(self, X, y, epochs=50, batch_size=32):
            """Train the neural network."""
            X_scaled = self.scaler.fit_transform(X)
            y_encoded = self.encoder.fit_transform(y)

            X_train, X_test, y_train, y_test = train_test_split(
                X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
            )

            num_classes = len(self.encoder.classes_)
            self.model = self.build(X_train.shape[1], num_classes)

            early_stop = callbacks.EarlyStopping(
                monitor='val_loss', patience=10, restore_best_weights=True
            )

            history = self.model.fit(
                X_train, y_train,
                epochs=epochs,
                batch_size=batch_size,
                validation_split=0.2,
                callbacks=[early_stop],
                verbose=0
            )

            loss, accuracy = self.model.evaluate(X_test, y_test, verbose=0)
            logger.info(f"NN Test Accuracy: {accuracy:.4f}")

            return history, accuracy

        def save_model(self, path='models/nn_model.h5'):
            """Save the neural network."""
            os.makedirs('models', exist_ok=True)
            self.model.save(path)
            logger.info(f"NN model saved: {path}")


def run_neural_network():
    """Execute neural network training."""
    if not TF_AVAILABLE:
        logger.warning("TensorFlow not available. Skipping NN.")
        return None

    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return None

    feature_cols = ['GDP', 'Employment', 'Exports', 'Imports',
                    'FDI', 'Inflation', 'Tax_Revenue']
    X = df[feature_cols].fillna(0).values
    y = df['Growth_Category'].fillna('Moderate').values

    nn = EconomicNN()
    history, accuracy = nn.train(X, y, epochs=50)

    print("\n" + "=" * 60)
    print("NEURAL NETWORK RESULTS")
    print("=" * 60)
    print(f"Test Accuracy: {accuracy:.4f}")

    nn.save_model()
    return accuracy


if __name__ == "__main__":
    run_neural_network()