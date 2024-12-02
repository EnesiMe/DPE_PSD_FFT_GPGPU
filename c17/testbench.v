// testbench.v - Testbench for C17 circuit
`timescale 1ns/1ps

module testbench;
    reg A, B, C, D, E;
    wire Z;

    // Instantiate the C17 module
    c17 uut (
        .N1(A), .N2(B), .N3(C), .N6(D), .N7(E),
        .N23(Z)
    );

    // Generate input stimuli
    initial begin
        // Dump signals to VCD file for waveform analysis
        $dumpfile("c17.vcd");
        $dumpvars(0, testbench);

        // Apply test vectors
        A = 0; B = 0; C = 0; D = 0; E = 0; #10;
        A = 1; B = 0; C = 0; D = 1; E = 0; #10;
        A = 1; B = 1; C = 0; D = 1; E = 1; #10;
        A = 0; B = 1; C = 1; D = 0; E = 1; #10;
        A = 1; B = 1; C = 1; D = 1; E = 1; #10;
        
        

        // End simulation
        $finish;
    end
endmodule

