#!powershell

# use different cases, spacing and plural of 'module' to exercise flexible powershell dialect
#ReQuiReS   -ModUleS    Quantum.ModuleUtils.Legacy
#Requires -Module Quantum.ModuleUtils.ValidTestModule

$o = CustomFunction

Exit-Json @{data=$o}
