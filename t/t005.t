
=head1 NAME

t005.pl	- How to use this module

=head1 DESCRIPTION

Check not combining Vayakhel/Pekudei in type 14 years


=cut

use strict;
use warnings;
use Test::More tests => 4;
use FindBin qw($Bin);
use lib qq($Bin/../lib);

use DateTime;
use DateTime::Event::Jewish::Parshah qw(parshah);
use DateTime::Calendar::Hebrew;

my $day	= 16;
for (my $year=5785; $year<= 5785; $year++) {
    my $RH01	= DateTime::Calendar::Hebrew->new(day=>$day, month=>7,
					year=>$year);
    my $RH11	= DateTime::Calendar::Hebrew->new(day=>$day, month=>7,
					year=>$year+1);
    my $daysInYear	= $RH11->{rd_days}- $RH01->{rd_days};
    #print "year: $year\n";
    #print "Days in year: $daysInYear\n";
    #print "RH1: ".$RH01->day_of_week."\n";
    next unless $daysInYear==355 && $RH01->day_of_week == 6;
    my $date	= DateTime::Calendar::Hebrew->new(day=>$day,
			month=>12, year=>$year);
    my $parshah	= parshah($date, 1);
    unlike($parshah, qr/Pekudei/, "Israel Vayakhel $year");
    like($parshah, qr/Vayakhel/, "Israel Vayakhel $year");
    $parshah	= parshah($date, 0);
    unlike($parshah, qr/Pekudei/, "Diaspora Vayakhel $year");
    like($parshah, qr/Vayakhel/, "Diaspora Vayakhel $year");
}

exit 0;
