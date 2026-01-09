# Parallel Translation Script for Redmoon Documents
# Translates all documents to IT and PR simultaneously

$SourceDir = "test/Redmoon/Documents Original"
$Languages = @{
    "it" = "test/Redmoon/Documents Trance IT"
    "pt" = "test/Redmoon/Documents Trance PR"
}
$Model = "gpt-4o-mini"
$Workers = 20
$LogFile = "$(Get-Location)\..\logs\parallel_translate.log"

"--- Parallel Translation Session Starting at $(Get-Date) ---" | Out-File -FilePath $LogFile -Append

# Get all PDF files
$Files = Get-ChildItem -Path $SourceDir -Filter "*.pdf"
Write-Host "Found $($Files.Count) files to translate"

# Create output directories
foreach ($lang in $Languages.Keys) {
    $outDir = $Languages[$lang]
    if (-not (Test-Path $outDir)) {
        New-Item -ItemType Directory -Path $outDir -Force | Out-Null
    }
}

# Launch all translations in parallel
$processes = @()
foreach ($file in $Files) {
    foreach ($lang in $Languages.Keys) {
        $outDir = $Languages[$lang]
        Write-Host "Launching: $($file.Name) -> $lang"
        
        $args = @(
            "translate.py",
            "`"$($file.FullName)`"",
            "--lang", $lang,
            "--model", $Model,
            "--workers", $Workers,
            "--output", "`"$outDir`""
        )
        
        $proc = Start-Process -FilePath "python" -ArgumentList $args -NoNewWindow -PassThru
        "Launched: $($file.Name) -> $lang (PID: $($proc.Id))" | Out-File -FilePath $LogFile -Append
        $processes += $proc
    }
}

Write-Host ""
Write-Host "Launched $($processes.Count) translation processes in parallel."
Write-Host "Use 'Get-Process python | Measure-Object' to monitor active processes."
Write-Host ""
Write-Host "Waiting for all processes to complete..."

# Wait for all processes
foreach ($proc in $processes) {
    $proc.WaitForExit()
}

Write-Host ""
Write-Host "All translations completed!"
