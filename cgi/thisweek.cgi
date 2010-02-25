#!perl 

=head1 NAME

thisweek.cgi - Shabbat infor for the coming Shabbat.

=head1 DESCRIPTION

Generate an HTML fragment with the basic info for the coming Shabbat.

You will have to alter the $place variable to suit your local requirements.

=cut

use strict;
use warnings;

use DateTime;
use DateTime::Duration;
use DateTime::Calendar::Hebrew;
use DateTime::Event::Jewish::Sunrise ;
use DateTime::Event::Jewish::Parshah qw(nextShabbat parshah);

my $place = [[51, 34, 57], [0,-13,-28], 'Europe/London']; # Actually, Hendon Central

my $location	= DateTime::Event::Jewish::Sunrise->new(@$place);

print "\n\n";
my $shabbat	= nextShabbat(DateTime->today);

    my $friday	= $shabbat - DateTime::Duration->new(days=>1);

    my $candles	= $location->kabbalatShabbat($friday);
    my $night	= $location->motzeiShabbat($shabbat);

    # In Adar of a non-leap year this will print 'AdarI' instead of
    # just 'Adar'. This is a bug in DateTime::Calendar::Hebrew.
    printf "<b>Shabbat</b> %d %s %d %s<br/>\n", $shabbat->day,
	    $shabbat->month_name, $shabbat->year, parshah($friday);
    printf "<b>Kabbalat Shabbat:</b> %02d:%02d<br/>\n", $candles->hour, $candles->minute;
    printf "<b>Motzei Shabbat:</b> %02d:%02d<br/>\n", $night->hour, $night->minute;

    my $mevarchin	= $shabbat->day() > 22;
    # A day that is definitely in next month
    my $nextMonth	= $shabbat+DateTime::Duration->new(days=>8);
    # No Mevarchin HaCodesh for Tishrei
    if ($mevarchin && $nextMonth->month != 7) {
	print "<b>Mevarchin hachodesh:</b> ", $nextMonth->month_name, "<br/>\n";
    }

    # Which days is Rosh Chodesh?
    if ($mevarchin) {
	my $roshChodesh1	 =
	$shabbat->clone->set(day=>DateTime::Calendar::Hebrew::_LastDayOfMonth($shabbat->year,$shabbat->month));
	my $roshChodesh	= $roshChodesh1->day_name;
	if ($roshChodesh1->day == 30) {
	    my $roshChodesh2	=
	    $roshChodesh1+DateTime::Duration->new(days=>1);
	    $roshChodesh	.= "/". $roshChodesh2->day_name;
	}
	print "<b>Rosh Chodesh:</b> $roshChodesh<br/>\n";
    }


print "\n\n";
exit 0;
