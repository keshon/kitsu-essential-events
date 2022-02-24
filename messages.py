

def say(lang, phrase):
    dict = {
        'ru': {
            'rtw_changed': 'Статус изменился на Ready to Work (RTW)',
            'plan_short': 'Факт дольше плана (дни): ',
            'plan_long': 'Факт быстрее плана (дни)',
            'cant_skip': 'Невозможно изменить статус задачи, тк предыдущие задачи не закрыты'
        },
        'en': {
            'rtw_changed': 'Status changed to Ready to Work (RTW)',
            'plan_short': 'Actual duration took longer than planned (days): ',
            'plan_long': 'Actual duration took faster than planned (days): ',            
            'cant_skip': 'Can\'t skip previous task(s). Status change aborted'
        }
    }

    return dict[lang][phrase]