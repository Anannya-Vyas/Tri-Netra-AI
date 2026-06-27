"""
CUDA verification + alert chime.
Called after PyTorch install completes.
Plays a celebratory chime the instant torch.cuda.is_available() returns True.
"""
import sys
import time

def play_alert():
    """Play a distinct victory chime: 3 ascending short beeps + 1 long high beep."""
    try:
        import winsound
        # Ascending victory fanfare
        freqs = [800, 1000, 1200]
        for f in freqs:
            winsound.Beep(f, 200)
            time.sleep(0.08)
        time.sleep(0.15)
        winsound.Beep(1500, 900)  # triumphant long note
    except Exception as e:
        print(f"[chime fallback] Could not play sound: {e}")

def main():
    print("=" * 60)
    print("  Tri-Netra-AI  ::  CUDA Verification")
    print("=" * 60)

    try:
        import torch
    except ImportError:
        print("[FAIL] torch is not installed!")
        sys.exit(1)

    print(f"  PyTorch version  : {torch.__version__}")
    print(f"  CUDA built with  : {torch.version.cuda}")
    print(f"  cuDNN version    : {torch.backends.cudnn.version() if torch.backends.cudnn.is_available() else 'N/A'}")

    cuda_ok = torch.cuda.is_available()
    print(f"  torch.cuda.is_available() => {cuda_ok}")

    if cuda_ok:
        dev = torch.cuda.get_device_name(0)
        mem = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
        print(f"  GPU device       : {dev}")
        print(f"  VRAM             : {mem:.1f} GB")
        print()
        print("  [OK]  CUDA IS LIVE -- playing alert chime NOW!")
        play_alert()

        # Quick smoke test: tensor on GPU
        print()
        print("  Running quick GPU smoke test...")
        x = torch.randn(1024, 1024, device="cuda")
        y = torch.matmul(x, x)
        print(f"  matmul result shape: {y.shape}, device: {y.device}")
        print("  [OK]  GPU smoke test PASSED")
    else:
        print()
        print("  [FAIL]  CUDA is NOT available. Check driver / install.")
        sys.exit(1)

    print()
    print("=" * 60)
    print("  Ready for your first live test!")
    print("=" * 60)

if __name__ == "__main__":
    main()
