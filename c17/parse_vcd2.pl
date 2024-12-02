# parse_vcd.pl
# Perl script to extract signal transitions from VCD file
use strict;
use warnings;

my $vcd_file = $ARGV[0];

open(my $vcd, '<', $vcd_file) or die "Cannot open VCD file";
open(my $out, '>', 'transitions.txt') or die "Cannot write output file";

while (<$vcd>) {
    # Parse relevant signal changes
    if (/^\$var/ || /^\d+/) {
        print $out $_; # Extract timestamp and signal transitions
    }
}

close $vcd;
close $out;
print "Parsed VCD data saved to transitions.txt\n";

