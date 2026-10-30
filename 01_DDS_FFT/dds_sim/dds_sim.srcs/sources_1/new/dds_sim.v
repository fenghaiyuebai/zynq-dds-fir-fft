`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// DDS 直接数字频率合成器 (Direct Digital Synthesizer)
// 输出: 8bit 正弦波, 采样率 50MHz
// f_out = FTW * f_clk / 2^N,  N=32, f_clk=50MHz
// 例: FTW=858993 -> f_out = 858993*50e6/2^32 ≈ 10kHz
//////////////////////////////////////////////////////////////////////////////////

module dds_sim #(
    parameter PHASE_WIDTH = 32,      // 相位累加器位宽
    parameter ADDR_WIDTH  = 8,       // 查找表地址位宽 (256 点)
    parameter DATA_WIDTH  = 8,       // 输出数据位宽
    parameter FTW         = 32'd858993   // 频率控制字 -> 约 10kHz
)(
    input  wire                     clk,        // 50MHz
    input  wire                     rst_n,      // 低有效复位
    output wire [DATA_WIDTH-1:0]    wave_out,   // 8bit 正弦波输出
    output wire [ADDR_WIDTH-1:0]    phase_addr  // 相位地址(调试观察用)
);

    // ---------------- 相位累加器 ----------------
    reg [PHASE_WIDTH-1:0] phase_acc;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            phase_acc <= {PHASE_WIDTH{1'b0}};
        else
            phase_acc <= phase_acc + FTW;
    end

    // ---------------- 取高 8 位作查找表地址 ----------------
    // 相位累加器的高 8 位就是正弦波一周期的 256 个点
    assign phase_addr = phase_acc[PHASE_WIDTH-1 : PHASE_WIDTH-ADDR_WIDTH];

    // ---------------- 256x8 正弦 ROM ----------------
    // 数据 = 128 + 127*sin(2*pi*n/256)，中心 128，幅度 ±127
    reg [DATA_WIDTH-1:0] sin_rom [0:255];

    initial begin
        sin_rom[  0] = 128; sin_rom[  1] = 131; sin_rom[  2] = 134; sin_rom[  3] = 137;
        sin_rom[  4] = 140; sin_rom[  5] = 143; sin_rom[  6] = 146; sin_rom[  7] = 149;
        sin_rom[  8] = 152; sin_rom[  9] = 155; sin_rom[ 10] = 158; sin_rom[ 11] = 162;
        sin_rom[ 12] = 165; sin_rom[ 13] = 168; sin_rom[ 14] = 170; sin_rom[ 15] = 173;
        sin_rom[ 16] = 176; sin_rom[ 17] = 179; sin_rom[ 18] = 182; sin_rom[ 19] = 184;
        sin_rom[ 20] = 187; sin_rom[ 21] = 189; sin_rom[ 22] = 192; sin_rom[ 23] = 194;
        sin_rom[ 24] = 197; sin_rom[ 25] = 199; sin_rom[ 26] = 201; sin_rom[ 27] = 203;
        sin_rom[ 28] = 205; sin_rom[ 29] = 207; sin_rom[ 30] = 209; sin_rom[ 31] = 211;
        sin_rom[ 32] = 212; sin_rom[ 33] = 214; sin_rom[ 34] = 215; sin_rom[ 35] = 217;
        sin_rom[ 36] = 218; sin_rom[ 37] = 219; sin_rom[ 38] = 220; sin_rom[ 39] = 221;
        sin_rom[ 40] = 222; sin_rom[ 41] = 223; sin_rom[ 42] = 224; sin_rom[ 43] = 225;
        sin_rom[ 44] = 225; sin_rom[ 45] = 226; sin_rom[ 46] = 226; sin_rom[ 47] = 227;
        sin_rom[ 48] = 227; sin_rom[ 49] = 227; sin_rom[ 50] = 227; sin_rom[ 51] = 228;
        sin_rom[ 52] = 228; sin_rom[ 53] = 228; sin_rom[ 54] = 228; sin_rom[ 55] = 228;
        sin_rom[ 56] = 227; sin_rom[ 57] = 227; sin_rom[ 58] = 227; sin_rom[ 59] = 227;
        sin_rom[ 60] = 226; sin_rom[ 61] = 226; sin_rom[ 62] = 225; sin_rom[ 63] = 225;
        sin_rom[ 64] = 224; sin_rom[ 65] = 223; sin_rom[ 66] = 222; sin_rom[ 67] = 221;
        sin_rom[ 68] = 220; sin_rom[ 69] = 219; sin_rom[ 70] = 218; sin_rom[ 71] = 217;
        sin_rom[ 72] = 215; sin_rom[ 73] = 214; sin_rom[ 74] = 212; sin_rom[ 75] = 211;
        sin_rom[ 76] = 209; sin_rom[ 77] = 207; sin_rom[ 78] = 205; sin_rom[ 79] = 203;
        sin_rom[ 80] = 201; sin_rom[ 81] = 199; sin_rom[ 82] = 197; sin_rom[ 83] = 194;
        sin_rom[ 84] = 192; sin_rom[ 85] = 189; sin_rom[ 86] = 187; sin_rom[ 87] = 184;
        sin_rom[ 88] = 182; sin_rom[ 89] = 179; sin_rom[ 90] = 176; sin_rom[ 91] = 173;
        sin_rom[ 92] = 170; sin_rom[ 93] = 168; sin_rom[ 94] = 165; sin_rom[ 95] = 162;
        sin_rom[ 96] = 158; sin_rom[ 97] = 155; sin_rom[ 98] = 152; sin_rom[ 99] = 149;
        sin_rom[100] = 146; sin_rom[101] = 143; sin_rom[102] = 140; sin_rom[103] = 137;
        sin_rom[104] = 134; sin_rom[105] = 131; sin_rom[106] = 128; sin_rom[107] = 125;
        sin_rom[108] = 122; sin_rom[109] = 119; sin_rom[110] = 116; sin_rom[111] = 113;
        sin_rom[112] = 110; sin_rom[113] = 107; sin_rom[114] = 104; sin_rom[115] = 101;
        sin_rom[116] =  98; sin_rom[117] =  94; sin_rom[118] =  91; sin_rom[119] =  88;
        sin_rom[120] =  86; sin_rom[121] =  83; sin_rom[122] =  80; sin_rom[123] =  77;
        sin_rom[124] =  74; sin_rom[125] =  72; sin_rom[126] =  69; sin_rom[127] =  67;
        sin_rom[128] =  64; sin_rom[129] =  62; sin_rom[130] =  60; sin_rom[131] =  58;
        sin_rom[132] =  56; sin_rom[133] =  54; sin_rom[134] =  52; sin_rom[135] =  50;
        sin_rom[136] =  49; sin_rom[137] =  47; sin_rom[138] =  46; sin_rom[139] =  44;
        sin_rom[140] =  43; sin_rom[141] =  42; sin_rom[142] =  41; sin_rom[143] =  40;
        sin_rom[144] =  39; sin_rom[145] =  38; sin_rom[146] =  37; sin_rom[147] =  36;
        sin_rom[148] =  36; sin_rom[149] =  35; sin_rom[150] =  35; sin_rom[151] =  34;
        sin_rom[152] =  34; sin_rom[153] =  34; sin_rom[154] =  34; sin_rom[155] =  33;
        sin_rom[156] =  33; sin_rom[157] =  33; sin_rom[158] =  33; sin_rom[159] =  33;
        sin_rom[160] =  34; sin_rom[161] =  34; sin_rom[162] =  34; sin_rom[163] =  34;
        sin_rom[164] =  35; sin_rom[165] =  35; sin_rom[166] =  36; sin_rom[167] =  36;
        sin_rom[168] =  37; sin_rom[169] =  38; sin_rom[170] =  39; sin_rom[171] =  40;
        sin_rom[172] =  41; sin_rom[173] =  42; sin_rom[174] =  43; sin_rom[175] =  44;
        sin_rom[176] =  46; sin_rom[177] =  47; sin_rom[178] =  49; sin_rom[179] =  50;
        sin_rom[180] =  52; sin_rom[181] =  54; sin_rom[182] =  56; sin_rom[183] =  58;
        sin_rom[184] =  60; sin_rom[185] =  62; sin_rom[186] =  64; sin_rom[187] =  67;
        sin_rom[188] =  69; sin_rom[189] =  72; sin_rom[190] =  74; sin_rom[191] =  77;
        sin_rom[192] =  80; sin_rom[193] =  83; sin_rom[194] =  86; sin_rom[195] =  88;
        sin_rom[196] =  91; sin_rom[197] =  94; sin_rom[198] =  98; sin_rom[199] = 101;
        sin_rom[200] = 104; sin_rom[201] = 107; sin_rom[202] = 110; sin_rom[203] = 113;
        sin_rom[204] = 116; sin_rom[205] = 119; sin_rom[206] = 122; sin_rom[207] = 125;
        sin_rom[208] = 128; sin_rom[209] = 131; sin_rom[210] = 134; sin_rom[211] = 137;
        sin_rom[212] = 140; sin_rom[213] = 143; sin_rom[214] = 146; sin_rom[215] = 149;
        sin_rom[216] = 152; sin_rom[217] = 155; sin_rom[218] = 158; sin_rom[219] = 162;
        sin_rom[220] = 165; sin_rom[221] = 168; sin_rom[222] = 170; sin_rom[223] = 173;
        sin_rom[224] = 176; sin_rom[225] = 179; sin_rom[226] = 182; sin_rom[227] = 184;
        sin_rom[228] = 187; sin_rom[229] = 189; sin_rom[230] = 192; sin_rom[231] = 194;
        sin_rom[232] = 197; sin_rom[233] = 199; sin_rom[234] = 201; sin_rom[235] = 203;
        sin_rom[236] = 205; sin_rom[237] = 207; sin_rom[238] = 209; sin_rom[239] = 211;
        sin_rom[240] = 212; sin_rom[241] = 214; sin_rom[242] = 215; sin_rom[243] = 217;
        sin_rom[244] = 218; sin_rom[245] = 219; sin_rom[246] = 220; sin_rom[247] = 221;
        sin_rom[248] = 222; sin_rom[249] = 223; sin_rom[250] = 224; sin_rom[251] = 225;
        sin_rom[252] = 225; sin_rom[253] = 226; sin_rom[254] = 226; sin_rom[255] = 227;
    end

    // 组合读出，无延迟
    assign wave_out = sin_rom[phase_addr];

endmodule
