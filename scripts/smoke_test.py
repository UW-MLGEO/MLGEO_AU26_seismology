import torch
import torch.nn as nn
from scipy.signal import butter, sosfilt

# 1. Define minimal 1D ConvNet model class
class SeismicConvNet1D(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv1d(in_channels=3, out_channels=16, kernel_size=5, padding=2)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Linear(16, 1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(x).squeeze(-1)
        return self.fc(x)

def run_smoke_test():
    print("--- Running Seismic Pipeline Smoke Test ---")
    
    # 2. Create dummy 3-component seismic waveform (1 sample, 3 channels, 300 time steps)
    dummy_trace = torch.randn(1, 3, 300)
    print(f"1. Dummy 3-component waveform loaded: shape {list(dummy_trace.shape)}")

    # 3. Apply 1-10 Hz Bandpass Filter
    sos = butter(4, [1, 10], btype='bandpass', fs=100, output='sos')
    filtered_np = sosfilt(sos, dummy_trace.numpy(), axis=-1)
    filtered_trace = torch.from_numpy(filtered_np).float()
    print("2. 1-10 Hz bandpass pre-processing filter executed.")

    # 4. Instantiate Model & Run Forward Pass
    model = SeismicConvNet1D()
    output = model(filtered_trace)
    print(f"3. Model forward pass complete. Predicted Mw: {output.item():.2f}")
    
    assert output.shape == (1, 1), "Output shape mismatch!"
    print("--- SUCCESS: Pipeline Smoke Test Passed! ---")

if __name__ == "__main__":
    run_smoke_test()