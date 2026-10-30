import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 参数 ============
Fs = 50e6        # 采样率 50MHz (DDS 时钟)
N  = 1024        # FFT 点数
PHASE_W = 32

# ============ 用 DDS 原理生成信号 ============
def dds_signal(fout, n_points):
    """按 DDS 原理生成正弦波: FTW = fout * 2^32 / Fs"""
    ftw = int(round(fout * (2**PHASE_W) / Fs))
    phase = (np.arange(n_points).astype(np.int64) * ftw) % (2**PHASE_W)
    addr = (phase >> (PHASE_W - 8)) & 0xFF
    n = np.arange(256)
    rom = np.round(128 + 127 * np.sin(2 * np.pi * n / 256)).astype(int)
    return rom[addr], ftw

# ============ 生成 3 个不同频率的信号 ============
freqs = [10000, 20000, 50000]     # 10k / 20k / 50k Hz

fig, axes = plt.subplots(3, 2, figsize=(14, 9))

for row, fout in enumerate(freqs):
    wave, ftw = dds_signal(fout, N)

    # -------- 左图：时域 --------
    ax_t = axes[row][0]
    show_n = 200
    ax_t.plot(range(show_n), wave[:show_n], 'b-', linewidth=1.5)
    ax_t.axhline(128, color='r', linestyle='--', linewidth=0.8, alpha=0.5)
    ax_t.set_ylabel('Amplitude', fontsize=10)
    ax_t.set_title(f'Time Domain  (f_out = {fout/1000:.0f} kHz)', fontsize=11, fontweight='bold')
    ax_t.grid(True, alpha=0.3)
    ax_t.set_ylim(0, 255)

    # -------- 右图：频域 (FFT) --------
    x = wave - 128                       # 去直流
    spec = np.abs(np.fft.fft(x))         # 幅度谱
    freqs_axis = np.fft.fftfreq(N, d=1/Fs) / 1e3   # kHz

    half = N // 2
    ax_f = axes[row][1]
    ax_f.plot(freqs_axis[:half], spec[:half], 'm-', linewidth=1.5)
    ax_f.set_xlabel('Frequency (kHz)', fontsize=10)
    ax_f.set_ylabel('Magnitude', fontsize=10)
    ax_f.set_title(f'Spectrum (FFT-{N})', fontsize=11, fontweight='bold')
    ax_f.grid(True, alpha=0.3)

    # 标出峰值位置
    peak_idx = np.argmax(spec[:half])
    peak_freq = freqs_axis[peak_idx]
    ax_f.axvline(peak_freq, color='r', linestyle='--', linewidth=1, alpha=0.7)
    ax_f.text(peak_freq, spec[peak_idx]*0.8,
              f'peak = {peak_freq:.1f} kHz',
              fontsize=9, color='r', fontweight='bold')

plt.tight_layout()
plt.savefig('D:/fft_result.png', dpi=150)
plt.close()

print('Done! Saved to D:/fft_result.png')

# ============ 单独画一张"信号分析仪"效果图 ============
fout = 20000
wave, _ = dds_signal(fout, N)
x = wave - 128
spec = np.abs(np.fft.fft(x))
freqs_axis = np.fft.fftfreq(N, d=1/Fs) / 1e3
half = N // 2

fig2, (a1, a2) = plt.subplots(2, 1, figsize=(11, 6.5))

a1.plot(range(N), wave, 'b-', linewidth=1.2)
a1.set_ylabel('Amplitude', fontsize=11)
a1.set_title(f'DDS Output - Time Domain (f = {fout/1000:.0f} kHz)', fontsize=12, fontweight='bold')
a1.grid(True, alpha=0.3)
a1.set_xlim(0, 300)

a2.plot(freqs_axis[:half], spec[:half], 'm-', linewidth=1.5)
a2.set_xlabel('Frequency (kHz)', fontsize=11)
a2.set_ylabel('Magnitude', fontsize=11)
a2.set_title(f'FFT Spectrum Analysis (N = {N})', fontsize=12, fontweight='bold')
a2.grid(True, alpha=0.3)

peak_idx = np.argmax(spec[:half])
axline = freqs_axis[peak_idx]
a2.axvline(axline, color='r', linestyle='--', linewidth=1.2, alpha=0.8)
a2.text(axline, spec[peak_idx]*0.7, f'{axline:.1f} kHz', 
        fontsize=11, color='r', fontweight='bold')

plt.tight_layout()
plt.savefig('D:/signal_analyzer.png', dpi=150)
plt.close()

print('Done! Saved to D:/signal_analyzer.png')
