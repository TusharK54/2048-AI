import json

colors = {}
colors['default'] = {'tile': '#000000', 'text': '#ffffff'}
colors[str(0)] = {'tile': '#bbada0', 'text': '#bbada0'}
colors[str(2)] = {'tile': '#eee4da', 'text': '#453C33'}
colors[str(4)] = {'tile': '#ede0c8', 'text': '#453C33'}
colors[str(8)] = {'tile': '#f2b179', 'text': '#f9f6f2'}
colors[str(16)] = {'tile': '#F59563', 'text': '#f9f6f2'}
colors[str(32)] = {'tile': '#f67c5f', 'text': '#f9f6f2'}
colors[str(64)] = {'tile': '#f65e3b', 'text': '#f9f6f2'}
colors[str(128)] = {'tile': '#edcf72', 'text': '#f9f6f2'}
colors[str(256)] = {'tile': '#edcc61', 'text': '#f9f6f2'}
colors[str(512)] = {'tile': '#edc850', 'text': '#f9f6f2'}
colors[str(1024)] = {'tile': '#f2b179', 'text': '#ffffff'}
colors[str(2048)] = {'tile': '#f2b179', 'text': '#ffffff'}
colors[str(4096)] = {'tile': '#f2b179', 'text': '#ffffff'}
colors[str(8192)] = {'tile': '#f2b179', 'text': '#ffffff'}
colors[str(16384)] = {'tile': '#f2b179', 'text': '#ffffff'}

with open('colorinfo.txt', mode='w') as f:
    json.dump(colors, f, indent=2)

print('DONE')