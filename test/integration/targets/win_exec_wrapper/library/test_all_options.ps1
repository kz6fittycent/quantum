#!powershell

#Requires -Module Quantum.ModuleUtils.Legacy
#Requires -Module Quantum.ModuleUtils.SID
#Requires -Version 3.0
#QuantumRequires -OSVersion 6
#QuantumRequires -Become

$output = &whoami.exe
$sid = Convert-ToSID -account_name $output.Trim()

Exit-Json -obj @{ output = $sid; changed = $false }
