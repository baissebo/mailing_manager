# mailings/hide_path.py

def hide_paths(request):
    return {
        'hide_paths': {
            'mailing': ['mailing_list', 'mailing_detail', 'mailing_create', 'mailing_update', 'mailing_delete'],
            'client': ['client_list', 'client_detail', 'client_create', 'client_update', 'client_delete'],
            'message': ['message_list', 'message_detail', 'message_create', 'message_update', 'message_delete'],
        },
        'section_titles': {
            'mailing': 'Рассылки',
            'client': 'Клиенты',
            'message': 'Сообщения'
        }
    }
