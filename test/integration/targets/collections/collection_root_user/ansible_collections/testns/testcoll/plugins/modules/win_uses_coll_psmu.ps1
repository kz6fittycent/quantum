#!powershell

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#QuantumRequires -CSharpUtil Quantum.Basic
#QuantumRequires -Powershell quantum_collections.testns.testcoll.plugins.module_utils.MyPSMU
#QuantumRequires -PowerShell quantum_collections.testns.testcoll.plugins.module_utils.subpkg.subps

$spec = @{
    options = @{
        data = @{ type = "str"; default = "called from $(Invoke-FromUserPSMU)" }
    }
    supports_check_mode = $true
}
$module = [Quantum.Basic.QuantumModule]::Create($args, $spec)
$data = $module.Params.data

if ($data -eq "crash") {
    throw "boom"
}

$module.Result.ping = $data
$module.Result.source = "user"
$module.Result.subpkg = Invoke-SubUserPSMU
$module.ExitJson()
