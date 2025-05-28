# This used to be in the plot cases in qt_annotator:
        # TODO: the sync is iffy with this one, but plotting a pd spectrum is
        # still a good idea. Just need to get the FFT parameters tuned - if
        # that's even possible.
        plot_spectrogram(self.data_axes[1],
                         waveform=l1.data,
                         ylim=(0, 60),
                         sampling_frequency=l1.sampling_rate,
                         noverlap=98, NFFT=100,
                         #  xtent_on_x=[-1, 1])  # ,
                         xtent_on_x=[ultra_time[0], ultra_time[-1]])  # ,