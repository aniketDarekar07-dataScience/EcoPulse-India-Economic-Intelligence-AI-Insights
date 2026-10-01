"""
EcoPulse India Economic Intelligence
LSTM Forecaster using PyTorch
"""

import pandas as pd
import numpy as np
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import torch
    import torch.nn as nn
    from sklearn.preprocessing import MinMaxScaler
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

from helpers import setup_logging, load_data

logger = setup_logging()


if TORCH_AVAILABLE:

    class GDPForecaster(nn.Module):
        """LSTM network for time-series GDP forecasting."""

        def __init__(self, input_size=1, hidden_size=64, num_layers=2, dropout=0.2):
            super().__init__()
            self.hidden_size = hidden_size
            self.num_layers = num_layers

            self.lstm = nn.LSTM(
                input_size=input_size,
                hidden_size=hidden_size,
                num_layers=num_layers,
                batch_first=True,
                dropout=dropout
            )
            self.fc = nn.Linear(hidden_size, 1)

        def forward(self, x):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            out, _ = self.lstm(x, (h0, c0))
            return self.fc(out[:, -1, :])


class TimeSeriesForecaster:
    """Complete training and prediction pipeline for GDP."""

    def __init__(self, sequence_length=3):
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch not installed")
        self.sequence_length = sequence_length
        self.scaler = MinMaxScaler()
        self.model = None

    def prepare_sequences(self, data):
        """Build supervised sequences from time series."""
        scaled = self.scaler.fit_transform(data.reshape(-1, 1))
        X, y = [], []

        for i in range(len(scaled) - self.sequence_length):
            X.append(scaled[i:i + self.sequence_length])
            y.append(scaled[i + self.sequence_length])

        return np.array(X), np.array(y)

    def train(self, data, epochs=100, lr=0.001):
        """Train LSTM on historical GDP series."""
        X, y = self.prepare_sequences(data)
        X_tensor = torch.FloatTensor(X)
        y_tensor = torch.FloatTensor(y)

        self.model = GDPForecaster()
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=lr)

        for epoch in range(epochs):
            self.model.train()
            optimizer.zero_grad()
            outputs = self.model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()

            if (epoch + 1) % 20 == 0:
                logger.info(f"Epoch {epoch + 1}/{epochs} Loss: {loss.item():.6f}")

        return self.model

    def predict(self, last_sequence, n_future=3):
        """Forecast future values."""
        self.model.eval()
        current = self.scaler.transform(last_sequence.reshape(-1, 1))
        predictions = []

        with torch.no_grad():
            for _ in range(n_future):
                seq = torch.FloatTensor(current[-self.sequence_length:]).reshape(
                    1, self.sequence_length, 1
                )
                pred = self.model(seq).item()
                predictions.append(pred)
                current = np.append(current, [[pred]], axis=0)

        return self.scaler.inverse_transform(
            np.array(predictions).reshape(-1, 1)
        ).flatten()

    def save_model(self, path='models/lstm_model.pt'):
        """Save PyTorch model weights."""
        os.makedirs('models', exist_ok=True)
        torch.save(self.model.state_dict(), path)
        logger.info(f"LSTM model saved: {path}")


def run_lstm_forecast():
    """Execute LSTM forecasting pipeline."""
    if not TORCH_AVAILABLE:
        logger.warning("PyTorch not available. Skipping LSTM forecast.")
        return None

    df = load_data('ecopulse_processed.csv')
    if df is None:
        logger.error("Processed data not found")
        return None

    yearly_gdp = df.groupby('Year')['GDP'].sum().values

    forecaster = TimeSeriesForecaster(sequence_length=3)
    forecaster.train(yearly_gdp, epochs=100)
    predictions = forecaster.predict(yearly_gdp, n_future=3)

    print("\n" + "=" * 60)
    print("GDP FORECAST (LSTM)")
    print("=" * 60)
    last_year = int(df['Year'].max())
    for i, value in enumerate(predictions):
        print(f"  {last_year + 1 + i}: {value:.2f} Lakh Cr")

    forecaster.save_model()
    return predictions


if __name__ == "__main__":
    run_lstm_forecast()