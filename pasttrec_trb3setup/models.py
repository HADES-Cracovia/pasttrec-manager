from django.core.exceptions import ValidationError
from django.db import models
import datetime

def check_range(var, low, high):
    return low <= var <= high

# Create your models here
class TDC(models.Model):
    trbnetid = models.CharField(max_length=6)

    def __str__(self):
        return self.trbnetid



class Setup(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Revision(models.Model):
    setup = models.ForeignKey(Setup, on_delete=models.CASCADE)
    creation_on = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.setup.name + ", rev: " + self.creation_on.strftime('%Y-%m-%d %H:%M')

    def export_name(self):
        return self.setup.name + "_rev_" + self.creation_on.strftime('%Y%m%d_%H%M')




class Card(models.Model):
    name = models.CharField(max_length=32)
    notes = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Connection(models.Model):
    revision = models.ForeignKey(Revision, on_delete=models.CASCADE)

    tdc = models.ForeignKey(TDC, on_delete=models.CASCADE)
    card1 = models.ForeignKey(Card, related_name='card1', on_delete=models.CASCADE, blank=True, null=True)
    card2 = models.ForeignKey(Card, related_name='card2', on_delete=models.CASCADE, blank=True, null=True)
    card3 = models.ForeignKey(Card, related_name='card3', on_delete=models.CASCADE, blank=True, null=True)

    inactive = models.BooleanField(default=False)

    notes = models.TextField(blank=True, default='')

    def __str__(self):
        c1 = self.card1.name if self.card1 else ' -no card- '
        c2 = self.card2.name if self.card2 else ' -no card- '
        c3 = self.card3.name if self.card3 else ' -no card- '

        return "{:s} -> Cable 1: {:s}  2: {:s}  3: {:s}".format(
            self.tdc.trbnetid, c1, c2, c3
        )



class CardSettings(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    revision = models.ForeignKey(Revision, related_name='card_revision', on_delete=models.CASCADE)
    map_to = models.ForeignKey('self', related_name='map_to_revision', on_delete=models.CASCADE, blank=True, null=True)

    # asic #1

    bg_int_0 = models.BooleanField(default=True)
    gain_0 = models.IntegerField(default=3)
    peaking_0 = models.IntegerField(default=3)
    tc1c_0 = models.IntegerField(default=3)
    tc1r_0 = models.IntegerField(default=6)
    tc2c_0 = models.IntegerField(default=2)
    tc2r_0 = models.IntegerField(default=5)

    threshold_0 = models.IntegerField(default=0)
    disabled_0 = models.BooleanField(default=False)

    baseline_00 = models.IntegerField(default=0)
    baseline_01 = models.IntegerField(default=0)
    baseline_02 = models.IntegerField(default=0)
    baseline_03 = models.IntegerField(default=0)
    baseline_04 = models.IntegerField(default=0)
    baseline_05 = models.IntegerField(default=0)
    baseline_06 = models.IntegerField(default=0)
    baseline_07 = models.IntegerField(default=0)

    disabled_00 = models.BooleanField(default=False)
    disabled_01 = models.BooleanField(default=False)
    disabled_02 = models.BooleanField(default=False)
    disabled_03 = models.BooleanField(default=False)
    disabled_04 = models.BooleanField(default=False)
    disabled_05 = models.BooleanField(default=False)
    disabled_06 = models.BooleanField(default=False)
    disabled_07 = models.BooleanField(default=False)

    # asic #2
    bg_int_1 = models.BooleanField(default=True)
    gain_1 = models.IntegerField(default=3)
    peaking_1 = models.IntegerField(default=3)
    tc1c_1 = models.IntegerField(default=3)
    tc1r_1 = models.IntegerField(default=6)
    tc2c_1 = models.IntegerField(default=2)
    tc2r_1 = models.IntegerField(default=5)

    threshold_1 = models.IntegerField(default=0)
    disabled_1 = models.BooleanField(default=False)

    baseline_10 = models.IntegerField(default=0)
    baseline_11 = models.IntegerField(default=0)
    baseline_12 = models.IntegerField(default=0)
    baseline_13 = models.IntegerField(default=0)
    baseline_14 = models.IntegerField(default=0)
    baseline_15 = models.IntegerField(default=0)
    baseline_16 = models.IntegerField(default=0)
    baseline_17 = models.IntegerField(default=0)

    disabled_10 = models.BooleanField(default=False)
    disabled_11 = models.BooleanField(default=False)
    disabled_12 = models.BooleanField(default=False)
    disabled_13 = models.BooleanField(default=False)
    disabled_14 = models.BooleanField(default=False)
    disabled_15 = models.BooleanField(default=False)
    disabled_16 = models.BooleanField(default=False)
    disabled_17 = models.BooleanField(default=False)

    def __str__(self):
        return self.card.name + "  " + self.revision.__str__()

    def clean(self):
        e = {}
        # asic #1
        if not check_range(self.gain_0, 0, 3):
            e['gain_0'] = 'Outside range 0-3'
        if not check_range(self.peaking_0, 0, 3):
            e['peaking_0'] = 'Outside range 0-3'

        if not check_range(self.tc1c_0, 0, 7):
            e['tc1c_0'] = 'Outside range 0-7'
        if not check_range(self.tc1r_0, 0, 7):
            e['tc1r_0'] = 'Outside range 0-7'
        if not check_range(self.tc2c_0, 0, 7):
            e['tc2c_0'] = 'Outside range 0-7'
        if not check_range(self.tc2r_0, 0, 7):
            e['tc2r_0'] = 'Outside range 0-7'

        if not check_range(self.threshold_0, 0, 127):
            e['threshold_0'] = 'Outside range 0-127'

        if not check_range(self.baseline_00, 0, 31):
            e['baseline_00'] = 'Outside range 0-31'
        if not check_range(self.baseline_01, 0, 31):
            e['baseline_01'] = 'Outside range 0-31'
        if not check_range(self.baseline_02, 0, 31):
            e['baseline_02'] = 'Outside range 0-31'
        if not check_range(self.baseline_03, 0, 31):
            e['baseline_03'] = 'Outside range 0-31'
        if not check_range(self.baseline_04, 0, 31):
            e['baseline_04'] = 'Outside range 0-31'
        if not check_range(self.baseline_05, 0, 31):
            e['baseline_05'] = 'Outside range 0-31'
        if not check_range(self.baseline_06, 0, 31):
            e['baseline_06'] = 'Outside range 0-31'
        if not check_range(self.baseline_07, 0, 31):
            e['baseline_07'] = 'Outside range 0-31'

        # asic #1
        if not check_range(self.gain_1, 0, 3):
            e['gain_1'] = 'Outside range 0-3'
        if not check_range(self.peaking_1, 0, 3):
            e['peaking_1'] = 'Outside range 0-3'

        if not check_range(self.tc1c_1, 0, 7):
            e['tc1c_1'] = 'Outside range 0-7'
        if not check_range(self.tc1r_1, 0, 7):
            e['tc1r_1'] = 'Outside range 0-7'
        if not check_range(self.tc2c_1, 0, 7):
            e['tc2c_1'] = 'Outside range 0-7'
        if not check_range(self.tc2r_1, 0, 7):
            e['tc2r_1'] = 'Outside range 0-7'

        if not check_range(self.threshold_1, 0, 127):
            e['threshold_1'] = 'Outside range 0-127'

        if not check_range(self.baseline_10, 0, 31):
            e['baseline_10'] = 'Outside range 0-31'
        if not check_range(self.baseline_11, 0, 31):
            e['baseline_11'] = 'Outside range 0-31'
        if not check_range(self.baseline_12, 0, 31):
            e['baseline_12'] = 'Outside range 0-31'
        if not check_range(self.baseline_13, 0, 31):
            e['baseline_13'] = 'Outside range 0-31'
        if not check_range(self.baseline_14, 0, 31):
            e['baseline_14'] = 'Outside range 0-31'
        if not check_range(self.baseline_15, 0, 31):
            e['baseline_15'] = 'Outside range 0-31'
        if not check_range(self.baseline_16, 0, 31):
            e['baseline_16'] = 'Outside range 0-31'
        if not check_range(self.baseline_17, 0, 31):
            e['baseline_17'] = 'Outside range 0-31'

        if len(e.items()):
            raise ValidationError(e)
