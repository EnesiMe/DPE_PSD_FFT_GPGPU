#!/usr/bin/perl
use strict;
use warnings;

# Check if VCD file is provided
if (@ARGV < 1) {
    die "Usage: perl parse_vcd.pl <vcd_file> [output_file]\n";
}

my $vcd_file = $ARGV[0];
my $output_file = $ARGV[1] || "output_time_series.txt";

# Open VCD file for reading
open my $vcd, '<', $vcd_file or die "Cannot open $vcd_file: $!\n";

# Open output file for writing
open my $out, '>', $output_file or die "Cannot open $output_file: $!\n";

my %signals;           # Hash to store signal definitions
my %signal_values;     # Hash to store current signal values
my $current_time = 0;  # Current time in the simulation

# Process the VCD file
while (my $line = <$vcd>) {
    chomp $line;

    # Parse signal definitions
    if ($line =~ /^\$var\s+\w+\s+\d+\s+(\S+)\s+(\S+)\s+\$/) {
        my $signal_id = $1;
        my $signal_name = $2;
        $signals{$signal_id} = $signal_name;
        $signal_values{$signal_id} = undef;  # Initialize signal value
        next;
    }

    # Detect simulation time change
    if ($line =~ /^#(\d+)/) {
        $current_time = $1;
        next;
    }

    # Parse signal value changes
    if ($line =~ /^([01zxZX])(\S+)/) {
        my $value = $1;
        my $signal_id = $2;

        # Update the signal value
        if (exists $signals{$signal_id}) {
            $signal_values{$signal_id} = $value;

            # Output time-value pair for the signal (adjust for the signal of interest)
            print $out "$current_time,$signals{$signal_id},$value\n";
        }
    }
}

# Close files
close $vcd;
close $out;

print "Time-series data written to $output_file\n";

