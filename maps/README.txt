Flags:

-f, --freq: Frequency input. Can be chosen as all (for all frequencies over all side band), s1 (for all frequencies in side band 1), s2, s3, and s4. Can also be a specific frequency as a list with side band number as first index and frequency number as second index. Ie. [1,2] for first side band second frequency

-p, --plot: one (a single plot), four (four plots), diff (difference plot between two side band. Needs to be follows by -s and a list of the two side bands. Ie. -s [1-2] wil lresult in sb_1 - sb_2.) or gif (an animation over all frequencies) 

-d, --data: all (plots for map, rms, map/rms and hitCount), rms (plot of rms), map/rms (plot of map/rms)

-s, --sb  : a list containing the two side bands for the -p diff option