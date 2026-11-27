import shutil
F = 'static/translations.js'
s = open(F, encoding='utf-8').read()
shutil.copy(F, F + '.bak_70')
L = s.splitlines(True)
alt = 0
for i, l in enumerate(L):
    if '70%' not in l:
        continue
    t = l.strip()
    if t.startswith('//'):
        continue
    if ('desc_coletivo:' in l) or (t[:3] in ('pt:', 'en:', 'es:', 'it:', 'fr:', 'de:',
                                             'ja:', 'zh:', 'ru:', 'he:', 'ar:', 'id:',
                                             'tr:', 'vi:')):
        L[i] = l.replace('70%', '50%')
        alt += 1
open(F, 'w', encoding='utf-8').write(''.join(L))
print('linhas corrigidas:', alt)