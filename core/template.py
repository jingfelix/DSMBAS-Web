
def file_warn(details:dict):
    return True

def reg_warn(details:dict):
    return True

def heap_warn(details:dict):
    return True

finish_list_template = '''
<a href="/e/report?id=[[ID]]" class="mdui-list-item mdui-ripple mdui-text-color-indigo-500">
        <i class="mdui-list-item-icon"></i>
        [[NAME]]
</a>'''

finish_card_template = '''
<div class="mdui-card mdui-m-y-2">
    <div class="mdui-card-menu">
        <button class="mdui-btn mdui-btn-icon mdui-text-color-theme-accent">
            <i class="mdui-icon material-icons">[[ICON]]</i>
        </button>
    </div>
    <!-- 卡片的标题和副标题 -->
    <div class="mdui-card-primary">
        <div class="mdui-card-primary-title mdui-text-color-[[COLOR]]">[[NAME]]</div>
        <div class="mdui-card-primary-subtitle">[[TIME]]</div>
    </div>
    <!-- 卡片的内容 -->
    <div class="mdui-card-content">
        [[ERROR]]
        <div class="mdui-chip">
            <span class="mdui-chip-icon mdui-color-orange">
                <i class="mdui-icon material-icons">error_outline</i>
            </span>
            <span class="mdui-chip-title">WARNING : [[WARNING]]</span>
        </div>
        <div class="mdui-chip">
            <span class="mdui-chip-icon mdui-color-indigo">
                <i class="mdui-icon material-icons">code</i>
            </span>
            <span class="mdui-chip-title">API : [[API_COUNT]]</span>
        </div>
    </div>
    <!-- 卡片的按钮 -->
    <div class="mdui-card-actions mdui-float-right">
        <a class="mdui-btn mdui-ripple" href="/e/report?id=[[ID]]" [[DISABLED]] >REPORT</a>
    </div>
</div>
'''

chip_error_html = '''
<div class="mdui-chip">
    <span class="mdui-chip-icon mdui-color-red-500">
        <i class="mdui-icon material-icons">clear</i>
    </span>
    <span class="mdui-chip-title">ERROR</span>
</div>
'''

api_list_template = '''
<tr>
    <td>[[NUM]]</td>
    <td>
        [[A_ICON]]
        [[API]]
    </td>
    <td>
        <ul class="mdui-list mdui-list-dense">
            [[ARGS]]
        </ul>
    </td>
    <td>
        <ul class="mdui-list">
            <li class="mdui-list-item mdui-ripple">[[W_ICON]]</li>
            <li class="mdui-list-item mdui-ripple">[[WARNING]]</li>
        </ul>
        
    </td>
</tr>'''

arg_list_template = '''
<li class="mdui-list-item mdui-ripple">[[KEY]]: [[VALUE]]</li>'''

icon_html = '''
<i class="mdui-icon material-icons">[[ICON]]</i>
'''

api_dict = {
    'MsgBoxA': {
        'icon': 'message',
    },
    'MsgBoxW': {
        'icon': 'message',
    },
    'HeapCreate': {
        'icon': 'memory',
    },
    'HeapAlloc': {
        'icon': 'memory',
    },
    'HeapFree': {
        'icon': 'memory',
        'warning': 'Heap double free detected',
        'handler': heap_warn,
    },
    'HeapDestroy': {
        'icon': 'memory',
    },
    'CreateFileA': {
        'icon': 'create_new_folder',
        'warning': 'Created vulnerable file',
        'handler': file_warn,
    },
    'WriteFile': {
        'icon': 'save',
        'warning': 'Wrote vulnerable file',
        'handler': file_warn,
    },
    'ReadFile': {
        'icon': 'folder_open',
        'warning': 'Read vulnerable file',
        'handler': file_warn,
    },
    'RegSetValueEx': {
        'icon': 'settings',
        'warning': 'Set registry value',
        'handler': reg_warn,
    },
    'RegCreateKeyEx': {
        'icon': 'settings',
        'warning': 'Created registry key',
        'handler': reg_warn,
    },
    'RegOpenKeyEx': {
        'icon': 'settings',
        'warning': 'Opened registry key',
        'handler': reg_warn,
    },
    'RegDeleteValue': {
        'icon': 'settings',
        'warning': 'Deleted registry value',
        'handler': reg_warn,
    },
    'RegCloseKey': {
        'icon': 'settings',
        'warning': 'Closed registry key',
        'handler': reg_warn,
    },
    'default': {
        'icon': 'code',
        'warning': 'Unknown API',
        'handler': lambda x: False,
    },
}

