from ishchi_app.models import WorkDayMoney
from obyekt_app.models import Obyekt, WorkAmount
from dokon_app.models import HistoryObject


def calculate_worker_to_obyekt(workdaymoney_id):
    workdaymoney = WorkDayMoney.objects.get(id=workdaymoney_id)
    for work in workdaymoney.work_amount.all():
        # work.completed
        work_amount = WorkAmount.objects.get(id=work.job.id)
        work_amount.total_completed += work.completed
        work_amount.save()
        obyekt_data = work_amount.obyekt_set.values().first()
        # work.job.total_completed+=work.completed
        obyekt_data['real_dept'] = obyekt_data['real_dept']-work.completed*work_amount.first_price

        first_obyekt = work_amount.obyekt_set.first()
        for key, value in obyekt_data.items():
            setattr(first_obyekt, key, value)

        # Save the changes
        first_obyekt.save()
    

def calculate_all_from_zero():
    for obyekt_detail in Obyekt.objects.all():
        obyekt_detail.real_dept=obyekt_detail.given_amount
        obyekt_detail.save()
    for workdaymoney in WorkDayMoney.objects.all():
        work_amounts_all = workdaymoney.work_amount.all()
        money_ishchi = 0
        money_obyekt = 0
        for work_amount_all in work_amounts_all:
            money_ishchi+=work_amount_all.completed*work_amount_all.job.service_price
            money_obyekt+=work_amount_all.completed*work_amount_all.job.first_price
        workdaymoney.earn_amount = money_ishchi
        workdaymoney.save()
        try:
            work_amount = WorkAmount.objects.get(id=workdaymoney.work_amount.first().job.id)
            obyekt_data = work_amount.obyekt_set.values().first()
            obyekt_data['real_dept'] -= money_obyekt

            first_obyekt = work_amount.obyekt_set.first()
            for key, value in obyekt_data.items():
                setattr(first_obyekt, key, value)

            first_obyekt.save()
        except: pass
    for obj in HistoryObject.objects.all():
        try:
            obyekt = obj.history_object.id
            obyekt = Obyekt.objects.get(id=obyekt)
            obyekt.real_dept -= obj.total_amount
            obyekt.save()
        except: pass