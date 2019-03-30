#! /usr/bin/python
from enigma.machine import EnigmaMachine
import copy

def next_position(M):
    L=copy.deepcopy(M)
    if L==len(L)*[25]:
        return L
    i=len(L)-1
    while L[i]==25:
        L[i]=0
        i-=1
    L[i]+=1
    return L

# example : nextposition([2,7,25]) = [2,8,1]

def get_setting():
    test=""
    ring_setting=[1,1,1]
    ciphertext = 'IPUXZGICZWASMJFGLFVIHCAYEG'
    plaintext="HOWDYAGGIESTHEWEATHERISFINE"
    while 'HOWDYAGGIES' not in test:
        ring_setting=next_position(ring_setting)
        machine = EnigmaMachine.from_key_sheet(
            rotors='I II III',
            reflector='B',
            ring_settings=ring_setting,
            plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')
        test = machine.process_text(ciphertext)
    return ring_setting
    
ring_setting=get_setting()
ciphertext="LTHCHHBUZODFLJOAFNNAEONXPLDJQVJCZPGAVOLN"
machine = EnigmaMachine.from_key_sheet(
   rotors='I II III',
   reflector='B',
   ring_settings=ring_setting,
   plugboard_settings='AV BS CG DL FU HZ IN KM OW RX')
plaintext = machine.process_text(ciphertext)   
print plaintext
