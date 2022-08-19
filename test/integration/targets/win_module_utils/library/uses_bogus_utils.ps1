#!powershell

# this should fail
#Requires -Module Quantum.ModuleUtils.BogusModule

Exit-Json @{ data="success" }
