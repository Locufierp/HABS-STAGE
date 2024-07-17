import pytest 
@pytest.mark.test_syracuse 
def suite_syracuse(n):
    suite = []

    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        suite.append(n)
    
    return suite

nombre_de_depart = 6
resultat = suite_syracuse(nombre_de_depart)
print(f"La suite de Syracuse pour {nombre_de_depart} est : {resultat}")
