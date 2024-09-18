"""
O objetivo é ligar o melhor conjunto de geradores que atendam o excedente de carga.
L1 * G1 + L2 * G2 + ... + L9 * G9 >= Demanda ultrapassada

L1 => é o Force State da Switch de cada gerador. Esse valor vira das restrições
G1 => é a potência em kVA que o gerador estará gerando com FP 0.8. Esse valor já vai ser lido das declarações

Função objetivo é a melhor combinação econômica de geradores:

Restrições:

(1) Os geradores tem capacidade de funcionar de x steps (valor individual). OK
(2) Os geradores precisam de x steps no mínimo para reabastecimento (valor individual). OK
(3) O período de reabastecimento é entre 8h00 e 18h, após isso vai até o fim.
(4) Se um gerador entrar em operação ele deve permanecer ligado por 3 steps pelo menos (o menor tempo que um dos
geradores aguentará é 3 steps). Só depois ele pode desligar e ficar 3 tempos desligado tambem."""

"""
Se o gerador x ligou

    se ele tiver mais de 3 steps de autonomia
        deve ser incluido na lista de solução e deve ficar ligado 3 steps pelo menos se for despachado
     se não   
        deve sair da soluçao e ser reabastecido        
            
    passou a utilização
        ele deve ficar 3 steps desligado
            se ele tiver menos de 3 steps de autonomia
                aproveita e já reabastece ele tirando da solucao o tempo que demora para reabastecer
            
            se tiver mais de 3 steps de autonomia
                abre contagem para entrar quando possível 
"""