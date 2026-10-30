# -*- coding: utf-8 -*-
"""
DDS 行为级仿真：模拟 32 位相位累加器 + 256 点正弦 ROM
验证不同 FTW(频率控制字) 下的输出波形
"""
import numpy as np
import matplotlib.pyplot as plt

# ==================== 参数（与 dds_sim.v 一致）====================
CLK      = 50e6      # 系统时钟 50 MHz
PHASE_W  = 32        # 相位累加器位宽
ADDR_W   = 8         # 查找表地址位宽
ROM_N    = 256       # 查找表深度

CASES = [
    (10e3, 858993),
    (20e3, 1717987),
    (50e3, 4294967),
]

CYCLES        = 5    # 每档看 5 个周期
PTS_PER_CYCLE = 200  # 每周期画 200 点

# ==================== 256 点正弦查找表 ====================
n   = np.arange(ROM_N)
rom = np.round(128 + 127 * np.sin(2 * np.pi * n / ROM_N)).astype(int)
rom = np.clip(rom, 0, 255)

# ==================== 行为级仿真 ====================
def dds_sim(ftw, f_out, cycles=CYCLES):
    npts = cycles * PTS_PER_CYCLE
    ts   = 1.0 / CLK                        # 20 ns
    # 每个输出周期的时长
    T_out = 1.0 / f_out
    # 采样间隔（秒）
    dt = T_out / PTS_PER_CYCLE
    # 每个采样点跨过的时钟数（可为小数）
    clk_per_pt = dt / ts
    # 相位每点增量（小数）
    inc = ftw * clk_per_pt / (1 << PHASE_W)     # 单位：圈

    k  = np.arange(npts)
    ph = (k * inc) % 1.0                         # 相位 0~1
    addr = (ph * ROM_N).astype(int) & 0xFF       # 地址 0~255
    wave = rom[addr]

    t = k * dt * 1e6                             # 单位 us
    return t, wave - 128

# ==================== 画图 ====================
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

fig, axes = plt.subplots(3, 1, figsize=(10, 8))

for ax, (f_out, ftw) in zip(axes, CASES):
    t, wave = dds_sim(ftw, f_out)
    ax.plot(t, wave, 'b-', linewidth=1.2)
    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8)
    ax.set_title('f_out = %d kHz  (FTW = %d)' % (f_out/1e3, ftw), fontsize=11)
    ax.set_xlabel('时间 (μs)')
    ax.set_ylabel('幅度')
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-160, 160)

plt.suptitle('DDS 输出波形行为级仿真（256 点正弦查找表）', fontsize=13)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(r'D:/项目素材/dds_wave_compare.png', dpi=150, bbox_inches='tight')
plt.show()

print('已保存: D:/项目素材/dds_wave_compare.png')

print('\n===== FTW 验证 =====')
for f_out, ftw in CASES:
    f_actual = ftw * CLK / (1 << PHASE_W)
    print('FTW = %10d  ->  理论频率 = %.2f Hz' % (ftw, f_actual))
