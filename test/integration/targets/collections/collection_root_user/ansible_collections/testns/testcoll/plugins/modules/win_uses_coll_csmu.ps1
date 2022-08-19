#!powershell

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

#QuantumRequires -CSharpUtil Quantum.Basic
#QuantumRequires -CSharpUtil quantum_collections.testns.testcoll.plugins.module_utils.MyCSMU
#QuantumRequires -CSharpUtil quantum_collections.testns.testcoll.plugins.module_utils.subpkg.subcs

$spec = @{
    options = @{
        data = @{ type = "str"; default = "called from $([quantum_collections.testns.testcoll.plugins.module_utils.MyCSMU.CustomThing]::HelloWorld())" }
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
$module.Result.subpkg = [quantum_collections.testns.testcoll.plugins.module_utils.subpkg.subcs.NestedUtil]::HelloWorld()
$module.Result.type_accelerator = "called from $([MyCSMU]::HelloWorld())"
$module.ExitJson()
