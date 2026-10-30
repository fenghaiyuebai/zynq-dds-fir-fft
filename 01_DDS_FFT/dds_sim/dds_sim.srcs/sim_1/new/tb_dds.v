`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// DDS Testbench  v3
// 采样 3000 点，保证覆盖 2 个以上完整正弦周期
//////////////////////////////////////////////////////////////////////////////////

module tb_dds;

    localparam CLK_PERIOD = 20;         // 50MHz -> 20ns
    localparam SAMPLE_NUM = 3000;       // 采样点数（改这里）
    localparam FTW_VALUE  = 32'd858993; // 约 10kHz

    reg         clk;
    reg         rst_n;
    wire [7:0]  wave_out;
    wire [7:0]  phase_addr;

    integer     i;
    integer     fp;

    // ---------------- 例化 DDS ----------------
    dds_sim #(
        .FTW (FTW_VALUE)
    ) u_dds (
        .clk        (clk),
        .rst_n      (rst_n),
        .wave_out   (wave_out),
        .phase_addr (phase_addr)
    );

    // ---------------- 时钟 ----------------
    initial begin
        clk = 1'b0;
        forever #(CLK_PERIOD/2) clk = ~clk;
    end

    // ---------------- 激励 + 采样 ----------------
    initial begin
        fp = $fopen("dds_out.csv", "w");
        if (fp == 0) begin
            $display("ERROR: cannot open dds_out.csv");
        end
        $fwrite(fp, "sample,phase,wave\n");

        // 复位
        rst_n = 1'b0;
        #(CLK_PERIOD * 10);
        rst_n = 1'b1;
        #(CLK_PERIOD * 10);

        $display("---DDS_SIM_BEGIN---");

        // 采样
        for (i = 0; i < SAMPLE_NUM; i = i + 1) begin
            @(posedge clk);
            #1;
            $display("SAMPLE %0d : phase=%0d wave=%0d", i, phase_addr, wave_out);
            $fwrite(fp, "%0d,%0d,%0d\n", i, phase_addr, wave_out);
        end

        $display("---DDS_SIM_END---");

        $fclose(fp);
        #(CLK_PERIOD * 10);
        $finish;
    end

endmodule
