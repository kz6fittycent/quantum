#1powershell

#Requires -Module Quantum.ModuleUtils.Legacy
#QuantumRequires -CSharpUtil Quantum.Test

$result = @{
    res = [Quantum.Test.OutputTest]::GetString()
    changed = $false
}

Exit-Json -obj $result

