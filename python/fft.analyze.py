import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

Fs = 500e3
N  = 4096
PHASE_W = 32

def dds_signal(fout, n_points):
    t = np.arange(n_points) / Fs
    wave = 128 + 127 * np.sin(2 * np.pi * fout * t)
    wave_q = np.round(wave).astype(int)
    wave_q = np.clip(wave_q, 0, 255)
    ftw = int(round(fout * (2**PHASE_W) / Fs))
    return wave_q, ftw

freqs = [10000, 20000, 50000]

fig, axes = plt.subplots(3, 2, figsize=(14, 9))

for row, fout in enumerate(freqs):
    wave, ftw = dds_signal(fout, N)

    # 左：时域
    ax_t = axes[row][0]
    ax_t.plot(range(300), wave[:300], 'b-', linewidth=1.5)
    ax_t.axhline(128, color='r', linestyle='--', linewidth=0.8, alpha=0.5)
    ax_t.set_ylabel('Amplitude', fontsize=10)
    ax_t.set_title(f'Time Domain  (f_out = {fout/1000:.0f} kHz)', fontsize=11, fontweight='bold')
    ax_t.grid(True, alpha=0.3)
    ax_t.set_ylim(0, 255)

    # 右：频域
    x = wave.astype(float) - 128
    x = x * np.hanning(N)
    spec = np.abs(np.fft.fft(x))
    fa = np.fft.fftfreq(N, d=1/Fs) / 1e3

    half = N // 2
    ax_f = axes[row][1]
    ax_f.plot(fa[:half], spec[:half], 'm-', linewidth=1.2)
    ax_f.set_xlabel('Frequency (kHz)', fontsize=10)
    ax_f.set_ylabel('Magnitude', fontsize=10)
    ax_f.set_title(f'Spectrum (FFT-{N})  FTW={ftw}', fontsize=11, fontweight='bold')
    ax_f.grid(True, alpha=0.3)
    ax_f.set_xlim(0, 100)

    peak_idx = np.argmax(spec[:half])
    peak_freq = fa[peak_idx]
    ax_f.axvline(peak_freq, color='r', linestyle='--', linewidth=1, alpha=0.7)
    ax_f.text(peak_freq + 2, spec[peak_idx]*0.85,
              f'peak = {peak_freq:.1f} kHz',
              fontsize=9, color='r', fontweight='bold')

plt.tight_layout()
plt.savefig('D:/fft_result.png', dpi=150)
plt.close()
print('Saved: D:/fft_result.png')

# 第二张图
fout = 20000
wave, _ = dds_signal(fout, N)
x = (wave.astype(float) - 128) * np.hanning(N)
spec = np.abs(np.fft.fft(x))
fa = np.fft.fftfreq(N, d=1/Fs) / 1e3
half = N // 2

fig2, (a1, a2) = plt.subplots(2, 1, figsize=(11, 6.5))

a1.plot(range(500), wave[:500], 'b-', linewidth=1.4)
a1.set_ylabel('Amplitude', fontsize=11)
a1.set_title(f'DDS Output - Time Domain (f = {fout/1000:.0f} kHz)', fontsize=12, fontweight='bold')
a1.grid(True, alpha=0.3)
a1.set_xlim(0, 500)
a1.set_ylim(0, 255)

a2.plot(fa[:half], spec[:half], 'm-', linewidth=1.4)
a2.set_xlabel('Frequency (kHz)', fontsize=11)
a2.set_ylabel('Magnitude', fontsize=11)
a2.set_title(f'FFT Spectrum Analysis (N = {N})', fontsize=12, fontweight='bold')
a2.grid(True, alpha=0.3)
a2.set_xlim(0, 100)

peak_idx = np.argmax(spec[:half])
pf = fa[peak_idx]
a2.axvline(pf, color='r', linestyle='--', linewidth=1.2, alpha=0.8)
a2.text(pf + 2, spec[peak_idx]*0.75, f'{pf:.1f} kHz',
        fontsize=12, color='r', fontweight='bold')

plt.tight_layout()
plt.savefig('D:/signal_analyzer.png', dpi=150)
plt.close()
print('Saved: D:/signal_analyzer.png')

# 打印度量结果
for f in freqs:
    w, _ = dds_signal(f, N)
    xx = (w.astype(float) - 128) * np.hanning(N)
    ss = np.abs(np.fft.fft(xx))
    ff = np.fft.fftfreq(N, d=1/Fs) / 1e3
    pi = np.argmax(ss[:half])
    print(f'set {f/1000:.0f} kHz -> detected {ff[pi]:.1f} kHz')
