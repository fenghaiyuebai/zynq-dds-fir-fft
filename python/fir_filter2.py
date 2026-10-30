import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# ============ 参数 ============
Fs   = 500e3        # 采样率 500kHz
N    = 4096         # 点数
fc   = 10e3         # 截止频率 15kHz
TAPS = 65           # 滤波器阶数

# ============ 1. 生成信号：10kHz 有用 + 30kHz 噪声 ============
t = np.arange(N) / Fs
f_sig  = 10e3
f_noise = 30e3

sig   = 100 * np.sin(2 * np.pi * f_sig * t)
noise =  50 * np.sin(2 * np.pi * f_noise * t)
x = sig + noise + 128                  # 加直流偏置模拟 8bit
x = np.clip(np.round(x), 0, 255).astype(float)
x = x - 128                            # 去直流

# ============ 2. FIR 低通滤波器设计 ============
# 理想低通 = sinc，加 Blackman 窗截断
n = np.arange(TAPS) - (TAPS - 1) / 2
h_ideal = 2 * fc / Fs * np.sinc(2 * fc / Fs * n)
win = np.blackman(TAPS)
h = h_ideal * win
h = h / np.sum(h)                      # 归一化，保证增益=1

# ============ 3. 卷积滤波 ============
y = np.convolve(x, h, mode='same')

# ============ 4. FFT 分析 ============
def spectrum(s):
    s = s * np.hanning(len(s))
    return np.abs(np.fft.fft(s))

X = spectrum(x)
Y = spectrum(y)
fa = np.fft.fftfreq(N, d=1/Fs) / 1e3     # kHz
half = N // 2

# ============ 5. 画图 ============
fig, axes = plt.subplots(3, 2, figsize=(14, 10))

# --- 左列：时域 ---
ax = axes[0][0]
ax.plot(range(300), x[:300], 'b-', linewidth=1.2)
ax.set_title('Input: 10kHz Signal + 30kHz Noise', fontsize=11, fontweight='bold')
ax.set_ylabel('Amplitude', fontsize=10)
ax.grid(True, alpha=0.3)

ax = axes[1][0]
ax.plot(range(300), y[:300], 'r-', linewidth=1.2)
ax.set_title('Output: After FIR Low-Pass (fc = 10kHz)', fontsize=11, fontweight='bold')
ax.set_ylabel('Amplitude', fontsize=10)
ax.grid(True, alpha=0.3)

# --- 右列：频域 ---
ax = axes[0][1]
ax.plot(fa[:half], X[:half], 'b-', linewidth=1.2)
ax.set_title('Input Spectrum', fontsize=11, fontweight='bold')
ax.set_ylabel('Magnitude', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 60)

ax = axes[1][1]
ax.plot(fa[:half], Y[:half], 'r-', linewidth=1.2)
ax.set_title('Output Spectrum (30kHz removed)', fontsize=11, fontweight='bold')
ax.set_ylabel('Magnitude', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 60)

# --- 底部：脉冲响应 + 幅频特性 ---
ax = axes[2][0]
ax.stem(n, h, basefmt=' ')
ax.set_title(f'FIR Impulse Response ({TAPS} taps)', fontsize=11, fontweight='bold')
ax.set_xlabel('Tap Index', fontsize=10)
ax.set_ylabel('h[n]', fontsize=10)
ax.grid(True, alpha=0.3)

# 幅频响应
H = np.abs(np.fft.fft(h, 1024))
fh = np.fft.fftfreq(1024, d=1/Fs) / 1e3
ax = axes[2][1]
ax.plot(fh[:512], 20 * np.log10(H[:512] + 1e-10), 'g-', linewidth=1.5)
ax.axvline(fc/1e3, color='r', linestyle='--', linewidth=1, alpha=0.7, label=f'fc={fc/1e3:.0f}kHz')
ax.set_title('FIR Magnitude Response', fontsize=11, fontweight='bold')
ax.set_xlabel('Frequency (kHz)', fontsize=10)
ax.set_ylabel('Gain (dB)', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_xlim(0, 60)
ax.set_ylim(-80, 5)
ax.legend()

plt.tight_layout()
plt.savefig('D:/fir_result.png', dpi=150)
plt.close()

print('Saved: D:/fir_result.png')

# ============ 量化效果 ============
def peak_at(s, f_target):
    s2 = s * np.hanning(len(s))
    S = np.abs(np.fft.fft(s2))
    fa2 = np.fft.fftfreq(len(s), d=1/Fs)
    idx = np.argmin(np.abs(fa2 - f_target))
    return S[idx]

p_in  = peak_at(x, f_sig)
p_in2 = peak_at(x, f_noise)
p_out = peak_at(y, f_sig)
p_out2 = peak_at(y, f_noise)

print('--- FIR Filter Result ---')
print(f'  10kHz : before = {p_in:.0f}   after = {p_out:.0f}   ({20*np.log10(p_out/p_in):+.1f} dB)')
print(f'  30kHz : before = {p_in2:.0f}  after = {p_out2:.0f}  ({20*np.log10(p_out2/p_in2+1e-10):+.1f} dB)')
