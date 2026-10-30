# 基于 Zynq-7000 的 DDS-FIR-FFT 实时信号处理系统

在 AMD Zynq-7000 XC7Z020 上实现「波形合成 → 低通滤波 → 频谱分析」全链路。
PL 端用 Verilog 完成实时运算，PS 端 ARM 负责参数配置。

## 目录结构

- 01_DDS_FFT/  DDS 波形发生 + FFT 频谱分析（工程 dds_sim）
- 02_FIR/      65 阶线性相位 FIR 低通滤波（工程 fir_sim）
- 03_BOARD/    板级数据通路：PS + AXI + BRAM（工程 sig_clean）
- python/      定点建模与验证脚本

每个子目录是完整的 Vivado 工程，含 .xpr、源码、约束和仿真文件。

## 关键指标

| 项目 | 参数 |
| --- | --- |
| 器件 | XC7Z020CLG400-1 |
| 时钟 | 100 MHz |
| DDS | 32 位相位累加器，256 点 ROM，FTW=858993 对应 10 kHz |
| FIR | 65 阶，fc=10 kHz，Fs=500 kHz，Blackman 窗，Q8 定点 |
| FFT | 4096 点，Fs=500 kHz，分辨率 122 Hz |
| 资源 | LUT 995 (1.87%)，FF 350 (0.33%)，DSP 0 |

## 复现

1. 用 Vivado 打开对应子目录下的 .xpr
2. Run Synthesis → Run Implementation → Generate Bitstream
3. 仿真：SIMULATION → Run Simulation

## 验证脚本

python/ 下的脚本按与 RTL 相同的定点规则重算，用于交叉比对：
dds_wave.py、fir_filter2.py、fft_analyze.py
