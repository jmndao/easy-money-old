
import django.utils.timezone as timezone
year = timezone.now().year


class Utils:
    def estimation_from_model(self, db_estimation, last=False, pk=None):
        if last:
            my_estimation = db_estimation.objects.last()
        else:
            my_estimation = db_estimation.objects.get(pk=pk)
        i_price = float(my_estimation.used_price)
        repair_amount = float(my_estimation.reparatinon_price)

        percentage_1 = 0
        if my_estimation.estate == 'NEUF':
            percentage_1 = 0
        elif my_estimation.estate == 'BON':
            percentage_1 = 0.05
        elif my_estimation.estate == 'MOYEN':
            percentage_1 = 0.1
        elif my_estimation.estate == 'MAUVAIS':
            percentage_1 = 0.2
        else:
            percentage_1 = 1

        i_price = i_price - i_price * percentage_1
        percentage_2 = 0
        if my_estimation.obsolescence == 'LENTE':
            percentage_2 = 0
        elif my_estimation.obsolescence == 'MOYENNE':
            percentage_2 = 0.05
        elif my_estimation.obsolescence == 'RAPIDE':
            percentage_2 = 0.1
        elif my_estimation.obsolescence == 'TRES_RAPIDE':
            percentage_2 = 0.2
        else:
            percentage_2 = 1
        i_price = i_price - i_price * percentage_2

        percentage_3 = 0
        if my_estimation.rarety == 'RARE':
            percentage_3 = 0
        elif my_estimation.rarety == 'COURANT':
            percentage_3 = 0.05
        elif my_estimation.rarety == 'TRES_COURANT':
            percentage_3 = 0.1
        else:
            percentage_3 = None
        i_price = i_price - i_price * percentage_3

        percentage_4 = 0
        if my_estimation.original_box == True:
            percentage_4 = 0
        else:
            percentage_4 = 0.05

        i_price = i_price - i_price * percentage_4

        percentage_5 = 0
        if my_estimation.charger == 'OUI':
            percentage_5 = 0
        elif my_estimation.charger == 'NON':
            percentage_5 = 0.05
        elif my_estimation.charger == 'PAS_BESOIN':
            percentage_5 = 0
        else:
            percentage_5 = 0
        i_price = i_price - i_price * percentage_5

        percentage_6 = 0
        if my_estimation.sale_bill == True:
            percentage_6 = 0
        else:
            percentage_6 = 0.05
        i_price = i_price - i_price * percentage_6

        percentage_7 = 0
        if my_estimation.dimension == 'PETIT':
            percentage_7 = 0
        elif my_estimation.dimension == 'MOYEN':
            percentage_7 = 0.05
        elif my_estimation.dimension == 'GRAND':
            percentage_7 = 0.1
        else:
            percentage_7 = None
        i_price = i_price - i_price * percentage_7

        i_price = i_price - repair_amount

        percentage_8 = 0.02
        diff_year = int(year) - \
            int(my_estimation.year_of_release)
        assert diff_year >= 0

        i_price = i_price - i_price * diff_year * percentage_8

        proposed_price = round(float(i_price) / 1000) * 1000

        return int(proposed_price)

    def estimation_from_form(self, form):

        i_price = form.instance.used_price = float(
            form.instance.new_price) // 2
        repair_amount = float(form.instance.reparatinon_price)

        percentage_1 = 0
        if form.instance.estate == 'NEUF':
            percentage_1 = 0
        elif form.instance.estate == 'BON':
            percentage_1 = 0.05
        elif form.instance.estate == 'MOYEN':
            percentage_1 = 0.1
        elif form.instance.estate == 'MAUVAIS':
            percentage_1 = 0.2
        else:
            percentage_1 = 1

        i_price = i_price - i_price * percentage_1
        percentage_2 = 0
        if form.instance.obsolescence == 'LENTE':
            percentage_2 = 0
        elif form.instance.obsolescence == 'MOYENNE':
            percentage_2 = 0.05
        elif form.instance.obsolescence == 'RAPIDE':
            percentage_2 = 0.1
        elif form.instance.obsolescence == 'TRES_RAPIDE':
            percentage_2 = 0.2
        else:
            percentage_2 = None
        i_price = i_price - i_price * percentage_2

        percentage_3 = 0
        if form.instance.rarety == 'RARE':
            percentage_3 = 0
        elif form.instance.rarety == 'COURANT':
            percentage_3 = 0.05
        elif form.instance.rarety == 'TRES_COURANT':
            percentage_3 = 0.1
        else:
            percentage_3 = None

        i_price = i_price - i_price * percentage_3

        percentage_4 = 0
        if form.instance.original_box == True:
            percentage_4 = 0
        else:
            percentage_4 = 0.05

        i_price = i_price - i_price * percentage_4

        percentage_5 = 0
        if form.instance.charger == 'OUI':
            percentage_5 = 0
        elif form.instance.charger == 'NON':
            percentage_5 = 0.05
        elif form.instance.charger == 'PAS_BESOIN':
            percentage_5 = 0
        else:
            percentage_5 = 0
        i_price = i_price - i_price * percentage_5

        percentage_6 = 0
        if form.instance.sale_bill == True:
            percentage_6 = 0
        else:
            percentage_6 = 0.05
        i_price = i_price - i_price * percentage_6

        percentage_7 = 0
        if form.instance.dimension == 'PETIT':
            percentage_7 = 0
        elif form.instance.dimension == 'MOYEN':
            percentage_7 = 0.05
        elif form.instance.dimension == 'GRAND':
            percentage_7 = 0.1
        else:
            percentage_7 = None
        i_price = i_price - i_price * percentage_7

        percentage_8 = 0.02
        diff_year = int(year) - \
            int(form.instance.year_of_release)
        assert diff_year >= 0

        i_price = i_price - i_price * diff_year * percentage_8

        i_price = i_price - repair_amount
        proposed_price = round(float(i_price) / 1000) * 1000
        return int(proposed_price)
