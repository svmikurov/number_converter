# Converting an integer to text in words

### Example
```
>>> from number_converter import convert_number
>>> convert_number(11_001_001_001, 'N', 'N')
'одиннадцать миллиардов один миллион одну тысячу одно'
```

### Flags
```
GENDERS = {
    'M': 'masculine',
    'F': 'feminine',
    'N': 'neuter',
}
CASES = {
    'N': 'nominative',
    'G': 'genitive',
    'D': 'dative',
    'A': 'accusative',
    'I': 'instrumental',
    'P': 'prepositional',
}
```

### Additional information
[Правило склонения имён числительных](https://www.yaklass.ru/p/russky-yazik/10-klass/razdel-morfologii-samostoiatelnye-chasti-rechi-10908/imia-chislitelnoe-10921/re-89c70ea5-6547-4cae-8da9-c2e4bd3a5ee8)