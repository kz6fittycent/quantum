#powershell

#Requires -Module Quantum.ModuleUtils.Legacy

$params = Parse-Args $args

$path = Get-QuantumParam -Obj $params -Name path -Type path

Exit-Json @{ path=$path }
