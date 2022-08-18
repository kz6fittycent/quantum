#!powershell

#Requires -Module Quantum.ModuleUtils.Legacy
#Requires -Module Quantum.ModuleUtils.Recursive3
#Requires -Version 2

$ErrorActionPreference = "Stop"

$result = @{
    changed = $false
    value = Get-Test3
}
Exit-Json -obj $result
