import importlib.util
from pathlib import Path
p=Path(__file__).parent/'working.py'
spec=importlib.util.spec_from_file_location('working',p)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
for values in [['Zoe', 'Amir', 'Zoe'], ['Éva', 'eva', 'Éva'], []]:
    original=values.copy()
    assert module.names_for_display(values)==original, 'Order and repeated names must survive'
    assert values==original, 'Do not mutate family submissions'
print('PASS: submitted order, repetitions and input preservation')
