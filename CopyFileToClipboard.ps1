$scriptDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Definition }
$FilePath = Join-Path -Path $scriptDir -ChildPath "pimages\ptest.png"

try {
    # 1. Basic check
    if (-not (Test-Path -Path $FilePath -PathType Leaf)) {
        throw "File not found: $FilePath"
    }

    $FilePath = (Resolve-Path -Path $FilePath).Path
    Write-Host "Start copying file: $FilePath"

    # 2. Use Shell.Application to copy (same as manual command)
    $shell = New-Object -ComObject Shell.Application
    $folder = $shell.Namespace((Split-Path -Path $FilePath -Parent))
    $fileItem = $folder.ParseName((Split-Path -Path $FilePath -Leaf))
    
    # 3. Explicitly call Copy verb (wait for completion)
    $copyVerb = $fileItem.Verbs() | Where-Object { $_.Name -match "Copy|复制" }
    if ($copyVerb) {
        $copyVerb.DoIt()
    } else {
        $fileItem.InvokeVerb("Copy")
    }

    # 4. Delay to ensure clipboard data is persisted
    Start-Sleep -Milliseconds 500

    # 5. Verify clipboard has file data
    $clipboardData = Get-Clipboard -Format FileDropList
    if ($clipboardData -and $clipboardData.FullName -contains $FilePath) {
        Write-Host "Copy success! Clipboard verified."
    } else {
        Write-Host "Copy reported success but clipboard data not found!"
    }
}
catch {
    Write-Host "Copy failed: $($_.Exception.Message)"
    exit 1
}
finally {
    # Clean up with delay
    Start-Sleep -Milliseconds 100
    if ($shell) { [System.Runtime.Interopservices.Marshal]::ReleaseComObject($shell) | Out-Null }
    if ($folder) { [System.Runtime.Interopservices.Marshal]::ReleaseComObject($folder) | Out-Null }
    if ($fileItem) { [System.Runtime.Interopservices.Marshal]::ReleaseComObject($fileItem) | Out-Null }
}

# Keep script session alive for a long time 
Start-Sleep -Seconds 86400