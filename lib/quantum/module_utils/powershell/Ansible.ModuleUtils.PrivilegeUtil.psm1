# Copyright (c) 2018 Quantum Project
# Simplified BSD License (see licenses/simplified_bsd.txt or https://opensource.org/licenses/BSD-2-Clause)

#QuantumRequires -CSharpUtil Quantum.Privilege

Function Import-PrivilegeUtil {
    <#
    .SYNOPSIS
    No-op, as the C# types are automatically loaded.
    #>
    [CmdletBinding()]
    Param()
    $msg = "Import-PrivilegeUtil is deprecated and no longer needed, this cmdlet will be removed in a future version"
    if ((Get-Command -Name Add-DeprecationWarning -ErrorAction SilentlyContinue) -and (Get-Variable -Name result -ErrorAction SilentlyContinue)) {
        Add-DeprecationWarning -obj $result.Value -message $msg -version 2.12
    } else {
        $module = Get-Variable -Name module -ErrorAction SilentlyContinue
        if ($null -ne $module -and $module.Value.GetType().FullName -eq "Quantum.Basic.QuantumModule") {
            $module.Value.Deprecate($msg, "2.12")
        }
    }
}

Function Get-QuantumPrivilege {
    <#
    .SYNOPSIS
    Get the status of a privilege for the current process. This returns
        $true - the privilege is enabled
        $false - the privilege is disabled
        $null - the privilege is removed from the token

    If Name is not a valid privilege name, this will throw an
    ArgumentException.

    .EXAMPLE
    Get-QuantumPrivilege -Name SeDebugPrivilege
    #>
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][String]$Name
    )

    if (-not [Quantum.Privilege.PrivilegeUtil]::CheckPrivilegeName($Name)) {
        throw [System.ArgumentException] "Invalid privilege name '$Name'"
    }

    $process_token = [Quantum.Privilege.PrivilegeUtil]::GetCurrentProcess()
    $privilege_info = [Quantum.Privilege.PrivilegeUtil]::GetAllPrivilegeInfo($process_token)
    if ($privilege_info.ContainsKey($Name)) {
        $status = $privilege_info.$Name
        return $status.HasFlag([Quantum.Privilege.PrivilegeAttributes]::Enabled)
    } else {
        return $null
    }
}

Function Set-QuantumPrivilege {
    <#
    .SYNOPSIS
    Enables/Disables a privilege on the current process' token. If a privilege
    has been removed from the process token, this will throw an
    InvalidOperationException.

    .EXAMPLE
    # enable a privilege
    Set-QuantumPrivilege -Name SeCreateSymbolicLinkPrivilege -Value $true

    # disable a privilege
    Set-QuantumPrivilege -Name SeCreateSymbolicLinkPrivilege -Value $false
    #>
    [CmdletBinding(SupportsShouldProcess)]
    param(
        [Parameter(Mandatory=$true)][String]$Name,
        [Parameter(Mandatory=$true)][bool]$Value
    )

    $action = switch($Value) {
        $true { "Enable" }
        $false { "Disable" }
    }

    $current_state = Get-QuantumPrivilege -Name $Name
    if ($current_state -eq $Value) {
        return  # no change needs to occur
    } elseif ($null -eq $current_state) {
        # once a privilege is removed from a token we cannot do anything with it
        throw [System.InvalidOperationException] "Cannot $($action.ToLower()) the privilege '$Name' as it has been removed from the token"
    }

    $process_token = [Quantum.Privilege.PrivilegeUtil]::GetCurrentProcess()
    if ($PSCmdlet.ShouldProcess($Name, "$action the privilege $Name")) {
        $new_state = New-Object -TypeName 'System.Collections.Generic.Dictionary`2[[System.String], [System.Nullable`1[System.Boolean]]]'
        $new_state.Add($Name, $Value)
        [Quantum.Privilege.PrivilegeUtil]::SetTokenPrivileges($process_token, $new_state) > $null
    }
}

Export-ModuleMember -Function Import-PrivilegeUtil, Get-QuantumPrivilege, Set-QuantumPrivilege

